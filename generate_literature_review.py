# generate_literature_review.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_literature_review(output_folder, filename):
    """Generate a literature review fragment for each source used in the research."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    literature_review_folder = os.path.join(new_paper_folder, 'Literature Review')

    # Create the necessary folders if they don't exist
    os.makedirs(literature_review_folder, exist_ok=True)

    # Load the abstract and research findings text
    abstract_file = os.path.join(output_folder, filename, 'full_abstract.txt')
    findings_file = os.path.join(output_folder, filename, 'Research findings', f'{filename}_research_findings.txt')

    # Exclude the "0. Brand new research paper" folder
    if filename == "0. Brand new research paper":
        return

    if not os.path.isfile(abstract_file):
        print(f"Abstract file not found for {filename}. Skipping Literature Review generation.")
        return

    if not os.path.isfile(findings_file):
        print(f"Research findings file not found for {filename}. Skipping Literature Review generation.")
        return

    with open(abstract_file, 'r', encoding='utf-8') as file:
        abstract_text = file.read().strip()

    with open(findings_file, 'r', encoding='utf-8') as file:
        findings_text = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please generate a concise literature review fragment for this source based on the provided abstract for it and the research findings that were derived from it. The metadata and abstract of the source is as follows:\n\n{abstract_text}\n\nThe research findings from the source are as follows:\n\n{findings_text}."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to generate a concise literature review fragment for the provided source based on the provided abstract and research findings. This literature review fragment should critically evaluate this work on the topic of our research goal. It should summarize the main points of view and analyze this article/book that had the greatest influence on the formation of the researcher's own opinion and helped achieve the results. Only relevant information should be included."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    literature_review_fragment = response['choices'][0]['message']['content'].strip()

    # Write the literature review fragment into a file
    literature_review_file = os.path.join(literature_review_folder, f'{filename}_Literature_Review.txt')
    with open(literature_review_file, 'w', encoding='utf-8') as file:
        file.write(literature_review_fragment)


if __name__ == "__main__":
    print("Generating literature review fragments...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Loop over all folders in the output folder
    subdirectories = [subdir for subdir in os.listdir(output_folder) if os.path.isdir(os.path.join(output_folder, subdir))]

    for subdir in subdirectories:
        generate_literature_review(output_folder, subdir)

    print("Literature review fragments generation complete.")