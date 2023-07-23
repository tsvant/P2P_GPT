# section_i_generation.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_section_i(output_folder, section_number):
    """Generate Section i based on the 'Section_i_Sources' and Literature Review fragments."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    section_sources_file = os.path.join(new_paper_folder, f'Section_{section_number}_Sources.txt')
    literature_review_folder = os.path.join(new_paper_folder, 'Literature Review')

    # Check if the current section's sources file exists
    if not os.path.isfile(section_sources_file):
        print(f"Section_{section_number}_Sources file is not yet created. Skipping Section {section_number} generation for now.")
        return

    # Load the 'Section_i_Sources' file
    with open(section_sources_file, 'r', encoding='utf-8') as file:
        section_sources_text = file.read().strip()

    # Load the Literature Review fragments
    literature_review_files = [file for file in os.listdir(literature_review_folder) if file.endswith('_Literature_Review.txt')]
    literature_review_fragments = []

    for file in literature_review_files:
        file_path = os.path.join(literature_review_folder, file)
        with open(file_path, 'r', encoding='utf-8') as file:
            fragment = file.read().strip()
            literature_review_fragments.append(fragment)

    # Join all Literature Review fragments
    literature_review_all = '\n\n'.join(literature_review_fragments)

    # Define the prompt
    prompt = f"GPT, please generate the text for Section {section_number} based on the provided advice and the Literature Review fragments. Here are the advice to follow strictly:\n\n{section_sources_text}\n\nThe Literature Review fragments are as follows:\n\n{literature_review_all}."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": f"You are a researcher. Your task is to generate the text for Section {section_number} based on the provided advice and the Literature Review fragments. Please ensure that the generated text aligns with the advice and incorporates relevant information from the Literature Review fragments. You should properly reference the sources you are given and acknowledge which source a particular idea comes from."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    section_i_text = response['choices'][0]['message']['content'].strip()

    # Write the Section i text into a file
    section_i_file = os.path.join(new_paper_folder, f'Section_{section_number}.txt')
    with open(section_i_file, 'w', encoding='utf-8') as file:
        file.write(section_i_text)


if __name__ == "__main__":
    print(f"Generating Section i...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Define the section numbers
    section_numbers = ["1.2", "1.3", "2.1", "2.2", "2.3"]

    for section_number in section_numbers:
        new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
        # Check if the current section's file already exists
        section_i_file = os.path.join(new_paper_folder, f'Section_{section_number}.txt')

        if os.path.isfile(section_i_file):
            print(f"Section {section_number} file already exists. Skipping its generation.")
            continue

        # Generate Section i
        generate_section_i(output_folder, section_number)

    print("Section generation complete.")