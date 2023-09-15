from __future__ import annotations
from load_class_files import load_class_files
from typing import List, Dict, Union, Set
import json
import os


class JavaClass:
    def __init__(self, type_id: str, name: str | None, is_base_type: bool) -> None:
        self.type_id = type_id
        if name == "this$0":
            name = "this"
        self.name = name
        self.is_base_type = is_base_type
        self.arg_ids: List[str] = []

    def add_one_arg_id(self, id: str) -> None:
        self.arg_ids.append(id)

    def get_detailed_type_id(self) -> str:
        if len(self.arg_ids) == 0:
            return self.type_id
        else:
            return f"{self.type_id}&lt;{', '.join(self.arg_ids)}&gt;"


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

        # get super class
        self.super_class_id = get_id(self.content_json["super"]["name"])

        # realization
        self.interface_set: Set[JavaClass] = set()
        interfaces_content: List[Dict[str]] = self.content_json["interfaces"]
        for interface_content in interfaces_content:
            interface_id = get_id(interface_content["name"])
            java_interface = JavaClass(interface_id, None, False)

            args_content: List[Dict[str]] = interface_content["args"]
            for arg_content in args_content:
                arg_id = get_id(arg_content["type"]["name"])
                java_interface.add_one_arg_id(arg_id)

            self.interface_set.add(java_interface)

        # aggregation
        self.field_set: Set[JavaClass] = set()
        fields_content: List[Dict[str]] = self.content_json["fields"]
        for field_content in fields_content:
            name = field_content["name"]

            type_content: Dict[str] = field_content["type"]
            if "name" in type_content.keys():
                type_id = get_id(field_content["type"]["name"])
                if type_id == self.id:
                    continue
                args_content: List[Dict[str]] = field_content["type"]["args"]
                java_class = JavaClass(type_id, name, False)
                for arg_content in args_content:
                    java_class.add_one_arg_id(get_id(arg_content["type"]["name"]))
            else:
                type_id = field_content["type"]["base"]
                java_class = JavaClass(type_id, name, True)

            self.field_set.add(java_class)


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

        def allocate_class_id(java_class: str | JavaClassAnalyzer | JavaClass) -> None:
            """
            allocate the id to java class if it doesn't have one
            """
            if isinstance(java_class, str) or isinstance(java_class, JavaClass):
                if isinstance(java_class, str):
                    java_class_id = java_class
                elif isinstance(java_class, JavaClass):
                    java_class_id = java_class.get_detailed_type_id()
                if java_class_id in dot_id_map:
                    return
                else:
                    dot_id_map[java_class_id] = str(self.dot_id)
                    dot_id = self.dot_id
                    self.dot_id += 1
                    self.dot_code += f"""
                        x{dot_id} [
                            shape=plain
                            label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4">
                                <tr> <td> <b>{java_class_id}</b> </td> </tr>
                                <tr> <td>
                                    <table border="0" cellborder="0" cellspacing="0" >
                                        <tr> <td align="left" >+ field</td> </tr>
                                        <tr> <td align="left" > ... </td> </tr>
                                    </table>
                                </td> </tr>
                                <tr> <td>
                                    <table border="0" cellborder="0" cellspacing="0" >
                                        <tr> <td align="left" >+ method</td> </tr>
                                        <tr> <td align="left" > ... </td> </tr>
                                    </table>
                                </td> </tr>
                            </table>>
                        ]

"""
            elif isinstance(java_class, JavaClassAnalyzer):
                java_class_id = java_class.id

                if java_class_id in dot_id_map:
                    return
                else:
                    dot_id_map[java_class_id] = str(self.dot_id)
                    dot_id = self.dot_id
                    self.dot_id += 1

                    field_code = ""
                    for field_class in java_class.field_set:
                        field_code += f'<tr> <td port="{field_class.name}" align="left" >- {field_class.name}: {field_class.get_detailed_type_id()}</td> </tr>'

                    self.dot_code += f"""
                        x{dot_id} [
                            shape=plain
                            label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4">
                                <tr> <td> <b>{java_class_id}</b> </td> </tr>
                                <tr> <td>
                                    <table border="0" cellborder="0" cellspacing="0" >
                                        <tr> <td align="left" >+ field</td> </tr>
                                        {field_code}
                                    </table>
                                </td> </tr>
                                <tr> <td>
                                    <table border="0" cellborder="0" cellspacing="0" >
                                        <tr> <td align="left" >+ method</td> </tr>
                                        <tr> <td align="left" >- method 1</td> </tr>
                                    </table>
                                </td> </tr>
                            </table>>
                        ]

"""

        # allocate the dot id to java class analyzer
        for java_class in self.java_class_set:
            allocate_class_id(java_class)
        for java_class in self.java_class_set:
            allocate_class_id(java_class.super_class_id)

            for java_interface in java_class.interface_set:
                allocate_class_id(java_interface)
                for arg_id in java_interface.arg_ids:
                    allocate_class_id(arg_id)

            for field in java_class.field_set:
                if field.is_base_type:
                    continue
                allocate_class_id(field.type_id)

        for java_class in self.java_class_set:
            dot_id = dot_id_map[java_class.id]
            # inheritance
            self.dot_code += f"""
                    edge [arrowhead=empty style=""]
                    x{dot_id} -> x{dot_id_map[java_class.super_class_id]}
"""
            for interface in java_class.interface_set:
                self.dot_code += f"""
                    edge [arrowhead=empty style=dashed]
                    x{dot_id} -> x{dot_id_map[interface.get_detailed_type_id()]}
"""

            # aggregation
            for field in java_class.field_set:
                if field.is_base_type:
                    continue
                dot_type_id = dot_id_map[field.type_id]
                self.dot_code += f"""
                    edge [arrowhead=odiamond style=""]
                    x{dot_type_id} -> x{dot_id}:{field.name}
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

    class_painter = ClassPainter(java_analyzer_list)
    class_painter.generate_graph_and_show()
