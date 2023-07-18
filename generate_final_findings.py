# generate_final_findings.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_final_findings(output_folder):
    """Generate finalized research findings based on the research_findings files for each research paper."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    new_paper_findings_file = os.path.join(new_paper_folder, 'Brand new findings.txt')

    # Create the necessary folders if they don't exist
    os.makedirs(new_paper_folder, exist_ok=True)

    # Retrieve the existing research findings for each paper
    research_findings = []
    for subdir in os.listdir(output_folder):
        if subdir != '0. Brand new research paper' and os.path.isdir(os.path.join(output_folder, subdir)):
            research_findings_file = os.path.join(output_folder, subdir, 'Research findings',
                                                  f'{subdir}_research_findings.txt')

            # Load the research findings file content
            with open(research_findings_file, 'r', encoding='utf-8') as file:
                research_findings.append(file.read())

    # Concatenate the research findings together
    findings_text = '\n\n'.join(research_findings)

    # Load the user's research goal text
    parent_directory = os.path.dirname(output_folder)
    user_input_folder = os.path.join(parent_directory, 'User input')
    user_goal_file = os.path.join(user_input_folder, 'user_goal.txt')

    with open(user_goal_file, 'r', encoding='utf-8') as file:
        user_goal = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please act as a researcher and generate comprehensive research findings based on the provided research findings. The user's goal, as well as the findings from the research papers, are summarized as follows:\n\n{findings_text}\n\nRequirements for the finalized research findings are:\n1. Clarity and Precision\n2. Reproducibility\n3. Statistical Significance\n4. Interpretation and Discussion\n5. Transparency\n6. Ethical Considerations.\n\nThe user's research goal is: '{user_goal}'."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to generate finalized research findings based on the provided research findings."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    final_findings = response['choices'][0]['message']['content'].strip()

    # Write the final findings into a file
    with open(new_paper_findings_file, 'w', encoding='utf-8') as file:
        file.write(final_findings)


if __name__ == "__main__":
    print("Generating final research findings...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate final research findings
    generate_final_findings(output_folder)

    print("Final research findings generation complete.")