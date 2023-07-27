# generate_literature_sources_list.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY

def generate_literature_sources_list(output_folder):
    """Generate the 'List of Literature Sources' based on the full abstracts of the papers."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    final_literature_sources_list_file = os.path.join(new_paper_folder, 'List_of_Literature_Sources.txt')

    # Load the full abstracts
    full_abstract_files = []
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            if file == 'full_abstract.txt':
                full_abstract_files.append(os.path.join(root, file))

    full_abstracts = []
    for file in full_abstract_files:
        with open(file, 'r', encoding='utf-8') as file:
            abstract = file.read().strip()
            full_abstracts.append(abstract)

    # Join all full abstracts
    full_abstracts_all = '\n\n'.join(full_abstracts)

    # Define the prompt
    prompt = f"Please generate a 'List of Literature Sources' based on the following full abstracts:\n\n{full_abstracts_all}."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to generate a 'List of Literature Sources' based on the provided metadata for each. The list should be in the following format: 'n. Authors. Name of the research paper. // Publishing House. - Year. - Issue. - Pages.' The sources should be sorted alphabetically."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    literature_sources_list = response['choices'][0]['message']['content'].strip()

    # Write the 'List of Literature Sources' into a file
    with open(final_literature_sources_list_file, 'w', encoding='utf-8') as file:
        file.write(literature_sources_list)

if __name__ == "__main__":
    print("Generating 'List of Literature Sources'...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate the 'List of Literature Sources'
    generate_literature_sources_list(output_folder)

    print("'List of Literature Sources' generation complete.")
