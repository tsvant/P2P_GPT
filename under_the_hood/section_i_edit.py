import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def edit_section_i(output_folder, section_number, prev_section_number):
    """Edit the Section i text to a finalized, ready-to-publish variant."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    toc_file = os.path.join(new_paper_folder, 'Research table of contents.txt')
    section_i_file = os.path.join(new_paper_folder, f'Section_{section_number}.txt')

    # Check if the current section's file exists
    if not os.path.isfile(section_i_file):
        print(f"Section {section_number} file not found. Skipping Section {section_number} editing.")
        return

    # Load the Research table of contents
    if not os.path.isfile(toc_file):
        print("Research table of contents file not found. Skipping Section {section_number} editing.")
        return

    with open(toc_file, 'r', encoding='utf-8') as file:
        toc_text = file.read().strip()

    # Load the Section i text
    with open(section_i_file, 'r', encoding='utf-8') as file:
        section_i_text = file.read().strip()

    # Load the previous section's finalized text
    prev_section_file = os.path.join(new_paper_folder, f'Section_{prev_section_number}_Final.txt')

    if not os.path.isfile(prev_section_file) and section_number != "1.2":
        print(
            f"Previous section file (Section_{prev_section_number}_Final.txt) not found. Skipping Section {section_number} editing.")
        return

    with open(prev_section_file, 'r', encoding='utf-8') as file:
        prev_section_text = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please edit the Section {section_number} text to a finalized, ready-to-publish variant based on the provided Research table of contents, the previous section's finalized text, and the current Section {section_number} text. The Research table of contents, for you to know the whole structure of the research paper and therefore to know what text should be present in our specific section, is as follows:\n\n{toc_text}\n\nThe previous section's finalized text, for you to refer to and maintain consistency, is as follows:\n\n{prev_section_text}\n\nThe current Section {section_number} text, for you to edit based on the prompt that follows, is as follows:\n\n{section_i_text}\n\nPrompt: Topic Sentence: Begin each section with a sentence that clearly states the main point or idea of that section. This serves as a guide to the reader and lets them know what to expect in the coming paragraphs.\n\nExplanation/Development: After your topic sentence, provide information, evidence, or arguments that expand upon and support your main point. This is where you delve into the details of your topic. Depending on what the section is about, this could involve presenting your research findings, analyzing a text, discussing a theoretical concept, etc.\n\nEvidence: Where appropriate, include specific evidence to support your points. This could be in the form of data from your research, quotes from primary or secondary sources, examples, etc. Make sure to properly cite all sources.\n\nAnalysis: Don't just present information or evidence; analyze it. Discuss what it means, why it's important, how it supports your main point, etc.\n\nEnd the section with a transition to the next topic or section (exception is only Section 2.3). This could be a sentence that summarizes the main point of the section and hints at what's to come, or a more explicit transition that directly states what the next section will be about.\n\nRemember to keep each section focused. Each section should have a clear main point, and everything in that section should support or develop that point. Avoid going off on tangents or including irrelevant information, as this can confuse the reader and dilute your main message.\n\nAlso, be aware of the flow and cohesion of your writing. Use transitions to guide the reader through your argument, and make sure your sentences and paragraphs flow smoothly from one to the next. Remember, that Section 2.3 is the last one of the main body of the research paper and thus it has to wrap everything up. Avoid using boring introductory phrases as 'in conclusion'."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": f"You are a researcher. Your task is to edit the Section {section_number} text to a finalized, ready-to-publish variant based on the provided Research table of contents, the previous section's finalized text, and the current Section {section_number} text. Follow the provided prompt to ensure the section has a clear topic sentence, includes relevant information and evidence, provides analysis, and ends with a transition. Maintain focus, coherence, and flow throughout the section. Make it engaging, but professional."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
    )

    # Extract the text from the response
    edited_section_i_text = response['choices'][0]['message']['content'].strip()

    # Write the edited Section i text into a file
    edited_section_i_file = os.path.join(new_paper_folder, f'Section_{section_number}_Final.txt')
    with open(edited_section_i_file, 'w', encoding='utf-8') as file:
        file.write(edited_section_i_text)


if __name__ == "__main__":
    print(f"Editing Section i...")

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

        # Check if the current section's finalized file already exists
        section_final_file = os.path.join(new_paper_folder, f'Section_{section_number}_Final.txt')

        if os.path.isfile(section_final_file):
            continue

        # Edit Section i
        edit_section_i(output_folder, section_number, prerequisite)

    print("Section editing complete.")