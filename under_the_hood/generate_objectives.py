# generate_objectives.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_research_objectives(output_folder):
    """Generate a list of research objectives based on the research findings and user's research goal."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    objectives_file = os.path.join(new_paper_folder, 'Research objectives list.txt')

    # Create the necessary folders if they don't exist
    os.makedirs(new_paper_folder, exist_ok=True)

    # Load the research findings text
    findings_file = os.path.join(new_paper_folder, 'Brand new findings.txt')
    with open(findings_file, 'r', encoding='utf-8') as file:
        findings_text = file.read().strip()

    # Load the user's research goal
    parent_directory = os.path.dirname(output_folder)
    user_input_folder = os.path.join(parent_directory, 'User input')
    user_goal_file = os.path.join(user_input_folder, 'user_goal.txt')

    with open(user_goal_file, 'r', encoding='utf-8') as file:
        user_goal = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please generate a list of research objectives based on the provided research findings and the user's research goal. The research findings are summarized as follows:\n\n{findings_text}\n\nThe user's research goal is: '{user_goal}'. The objectives should be carefully formulated and should form the content of the chapters in the research paper. The list of these objectives should not go beyond those ones that can be performed using our scientific literature sources, and should ultimately lead us to our research findings. The list of tasks should include, relatively speaking, theoretical and more practical objectives. The objectives of the theoretical part should be descriptive in nature, answer the questions 'what is this research about?', 'what is important when considering this in the framework of fulfilling the goal of our research?', 'what scientific literature should be relied upon when considering this issue in accordance with our goal?', and 'how do we formulate hypotheses for the practical part of our research in accordance to our goal, which will receive an answer in the final conclusion of the work?'. The objectives of the practical part should be of a specific working nature, help to take the necessary actions for a logical approach to reach our research findings, and may include the development of a research methodology, a description of the process of collecting and specific analysis of data from the sources used, a conclusion based on the results obtained and the interpretation of this conclusion with taking into account the goals of the study and hypotheses, and a description of the significance of the study, along with descriptions of further research directions."
    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to generate a list of research objectives based on the provided research findings and the user's research goal."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    objectives = response['choices'][0]['message']['content'].strip()

    # Write the research objectives into a file
    with open(objectives_file, 'w', encoding='utf-8') as file:
        file.write(objectives)


if __name__ == "__main__":
    print("Generating research objectives...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate research objectives
    generate_research_objectives(output_folder)

    print("Research objectives generation complete.")