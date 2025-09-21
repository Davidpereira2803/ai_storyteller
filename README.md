# AI Storyteller — Interactive Generative Narrative

A web-based interactive storytelling game that uses large language models (LLMs) to dynamically generate scenes and choices. This project demonstrates AI integration, stateful prompt design, and full-stack engineering through iterative development.

## Overview

AI Storyteller is an interactive narrative game that combines traditional choice-based storytelling with AI-powered content generation. Players navigate through branching storylines where their choices shape the narrative, with an integrated LLM (via Ollama) dynamically generating new story content, scenes, and choices in real-time.

## Current Implementation

The project features both console and web-based interfaces with:

- **AI-Powered Story Generation**: Dynamic content creation using Ollama LLM integration
- **Interactive Story Engine**: Navigate through branching narratives with choice-based progression
- **Web Interface**: Modern Streamlit-based UI for enhanced user experience
- **Save/Load System**: Persistent game state management using JSON serialization
- **Modular Story Data**: Structured story tree with nodes, choices, and metadata
- **Demo Content**: "The Broken Crown" fantasy scenario for testing and demonstration

### Core Components

- [`main.py`](main.py) - Core game logic and Ollama LLM integration
- [`gui_streamlit.py`](gui_streamlit.py) - Web-based Streamlit interface
- [`story_data.py`](story_data.py) - Story tree structure and initial content
- [`utils.py`](utils.py) - Save/load utilities and file management
- [`save.json`](save.json) - Persistent game state storage

## Features

### ✅ Currently Implemented
- **AI Story Generation**: Real-time content generation using Ollama LLM
- **Web Interface**: Streamlit-based UI with responsive design
- **Interactive Storytelling**: Choice-driven narrative progression
- **Game State Persistence**: Save/load functionality
- **Error Handling**: Robust fallback mechanisms for AI failures
- **Modular Architecture**: Clean separation of concerns

### 🚧 Planned Features
- Advanced prompt engineering for better story coherence
- Character development and relationship tracking
- Image generation for scenes
- Multiple LLM model support
- Story branching visualization
- Enhanced UI/UX improvements

## Getting Started

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.ai/) installed and running
- LLM model downloaded (recommended: `llama3.1:8b` or `mistral:7b`)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai_storyteller
```

2. Install Python dependencies:
```bash
pip install streamlit
```

3. Install and setup Ollama:
```bash
# Install Ollama from https://ollama.ai/
# Then pull a model:
ollama pull llama3.1:8b
```

4. Configure the model in `main.py`:
```python
OLLAMA_MODEL = "llama3.1:8b"  # or your preferred model
```

### Running the Application

#### Web Interface (Recommended)
```bash
streamlit run gui_streamlit.py
```
Then open your browser to `http://localhost:8501`

#### Console Interface
```bash
python main.py
```

### Model Configuration

The application supports various Ollama models. Edit the `OLLAMA_MODEL` variable in `main.py`:

**Recommended Models:**
- `llama3.1:8b` - Best balance of quality and performance
- `mistral:7b` - Lighter, fast generation
- `llama3.1:70b` - Superior quality (requires significant RAM)

## Project Structure

```
ai_storyteller/
├── main.py                 # Core game logic and LLM integration
├── gui_streamlit.py        # Streamlit web interface
├── story_data.py          # Initial story content and structure
├── utils.py               # Utility functions (save/load)
├── save.json             # Game state persistence
├── requirements.txt      # Python dependencies
├── .env                  # Environment configuration
├── .gitignore           # Git ignore rules
├── LICENSE.md           # MIT License
└── README.md            # This file
```

## How It Works

### AI Story Generation
The application uses Ollama to generate story content through structured prompts:

1. **Context Building**: Current story state and player choice are formatted into a prompt
2. **LLM Generation**: Ollama processes the prompt and generates JSON-formatted responses
3. **Response Parsing**: The application extracts story text and new choices
4. **Fallback Handling**: If AI generation fails, predefined fallback content ensures continuity

### Story Flow
```
Initial Scene → Player Choice → AI Generation → New Scene → Repeat
```

### Prompt Engineering
The system uses carefully crafted prompts to ensure:
- Consistent JSON output format
- Narrative coherence
- Appropriate choice generation
- Genre consistency

## Web Interface Features

The Streamlit interface provides:
- **Clean Story Display**: Easy-to-read narrative text
- **Interactive Choices**: Click-to-select choice buttons
- **Real-time Generation**: Loading indicators during AI processing
- **Game Management**: Save, load, and restart functionality
- **Responsive Design**: Works on desktop and mobile devices

## Development Roadmap

### Iteration 1 ✅ (Completed)
- [x] Python prototype implementation
- [x] Ollama LLM integration
- [x] Streamlit web interface
- [x] Basic story structure and save system

### Iteration 2 🚧 (Current)
- [ ] Enhanced prompt engineering
- [ ] Better error handling and user feedback
- [ ] Story history visualization
- [ ] Multiple model support

### Iteration 3 📋 (Upcoming)
- [ ] Character development tracking
- [ ] Advanced narrative coherence
- [ ] Image generation integration
- [ ] Story analytics and metrics

### Iteration 4+ 📋 (Future)
- [ ] Multi-modal AI features
- [ ] Collaborative storytelling
- [ ] Story sharing and community features
- [ ] Advanced UI/UX improvements

## Story Format

Initial stories are defined in [`story_data.py`](story_data.py):

```python
STORY_TREE = {
    "meta": {"title": "Story Title", "genre": "Genre"},
    "nodes": {
        "node_id": {
            "id": "node_id",
            "text": "Story text content",
            "choices": [
                {"id": "choice_id", "text": "Choice description"}
            ]
        }
    }
}
```

AI-generated content follows the same structure, ensuring consistency throughout the experience.

## Configuration

### Environment Variables
Create a `.env` file for future configuration:
```env
OLLAMA_MODEL=llama3.1:8b
OLLAMA_HOST=localhost:11434
```

### Model Selection
Choose your model based on your system capabilities:
- **4-8GB RAM**: `mistral:7b`
- **8-16GB RAM**: `llama3.1:8b`
- **32GB+ RAM**: `llama3.1:70b`

## Troubleshooting

### Common Issues

**Ollama not responding:**
```bash
# Check if Ollama is running
ollama list
# If not, start Ollama service
ollama serve
```

**Model not found:**
```bash
# Pull the required model
ollama pull llama3.1:8b
```

**JSON parsing errors:**
- The application includes fallback mechanisms
- Check Ollama model output in console for debugging

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m "Add feature"`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines
- Test with different Ollama models
- Ensure fallback mechanisms work
- Follow existing code structure
- Update documentation for significant changes

## Performance Tips

- Use smaller models (`mistral:7b`) for faster generation
- Ensure adequate RAM for your chosen model
- Consider using quantized models for better performance
- Monitor Ollama resource usage during development

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM infrastructure
- [Streamlit](https://streamlit.io/) for rapid web app development
- Inspired by classic interactive fiction and modern AI capabilities
- Built for educational and demonstration purposes

## Contact

Please open issues for:
- Bug reports and troubleshooting
- Feature requests
- Model compatibility questions
- Prompt engineering improvements
- General questions and discussion

---

**Note**: This project demonstrates practical AI integration in game development. The combination of local LLMs via Ollama and web interfaces via Streamlit provides a foundation for exploring AI-powered interactive narratives.

