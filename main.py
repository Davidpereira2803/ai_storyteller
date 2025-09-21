import subprocess
import json
import re
import os
from story_data import STORY_TREE
from utils import save_game, load_game

OLLAMA_MODEL = "llama3.1:8b"  # replace with your local model name

def generate_next_node_ollama(current_text, choice_text, history, story_meta=None):
    # Build context from history for better coherence
    context = ""
    if history:
        recent_history = history[-3:]  # Last 3 choices for context
        context = "\n".join([f"Previously: {h.get('choice', '')}" for h in recent_history])
    
    # Get story metadata for consistency
    meta = story_meta or STORY_TREE.get("meta", {})
    genre = meta.get("genre", "Adventure")
    tone = meta.get("tone", "mysterious")
    
    prompt = f"""You are an expert {genre.lower()} storyteller. 

STORY CONTEXT:
Genre: {genre}
Tone: {tone}
{context}

CURRENT SCENE:
{current_text}

PLAYER ACTION: {choice_text}

INSTRUCTIONS:
- Continue the story with 2-3 engaging sentences
- Maintain {genre.lower()} genre and {tone} tone
- Create 2-4 meaningful choices that advance the plot
- Each choice should lead to different story paths
- Keep choices concise but descriptive
- Ensure narrative coherence with previous events

RESPONSE FORMAT (JSON only):
{{
    "text": "Next scene description (2-3 sentences)",
    "choices": [
        {{"id": "choice1", "text": "Action-oriented choice"}},
        {{"id": "choice2", "text": "Investigation choice"}},
        {{"id": "choice3", "text": "Social/dialogue choice"}},
        {{"id": "choice4", "text": "Creative/alternative choice"}}
    ]
}}"""

    try:
        # Set environment variables for proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',  # Force UTF-8 encoding
            errors='replace',  # Replace problematic characters
            check=True,
            timeout=30,
            env=env  # Pass environment with UTF-8 setting
        )
        
        output = result.stdout.strip()
        
        # Enhanced JSON extraction
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            parsed = json.loads(json_str)
            
            # Validate response structure
            if validate_response(parsed):
                return parsed
            else:
                raise ValueError("Invalid response structure")
        else:
            raise ValueError("No JSON found in response")
            
    except subprocess.TimeoutExpired:
        print("⚠️ Generation timed out. Using fallback...")
        return create_fallback_response(choice_text)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON parsing failed: {e}")
        print(f"Raw output: {result.stdout if 'result' in locals() else 'No output'}")
        return create_fallback_response(choice_text)
    except UnicodeDecodeError as e:
        print(f"⚠️ Unicode error: {e}")
        return create_fallback_response(choice_text)
    except Exception as e:
        print(f"⚠️ Generation failed: {e}")
        return create_fallback_response(choice_text)

def validate_response(response):
    """Validate AI response structure"""
    required_keys = ["text", "choices"]
    if not all(key in response for key in required_keys):
        return False
    
    if not isinstance(response["choices"], list) or len(response["choices"]) < 2:
        return False
    
    for choice in response["choices"]:
        if not isinstance(choice, dict) or "id" not in choice or "text" not in choice:
            return False
    
    return True

def create_fallback_response(choice_text=""):
    """Create contextual fallback based on player choice"""
    fallbacks = {
        "inspect": {
            "text": "You examine the area carefully, noticing details that weren't apparent before. Something important catches your attention.",
            "choices": [
                {"id": "investigate_further", "text": "Investigate the discovery"},
                {"id": "look_around", "text": "Search the surrounding area"}
            ]
        },
        "talk": {
            "text": "The conversation reveals more than expected. New information changes your understanding of the situation.",
            "choices": [
                {"id": "ask_more", "text": "Press for more details"},
                {"id": "consider_info", "text": "Think about what you've learned"}
            ]
        },
        "leave": {
            "text": "As you prepare to leave, something makes you pause. The situation isn't as simple as it first appeared.",
            "choices": [
                {"id": "reconsider", "text": "Reconsider your decision"},
                {"id": "continue_leaving", "text": "Continue on your way"}
            ]
        }
    }
    
    # Choose fallback based on choice keywords
    for keyword, fallback in fallbacks.items():
        if keyword.lower() in choice_text.lower():
            return fallback
    
    # Default fallback
    return {
        "text": "The story takes an unexpected turn. Your choice leads to new possibilities you hadn't considered.",
        "choices": [
            {"id": "adapt", "text": "Adapt to the new situation"},
            {"id": "stay_course", "text": "Stick to your original plan"}
        ]
    }

def run():
    state = load_game()
    if state:
        current_text = state.get("current_text", STORY_TREE["nodes"]["start"]["text"])
        history = state.get("history", [])
        if history and "choices" in history[-1]:
            choices = history[-1]["choices"]
        else:
            choices = STORY_TREE["nodes"]["start"]["choices"]
    else:
        current_text = STORY_TREE["nodes"]["start"]["text"]
        history = []
        choices = STORY_TREE["nodes"]["start"]["choices"]

    while True:
        print(f"\n{current_text}\n")
        
        print("Your choices:")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice['text']}")
        
        try:
            choice_num = int(input("\nEnter your choice (number): ")) - 1
            if 0 <= choice_num < len(choices):
                selected_choice = choices[choice_num]
                
                print("Generating next scene...")
                next_node = generate_next_node_ollama(current_text, selected_choice["text"], history)
                
                history.append({"choice": selected_choice["text"], "choices": next_node.get("choices", [])})
                current_text = next_node["text"]
                choices = next_node.get("choices", [])
                
                # Auto-save
                save_game({"current_text": current_text, "history": history})
                
            else:
                print("Invalid choice. Please try again.")
        except (ValueError, KeyboardInterrupt):
            print("\nGame ended.")
            break

if __name__ == "__main__":
    run()
