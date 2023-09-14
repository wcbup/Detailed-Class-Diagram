from __future__ import annotations
from typing import List
from glob import glob
import os


def load_class_files(project_name: str) -> List[str]:
    """
    load all the contents of java class files in the project
    return a list of the json str content
    """
    file_paths: List[str] = []
    for file_path in glob("./" + project_name + "/**/*.class", recursive=True):
        file_paths.append(file_path)

    # print(file_paths)

    def get_filename(file_path: str) -> str:
        slash_loc = file_path.rfind("\\")
        dot_loc = file_path.rfind(".")
        return file_path[slash_loc + 1 : dot_loc]

    # the content of the json
    json_list: List[str] = []

    for file_path in file_paths:
        json_path = f".\\json\\{get_filename(file_path)}.json"
        command = f".\\jvm2json.exe -s {file_path} -t {json_path}"
        os.system(command)
        with open(json_path, "r") as f:
            json_list.append(f.read())

    return json_list


# test code
if __name__ == "__main__":
    load_class_files("example-project")
    # for content in load_class_files("example-project"):
    #     print(content)