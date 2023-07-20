# generate_intro.py

import os
import openai
from openai import ChatCompletion
from config import API_KEY

openai.api_key = API_KEY


def generate_intro(output_folder):
    """Generate the Introduction section for the research paper."""

    # Define necessary file and folder paths
    new_paper_folder = os.path.join(output_folder, '0. Brand new research paper')
    intro_file = os.path.join(new_paper_folder, 'Brand new intro.txt')

    # Load the user's research goal
    user_input_folder = os.path.join(os.getcwd(), 'User input')
    user_goal_file = os.path.join(user_input_folder, 'user_goal.txt')

    if not os.path.isfile(user_goal_file):
        print("User goal file not found. Skipping 'Введение' (Introduction) section generation.")
        return

    with open(user_goal_file, 'r', encoding='utf-8') as file:
        user_goal = file.read().strip()

    # Load the research objectives
    objectives_file = os.path.join(new_paper_folder, 'Research objectives list.txt')

    if not os.path.isfile(objectives_file):
        print("Research objectives file not found. Skipping 'Введение' (Introduction) section generation.")
        return

    with open(objectives_file, 'r', encoding='utf-8') as file:
        objectives_text = file.read().strip()

    # Load the research table of contents
    toc_file = os.path.join(new_paper_folder, 'Research table of contents.txt')

    if not os.path.isfile(toc_file):
        print("Research table of contents file not found. Skipping 'Введение' (Introduction) section generation.")
        return

    with open(toc_file, 'r', encoding='utf-8') as file:
        toc_text = file.read().strip()

    # Load the final literature review
    literature_review_file = os.path.join(new_paper_folder, '0. Final_Literature_Review.txt')

    if not os.path.isfile(literature_review_file):
        print("Final 'Literature Review' file not found. Skipping 'Введение' (Introduction) section generation.")
        return

    with open(literature_review_file, 'r', encoding='utf-8') as file:
        literature_review_text = file.read().strip()

    # Load the brand new findings
    findings_file = os.path.join(new_paper_folder, 'Brand new findings.txt')

    if not os.path.isfile(findings_file):
        print("Brand new findings file not found. Skipping 'Введение' (Introduction) section generation.")
        return

    with open(findings_file, 'r', encoding='utf-8') as file:
        findings_text = file.read().strip()

    # Define the prompt
    prompt = f"GPT, please generate the Introduction section for our research paper based on the provided information. A general example of a standard structure of the introduction looks like this: - introductory sentences; - substantiation of the relevance of the topic; - research problematics; - object and subject of research; - research goal - research objectives; - methodology. Introductory sentences should be engaging, capturing the attention of the reader, but still be very professional. The relevance of the research lies in the practical and theoretical benefits of the topic of your work, and, in general, whether it is needed in real life. The problematics of the research. Without identifying the underlying problem, you won't be able to research and find a solution. The object of study in research is often confused with the concept of the subject of study. The concept of an object is much broader than the concept of an object. The subject of the research is a narrower concept than the object. The subject allows you to narrow down the search for information on the topic of your work in order to concentrate and select exactly what you need from the vast ocean of information. The goal of research should offer a solution and be fully relevant to the problematics of your work. Reword the user's research goal so that it matches to what we came up with in the research findings provided, but don't mention that research goal was revised. Objectives you should just take from the corresponding file with objectives, but don't split them into theoretical and practical, just say that in order to achieve the goal of research we've come up with relevant research objectives and give the whole list. Methodological base. This research paper is built on a comprehensive and systematic review of existing literature pertaining to the topic at hand. The purpose of this methodology is to provide a clear understanding of how the analysis of the collected literature led to the conclusions drawn in this paper. Talk about Literature Search, Selection Criteria, Data extraction, Data analysis, synthesis of findings. Our research goal is: '{user_goal}'. The research objectives are as follows:\n\n{objectives_text}\n\n The research table of contents is as follows:\n\n{toc_text}\n\nDon't mention table of contents, just remember it. The final 'Literature Review' section is as follows:\n\n{literature_review_text}\n\nThe brand new findings are as follows:\n\n{findings_text}. You should not mention in the Introduction section what we will come up with at the end of the research work in research findings. Don't ever tell what sections the research paper consists of."

    # New system prompt
    system_prompt = "You are a researcher. Your task is to generate the Introduction section for the research paper based on the provided information. The Introduction section should introduce the research topic, provide background information, substantiate the relevance of the topic, describe the research problematics, object and subject of the research, and clearly state the revised research goal and objectives. It should also mention the methodology used and briefly summarize the research table of contents, the final 'Literature Review' section, and the brand new findings. Please ensure that the Introduction section is concise, coherent, and engaging. Don't ever tell what sections the research paper consists of. Don't mention that research goal was revised."

    # Query GPT-3
    response = ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )

    # Extract the text from the response
    intro_text = response['choices'][0]['message']['content'].strip()

    # Write the Introduction section into a file
    with open(intro_file, 'w', encoding='utf-8') as file:
        file.write(intro_text)


if __name__ == "__main__":
    print("Generating Introduction section...")

    output_folder = os.path.join(os.getcwd(), 'P2P Output')

    # Generate the Introduction section
    generate_intro(output_folder)

    print("Introduction section generation complete.")