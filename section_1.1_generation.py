# section_1.1_generation.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_section_1_1(output_folder):
    """Generate Section 1.1 based on the 'Section_1.1_Sources' and Literature Review fragments."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    section_sources_file = os.path.join(new_paper_folder, 'Section_1.1_Sources.txt')
    literature_review_folder = os.path.join(new_paper_folder, 'Literature Review')

    # Load the 'Section_1.1_Sources' file
    if not os.path.isfile(section_sources_file):
        print("Section_1.1_Sources file not found. Skipping Section 1.1 generation.")
        return

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
    prompt = f"GPT, please generate the text for Section 1.1 based on the provided advices and the Literature Review fragments. Here are the advices to follow strictly:\n\n{section_sources_text}\n\nThe Literature Review fragments are as follows:\n\n{literature_review_all}."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to generate the text for Section 1.1 based on the provided advices and the Literature Review fragments. Please ensure that the generated text aligns with the advices and incorporates relevant information from the Literature Review fragments. You should do the referencing for the sources you are given and take relevant information from, a proper acknowledgement of which source a particular idea comes from."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    section_1_1_text = response['choices'][0]['message']['content'].strip()

    # Write the Section 1.1 text into a file
    section_1_1_file = os.path.join(new_paper_folder, 'Section_1.1.txt')
    with open(section_1_1_file, 'w', encoding='utf-8') as file:
        file.write(section_1_1_text)


if __name__ == "__main__":
    print("Generating Section 1.1...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate Section 1.1
    generate_section_1_1(output_folder)

    print("Section 1.1 generation complete.")