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
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Your task is to find details about the given text, including the abstract, author name(s), paper name, place of publishing, and year of issue. This information could be anywhere in the text, not just at the beginning. Usually these bits of information are given in small sentences with no verbs. If a certain bit of information is not found, specify it as 'Empty.' and look for the next one. Format the response strictly in the following style, filling in the bits of info you've found: '**Author(s) Last Name(s)**, **Initial(s)**. **Title of the Paper**. //**Journal Name**. – **Year**. – **Volume**. – **Issue**. – **Pages**. **Abstract**'. Here's an example for you: 'One Useful Thing Subscribe Sign in How to use AI to do practical stuff: A new guide People often ask me how to use AI. Here's an overview with lots of links. ETHAN MOLLICK 30 МАР. 2023 Г. We live in an era of practical AI, but many people haven’t yet experienced it, or, if they have, they might have wondered what the big deal is. Thus, this guide. It is a modified version of one I put out for my students earlier in the year, but a lot has changed. It is an overview of ways to get AI to do practical things. Why people keep missing what AI can do.' As you can see, this text contains a few sentences that don't have any verbs, which makes us think these are some informational bits. 'One Useful Thing' is meaningless, it doesn't have anything to do with the text, so it might as well be a name of the website, which we will treated as a place of publishing. 'ETHAN MOLLICK' is a name, that doesn't have any additional info, which makes us think that it is the name of the author of this text. 'Subscribe Sign in' are meaningless and don't contain any information, so we ignore them. '30 МАР. 2023 Г.' is a date that isn't attached to anything else, so it is probably a date of publishing the text. 'How to use AI to do practical stuff: A new guide' sounds a lot like a name of the text, which it probably is. Everything else is just the content of the text. So, our output should be: 'Mollick, E. How to use AI to do practical stuff: A new guide. //One Useful Thing. – 2023. – **Volume**. – **Issue**. – **Pages**. **Abstract**'. Here's the text: {text}"},
        ],
        temperature=1,
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