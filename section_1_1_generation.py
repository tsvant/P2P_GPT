# section_1.1_generation.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_section_1_1(output_folder):
    """Generate Section 1.1 based on the 'Section_1.1_Sources' and Literature Review fragments."""

    print("Starting to generate Section 1.1...")

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
    literature_review_files = [file for file in os.listdir(literature_review_folder) if
                               file.endswith('_Literature_Review.txt')]
    literature_review_fragments = []

    for file in literature_review_files:
        file_path = os.path.join(literature_review_folder, file)
        with open(file_path, 'r', encoding='utf-8') as file:
            fragment = file.read().strip()
            literature_review_fragments.append(fragment)

    # Join all Literature Review fragments
    literature_review_all = '\n\n'.join(literature_review_fragments)

    # Split the literature review into chunks of approximately 12000 characters each
    chunk_size = 8000  # Define the size of each chunk
    review_chunks = [literature_review_all[i:i + chunk_size] for i in range(0, len(literature_review_all), chunk_size)]

    section_1_1_text_chunks = []
    for i, chunk in enumerate(review_chunks):
        print(f"Processing chunk {i + 1} of {len(review_chunks)}...")

        # Define the prompt for this chunk
        prompt = f"Here are the advices to follow strictly:\n\n{section_sources_text}\n\nThe Literature Review fragments for individual papers are as follows:\n\n{chunk}.\n\nResearcher, please write the text for Section 1.1 based on the provided advices and the Literature Review fragments for individual papers above. You should do the referencing for the sources you are given and take relevant information from, a proper acknowledgement of which source a particular idea comes from. If idea written is taken from a source with a reference, refer to this source inside text like this: '(Gao, T., 2021).'. If it's first reference to a source, write its name, author and year in full inside the text like this: '(Gao, T., 2021, The mixed-ownership reform of Chinese state-owned enterprises and its implications for overseas economic expansion).'."

        # Query GPT-3
        response = ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system",
                 "content": "You are a researcher. Your task is to generate the text for Section 1.1 based on the provided advices and the Literature Review fragments. Please ensure that the generated text aligns with the advices and incorporates relevant information from the Literature Review fragments. You should do the referencing for the sources you are given and take relevant information from, a proper acknowledgement of which source a particular idea comes from. If idea written is taken from a source with a reference, refer to this source inside text like this: '(Gao, T., 2021).'. If it's first reference to a source, write its name, author and year in full inside the text like this: '(Gao, T., 2021, The mixed-ownership reform of Chinese state-owned enterprises and its implications for overseas economic expansion).'."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        # Extract the text from the response and add to the list of chunks
        section_1_1_text_chunks.append(response['choices'][0]['message']['content'].strip())

    print("Refining Section 1.1 text...")

    # Continue to refine section 1.1 until it is under 12000 characters
    while len(section_1_1_text_chunks) > 1:
        refined_section_1_1_chunks = []
        for i in range(0, len(section_1_1_text_chunks), 2):
            print(f"Refining chunks {i + 1} and {i + 2} of {len(section_1_1_text_chunks)}...")
            if i + 1 < len(section_1_1_text_chunks):  # Check if there's a next chunk
                prompt = f"GPT, please generate the refined text for Section 1.1 that combines the two drafts. The drafts are as follows:\n\nDraft 1:\n{section_1_1_text_chunks[i]}\n\nDraft 2:\n{section_1_1_text_chunks[i + 1]}"
                response = ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system",
                         "content": "You are a researcher. Your task is to read the drafts of Section 1.1 of our research paper and to write a ready-to-print version that combines the two drafts."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                )
                refined_section_1_1_chunks.append(response['choices'][0]['message']['content'].strip())
            else:  # If there's no next chunk, just add the current chunk to the refined review chunks
                refined_section_1_1_chunks.append(section_1_1_text_chunks[i])
        section_1_1_text_chunks = refined_section_1_1_chunks

    section_1_1_text = section_1_1_text_chunks[0]  # Now, only one chunk is left which is the final section 1.1 text

    print("Writing Section 1.1 text to file...")

    # Write the Section 1.1 text into a file
    section_1_1_file = os.path.join(new_paper_folder, 'Section_1.1.txt')
    with open(section_1_1_file, 'w', encoding='utf-8') as file:
        file.write(section_1_1_text)

    print("Section 1.1 generation complete.")

if __name__ == "__main__":
    print("Generating Section 1.1...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate Section 1.1
    generate_section_1_1(output_folder)

    print("Section 1.1 generation complete.")