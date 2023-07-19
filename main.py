import os
import openai
from openai import ChatCompletion
from config import API_KEY
from data_processing import split_text, process_file, find_abstract, compile_abstracts
from goal_alignment import create_step_by_step_chunk_analysis
from generate_findings import generate_research_findings
from generate_final_findings import generate_final_findings
from generate_objectives import generate_research_objectives
from generate_table_of_contents import generate_table_of_contents
from generate_literature_review import generate_literature_review

import time
import openai.error

openai.api_key = API_KEY


def get_user_goal(output_folder):
    """Prompt the user to enter the goal of their research paper and save it in a text file."""
    user_input_folder = os.path.join(os.path.dirname(output_folder), 'User input')
    os.makedirs(user_input_folder, exist_ok=True)

    user_goal = input("Please enter the goal of your research paper: ")
    goal_filename = os.path.join(user_input_folder, "user_goal.txt")

    with open(goal_filename, 'w', encoding="utf-8") as file:
        file.write(user_goal)

    return goal_filename


def save_checkpoint(output_folder, file_index):
    """Save the current file index to a checkpoint file."""
    checkpoint_file = os.path.join(output_folder, 'checkpoint.txt')

    with open(checkpoint_file, 'w', encoding='utf-8') as file:
        file.write(str(file_index))


def load_checkpoint(output_folder):
    """Load the last processed file index from the checkpoint file."""
    checkpoint_file = os.path.join(output_folder, 'checkpoint.txt')

    if os.path.isfile(checkpoint_file):
        with open(checkpoint_file, 'r', encoding='utf-8') as file:
            return int(file.read().strip())

    return 0


def main():
    print("Starting data processing...")
    input_folder = 'Upload here'
    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Retrieve the last processed file index from the checkpoint
    last_processed_file_index = load_checkpoint(output_folder)

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(input_folder, exist_ok=True)

    parent_directory = os.path.dirname(output_folder)
    user_input_folder = os.path.join(parent_directory, 'User input')
    os.makedirs(user_input_folder, exist_ok=True)

    user_goal_filename = get_user_goal(output_folder)  # Collect user goal

    # Loop over all text files in the input folder
    input_files = [filename for filename in os.listdir(input_folder) if filename.endswith('.txt')]
    total_files = len(input_files)
    print(f"Total files for processing: {total_files}\n")

    # Start from the last processed file index
    for file_index, filename in enumerate(input_files[last_processed_file_index:], start=last_processed_file_index + 1):
        print(f"Processing file {file_index}/{total_files}: {filename}")

        try:
            process_file(os.path.join(input_folder, filename), output_folder)

            subdirectory = os.path.splitext(filename)[0]
            create_step_by_step_chunk_analysis(output_folder, user_goal_filename, subdirectory)

            generate_research_findings(output_folder, subdirectory)
            generate_research_objectives(output_folder)
            generate_literature_review(output_folder, filename)  # Pass 'filename' as a parameter

            save_checkpoint(output_folder, file_index)

        except openai.error.ServiceUnavailableError:
            print("Service Unavailable Error. Retrying after 30 seconds...")
            time.sleep(30)  # Wait for 30 seconds before retrying the API call
            file_index -= 1  # Decrement file_index to retry the same file
            continue

        # Save the checkpoint after each successful iteration
        save_checkpoint(output_folder, file_index)

        print(f"Completed processing file {file_index}/{total_files}: {filename}\n")

    # Generate final research findings
    generate_final_findings(output_folder)

    # Generate research objectives
    generate_research_objectives(output_folder)

    generate_table_of_contents(output_folder)

    generate_literature_review(output_folder)

    print("Data processing complete.")


if __name__ == "__main__":
    main()