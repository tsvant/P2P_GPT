import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY

def generate_abstract(output_folder):
    """Generate the Abstract section for the research paper."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    abstract_file = os.path.join(new_paper_folder, 'Brand new abstract.txt')

    # Load necessary files
    files_to_load = ['Brand new intro.txt', 'Brand new conclusion.txt']
    loaded_texts = {}

    for filename in files_to_load:
        file_path = os.path.join(new_paper_folder, filename)

        if not os.path.isfile(file_path):
            print(f"{filename} not found. Skipping Abstract section generation.")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            loaded_texts[filename] = file.read().strip()

    # Define the prompt
    prompt = f"""Researcher, please write an Abstract section for our research paper based on the provided information. 

    The Introduction section is as follows:\n\n{loaded_texts['Brand new intro.txt']}

    The Conclusion section is as follows:\n\n{loaded_texts['Brand new conclusion.txt']}
    
    The Abstract should be self-contained, fully understandable on its own, and reflect the structure of the larger work. It should start by defining the purpose of the research, state the objective, describe the research methods used, summarize the main research results, and discuss the main conclusions. The abstract should also provide keywords related to the research, use only the most relevant terms. The abstract should avoid passive sentences, long sentences, obscure jargon, repetition and filler words, and detailed descriptions. Please ensure that the Abstract section is concise, coherent, and engaging. Avoid using boring introductory phrases as 'in conclusion'.
    """

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to write an Abstract section for the research paper based on the provided information. The Abstract should be a self-contained text, not an excerpt from your paper, and fully understandable on its own. It should reflect the structure of your larger work, starting by clearly defining the purpose of your research. This part should be in the present or past simple tense. Next, indicate the research methods that you used to answer your question, providing a straightforward description without evaluating validity or obstacles. Summarize the main research results, highlighting the most important findings. Finally, discuss the main conclusions of your research, if very necessary include recommendations for implementation or suggestions for further research. Provide a list of keywords related to the research at the end, use only the most relevant terms. Remember to avoid passive sentences, long sentences, obscure jargon, repetition and filler words, and detailed descriptions. Keep it as short as possible without leaving important information."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )

    # Extract the text from the response
    abstract_text = response['choices'][0]['message']['content'].strip()

    # Write the Abstract section into a file
    with open(abstract_file, 'w', encoding='utf-8') as file:
        file.write(abstract_text)


if __name__ == "__main__":
    print("Generating Abstract section...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate the Abstract section
    generate_abstract(output_folder)

    print("Abstract section generation complete.")
