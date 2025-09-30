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

def check_for_sections(func):
    """Determine which sections are needed in a docstring for the given function

    Args:
        func (FunctionInfo): NamedTuple FunctionInfo with information on the "name", "args", "docstring", "body", "start_line" of the given str

    Returns:
        list: list of str sections that need to be included in the given functions docstring
    """
    RETURN_REGEX = "\Wreturn\W\S"
    RAISE_REGEX = "\Wraise\W"
    YIELD_REGEX = "\Wyield\W"

    required_sections = []
    if len(func.args) > 1:
        required_sections.append("args")
    # Special case if the only arg is self
    elif len(func.args) == 1 and func.args[0].strip() not in {"self", "cls"}:
        required_sections.append("args")
    # Check for returns section
    if re.search(RETURN_REGEX, func.body) is not None:
        required_sections.append("returns")
    # Check for yields section
    if re.search(YIELD_REGEX, func.body) is not None:
        required_sections.append("yields")
    # This just checks if there is a raises or not, it may be improved
    # in the future by identifying each different exception that
    # could be raised
    if re.search(RAISE_REGEX, func.body) is not None:
        required_sections.append("raises")

    return required_sections

def check_sections(func):
    """Check if the given functions docstring contains all required sections

    Args:
        func (FunctionInfo): NamedTuple FunctionInfo with information on the "name", "args", "docstring", "body", "start_line" of the given str

    Returns:
        Bool: True if passed, False if failed
    """
    # Check that each required section is present
    required_sections = check_for_sections(func)
    # Normalize the function body to identify section headers
    docstring_lines = func.docstring.split("\n")
    norm_lines = ["".join([char for char in line if char.isalnum()]) for line in docstring_lines]

    for section in required_sections:
        passed = False
        for line in norm_lines:
            logger.debug(line)
            if line.lower() == section:
                passed = True
        if not passed:
            logger.warning(f"Missing section {section} in docstring for function {func.name} at line {func.start_line}")
            return False
    return True

def check_docstrings(path, check_internal_functions=CHECK_INTERNAL_FUNCTIONS):
    """Check whether docstrings are present for each function in the given .py file

    Args:
        path (str): Path to file to check
        check_internal_functions (bool): If True, will check internal functions (prepended with '_') if False these will be ignored
    Returns:
        bool: True if the file has all docstrings, False if the file is missing some docstrings
    """
    passed = True
    functions = get_functions(path)
    for func in functions:
        if not check_internal_functions and func.name[0] == "_":
            logger.debug(f"Skipping internal function {func.name}")
            continue
        elif func.docstring is None:
            logger.warning(f"Docstring missing for function {func.name} at line {func.start_line} in file {path}")
            passed = False
        else:
            # Check that each arg is documented
            for arg in func.args:
                if arg not in func.docstring:
                    passed = False
                    logger.warning(f"Undocumented argument `{arg}` for function {func.name} at line {func.start_line} in file {path}")
            has_all_sections = check_sections(func)
            if not has_all_sections:
                passed = False
    return passed
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for missing docstrings')
    parser.add_argument('path', metavar='path', type=str,
                        help='Path to the folder or python file to check. If a folder is provided, all python files within it are searched, including subdirectories, recursively.')
    args = parser.parse_args()
    path = args.path
    if CHECK_INTERNAL_FUNCTIONS:
        logger.info(f"Checking all functions (Including internal functions)")
    else:
        logger.info("Ignoring checks on any functions prefixed by '_'")
    functions = []
    check_passed = True

    if path[-3:] == ".py":
        check_passed = check_docstrings(path)
    else:
        for path in Path(path).rglob('*.py'):
            logger.debug(f"Checking file '{path}'")
            if not check_docstrings(path):
                check_passed = False
    if check_passed:
        exit(0)
    else:
        exit(1)
        