import os
import argparse
import re
import time

def replace_with_id(content, string):
    lines = content.split("\n")
    updated_content = []
    ids = []
    for line in lines:
#        updated_content.append(re.sub(r" \^\d+", "", line))
#        continue
        if re.search(rf"\b{re.escape(string)}\b", line):
            match = re.findall(r"\^(\d+)", line)
            
            if match:
                updated_content.append(line)
                ids.append(match[0])
            else:
                line_id = str(time.time_ns())
                updated_content.append(line + " ^" + line_id)
                ids.append(line_id)
        else:
            updated_content.append(line)
    updated_content = "\n".join(updated_content)
    return updated_content, ids

def getfilepaths(extensions):
    files_queue = []

    for dir_path, dirs, files in os.walk("."):
        rel_path = os.path.relpath(dir_path, ".")
        dirs[:] = [d for d in dirs if not d[0] == '.']
        files = [f for f in files if not f[0] == '.']
        for file in files:
            files_queue.append(rel_path + "/" + file)

    files = []
    for file in files_queue:
        for ext in extensions:
            if file.endswith("."+ext):
                files.append(file)
                break
    return files

def updatefiles(files, string):
    file_id_dict = {}
    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            content_adjusted, ids = replace_with_id(content, string)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content_adjusted)
        file_id_dict[filepath] = ids
    return file_id_dict

def create_links_file(string, file_id_dict):
    filename = string + ".md"
    if os.path.exists(filename) and not args.overwrite:
        print(f"Exiting now, file {filename} already exists, delete it or rename it if you want to run this script")
        return 1
    with open(filename, "w", encoding="utf-8") as file:
        for path, ids in sorted(file_id_dict.items()):
            if not ids:
                continue
            file.write("### " + path + "\n\n")
            for linkid in ids:
                file.write(f"- [ ] [[{path}#^{linkid}]]\n")
            file.write("\n")
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        "tagger_id_generator", 
        description="Add unique IDs to lines matching a string in selected file types."
    )

    parser.add_argument(
        "string", 
        help="Specify what string you are searching in files (can be a regex)", 
        type=str
    )

    parser.add_argument(
        "extensions", 
        nargs='?', 
        const="md", 
        help="Specify a filename extension to look for, can search for multiple extension by separating them with a '/', example: 'md/txt/py', by default it will search for .md files", 
        type=str
    )

    parser.add_argument(
        "--overwrite", 
        action="store_true", 
        help="Allow overwriting of the output .md file"
    )

    args = parser.parse_args()

    extensions = [ext.strip().lower() for ext in args.extensions.split("/")]

    files = getfilepaths(args.extensions)
    print(f"Fetched {len(files)} files.")

    file_id_dict = updatefiles(files, args.string)
    
    if sum(len(i) for i in file_id_dict.values()) == 0:
        print("No matches found. No changes made.")
    else:
        print(f"Fetched {sum(len(i) for i in file_id_dict.values())} instances of string '{args.string}' in {len(file_id_dict)} files")
        create_links_file(args.string, file_id_dict)
        print(f"Stored all infos in {args.string}.md file")
