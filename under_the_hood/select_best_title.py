# select_best_title.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY

def select_best_title(output_folder):
    """Select the best title for the research paper."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    best_title_file = os.path.join(new_paper_folder, 'Best title.txt')

    # Load the conclusion and potential titles files
    files_to_load = ['Brand new conclusion.txt', 'Potential titles.txt']
    loaded_texts = {}

    for filename in files_to_load:
        file_path = os.path.join(new_paper_folder, filename)

        if not os.path.isfile(file_path):
            print(f"{filename} not found. Skipping best title selection.")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            loaded_texts[filename] = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please select the best title for our research paper based on its conclusion and the list of potential titles. The conclusion of the paper is as follows:\n\n{loaded_texts['Brand new conclusion.txt']}\n\nThe list of potential titles is as follows:\n\n{loaded_texts['Potential titles.txt']}"

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to select the best title for the research paper based on its conclusion and the list of potential titles. Reply with just its title."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,  # Make the output completely deterministic
    )

    # Extract the text from the response
    best_title = response['choices'][0]['message']['content'].strip()

    # Write the best title into a file
    with open(best_title_file, 'w', encoding='utf-8') as file:
        file.write(best_title)


if __name__ == "__main__":
    print("Selecting the best title...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Select the best title
    select_best_title(output_folder)

    print("Best title selection complete.")
