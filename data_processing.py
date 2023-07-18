import os
import openai
from openai import ChatCompletion

def split_text(text, length):
    """Split the text into chunks of the given length."""
    return [text[i:i+length] for i in range(0, len(text), length)]

def process_file(filename, output_folder):
    """Process a single file."""
    # Only take the name of the file without extension for creating sub-folder
    base_filename = os.path.splitext(os.path.basename(filename))[0]

    # Create base sub-folder in the output folder, identical to the .txt file name
    base_subfolder = os.path.join(output_folder, base_filename)
    os.makedirs(base_subfolder, exist_ok=True)

    # Create subfolders for chunks and abstracts
    chunks_folder = os.path.join(base_subfolder, 'chunks')
    abstracts_folder = os.path.join(base_subfolder, 'abstract_search')
    os.makedirs(chunks_folder, exist_ok=True)
    os.makedirs(abstracts_folder, exist_ok=True)

    with open(filename, 'r', encoding="utf-8") as file:
        content = file.read()

    chunks = split_text(content, 3000)
    limited_chunks = chunks[:2]  # Limit the number of chunks to the first two

    for i, chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(chunks_folder, f'chunk_{i}.txt')
        # Save chunk to a separate file
        with open(chunk_filename, "w", encoding="utf-8") as file:
            file.write(chunk)

        # Generate abstract and save it into a separate file in the abstract_search folder
        if i <= 2:  # Only analyze the first two chunks
            abstract = find_abstract(chunk)
            abstract_filename = os.path.join(abstracts_folder, f'chunk_{i}_abstract.txt')
            with open(abstract_filename, "w", encoding="utf-8") as file:
                file.write(abstract)

    compile_abstracts(base_subfolder, abstracts_folder)

def find_abstract(text):
    """Use GPT-3 to identify the abstract, author names, paper name, place of publishing, and year of issue of a scientific paper."""
    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Your task is to identify if the given text contains an abstract, author names, paper name, place of publishing, and year of issue of a scientific paper. Do not infer or guess. You should only identify text that is explicitly labeled as an abstract or contains the specific information for author names, paper name, place of publishing, and year of issue of this paper. If you succeed, respond with 'Here are the details: *paste the actual content of the abstract or details here*'. If there isn't any relevant information, respond only with 'Empty.'. Format the response for author names, paper name, place of publishing, and year of issue strictly in the following style: ''**Author(s) Last Name(s)**, **Initial(s)**. **Title of the Paper**. //**Journal Name**. – **Year**. – **Volume**. – **Issue**. – **Pages**. **Abstract**''"},
            {"role": "user", "content": f"{text}. You are a helpful assistant. Your task is to identify if the given text contains an abstract, author names, paper name, place of publishing, and year of issue of a scientific paper. Do not infer or guess. You should only identify text that is explicitly labeled as an abstract or contains the specific information for author names, paper name, place of publishing, and year of issue of this paper. If you succeed, respond with 'Here are the details: *paste the actual content of the abstract or details here*'. If there isn't any relevant information, respond only with 'Empty.'. Format the response for author names, paper name, place of publishing, and year of issue strictly in the following style: ''**Author(s) Last Name(s)**, **Initial(s)**. **Title of the Paper**. //**Journal Name**. – **Year**. – **Volume**. – **Issue**. – **Pages**. **Abstract**''"},
        ],
        temperature=0.2,
    )

    return response['choices'][0]['message']['content'].strip()

def compile_abstracts(base_subfolder, abstracts_folder):
    """Compile all abstracts into a single file."""
    combined_abstracts = []
    for filename in sorted(os.listdir(abstracts_folder)):
        if filename.startswith('chunk_') and filename.endswith('_abstract.txt'):
            chunk_number = filename.split('_')[1]  # Extract chunk number from filename
            with open(os.path.join(abstracts_folder, filename), 'r', encoding="utf-8") as file:
                abstract = file.read()
            combined_abstracts.append(f"Chunk {chunk_number}:\n{abstract}")
    full_abstract_text = "\n\n".join(combined_abstracts)
    with open(os.path.join(base_subfolder, 'full_abstract.txt'), 'w', encoding="utf-8") as file:
        file.write(full_abstract_text)