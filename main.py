import os
import openai
from config import API_KEY
from get_user_goal import get_user_goal
from save_checkpoint import save_checkpoint
from load_checkpoint import load_checkpoint
from data_processing import split_text, process_file, find_abstract, compile_abstracts
from goal_alignment import create_step_by_step_chunk_analysis
from generate_findings import generate_research_findings
from generate_final_findings import generate_final_findings
from generate_objectives import generate_research_objectives
from generate_table_of_contents import generate_table_of_contents
from generate_literature_review import generate_literature_review
from generate_final_literature_review import generate_final_literature_review
from generate_intro import generate_intro
from section_1_1_sources import generate_section_sources as generate_section_1_1_sources
from section_1_1_generation import generate_section_1_1
from section_1_1_edit import edit_section_1_1
from section_i_sources import generate_section_sources as generate_section_i_sources
from section_i_generation import generate_section_i
from section_i_edit import edit_section_i
from generate_conclusion import generate_conclusion
from generate_titles import generate_titles
from select_best_title import select_best_title
from generate_literature_sources_list import generate_literature_sources_list
from generate_abstract import generate_abstract
from generate_final_paper import generate_final_paper




import time
import openai.error

openai.api_key = API_KEY

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
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Brand new findings.txt')):
        generate_final_findings(output_folder)

    # Generate research objectives
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Research objectives list.txt')):
        generate_research_objectives(output_folder)

    # Generate table of contents
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Research table of contents.txt')):
        generate_table_of_contents(output_folder)

    # Generate literature review fragments
    for subdir in os.listdir(output_folder):
        generate_literature_review(output_folder, subdir)

    # Generate the final 'Literature Review' section
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', '0. Final_Literature_Review.txt')):
        generate_final_literature_review(output_folder)

    # Generate intro
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Brand new intro.txt')):
        generate_intro(output_folder)

    # Also pass necessary parameters to generate_section_sources
    section_number = "1.1"
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')

    # Load the table of contents
    toc_file = os.path.join(new_paper_folder, 'Research table of contents.txt')
    with open(toc_file, 'r', encoding='utf-8') as file:
        toc_text = file.read().strip()

    # Load the final literature review
    literature_review_file = os.path.join(new_paper_folder, '0. Final_Literature_Review.txt')
    with open(literature_review_file, 'r', encoding='utf-8') as file:
        literature_review_text = file.read().strip()

    # Load the research objectives
    objectives_file = os.path.join(new_paper_folder, 'Research objectives list.txt')
    with open(objectives_file, 'r', encoding='utf-8') as file:
        objectives_text = file.read().strip()

    if not os.path.exists(os.path.join(new_paper_folder, f'Section_1.1_Sources.txt')):
        generate_section_1_1_sources(output_folder, section_number, toc_text, literature_review_text, objectives_text)
    if not os.path.exists(os.path.join(new_paper_folder, f'Section_1.1.txt')):
        generate_section_1_1(output_folder)
    if not os.path.exists(os.path.join(new_paper_folder, f'Section_1.1_Final.txt')):
        edit_section_1_1(output_folder)

    # After section 1.1 scripts
    section_numbers = ["1.2", "1.3", "2.1", "2.2", "2.3"]  # Add the section numbers you want to process
    section_to_prerequisite = {
        "1.2": "1.1",
        "1.3": "1.2",
        "2.1": "1.3",
        "2.2": "2.1",
        "2.3": "2.2"
    }

    for section_number in section_numbers:
        prerequisite = section_to_prerequisite.get(section_number)
        if not os.path.exists(os.path.join(new_paper_folder, f'Section_{section_number}_Sources.txt')):
            generate_section_i_sources(output_folder, section_number, toc_text, literature_review_text, objectives_text)
        if not os.path.exists(os.path.join(new_paper_folder, f'Section_{section_number}.txt')):
            generate_section_i(output_folder, section_number)
        if prerequisite and not os.path.exists(os.path.join(new_paper_folder, f'Section_{section_number}_Final.txt')):
            edit_section_i(output_folder, section_number, prerequisite)

    # Generate the Conclusion section
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Brand new conclusion.txt')):
        generate_conclusion(output_folder)

    # Generate the titles
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Potential titles.txt')):
        generate_titles(output_folder)

    # Select the best title
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Best title.txt')):
        select_best_title(output_folder)

    # Generate the list of literature sources
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'List_of_Literature_Sources.txt')):
        generate_literature_sources_list(output_folder)

    # Generate the abstract
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Brand new abstract.txt')):
        generate_abstract(output_folder)

    # Generate the final research paper
    if not os.path.exists(os.path.join(output_folder, '0. Brand new research paper', 'Final Research Paper.docx')):
        generate_final_paper(output_folder)

    print("Data processing complete.")

if __name__ == "__main__":
    main()
