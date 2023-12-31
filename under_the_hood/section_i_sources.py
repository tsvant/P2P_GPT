import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_section_sources(output_folder, section_number, toc_text, literature_review_text, objectives_text):
    """Generate the 'Section_i_Sources' file for a specific section of the research paper."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    section_sources_file = os.path.join(new_paper_folder, f'Section_{section_number}_Sources.txt')

    # Define the section number and its prerequisite
    section_to_prerequisite = {
        "1.2": "1.1",
        "1.3": "1.2",
        "2.1": "1.3",
        "2.2": "2.1",
        "2.3": "2.2"
    }

    prev_section_number = section_to_prerequisite.get(section_number, "1")
    prev_section_file = os.path.join(new_paper_folder, f'Section_{prev_section_number}_Final.txt')

    if not os.path.isfile(prev_section_file) and section_number != "1":
        print(f"Previous section file (Section_{prev_section_number}_Final.txt) not found. Skipping 'Section_{section_number}_Sources' file generation.")
        return

    # Define the prompt
    prompt = f"The table of contents is as follows:\n\n{toc_text}\n\nThe final 'Literature Review' section is as follows:\n\n{literature_review_text}\n\nThe research objectives are as follows:\n\n{objectives_text}.\n\n Researcher, please analyze the table of contents, the final 'Literature Review' section, and the research objectives to name the naming of Section {section_number}, determine the relevant sources for Section {section_number}, and provide information on which specific research objective(s) is(are) expected to be addressed within this section. By analyzing the table of contents and objectives, please tell what role, narratively, in the process of gradually meeting our objectives section by section, Section {section_number} has to play in the overall research paper and with connection to other sections, give advices to the writer. Remember, that Section 2.3 is the last one of the main body of the research paper and thus it has to wrap everything up."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to analyze the table of contents, the final 'Literature Review' section, and the research objectives to determine the relevant sources for the specific section of the research paper. Please ensure that the selected sources are directly related to the content of the section and provide valuable insights and information. Additionally, provide information on which specific research objective is expected to be addressed within this section."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    # Extract the text from the response
    section_sources_text = response['choices'][0]['message']['content'].strip()

    # Write the 'Section_i_Sources' file
    with open(section_sources_file, 'w', encoding='utf-8') as file:
        file.write(section_sources_text)


if __name__ == "__main__":
    print("Generating 'Section_i_Sources' file...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Define the section number and its prerequisite
    section_to_prerequisite = {
        "1.2": "1.1",
        "1.3": "1.2",
        "2.1": "1.3",
        "2.2": "2.1",
        "2.3": "2.2"
    }

    for section_number, prerequisite in section_to_prerequisite.items():
        new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
        prev_section_file = os.path.join(new_paper_folder, f'Section_{prerequisite}_Final.txt')

        if not os.path.isfile(prev_section_file):
            continue

        # Check if the current section's sources file already exists
        section_sources_file = os.path.join(new_paper_folder, f'Section_{section_number}_Sources.txt')

        if os.path.isfile(section_sources_file):
            continue

        # Load the table of contents
        toc_file = os.path.join(new_paper_folder, 'Research table of contents.txt')

        if not os.path.isfile(toc_file):
            continue

        with open(toc_file, 'r', encoding='utf-8') as file:
            toc_text = file.read().strip()

        # Load the final literature review
        literature_review_file = os.path.join(new_paper_folder, '0. Final_Literature_Review.txt')

        if not os.path.isfile(literature_review_file):
            continue

        with open(literature_review_file, 'r', encoding='utf-8') as file:
            literature_review_text = file.read().strip()

        # Load the research objectives
        objectives_file = os.path.join(new_paper_folder, 'Research objectives list.txt')

        if not os.path.isfile(objectives_file):
            continue

        with open(objectives_file, 'r', encoding='utf-8') as file:
            objectives_text = file.read().strip()

        # Generate the 'Section_i_Sources' file
        generate_section_sources(output_folder, section_number, toc_text, literature_review_text, objectives_text)

    print("Section sources file generation complete.")


