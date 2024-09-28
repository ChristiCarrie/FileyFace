# rename(), move()
import os
import math

def moveFile(src, dst):
    for i in range (math.inf):
        try:
            os.rename(src, dst)
            break
        except OSError as e:
            text = os.path.splitext(".")
            dst = text[0] + '(' + str(i) + ')' + text[1]

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

# Hardcoded:
directory = r'D:\College\Georgia Tech\06 Textbooks'
output_file = r'D:\College\Georgia Tech\15 HackGT11\directory_tree.txt'

directory_tree = list_directory_tree(directory)
save_tree_to_file(directory_tree, output_file)

print(f"Directory tree saved to {output_file}")