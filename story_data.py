STORY_TREE = {
    "meta": {
        "title": "The Broken Crown (Demo)", 
        "genre": "Fantasy",
        "tone": "mysterious",
        "author": "AI Storyteller",
        "version": "1.0"
    },
    "nodes": {
        "start": {
            "id": "start",
            "text": "You stand at the cracked threshold of the crown hall. Ancient tapestries flutter in the cold wind that seeps through broken windows. The once-magnificent throne sits empty, its golden surface tarnished and split. Shadows dance across the floor as torches gutter in their sconces.",
            "choices": [
                {"id": "inspect_throne", "text": "Approach and inspect the damaged throne"},
                {"id": "question_guard", "text": "Question the lone guard in the corner"},
                {"id": "examine_tapestries", "text": "Examine the ancient tapestries"},
                {"id": "leave_hall", "text": "Leave the hall quietly"}
            ]
        }
    }
}

# Story templates for better AI generation
STORY_TEMPLATES = {
    "fantasy": {
        "tone_words": ["mystical", "ancient", "magical", "enchanted"],
        "common_elements": ["magic", "kingdoms", "quests", "artifacts"],
        "choice_types": ["investigate", "use magic", "consult wisdom", "seek allies"]
    },
    "mystery": {
        "tone_words": ["suspicious", "intriguing", "hidden", "secretive"],
        "common_elements": ["clues", "suspects", "evidence", "revelations"],
        "choice_types": ["investigate", "question", "analyze", "follow leads"]
    }
}
