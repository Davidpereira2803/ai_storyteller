STORY_TREE = {
    "meta": {"title": "The Broken Crown (Demo)", "genre": "Fantasy"},
    "nodes": {
        "start": {
            "id": "start",
            "text": "You stand at the cracked threshold of the crown hall. Torches gutter in the cold wind; the throne sits empty.",
            "choices": [
                {"id": "inspect_throne", "text": "Inspect the throne"},
                {"id": "question_guard", "text": "Question the guard"},
                {"id": "leave_hall", "text": "Leave quietly"}
            ]
        },
        "inspect_throne": {
            "id": "inspect_throne",
            "text": "A curtain of royal cloth has been slashed; a single thread clings to the throne. Something glitters under the cushions.",
            "choices": [
                {"id": "search_cushions", "text": "Search the cushions"},
                {"id": "follow_thread", "text": "Follow the thread out of the hall"}
            ]
        },
        "question_guard": {
            "id": "question_guard",
            "text": "The guard looks at you with tired eyes. 'Not my place to talk of the crown,' he says, but his hand rests near his dagger.",
            "choices": [
                {"id": "bribe_guard", "text": "Bribe the guard"},
                {"id": "intimidate_guard", "text": "Intimidate the guard"}
            ]
        },
        # ... add other nodes and endings here
    }
}
