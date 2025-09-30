import re
import ast
import logging
import argparse
from collections import namedtuple
from pathlib import Path

# Setup Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Whether to check functions prefixed with a '_' or not
CHECK_INTERNAL_FUNCTIONS = True

FunctionInfo = namedtuple("FunctionInfo", ["name", "args", "docstring", "body", "start_line"])

def load_ast_tree(path, return_text=False):
    """Catch common errors when loading the AST tree

    Args:
        path (str): Path to .py file to parse
        return_text (bool): If True, returns a tuple of the AST root node and file text. Defaults to False
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
    """Get information about each function defined in the given file, including name, docstring, and body

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
            body = "\n".join(text.split("\n")[node.lineno+doc_str_lines+1:node.end_lineno])
            args = [item.arg for item in node.args.args if item.arg not in {"self", "cls"}]
            f_info = FunctionInfo(name, args, doc_str, body, node.lineno)
            func_list.append(f_info)
    return func_list

def count_print_in_docstrings(path, check_internal_functions=CHECK_INTERNAL_FUNCTIONS):
    """Count number of print statements for each function in the given .py file

    Args:
        path (str): Path to file to count
        check_internal_functions (bool): If True, will check internal functions (prepended with '_') if False these will be ignored
    Returns:
        count: Number of print statements
    """
    PRINT_REGEX = "(^|[\W]*)print\("
    functions = get_functions(path)
    count = 0
    for func in functions:
        if not check_internal_functions and func.name[0] == "_":
            logger.debug(f"Skipping internal function {func.name}")
            continue
        elif func.docstring is not None:
            # check if docstring has print
            num_matches = len(re.findall(PRINT_REGEX, func.docstring))
            count += num_matches

    return count

def count_print_in_file(path):
    """Counts total number of prints in the given .py file

    Args:
        file (path): Path to a python file to check
    Returns:
        count: Number of print statements
    """
    RETURN_REGEX = r"\bprint\("
    with open(path, "r") as fh:
        text = fh.read()
    matches = re.findall(RETURN_REGEX, text)
    return len(matches)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Check for any print statements in production')
    parser.add_argument('path', metavar='path', type=str,
                        help='Path to the folder or python file to check. If a folder is provided, all python files within it are searched, including subdirectories, recursively.')
    args = parser.parse_args()
    path = args.path

    functions = []
    check_passed = True

    if path[-3:] == ".py":
        tot_print_count = count_print_in_file(path)
        tot_docstring_print_count = count_print_in_docstrings(path)
        if tot_docstring_print_count != tot_print_count:
            logger.warning(f"Found some print statements in file '{path}'")
            check_passed = False
    else:
        for path in Path(path).rglob('*.py'):
            logger.debug(f"Checking file '{path}'")

            tot_print_count = count_print_in_file(path)
            tot_docstring_print_count = count_print_in_docstrings(path)
            
            if tot_docstring_print_count != tot_print_count:
                logger.warning(f"Found some print statements in file '{path}'")
                check_passed = False
            
    if check_passed:
        exit(0)
    else:
        exit(1)