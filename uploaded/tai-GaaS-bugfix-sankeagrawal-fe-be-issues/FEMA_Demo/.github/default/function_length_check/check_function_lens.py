import ast
import logging
import argparse
from collections import namedtuple
from pathlib import Path

# Setup Logging
logger = logging.getLogger(__name__)



LINE_LIMIT = 40

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
            args = [item.arg for item in node.args.args if item.arg != "self"]
            f_info = FunctionInfo(name, args, doc_str, body, node.lineno)
            func_list.append(f_info)
    return func_list

def is_commented(line):
    """Check if the whole line is commented

    Args:
        line (str): str line from a python file

    Returns:
        Bool: True if the first non-whitespace character is a "#" else False
    """
    stripped_line = line.strip()
    return len(stripped_line) == 0 or line.strip()[0] == "#"



def find_commented_lines(lines):
    """Find the indexes of lines in the given iterable that are commented with a "#" at the start.

    Args:
        lines (iterable): Iterable of strings which are single lines from a .py file to check

    Returns:
        list: List of indexes of commented lines in given 'lines'
    """
    commented_lines = [i for i, line in enumerate(lines) if is_commented(line)]
    return commented_lines

def find_empty_lines(lines):
    """Find the indexes of lines in the given iterable that are only whitespace

    Args:
        lines (iterable): Iterable of strings

    Returns:
        list: List of line indexes that are just whitespace in lines
    """
    empty_lines = [i for i, line in enumerate(lines) if line.strip() == ""]
    return empty_lines

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Check function lengths in a folder or directory')
    parser.add_argument('path', metavar='path', type=str,
                        help='Path to the folder or python file to check. If a folder is provided, all python files within it are searched, including subdirectories, recursively.')
    parser.add_argument('--exclude', metavar='function_names', type=str, nargs='+', default=None,
                        help='Name of the function to exclude from the function length check.')
    args = parser.parse_args()
    path = args.path
    exclude = args.exclude
    logger.info(f"Running with line limit of '{LINE_LIMIT}' lines")
    functions = []
    too_many_lines = False

    if path[-3:] == ".py":
        functions = get_functions(path)
        for func in functions:
            if exclude is None or (func.name not in exclude):
                lines = func.body.split("\n")
                num_commented_lines = len(find_commented_lines(lines))
                num_empty_lines = len(find_empty_lines(lines))
                logger.debug(f"Found {len(lines)} lines with {num_commented_lines} commented lines and {num_empty_lines} blank lines")
                
                num_lines = len(lines) - num_commented_lines - num_empty_lines
                if num_lines < LINE_LIMIT:
                    logger.debug(f"Function {func.name} passed with {num_lines} lines")
                else:
                    logger.warning(f"Found function {func.name} in file {path} with too many lines! ({num_lines})")
                    too_many_lines = True
    else:
        for path in Path(path).rglob('*.py'):
            logger.debug(f"Checking file '{path}'")
            new_funcs = get_functions(path)
            for func in new_funcs:
                if exclude is None or (func.name not in exclude):
                    lines = func.body.split("\n")
                    num_commented_lines = len(find_commented_lines(lines))
                    num_empty_lines = len(find_empty_lines(lines))
                    logger.debug(f"Found {len(lines)} lines with {num_commented_lines} commented lines and {num_empty_lines} blank lines")
                    num_lines = len(lines) - num_commented_lines - num_empty_lines
                    if num_lines < LINE_LIMIT:
                        logger.debug(f"Found function {func.name} in file {path} with {num_lines} lines")
                    else:
                        logger.warning(f"Found function {func.name} in file {path} with too many lines! ({num_lines})")
                        too_many_lines = True
            functions.extend(new_funcs)
    if too_many_lines:
        exit(1)
    else:
        exit(0)
        
