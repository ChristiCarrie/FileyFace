import openai
import os
from FileAnalyser import fileAll

openai.api_key = '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'

def ask_for_file(path, username):
    fileName, fileExtension, fileContent = fileAll(path)
    directory_tree = get_directory_tree(username)
    with open("directory_tree", "r") as file:
        tree = file.read()

    response = openai.Completion.create(
        model = "gpt-4o-mini",
        prompt = "Below is a directory tree of my file explorer. I have a downloaded file that I need to reliably categorise.\n" +
        "I will give you details including the name of file, the type (extension) of the file, and a summary of the file contents.\n" +
        "You must either choose a folder to put this file in, or you can create any number of new folders anywhere if you feel like the file doesn't reliably fit anywhere.\n" +
        "I want back from you the new file path from the root of the directory to the newly downloaded file. ONLY the file path, nothing more nothing less.\n" +
        "file_name = " + fileName + "\n" +
        "file_type = " + fileExtension + "\n" +
        "file_content_summary = " + str(fileContent) + "\n\n" +
        "directory_tree = \n" + tree,
        max_tokens = 100
    )

    print(response.choices[0].text.strip())

    return response.choices[0].text.strip()


def get_directory_tree(username):
    directory = fr'C:\User\{username}\FileyFace'
    output_file = fr'C:\User\{username}\FileyFace\directory_tree.txt'
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