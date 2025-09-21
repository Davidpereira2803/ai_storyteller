from story_data import STORY_TREE
from utils import save_game, load_game

def run():
    # Load previous save if available
    state = load_game()
    if state:
        current_node = state["current_node"]
        history = state["history"]
        print("Loaded previous game!")
    else:
        current_node = "start"
        history = []

    while True:
        node = STORY_TREE["nodes"][current_node]
        print("\n" + "="*50)
        print(f"{node['text']}\n")

        if node.get("choices"):
            for i, choice in enumerate(node["choices"], 1):
                print(f"{i}. {choice['text']}")
            print("0. Quit / Save")

            try:
                selection = int(input("\nChoose an option: "))
                if selection == 0:
                    save_game({"current_node": current_node, "history": history})
                    print("Game saved. Goodbye!")
                    break
                selected_choice = node["choices"][selection - 1]
            except (ValueError, IndexError):
                print("Invalid choice. Try again.")
                continue

            history.append({"node": current_node, "choice": selected_choice["id"]})
            current_node = selected_choice["id"]

        else:
            print("-- End of demo path --")
            replay = input("Do you want to restart? (y/n): ").lower()
            if replay == "y":
                current_node = "start"
                history = []
            else:
                break

if __name__ == "__main__":
    run()
