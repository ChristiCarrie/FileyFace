from openai import OpenAI
import os
from FileAnalyser import fileAll

client = OpenAI(
    api_key = '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'
)

def ask_for_file(path, username):
    fileName, fileExtension, fileContent = fileAll(path)
    directory_tree = get_directory_tree(username)
    with open(directory_tree, "r") as file:
        tree = file.read()

    prompt = f"""Below is a directory tree of my file explorer. I have a downloaded file that I need to reliably categorise.
    I will give you details including the name of file, the type (extension) of the file, and a summary of the file contents.
    You must either choose a folder to put this file in, or you can create any number of new folders anywhere if you feel like the file doesn't reliably fit anywhere.
    I want back from you the new file path from the root of the directory to the newly downloaded file. ONLY the file path, nothing more nothing less.
    file_name = {fileName},
    file_type = {fileExtension},
    file_content_summary = {str(fileContent)},
    directory_tree = {tree}"""

    response = client.chat.completions.create(
        messages = [
            {"role": "user", "content": prompt}
        ],
        model = "gpt-4o-mini",
        max_tokens = 50,
        temperature=0,
    )

    print(fr'C:/Users/{username}/' + response.choices[0].message.content)

    #return response['choices'][0]['message']['content'].strip()


def get_directory_tree(username):
    directory = fr'C:\Users\{username}\FileyFace'
    output_file = fr'C:\Users\{username}\FileyFace\directory_tree.txt'
    os.makedirs(directory, exist_ok=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    tree = list_directory_tree(directory)
    save_tree_to_file(tree, output_file)
    return output_file

def list_directory_tree(start_path):
    tree = []
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            tree.append(f"{sub_indent}{file}")
    return tree

def save_tree_to_file(tree, file_name):
    with open(file_name, 'w') as f:
        for line in tree:
            f.write(line + '\n')