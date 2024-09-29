from openai import OpenAI
import os
from FileAnalyser import fileAll
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

def ask_for_file(path, username, add_suggestions):
    fileName, fileExtension, fileSummary, fileContent, webAddress = fileAll(path)
    directory_tree = get_directory_tree(username)
    with open(directory_tree, "r") as file:
        tree = file.read()

    prompt = f"""Below is a directory tree of my file explorer. I have a downloaded file that I need to reliably categorise.
    I will give you details including the name of file, the type (extension) of the file, two summaries of the file contents, and the chrome url from which the file was downloaded.
    You must take these all into consideration when performing the following steps.
    You must either choose a folder to put this file in, or you can create a few new folders anywhere if you feel like the file doesn't reliably fit anywhere.
    I want back from you the new file path from the root of the directory to the newly downloaded file. ONLY the file path, nothing more nothing less, DO NOT add new line character after slash
    Maybe you'll want to generalise documents or powerpoints or spreadsheets or text documents or images and so on.
    file_name = {fileName},
    file_type = {fileExtension},
    file_content_summary = {str(fileSummary)},
    file_content_summary_2 = {str(fileContent)},
    download_web_address = {str(webAddress)},
    directory_tree = {tree}
    """
    
    if add_suggestions != '':
        prompt += f'Additional suggestions from user: {add_suggestions}'

    response = client.chat.completions.create(
        messages = [
            {"role": "system", "content": """
                YOU MUST FOLLOW THESE IMPORTANT RULES:
                #1: File path must begin with 'FileyFace'
                #2: Please be consistent with the directory tree. For example, if 'Lecture09.pdf' is stored within its own folder 'Lecture09-topic'
                the a similar file named 'Lecture08.pdf' should also be stored within its own folder 'Lecture08-topic'
                #3: If a file does not contain any defining features or characteristics, please put it in an 'Other' folder (USE THIS AS A LAST RESORT AND LAST RESORT ONLY!!)
                #4: DO NOT leave off the file extension
                #5: Adopt a breadth-first strategy. DO NOT put a file under an existing directory unless it does correlate with it or the user requires it
                #6: Similar folders should be in the same level of hierarchy. For example, 'CS3630' and 'MATH3215' should at the same level in the directory tree
             """},
            {"role": "user", "content": prompt}],
        model = "gpt-4o-mini",
        max_tokens = 30,
        temperature=0,
    )
    
    dst_file_path = fr'C:/Users/{username}/' + response.choices[0].message.content
    print(dst_file_path)    # for temp debug

    return dst_file_path


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