import argparse
import ast
import logging
import sys
from collections import namedtuple
from itertools import chain, combinations
from pathlib import Path

import astor
from thefuzz import fuzz

# Setup Logging
logger = logging.getLogger(__name__)

FunctionInfo = namedtuple(
    "FunctionInfo",
    ["name", "args", "docstring", "body",
        "start_line", "normalized_body", "file_name"],
)


class CodeNormalizer:
    """Class containing methods to normalize and process Python AST"""

    STR_PLACEHOLDER = ""

    @classmethod
    def remove_docstring(cls, tree):
        """
        Remove docstrings from the given AST tree.

        Args:
            tree (ast.AST): The input AST tree.

        Returns:
            ast.AST: The AST tree with docstrings removed.
        """
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module)):
                if (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, (ast.Str, ast.Constant))
                ):
                    node.body = node.body[1:]
        return tree

    @classmethod
    def strip_comments_and_strings(cls, tree):
        """
        Remove comments and strings from the given AST tree.

        Args:
            tree (ast.AST): The input AST tree.

        Returns:
            ast.AST: The AST tree with comments and strings removed.
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.Str):
                node.s = cls.STR_PLACEHOLDER
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                node.value = cls.STR_PLACEHOLDER
        return tree

    @classmethod
    def rename_variables(cls, tree):
        """
        Rename variables in the given AST tree.

        Args:
            tree (ast.AST): The input AST tree.

        Returns:
            ast.AST: The AST tree with variables renamed.
        
        Note:
            The current version have trouble to tell apart a function call from 
            local variable. I.e. 
            Input:
            def pretty_print_result(result, operation, a, b):
                '''Placeholder docstring'''
                pretty_print_result(f'The {operation} of {a} and {b} is {result}.')
                c = a + b # Smart comment
                return c
            Output:
            def pretty_print_result(var1, var2, var3, var4):
                var6(f'{var2}{var3}{var4}{var1}')
                var5 = var3 + var4
                return var5
            
        """

        def replace_name(node, names_map):
            """
            Replace the names of the variables in the given AST node.

            Args:
                node (ast.AST): The input AST node.
                names_map (dict): A dictionary mapping the original variable names to new names.

            Returns:
                None: The function modifies the input node in-place.
            """
            if isinstance(node, ast.Name) and not isinstance(
                getattr(node, "parent", None), ast.FunctionDef
            ):
                # Check if the node is an attribute of a function call
                if not (
                    isinstance(getattr(node, "parent", None),
                               ast.Call) and node.parent.func is node
                ):
                    if node.id not in names_map:
                        names_map[node.id] = f"var{len(names_map) + 1}"
                    node.id = names_map[node.id]

        for node in ast.walk(tree):
            func_names_map = {}
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.arg not in func_names_map:
                        func_names_map[arg.arg] = f"var{len(func_names_map) + 1}"
                    arg.arg = func_names_map[arg.arg]
                for child in ast.walk(node):
                    replace_name(child, func_names_map)

        return tree

    @classmethod
    def normalize(cls, tree):
        """
        Normalize the given AST tree.

        Args:
            tree (ast.AST): The input AST tree.

        Returns:
            str: The normalized code as a string.
        """
        tree = cls.remove_docstring(tree)
        tree = cls.strip_comments_and_strings(tree)
        tree = cls.rename_variables(tree)
        return astor.to_source(tree)


def load_ast_tree(path, return_text=False):
    """Catch common errors when loading the AST tree

    Args:
        path (str): Path to .py file to parse
        return_text (bool): If True, returns a tuple of the AST root node and file text.
            Defaults to False
    Returns:
        ast.AST: An AST node (root node for the given file) or None if an error was encountered
        or
        tuple : (ast.AST, str) if return_text is True
    """

    try:
        with open(path, "r") as fh:
            text = fh.read()
            root = ast.parse(text, path)
    except UnicodeDecodeError:
        logger.error(f"File `{path}` failed to open (Invalid Unicode)")
        return None
    except FileNotFoundError:
        logger.error(f"File `{path}` was not found")
        return None
    except SyntaxError:
        logger.error(f"File `{path}` failed to compile")
        return None
    if return_text:
        return (root, text)
    return root


def get_functions(path):
    """Get information about each function defined in the given file, including name, docstring and body

    Args:
        path (str): Path to a python file to get function lengths from

    Returns:
        list: List of FunctionInfo named tuples
    """
    root, text = load_ast_tree(path, return_text=True)
    func_list = []
    for node in ast.walk(root):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            doc_str = ast.get_docstring(node)
            doc_str_lines = 0
            if doc_str is not None:
                doc_str_lines = len(doc_str.split("\n"))
            body = "\n".join(text.split(
                "\n")[node.lineno + doc_str_lines + 1: node.end_lineno])
            func_args = [
                item.arg for item in node.args.args if item.arg != "self"]
            normalized_body = CodeNormalizer.normalize(node)
            f_info = FunctionInfo(
                name, func_args, doc_str, body, node.lineno, normalized_body, path
            )
            func_list.append(f_info)
    return func_list


def find_duplicate_funcs(func_list, threshold):
    """
    Find duplicate functions in the list of FunctionInfo tuples based on the given threshold.

    Args:
        func_list (list): List of FunctionInfo named tuples
        threshold (int): The minimum similarity score required to consider two functions as duplicates

    Returns:
        list: List of tuples containing similarity score and the two duplicate FunctionInfo named tuples
    """
    duplicate_funcs = []
    for func1, func2 in combinations(func_list, 2):
        ratio = fuzz.ratio(func2.normalized_body, func1.normalized_body)
        if ratio >= threshold:
            duplicate_funcs.append((ratio, func1, func2))
    return sorted(duplicate_funcs, reverse=True)


def get_all_scripts(path):
    """
    Get all Python scripts in the given path.

    Args:
        path (str): Path to a directory or a single .py file

    Returns:
        list: List of Path objects representing Python scripts
    """
    path_obj = Path(path)

    if path_obj.is_file() and path_obj.suffix == ".py":
        return [path_obj]

    if path_obj.is_dir():
        return list(path_obj.rglob("*.py"))

    return []


def show_info(func_info):
    """Generate a string contains file name, line no and function name.

    Args:
        func_info (FunctionInfo): A named tuple contains function information

    Returns:
        str: string contains function information
    """
    return f"{func_info.file_name}:L{func_info.start_line}:{func_info.name}"


def main(args):
    """
    Main function to analyze the given path for duplicate functions.

    Args:
        args (argparse.Namespace): The command line arguments namespace object containing 'path' and 'threshold'

    """
    func_list = list(
        chain.from_iterable(get_functions(file)
                            for file in get_all_scripts(args.path))
    )
    dup_func_list = find_duplicate_funcs(func_list, args.threshold)

    for _, func1, func2 in dup_func_list:
        logging.warning(
            f"Similar functions found, {show_info(func1)}, {show_info(func2)}")
    if len(dup_func_list):
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find similar functions in Python files.")
    parser.add_argument(
        "path", type=str, default="src", help="Path to a directory or a single .py file"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=80,
        help="The minimum similarity score required to consider two functions as duplicates (default: 80)",
    )
    args = parser.parse_args()
    main(args)
