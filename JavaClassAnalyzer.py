from __future__ import annotations
from load_class_files import load_class_files
from typing import List, Dict, Union
import json


class JavaClassAnalyzer:
    """
    class for analyzing one java class file
    """

    def __init__(self, content_str: str) -> None:
        self.content_json: Dict[str, Union[str, List[str], Dict]] = json.loads(content_str)
        self.name = self.content_json["name"].replace("/", ".")


# test code
if __name__ == "__main__":
    content_str_list = load_class_files("example-project")
    java_analyzer_list: List[JavaClassAnalyzer] = []
    for content_str in content_str_list:
        java_analyzer_list.append(JavaClassAnalyzer(content_str))

    print(java_analyzer_list[0].name)
