import os
import openai
from openai import ChatCompletion

def create_goal_alignment_analysis(output_folder, user_goal_filename):
    """Create the 'Goal alignment' folders and 'Goal alignment analysis' files for each paper in the output folder."""
    subdirectories = [entry for entry in os.listdir(output_folder) if os.path.isdir(os.path.join(output_folder, entry))]
    for subdirectory in subdirectories:
        subdirectory_name = os.path.basename(os.path.normpath(subdirectory))
        goal_alignment_folder = os.path.join(output_folder, subdirectory_name, 'Goal alignment')
        os.makedirs(goal_alignment_folder, exist_ok=True)

        goal_alignment_analysis_file = os.path.join(goal_alignment_folder, f'{subdirectory_name}_Goal_alignment_analysis.txt'.replace('/', ''))
        with open(goal_alignment_analysis_file, 'w', encoding='utf-8') as file:
            file.write(f"Goal alignment analysis for paper: {subdirectory_name}\n\n")
            file.write("User goal:\n")
            with open(user_goal_filename, 'r', encoding='utf-8') as goal_file:
                file.write(goal_file.read())


def create_step_by_step_chunk_analysis(output_folder, user_goal_filename, subdirectory_name):
    """Create the 'Step by step chunk analysis' folders and files for each paper."""
    subdirectory_folder = os.path.join(output_folder, subdirectory_name)  # Get the subdirectory path
    step_by_step_chunk_folder = os.path.join(subdirectory_folder, 'Step by step chunk analysis')
    os.makedirs(step_by_step_chunk_folder, exist_ok=True)  # Ensure folder creation

    chunks_folder = os.path.join(subdirectory_folder, 'chunks')
    if not os.path.exists(chunks_folder):
        return  # Skip processing if chunks folder is not found

    num_chunks = len(os.listdir(chunks_folder))

    alignment_texts = []

    for i in range(1, num_chunks + 1):
        chunk_file = os.path.join(chunks_folder, f'chunk_{i}.txt')
        chunk_alignment_file = os.path.join(step_by_step_chunk_folder, f'chunk_{i}_alignment.txt')

        with open(user_goal_filename, 'r', encoding='utf-8') as goal_file:
            user_goal = goal_file.read().strip()
        abstract_file = os.path.join(subdirectory_folder, 'full_abstract.txt')

        with open(chunk_file, 'r', encoding='utf-8') as chunk:
            chunk_text = chunk.read()

        prompt = f"""
                You are a researcher assistant exploring scientific papers. Your primary focus is to scrutinize the given text and identify sections that are specifically relevant to the user's research goal provided. The user's research goal is: '{user_goal}'. Don't confuse given paper's abstract with user's goal! This is very important. Use your capabilities to discern relevant information related to the research goal, note this information down. If there isn't any relevant information tied to the research goal, confidently state 'Empty'. If not 'Empty', start your reply this way: 'Text is relevant to user's goal ('{user_goal}') since it...'
                """

        alignment = generate_alignment_text(prompt, chunk_text, user_goal, abstract_file)
        alignment_texts.append(alignment)

        with open(chunk_alignment_file, 'w', encoding='utf-8') as alignment_file:
            alignment_file.write(alignment)

    goal_alignment_folder = os.path.join(subdirectory_folder, 'Goal alignment')  # Updated line
    os.makedirs(goal_alignment_folder, exist_ok=True)

    goal_alignment_analysis_file = os.path.join(goal_alignment_folder, f'{subdirectory_name}_Goal_alignment_analysis.txt'.replace('/', ''))
    with open(goal_alignment_analysis_file, 'w', encoding='utf-8') as alignment_analysis_file:  # Updated line
        alignment_analysis_file.write(f"Alignment for chunk analysis: {subdirectory_name}\n\n")
        alignment_analysis_file.write("\n".join(alignment_texts))
        alignment_analysis_file.write("\n\n")
def generate_alignment_text(prompt, chunk_text, user_goal, abstract_file):
    """Generate the alignment text using OpenAI GPT."""
    full_prompt = f"Scrutinize the given text of a scientific paper we want to use as a source for user's research and identify sections that are specifically relevant to the user's research goal provided; if there isn't any relevant information tied to the research goal, strictly respond with just word 'Empty' and nothing else. This is very important to just write 'Empty' in this case. First, I'll provide you with a short summary of this paper we use as a source. Then, I'll give you a chunk of text of this paper, and you must scrutinize the given text and identify sections that are specifically relevant to the user's research goal provided. Don't confuse this paper's abstract with user's goal! Here's a short summary of the paper we use as a source: '{abstract_file}'. Don't confuse this paper's abstract with user's goal! The user's research goal is: '{user_goal}'. Here's a chunk of text of this paper:\n\n"
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": full_prompt + chunk_text}
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return response['choices'][0]['message']['content']