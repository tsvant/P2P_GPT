# generate_literature_sources_list.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY
import futures3
from futures3 import ThreadPoolExecutor

openai.api_key = API_KEY

def generate_source_list(chunk):
    # Define the prompt for this chunk
    prompt = f"Researcher, please write a 'List of Literature Sources' based on the following mess of metadata on the sources used in our research:\n\n{chunk}. \n\n Researcher, the 'List of Literature Sources' should be written by you in the following format: 'n. Authors. Name of the research paper. // Publishing House. - Year. - Issue. - Pages.' The sources should be sorted alphabetically. Each source has to be mentioned once."

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
    return response['choices'][0]['message']['content'].strip()

def generate_literature_sources_list(output_folder):
    """Generate the 'List of Literature Sources' based on the full abstracts of the papers."""

    print("Starting to generate 'List of Literature Sources'...")

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

    # Split the full abstracts into chunks of approximately 12000 characters each
    chunk_size = 12000  # Define the size of each chunk
    abstract_chunks = [full_abstracts_all[i:i + chunk_size] for i in range(0, len(full_abstracts_all), chunk_size)]

    with ThreadPoolExecutor() as executor:
        literature_sources_lists = list(executor.map(generate_source_list, abstract_chunks))

    # Continue to refine list of literature sources until it is a single list
    print("Refining 'List of Literature Sources'...")

    # Continue to refine list of literature sources until it is a single list
    while len(literature_sources_lists) > 1:
        refined_literature_sources_lists = []
        for i in range(0, len(literature_sources_lists), 2):
            print(f"Refining lists {i + 1} and {i + 2} of {len(literature_sources_lists)}...")
            if i + 1 < len(literature_sources_lists):  # Check if there's a next list
                prompt = f"Researched, please write a single 'List of Literature Sources' that combines and alphabetizes the two given lists. The lists are as follows:\n\nList 1:\n{literature_sources_lists[i]}\n\nList 2:\n{literature_sources_lists[i + 1]} \n\n Researcher, if some specific bit of information on a certain paper says 'Empty', don't write this bit of information, write just the known bit on each paper. The same goes when it says a bit is unknown, or the bit doesn't actually contain any info, for example instead of numbers of pages it just says 'Pages', you are supposed to ignore these bits."
                response = ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system",
                         "content": "You are a researcher. Your task is to read the two lists of literature sources and to write a single, alphabetized 'List of Literature Sources' that combines them. Researcher, if some specific bit of information on a certain paper says 'Empty', don't write this bit of information, write just the known bits on each paper. The same goes when it says a bit is unknown, or the bit doesn't actually contain any info, for example instead of numbers of pages it just says 'Pages', you are supposed to ignore these bits."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                )
                refined_literature_sources_lists.append(response['choices'][0]['message']['content'].strip())
            else:  # If there's no next list, just add the current list to the refined lists
                refined_literature_sources_lists.append(literature_sources_lists[i])
        literature_sources_lists = refined_literature_sources_lists

    literature_sources_list = literature_sources_lists[0]  # Now, only one list is left which is the final list of literature sources

    print("Writing 'List of Literature Sources' to file...")

    # Write the 'List of Literature Sources' into a file
    with open(final_literature_sources_list_file, 'w', encoding='utf-8') as file:
        file.write(literature_sources_list)

    print("'List of Literature Sources' generation complete.")

if __name__ == "__main__":
    print("Generating 'List of Literature Sources'...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate the 'List of Literature Sources'
    generate_literature_sources_list(output_folder)

    print("'List of Literature Sources' generation complete.")