import streamlit as st
import time
from datetime import datetime
from main import generate_next_node_ollama, OLLAMA_MODEL
from story_data import STORY_TREE
from utils import save_game, load_game

st.set_page_config(
    page_title="AI Storyteller", 
    layout="wide",
    page_icon="🏰",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize or load game state"""
    if 'initialized' not in st.session_state:
        state = load_game()
        if state:
            st.session_state.current_text = state.get("current_text", STORY_TREE["nodes"]["start"]["text"])
            st.session_state.history = state.get("history", [])
            st.session_state.story_meta = state.get("story_meta", STORY_TREE.get("meta", {}))
            if st.session_state.history and "choices" in st.session_state.history[-1]:
                st.session_state.choices = st.session_state.history[-1]["choices"]
            else:
                st.session_state.choices = STORY_TREE["nodes"]["start"]["choices"]
        else:
            new_game()
        st.session_state.initialized = True
        st.session_state.generation_count = 0

def new_game():
    """Start a new game"""
    st.session_state.current_text = STORY_TREE["nodes"]["start"]["text"]
    st.session_state.history = []
    st.session_state.choices = STORY_TREE["nodes"]["start"]["choices"]
    st.session_state.story_meta = STORY_TREE.get("meta", {})
    st.session_state.generation_count = 0

def display_sidebar():
    """Enhanced sidebar with game info and controls"""
    with st.sidebar:
        st.title("🎮 Game Controls")
        
        # Story info
        meta = st.session_state.get('story_meta', {})
        st.info(f"**{meta.get('title', 'Unknown Story')}**\n\n*Genre: {meta.get('genre', 'Adventure')}*")
        
        # Game stats
        st.metric("Choices Made", len(st.session_state.get('history', [])))
        st.metric("Scenes Generated", st.session_state.get('generation_count', 0))
        
        st.divider()
        
        # Controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", use_container_width=True):
                save_game({
                    "current_text": st.session_state.current_text,
                    "history": st.session_state.history,
                    "story_meta": st.session_state.story_meta
                })
                st.success("Saved!")
                time.sleep(1)
                st.rerun()
        
        with col2:
            if st.button("🔄 New Game", use_container_width=True):
                new_game()
                st.success("New game started!")
                time.sleep(1)
                st.rerun()
        
        if st.button("📁 Load Game", use_container_width=True):
            state = load_game()
            if state:
                st.session_state.current_text = state.get("current_text", STORY_TREE["nodes"]["start"]["text"])
                st.session_state.history = state.get("history", [])
                st.session_state.story_meta = state.get("story_meta", STORY_TREE.get("meta", {}))
                if st.session_state.history and "choices" in st.session_state.history[-1]:
                    st.session_state.choices = st.session_state.history[-1]["choices"]
                else:
                    st.session_state.choices = STORY_TREE["nodes"]["start"]["choices"]
                st.success("Game loaded!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("No save file found!")
        
        st.divider()
        
        # Story history
        if st.session_state.get('history'):
            with st.expander("📖 Story History"):
                for i, entry in enumerate(st.session_state.history[-5:], 1):
                    st.caption(f"{i}. {entry.get('choice', 'Unknown choice')}")
        
        # Model info
        st.caption(f"🤖 Model: {OLLAMA_MODEL}")

def display_story():
    """Enhanced story display"""
    st.title("🏰 AI Storyteller")
    
    # Story text with better formatting
    with st.container():
        st.markdown("### Current Scene")
        story_container = st.container()
        with story_container:
            # Add some styling with black text
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #4CAF50;
                margin: 10px 0;
                font-size: 16px;
                line-height: 1.6;
                color: black;
            ">
                {st.session_state.current_text}
            </div>
            """, unsafe_allow_html=True)

def handle_choice_selection():
    """Enhanced choice handling with better UX"""
    st.markdown("### What do you do?")
    
    # Display choices in a more engaging way
    cols = st.columns(min(len(st.session_state.choices), 2))
    
    for i, choice in enumerate(st.session_state.choices):
        col = cols[i % len(cols)]
        
        with col:
            # Add icons based on choice type
            icon = get_choice_icon(choice["text"])
            
            if st.button(
                f"{icon} {choice['text']}", 
                key=f"choice_{i}", 
                use_container_width=True,
                type="primary" if i == 0 else "secondary"
            ):
                return choice
    
    return None

def get_choice_icon(choice_text):
    """Get appropriate icon for choice type"""
    text_lower = choice_text.lower()
    if any(word in text_lower for word in ["inspect", "examine", "look", "search"]):
        return "🔍"
    elif any(word in text_lower for word in ["talk", "speak", "ask", "question"]):
        return "💬"
    elif any(word in text_lower for word in ["fight", "attack", "defend"]):
        return "⚔️"
    elif any(word in text_lower for word in ["leave", "go", "move", "walk"]):
        return "🚶"
    elif any(word in text_lower for word in ["use", "take", "grab"]):
        return "🤲"
    else:
        return "✨"

def generate_with_progress(selected_choice):
    """Generate next scene with progress indication"""
    progress_container = st.empty()
    status_container = st.empty()
    
    with progress_container.container():
        progress_bar = st.progress(0)
        
        # Simulate progress steps
        steps = [
            "🤖 Thinking about your choice...",
            "📝 Crafting the next scene...", 
            "🎭 Adding dramatic elements...",
            "✨ Finalizing the story..."
        ]
        
        for i, step in enumerate(steps):
            status_container.info(step)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.5)
    
    # Generate content
    try:
        next_node = generate_next_node_ollama(
            st.session_state.current_text,
            selected_choice["text"],
            st.session_state.history,
            st.session_state.story_meta
        )
        
        # Clear progress indicators
        progress_container.empty()
        status_container.empty()
        
        return next_node
        
    except Exception as e:
        progress_container.empty()
        status_container.error(f"Generation failed: {e}")
        return None

def main():
    initialize_session_state()
    display_sidebar()
    display_story()
    
    # Handle choice selection
    selected_choice = handle_choice_selection()
    
    if selected_choice:
        next_node = generate_with_progress(selected_choice)
        
        if next_node:
            # Update game state
            st.session_state.history.append({
                "choice": selected_choice["text"],
                "choices": next_node.get("choices", []),
                "timestamp": datetime.now().isoformat()
            })
            st.session_state.current_text = next_node["text"]
            st.session_state.choices = next_node.get("choices", [])
            st.session_state.generation_count += 1
            
            # Auto-save
            save_game({
                "current_text": st.session_state.current_text,
                "history": st.session_state.history,
                "story_meta": st.session_state.story_meta
            })
            
            st.rerun()

if __name__ == "__main__":
    main()