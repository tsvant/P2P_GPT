# generate_titles.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY

def generate_titles(output_folder):
    """Generate a list of potential titles for the research paper."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    titles_file = os.path.join(new_paper_folder, 'Potential titles.txt')

    # Load the conclusion file
    conclusion_file = os.path.join(new_paper_folder, 'Brand new conclusion.txt')

    if not os.path.isfile(conclusion_file):
        print("Conclusion file not found. Skipping title generation.")
        return

    with open(conclusion_file, 'r', encoding='utf-8') as file:
        conclusion_text = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please generate a list of creative, engaging, and relevant titles for our research paper based on its conclusion. The conclusion of the paper is as follows:\n\n{conclusion_text}"

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to generate a list of potential titles for the research paper based on its conclusion. The titles should be creative, engaging, and relevant to the paper's content."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
    )

    # Extract the text from the response
    titles_text = response['choices'][0]['message']['content'].strip()

    # Write the titles into a file
    with open(titles_file, 'w', encoding='utf-8') as file:
        file.write(titles_text)


if __name__ == "__main__":
    print("Generating title options...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate the titles
    generate_titles(output_folder)

    print("Title generation complete.")
