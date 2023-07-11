import os
import openai
from openai import ChatCompletion

openai.api_key = '<Insert OpenAI Key Here>'

def split_text(text, length):
    """Split the text into chunks of the given length."""
    return [text[i:i+length] for i in range(0, len(text), length)]

def process_file(filename):
    """Process a single file."""
    # Create base sub-folder identical to the .txt file name
    base_subfolder = os.path.splitext(filename)[0]
    os.makedirs(base_subfolder, exist_ok=True)

    # Create subfolders for chunks and abstracts
    chunks_folder = f'{base_subfolder}/chunks'
    abstracts_folder = f'{base_subfolder}/abstract_search'
    os.makedirs(chunks_folder, exist_ok=True)
    os.makedirs(abstracts_folder, exist_ok=True)

    with open(filename, 'r', encoding="utf-8") as file:
        content = file.read()

    chunks = split_text(content, 3000)

    for i, chunk in enumerate(chunks, start=1):
        chunk_filename = f'{chunks_folder}/chunk_{i}.txt'
        # Save chunk to a separate file
        with open(chunk_filename, "w", encoding="utf-8") as file:
            file.write(chunk)

        # Generate abstract and save it into a separate file in the abstract_search folder
        abstract = find_abstract(chunk)
        abstract_filename = f'{abstracts_folder}/chunk_{i}_abstract.txt'
        with open(abstract_filename, "w", encoding="utf-8") as file:
            file.write(abstract)

    compile_abstracts(base_subfolder, abstracts_folder)

def find_abstract(text):
    """Use GPT-3 to identify the abstract of the text."""
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Your task is to identify if the given text contains an abstract of a scientific paper. Do not infer or guess. You should only identify text that is explicitly labeled as an abstract. If you find such abstract, respond with 'Here's an abstract: *paste the actual content of the abstract here*'. If there isn't, respond only with 'Empty.'"},
            {"role": "user", "content": f"{text}"},
        ],
        temperature=0.1,  # Lower the temperature to make output more deterministic
    )

    return response['choices'][0]['message']['content'].strip()

def compile_abstracts(base_subfolder, abstracts_folder):
    """Compile all abstracts into a single file."""
    combined_abstracts = []
    for filename in sorted(os.listdir(abstracts_folder)):
        chunk_number = filename.split('_')[1]  # Extract chunk number from filename
        with open(f'{abstracts_folder}/{filename}', 'r', encoding="utf-8") as file:
            abstract = file.read()
        combined_abstracts.append(f"Chunk {chunk_number}:\n{abstract}")
    full_abstract_text = "\n\n".join(combined_abstracts)
    with open(f'{base_subfolder}/full_abstract.txt', 'w', encoding="utf-8") as file:
        file.write(full_abstract_text)

print("Starting data processing...")
folder = '<Insert Folder Directory Here>'

# Loop over all text files in the primary folder
for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        process_file(f'{folder}/{filename}')

print("Data processing complete.")