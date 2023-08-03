# generate_final_literature_review.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_final_literature_review(output_folder):
    """Generate the final 'Literature Review' section based on the research objectives and literature review fragments."""

    print("Starting to generate final 'Literature Review' section...")

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    literature_review_folder = os.path.join(new_paper_folder, 'Literature Review')
    final_literature_review_file = os.path.join(new_paper_folder, '0. Final_Literature_Review.txt')

    # Load the user's research goal
    user_input_folder = os.path.join(os.getcwd(), 'User input')
    user_goal_file = os.path.join(user_input_folder, 'user_goal.txt')

    if not os.path.isfile(user_goal_file):
        print("User goal file not found. Skipping final 'Literature Review' section generation.")
        return

    with open(user_goal_file, 'r', encoding='utf-8') as file:
        user_goal = file.read().strip()

    # Load the research objectives
    objectives_file = os.path.join(new_paper_folder, 'Research objectives list.txt')

    if not os.path.isfile(objectives_file):
        print("Research objectives file not found. Skipping final 'Literature Review' section generation.")
        return

    with open(objectives_file, 'r', encoding='utf-8') as file:
        objectives_text = file.read().strip()

    # Load the literature review fragments
    literature_review_files = [file for file in os.listdir(literature_review_folder) if
                               file.endswith('_Literature_Review.txt')]
    literature_review_fragments = []

    for file in literature_review_files:
        file_path = os.path.join(literature_review_folder, file)
        with open(file_path, 'r', encoding='utf-8') as file:
            fragment = file.read().strip()
            literature_review_fragments.append(fragment)

    # Join all literature review fragments
    literature_review_all = '\n\n'.join(literature_review_fragments)

    # Define the basic part of the prompt
    basic_prompt = f"Our research goal is: '{user_goal}'. You are not allowed to generate new sources. Just work with the research papers and authors that were given as a source. You are not allowed to mention other sources/authors. It is strictly forbidden. However little sources/authors you are given, this is how many you should use. "

    # Split the literature review into chunks of approximately 12000 characters each
    chunk_size = 12000  # Define the size of each chunk
    review_chunks = [literature_review_all[i:i + chunk_size] for i in range(0, len(literature_review_all), chunk_size)]

    final_literature_review = ""
    for i, chunk in enumerate(review_chunks):
        print(f"Processing chunk {i + 1} of {len(review_chunks)}...")

        # Define the prompt for this chunk
        prompt = f"The research objectives are as follows:\n\n{objectives_text}\n\nThe literature review fragments for each source are as follows:\n\n{chunk}\n\n{basic_prompt} \n\n Researcher, please write the final 'Literature Review' section for our study and our research goal based on the provided research objectives and literature review fragments. Refer to sources inside text like this: '(Author's surname, Author's initials, YEAR).'. If it's a first reference to a source in your written text, write its name, author and year in full inside the text like this: '(Author's surname, Author's initials, YEAR, name of the paper)'."

        # Query GPT-3
        response = ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system",
                 "content": "You are a researcher. Your task is to generate the final 'Literature Review' section based ONLY on the provided research objectives and literature review fragments. The literature review should critically evaluate the works we mention. It should summarize the main points of view and analyze these mentioned books or articles, emphasize what influence on the formation of the researcher's own opinion and helped achieve the results. Only relevant sources dedicated to our research goal and containing interesting and relevant information should be included. Please ensure that the final 'Literature Review' section provides a logical connection between the mentioned sources and groups them according to the authors' positions, the period of creation, or other relevant features. You are not allowed to generate new sources/authors. You are punished for every extra reference. It is strictly forbidden. However little sources/authors you are given, this is how many you should use. If there's only one source/author, use only one source/author, it is more important."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        # Extract the text from the response
        final_literature_review += response['choices'][0]['message']['content'].strip() + "\n\n"

    print("Refining final 'Literature Review' section...")

    # Take chunks and make one out of two, up until the only left
    while len(review_chunks) > 1:
        refined_review_chunks = []
        for i in range(0, len(review_chunks), 2):
            print(f"Refining chunks {i + 1} and {i + 2} of {len(review_chunks)}...")
            if i + 1 < len(review_chunks):  # Check if there's a next chunk
                prompt = f"You are a researcher. Your task is to read the drafts of a 'Literature Review' section of our research paper and to write a ready-to-print version that combines the two drafts. The literature review drafts are as follows:\n\nDraft 1:\n{review_chunks[i]}\n\nDraft 2:\n{review_chunks[i + 1]}. \nResearcher, please write the final 'Literature Review' section for our study. Don't say what this sections has to contain, fill it with what it has to contain. Don't mention drafts. If idea written is taken from a source with a reference, refer to this source inside text like this: '(Author's surname, Author's initials, YEAR).'. If it's first reference to a source in your written text, write its name, author and year in full inside the text like this: '(Author's surname, Author's initials, YEAR, name of the paper)'. Don't mention drafts. Please start writing."
                response = ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system",
                         "content": "You are a researcher. Your task is to read the drafts of a 'Literature Review' section of our research paper and to write a ready-to-print version that combines the two drafts."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                )
                refined_review_chunks.append(response['choices'][0]['message']['content'].strip())
            else:  # If there's no next chunk, just add the current chunk to the refined review chunks
                refined_review_chunks.append(review_chunks[i])
        review_chunks = refined_review_chunks

    final_literature_review = review_chunks[0]  # Now, only one chunk is left which is the final literature review

    print("Writing final 'Literature Review' section to file...")

    # Write the final 'Literature Review' section into a file
    with open(final_literature_review_file, 'w', encoding='utf-8') as file:
        file.write(final_literature_review)

    print("Final 'Literature Review' section generation complete.")

if __name__ == "__main__":
    print("Generating final 'Literature Review' section...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate the final 'Literature Review' section
    generate_final_literature_review(output_folder)

    print("Final 'Literature Review' section generation complete.")