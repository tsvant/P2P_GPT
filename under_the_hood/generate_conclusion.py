# generate_conclusion.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY

def generate_conclusion(output_folder):
    """Generate the Conclusion section for the research paper."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    conclusion_file = os.path.join(new_paper_folder, 'Brand new conclusion.txt')

    # Load necessary files
    files_to_load = ['Brand new intro.txt', 'Brand new findings.txt',
                     'Research table of contents.txt', 'Section_2.3_Final.txt']
    loaded_texts = {}

    for filename in files_to_load:
        file_path = os.path.join(new_paper_folder, filename)

        if not os.path.isfile(file_path):
            print(f"{filename} not found. Skipping Conclusion section generation.")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            loaded_texts[filename] = file.read().strip()

    # Define the prompt
    prompt = f"""Researcher, please write the Conclusion section for our research paper based on the provided information. 

    The Introduction section is as follows:\n\n{loaded_texts['Brand new intro.txt']}

    The research findings are as follows:\n\n{loaded_texts['Brand new findings.txt']}

    The research table of contents is as follows:\n\n{loaded_texts['Research table of contents.txt']}

    The final section of the main body is as follows:\n\n{loaded_texts['Section_2.3_Final.txt']}
    
    The conclusion should reflect upon the fulfillment of the research goals and objectives, justify the relevance of the chosen topic, describe the activities carried out, and analyze the obstacles faced during the research. The conclusion should start with the word 'Conclusion'., and a few introductory sentences (but never boring introductory phrases, e.g. 'in conclusion'), then provide a brief summary of the main part of the paper, and offer conclusions and recommendations. It should end with a memorable final paragraph. Please ensure that the Conclusion section is concise, coherent, and engaging. Never boring introductory phrases, e.g. 'in conclusion'.
    """

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to generate the Conclusion section for the research paper based on the provided information. The Conclusion should wrap up the paper by reflecting on the research goals and objectives, justifying the relevance of the topic, summarizing the activities carried out, and analyzing the obstacles faced during the research. It should also provide conclusions and recommendations and end with a memorable final paragraph. Please ensure that the Conclusion section is concise, coherent, and engaging. Never boring introductory phrases, e.g. 'in conclusion'."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )

    # Extract the text from the response
    conclusion_text = response['choices'][0]['message']['content'].strip()

    # Write the Conclusion section into a file
    with open(conclusion_file, 'w', encoding='utf-8') as file:
        file.write(conclusion_text)


if __name__ == "__main__":
    print("Generating Conclusion section...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate the Conclusion section
    generate_conclusion(output_folder)

    print("Conclusion section generation complete.")
