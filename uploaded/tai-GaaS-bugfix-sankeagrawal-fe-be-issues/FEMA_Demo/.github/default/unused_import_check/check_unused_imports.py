import ast
import argparse
import logging
from collections import namedtuple
from pathlib import Path
import os

logging.basicConfig(level=logging.INFO )
logger = logging.getLogger(__name__)

Import = namedtuple("Import", ["module", "name", "alias"])

def get_imports(path):
    """Get all imports used in the given python file

    Args:
        path (str): File to identify imports in
    
    Returns:
        None : Returns None if an error is encountered

    Yields:
        Import: namedtuple with module, name, and alias of the import
    """
    try:
        with open(path) as fh:        
            root = ast.parse(fh.read(), path)

    except UnicodeDecodeError:
        logger.error(f"File `{path}` failed to open (Invalid Unicode)")
        yield None
    except FileNotFoundError:
        logger.error(f"File `{path}` was not found")
        yield None
    except SyntaxError:
        logger.error(f"File `{path}` failed to compile")
        yield None
    
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom) and node.module is not None:  
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)

def check_imports(file_path):
    """Check for unused imports at the given file_path

    Args:
        file_path (str): Path to a .py file to check for unused imports

    Returns:
        int: 0 if no unused imports are found, else 1
    """
    try:
        with open(file_path, "r") as fh:
            text = fh.read()
    except UnicodeDecodeError:
        logger.error(f"File `{file_path}` failed to open (Invalid Unicode)")
        return 0
    except FileNotFoundError:
        logger.error(f"File `{file_path}` was not found")
        return 0
    
    ret_val = 0
    for imp in get_imports(file_path):
        if imp.alias is not None:
            check_str = imp.alias
        else:
            check_str = ".".join(imp.name)
            count = text.count(check_str)
            if count == 1:
                logger.info(f"Found unused import : `{check_str}` in file : `{file_path}`")
                ret_val = 1
    return ret_val


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for unused imports in a python file or directory')
    parser.add_argument('path', metavar='path', type=str,
                        help='Path to the folder or python file to check. If a folder is provided, all python files within it are searched, including subdirectories, recursively.')
    args = parser.parse_args()
    exit_val = 0
    if args.path[-3:] == ".py":
        if args.path != "__init__.py": 
            exit_val = check_imports(args.path)
        else:
            logger.info("Input is an '__init__.py' file. It will be ignored")
    else:
        for path in Path(args.path).rglob('*.py'):
            if os.path.basename(path) != "__init__.py" and check_imports(path) == 1:
                exit_val = 1
    exit(exit_val)
        
    


    