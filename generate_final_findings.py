# generate_final_findings.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY
from futures3 import ThreadPoolExecutor

openai.api_key = API_KEY

def load_research_findings(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def process_findings_chunk(chunk, basic_prompt):
    prompt = f"GPT, please act as a researcher and generate comprehensive research findings based on the provided research findings. The findings from the research papers are summarized as follows:\n\n{chunk}\n\n{basic_prompt}"
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a researcher. Your task is to generate finalized research findings based on the provided research findings."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response['choices'][0]['message']['content'].strip() + "\n\n"

def generate_final_findings(output_folder):
    """Generate finalized research findings based on the research_findings files for each research paper."""

    print("Starting to generate final research findings...")

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    new_paper_findings_file = os.path.join(new_paper_folder, 'Brand new findings.txt')

    # Create the necessary folders if they don't exist
    os.makedirs(new_paper_folder, exist_ok=True)

    # Retrieve the existing research findings for each paper
    research_findings_files = [
        os.path.join(output_folder, subdir, 'Research findings', f'{subdir}_research_findings.txt') for subdir in
        os.listdir(output_folder) if
        subdir != '0. Brand new research paper' and os.path.isdir(os.path.join(output_folder, subdir))]

    with ThreadPoolExecutor() as executor:
        research_findings = list(executor.map(load_research_findings, research_findings_files))

    # Load the user's research goal text
    parent_directory = os.path.dirname(output_folder)
    user_input_folder = os.path.join(parent_directory, 'User input')
    user_goal_file = os.path.join(user_input_folder, 'user_goal.txt')

    with open(user_goal_file, 'r', encoding='utf-8') as file:
        user_goal = file.read().strip()

    # Define the basic part of the prompt
    basic_prompt = f"Requirements for the finalized research findings are:\n1. Clarity and Precision\n2. Reproducibility\n3. Statistical Significance\n4. Interpretation and Discussion\n5. Transparency\n6. Ethical Considerations.\n\nThe user's research goal is: '{user_goal}'."

    # Concatenate the research findings together
    findings_text = '\n\n'.join(research_findings)

    # Split the findings text into chunks of approximately 12000 characters each
    chunk_size = 12000  # Define the size of each chunk
    findings_chunks = [findings_text[i:i + chunk_size] for i in range(0, len(findings_text), chunk_size)]

    final_findings = ""
    with ThreadPoolExecutor() as executor:
        final_findings_parts = list(
            executor.map(lambda chunk: process_findings_chunk(chunk, basic_prompt), findings_chunks))
    final_findings = ''.join(final_findings_parts)

    print("Refining final research findings...")

    # Continue to refine findings until they are under 12000 characters
    while len(final_findings) > chunk_size:
        findings_chunks = [final_findings[i:i + chunk_size] for i in range(0, len(final_findings), chunk_size)]
        refined_findings = ""
        for i, chunk in enumerate(findings_chunks):
            print(f"Refining chunk {i + 1} of {len(findings_chunks)}...")
            prompt = f"GPT, please refine these research findings by selecting the most valuable insights. The findings are as follows:\n\n{chunk}\n\n{basic_prompt}"
            response = ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system",
                     "content": "You are a researcher. Your task is to refine these research findings."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )
            refined_findings += response['choices'][0]['message']['content'].strip() + "\n\n"
        final_findings = refined_findings

    print("Writing final research findings to file...")

    # Write the final findings into a file
    with open(new_paper_findings_file, 'w', encoding='utf-8') as file:
        file.write(final_findings)

    print("Final research findings generation complete.")

if __name__ == "__main__":
    print("Generating final research findings...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate final research findings
    generate_final_findings(output_folder)

    print("Final research findings generation complete.")