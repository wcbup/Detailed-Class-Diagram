from __future__ import annotations
from load_class_files import load_class_files
from typing import List, Dict, Union, Set
import json
import os


class JavaClassAnalyzer:
    """
    class for analyzing one java class file
    """

    def __init__(self, content_str: str) -> None:
        self.content_json: Dict[str, Union[str, List[str], Dict]] = json.loads(
            content_str
        )

        def get_id(name: str) -> str:
            """
            change name into id
            """
            return name.replace("/", ".")

        self.id = get_id(self.content_json["name"])
        self.super_class_id = get_id(self.content_json["super"]["name"])



class ClassPainter:
    """
    class that draws the class diagram
    """

    def __init__(self, java_class_list: List[JavaClassAnalyzer]) -> None:
        self.dot_code = ""  # the dot code representing the graph
        self.java_class_set: Set[JavaClassAnalyzer] = set(java_class_list)

    def generate_dot_code(self) -> None:
        """
        generate the dot code
        save the code into './result.dot'
        """
        dot_id_map: Dict[str, str] = {}  # java class id maps to dot id
        id_class_map: Dict[str, JavaClassAnalyzer] = {}  # java id to java class
        self.dot_code = """
        digraph Class_Diagram {
        graph [
		label="Detailed Class Diagram"
		labelloc="t"
		fontname="Helvetica,Arial,sans-serif"
	]
        node [
		fontname="Helvetica,Arial,sans-serif"
		shape=record
		style=filled
		fillcolor=gray95
	]
    """
        self.dot_id = 0  # the id for java class in dot class

        def allocate_id(java_class_id: str) -> None:
            """
            allocate the id to java class if it doesn't have one
            """
            if java_class_id in dot_id_map:
                return
            else:
                dot_id_map[java_class_id] = str(self.dot_id)
                self.dot_id += 1

        # allocate the dot id to java class analyzer
        for java_class in self.java_class_set:
            allocate_id(java_class.id)
            allocate_id(java_class.super_class_id)
            id_class_map[java_class.id] = java_class

        for java_class_id in dot_id_map:
            dot_id = dot_id_map[java_class_id]
            field_code = ""  # dot code for the field
            method_code = ""  # dot code for method
            if java_class_id in id_class_map:
                java_class = id_class_map[java_class_id]
                field_code = f"""
                            <table border="0" cellborder="0" cellspacing="0" >
                                <tr> <td align="left" >+ field</td> </tr>
                                <tr> <td port="ss1" align="left" >- Subsystem 1</td> </tr>
                                <tr> <td port="ss2" align="left" >- Subsystem 2</td> </tr>
                                <tr> <td port="ss3" align="left" >- Subsystem 3</td> </tr>
                            </table>
"""
                method_code = f"""
                            <table border="0" cellborder="0" cellspacing="0" >
                                <tr> <td align="left" >+ method</td> </tr>
                                <tr> <td align="left" >- method 1</td> </tr>
                            </table>
"""
            else:
                field_code = f"""
                            <table border="0" cellborder="0" cellspacing="0" >
                                <tr> <td align="left" >+ field</td> </tr>
                                <tr> <td align="left" > ... </td> </tr>
                            </table>
"""
                method_code = f"""
                            <table border="0" cellborder="0" cellspacing="0" >
                                <tr> <td align="left" >+ method</td> </tr>
                                <tr> <td align="left" > ... </td> </tr>
                            </table>
"""


            self.dot_code += f"""
                x{dot_id} [
                    shape=plain
                    label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4">
                        <tr> <td> <b>{java_class_id}</b> </td> </tr>
                        <tr> <td>
                        {field_code}
                        </td> </tr>
                        <tr> <td>
                        {method_code}
                        </td> </tr>
                    </table>>
                ]

"""
        for java_class in self.java_class_set:
            self.dot_code += f"""
                    edge [arrowhead=empty style=""]
                    x{dot_id_map[java_class.id]} -> x{dot_id_map[java_class.super_class_id]} [xlabel=inheritance]
"""

        self.dot_code += "}"

        dot_file_path = "./result.dot"
        with open(dot_file_path, "w") as f:
            f.write(self.dot_code)

    def generate_graph_and_show(self) -> None:
        """
        generate the graph
        save the graph to './result.png'
        show the graph
        """

        DPI = 500  # the dpi of the result picture
        self.generate_dot_code()
        command = (
            f".\\Graphviz\\bin\\dot.exe -Tpng -Gdpi={DPI} .\\result.dot -o result.png"
        )
        os.system(command)
        command = ".\\result.png"
        os.system(command)


# test code
if __name__ == "__main__":
    content_str_list = load_class_files("example-project")
    java_analyzer_list: List[JavaClassAnalyzer] = []
    for content_str in content_str_list:
        java_analyzer_list.append(JavaClassAnalyzer(content_str))

    print(java_analyzer_list[0].id)

    class_painter = ClassPainter(java_analyzer_list)
    class_painter.generate_graph_and_show()
