import os

def get_user_goal(output_folder):
    """Prompt the user to enter the goal of their research paper and save it in a text file."""
    user_input_folder = os.path.join(os.path.dirname(output_folder), 'User input')
    os.makedirs(user_input_folder, exist_ok=True)

    user_goal = input("Please enter the goal of your research paper: ")
    goal_filename = os.path.join(user_input_folder, "user_goal.txt")

    with open(goal_filename, 'w', encoding="utf-8") as file:
        file.write(user_goal)

    return goal_filename
