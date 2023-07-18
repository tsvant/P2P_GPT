import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_research_findings(output_folder, subdirectory_name):
    """Generate a file containing key research findings for each paper based on the alignment analysis and user's goal."""

    # Define necessary file and folder paths
    subdirectory_folder = os.path.join(output_folder, subdirectory_name)
    goal_findings_folder = os.path.join(subdirectory_folder, 'Research findings')
    os.makedirs(goal_findings_folder, exist_ok=True)  # Create the necessary folder if it doesn't exist

    # File containing previous alignment analysis
    alignment_analysis_file = os.path.join(subdirectory_folder, 'Goal alignment', f'{subdirectory_name}_Goal_alignment_analysis.txt'.replace('/', ''))

    # User's goal
    parent_directory = os.path.dirname(output_folder)
    user_input_folder = os.path.join(parent_directory, 'User input')
    goal_file = os.path.join(user_input_folder, 'user_goal.txt')

    # Load the alignment analysis and goal
    with open(alignment_analysis_file, 'r', encoding='utf-8') as file:
        alignment_analysis = file.read().strip()

    with open(goal_file, 'r', encoding='utf-8') as file:
        user_goal = file.read().strip()

    # Define the prompt
    prompt = f"The user's research goal is: '{user_goal}'. The alignment to user's research goal analysis of the paper is provided. Generate a comprehensive summary of the key findings based on the alignment analysis: '{alignment_analysis}'."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a researcher assistant. Your task is to process the given information and derive key research findings."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    findings = response['choices'][0]['message']['content'].strip()

    # Write the key findings into a file
    findings_file = os.path.join(goal_findings_folder, f'{subdirectory_name}_research_findings.txt')
    with open(findings_file, 'w', encoding='utf-8') as file:
        file.write(findings)


if __name__ == "__main__":
    print("Generating research findings...")

    input_folder = 'Upload here'
    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Loop over all folders in the output folder
    subdirectories = [subdir for subdir in os.listdir(output_folder) if os.path.isdir(os.path.join(output_folder, subdir))]

    for subdir in subdirectories:
        generate_research_findings(output_folder, subdir)

    print("Research findings generation complete.")