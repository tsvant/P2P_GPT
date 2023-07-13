import os
import openai
from openai import ChatCompletion
from config import API_KEY
from data_processing import split_text, process_file, find_abstract, compile_abstracts
from goal_alignment import create_goal_alignment_analysis, create_step_by_step_chunk_analysis

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


print("Starting data processing...")
input_folder = 'Upload here'
output_folder = os.path.join(os.getcwd(), 'P2P Output')
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

for file_index, filename in enumerate(input_files, start=1):
    print(f"Processing file {file_index}/{total_files}: {filename}")

    process_file(os.path.join(input_folder, filename), output_folder)

    # Get the subdirectory name for the current file being processed
    subdirectory = os.path.splitext(filename)[0]

    # Create goal alignment analysis and step by step chunk analysis for the subdirectory
    create_goal_alignment_analysis(output_folder, user_goal_filename)
    create_step_by_step_chunk_analysis(output_folder, user_goal_filename, subdirectory)

    print(f"Completed processing file {file_index}/{total_files}: {filename}\n")

print("Data processing complete.")