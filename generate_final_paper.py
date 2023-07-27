# generate_final_paper.py

import os
from docx import Document

def add_section_from_file(doc, filename):
    """Add a new section to the document and fill it with the contents of the specified file."""
    section = doc.add_section()
    with open(filename, 'r', encoding='utf-8') as file:
        section_text = file.read().strip()
        doc.add_paragraph(section_text)

def generate_final_paper(output_folder):
    """Generate the final research paper."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    final_paper_file = os.path.join(new_paper_folder, 'Final Research Paper.docx')

    # Create a new Word document
    doc = Document()

    # Add the sections to the document
    files_to_add = ['Best title.txt', 'Research table of contents.txt',
                    'Brand new intro.txt', '0. Final_Literature_Review.txt',
                    'Section_1.1_Final.txt', 'Section_1.2_Final.txt',
                    'Section_1.3_Final.txt', 'Section_2.1_Final.txt',
                    'Section_2.2_Final.txt', 'Section_2.3_Final.txt',
                    'Brand new conclusion.txt', 'List_of_Literature_Sources.txt']

    for filename in files_to_add:
        file_path = os.path.join(new_paper_folder, filename)

        if not os.path.isfile(file_path):
            print(f"{filename} not found. Skipping this section.")
            continue

        add_section_from_file(doc, file_path)

    # Save the document
    doc.save(final_paper_file)

    print("Final research paper generated.")

if __name__ == "__main__":
    print("Generating final research paper...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate the final research paper
    generate_final_paper(output_folder)

    print("Research paper generation complete.")
