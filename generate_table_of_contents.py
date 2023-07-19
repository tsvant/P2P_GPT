# generate_table_of_contents.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_table_of_contents(output_folder):
    """Generate a research table of contents based on the research objectives and user's research goal."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    toc_file = os.path.join(new_paper_folder, 'Research table of contents.txt')

    # Create the necessary folders if they don't exist
    os.makedirs(new_paper_folder, exist_ok=True)

    # Load the research objectives text
    objectives_file = os.path.join(new_paper_folder, 'Research objectives list.txt')
    with open(objectives_file, 'r', encoding='utf-8') as file:
        objectives_text = file.read().strip()

    # Load the user's research goal
    parent_directory = os.path.dirname(output_folder)
    user_input_folder = os.path.join(parent_directory, 'User input')
    user_goal_file = os.path.join(user_input_folder, 'user_goal.txt')

    with open(user_goal_file, 'r', encoding='utf-8') as file:
        user_goal = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please generate a research table of contents based on the provided research objectives and the user's research goal. The research objectives are as follows:\n\n{objectives_text}\n\nThe user's research goal is: '{user_goal}'. Create namings for the parts that need namings. Namings should not be too technical. There should be no more than two chapters. Chapters should consist of no more than three sections. The table of contents should be structured as follows:\n\n1. Title page\n2. Abstract\n3. Introduction\n4. Literature review\n5. Chapter 1. (Theoretical, don't mention the word 'theoretical', up to 5 words)\n5.1. Section 1.1 (up to 5 words)\n5.2. Section 1.2 (up to 5 words)\n5.3. Section 1.3 (up to 5 words)\n6. Chapter 2 (Practical, don't mention the word 'practical', up to 5 words)\n6.1. Section 2.1 (up to 5 words)\n6.2. Section 2.2 (up to 5 words)\n6.3. Section 2.3 (up to 5 words)\n7. Conclusion\n8. List of literature sources."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to generate a research table of contents based on the provided research objectives and the user's research goal."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    toc = response['choices'][0]['message']['content'].strip()

    # Write the research table of contents into a file
    with open(toc_file, 'w', encoding='utf-8') as file:
        file.write(toc)


if __name__ == "__main__":
    print("Generating research table of contents...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate research table of contents
    generate_table_of_contents(output_folder)

    print("Research table of contents generation complete.")