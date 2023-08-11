import os

def get_user_goal(output_folder):
    """Prompt the user to enter the goal of their research paper and save it in a text file."""
    user_input_folder = os.path.join(os.path.dirname(output_folder), 'User input')
    os.makedirs(user_input_folder, exist_ok=True)

    user_goal = input("Welcome to P2P_GPT! \n\n In order to start creating your own research paper, \n based on the sources you proive, you should do two things: \n\n 1. Upload .txt files of your desired sources in the 'Upload here' folder of the project. \n 2. When you finish step 1, fill in the research goal you have in mind in the blank below: \n\n Please enter the goal of your research paper: ")
    goal_filename = os.path.join(user_input_folder, "user_goal.txt")

    with open(goal_filename, 'w', encoding="utf-8") as file:
        file.write(user_goal)

    return goal_filename
