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

    # Split the alignment analysis into chunks of approximately 12000 characters each
    chunk_size = 12000  # Define the size of each chunk
    analysis_chunks = [alignment_analysis[i:i + chunk_size] for i in range(0, len(alignment_analysis), chunk_size)]

    findings_chunks = []
    for i, chunk in enumerate(analysis_chunks):
        print(f"Processing chunk {i + 1} of {len(analysis_chunks)}...")

        # Define the prompt for this chunk
        prompt = f"The user's research goal is: '{user_goal}'. The alignment to user's research goal analysis of the paper is provided. Generate a comprehensive summary of the key findings based on the alignment analysis: '{chunk}'."

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
        findings_chunks.append(findings)

    # Refine the findings chunks
    while len(findings_chunks) > 1:
        refined_findings_chunks = []
        for i in range(0, len(findings_chunks), 2):
            print(f"Refining chunks {i + 1} and {i + 2} of {len(findings_chunks)}...")
            if i + 1 < len(findings_chunks):  # Check if there's a next chunk
                prompt = f"You are a researcher assistant. Your task is to read two sets of research findings and identify the most valuable findings based on the user's research goal: '{user_goal}'. The research findings are as follows:\n\nFindings set 1:\n{findings_chunks[i]}\n\nFindings set 2:\n{findings_chunks[i + 1]}.\n\nResearcher, please write the most valuable research findings that are directly relevant to the user's goal."
                response = ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system",
                         "content": "You are a researcher assistant. Your task is to read two sets of research findings and identify the most valuable findings based on the user's research goal."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                )
                refined_findings_chunks.append(response['choices'][0]['message']['content'].strip())
            else:  # If there's no next chunk, just add the current chunk to the refined review chunks
                refined_findings_chunks.append(findings_chunks[i])
        findings_chunks = refined_findings_chunks

    final_findings = findings_chunks[0]  # Now, only one chunk is left which is the final findings

    # Write the key findings into a file
    findings_file = os.path.join(goal_findings_folder, f'{subdirectory_name}_research_findings.txt')
    with open(findings_file, 'w', encoding='utf-8') as file:
        file.write(final_findings)


if __name__ == "__main__":
    print("Generating research findings...")

    input_folder = 'Upload here'
    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Loop over all folders in the output folder
    subdirectories = [subdir for subdir in os.listdir(output_folder) if os.path.isdir(os.path.join(output_folder, subdir))]

    for subdir in subdirectories:
        generate_research_findings(output_folder, subdir)

    print("Research findings generation complete.")