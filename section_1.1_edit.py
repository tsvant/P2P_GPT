# section_1.1_edit.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def edit_section_1_1(output_folder):
    """Edit the Section 1.1 text to a finalized, ready-to-publish variant."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    toc_file = os.path.join(new_paper_folder, 'Research table of contents.txt')
    section_1_1_file = os.path.join(new_paper_folder, 'Section_1.1.txt')

    # Load the Research table of contents
    if not os.path.isfile(toc_file):
        print("Research table of contents file not found. Skipping Section 1.1 editing.")
        return

    with open(toc_file, 'r', encoding='utf-8') as file:
        toc_text = file.read().strip()

    # Load the Section 1.1 text
    if not os.path.isfile(section_1_1_file):
        print("Section 1.1 file not found. Skipping Section 1.1 editing.")
        return

    with open(section_1_1_file, 'r', encoding='utf-8') as file:
        section_1_1_text = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please edit the Section 1.1 text to a finalized, ready-to-publish variant based on the provided Research table of contents and the current Section 1.1 text. The Research table of contents, for you to know the whole structure of the research paper and therefore to know what text should be present in our specific section, is as follows:\n\n{toc_text}\n\nThe current Section 1.1 text, for you to edit based on the prompt that follows, is as follows:\n\n{section_1_1_text}\n\nPrompt: Topic Sentence: Begin each section with a sentence that clearly states the main point or idea of that section. This serves as a guide to the reader and lets them know what to expect in the coming paragraphs.\n\nExplanation/Development: After your topic sentence, provide information, evidence, or arguments that expand upon and support your main point. You can get a little creative here and let yourself wander around to make the topic a little lighter. This thought process has to naturally lead you to the paragraph where you delve into the details of your topic. Depending on what the section is about, this could involve presenting your research findings, analyzing a text, discussing a theoretical concept, etc.\n\nEvidence: Where appropriate, include specific evidence to support your points. This could be in the form of data from your research, quotes from primary or secondary sources, examples, etc. Make sure to properly cite all sources.\n\nAnalysis: Don't just present information or evidence; analyze it. Discuss what it means, why it's important, how it supports your main point, etc.\n\nTransition: You can get a little creative here and let yourself wander around to make the information you came up with a little lighter. This thought process has to naturally lead you to the transition to the next topic that is going to be disclosed in the next section. This could be a sentence that summarizes the main point of the section and hints at what's to come, or a more explicit transition that directly states what the next section will be about.\n\nRemember to keep each section focused. Each section should have a clear main point, and everything in that section should support or develop that point. Avoid going off on tangents or including irrelevant information, as this can confuse the reader and dilute your main message.\n\nAlso, be aware of the flow and cohesion of your writing. Use transitions to guide the reader through your argument, and make sure your sentences and paragraphs flow smoothly from one to the next. Make it engaging, but professional."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You are a researcher. Your task is to edit the Section 1.1 text to a finalized, ready-to-publish variant based on the provided Research table of contents and the current Section 1.1 text. Follow the provided prompt to ensure the section has a clear topic sentence, includes relevant information and evidence, provides analysis, and ends with a transition. Maintain focus, coherence, and flow throughout the section. Make it engaging, but professional."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
    )

    # Extract the text from the response
    edited_section_1_1_text = response['choices'][0]['message']['content'].strip()

    # Write the edited Section 1.1 text into a file
    edited_section_1_1_file = os.path.join(new_paper_folder, 'Section_1.1_Final.txt')
    with open(edited_section_1_1_file, 'w', encoding='utf-8') as file:
        file.write(edited_section_1_1_text)


if __name__ == "__main__":
    print("Editing Section 1.1...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Edit Section 1.1
    edit_section_1_1(output_folder)

    print("Section 1.1 editing complete.")