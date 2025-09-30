#!/bin/sh -l
echo "Run Lint test"
flake8 --toml-config=.github/default/lint_check/config.toml .
pylint --rcfile=.github/default/lint_check/config.toml src
find . -type f -name "*.py" ! -path "./src/*" -print0 | xargs -0 pylint --rcfile=.github/default/lint_check/config.toml
echo ""
echo "Check md todos"
.github/default/md_todo_check/check_md_todos.sh
echo ""
echo "Check py todos"
.github/default/py_todo_check/check_py_todos.sh
echo ""
echo "Check docstrings"
python .github/default/docstring_check/check_docstrings.py .
echo ""
echo "Check function length"
python .github/default/function_length_check/check_function_lens.py .
echo ""
echo "Check commented code"
bash .github/default/commented_code_check/check_commented_code.sh
echo ""
echo "Check print"
python .github/default/print_check/check_prints.py .
echo ""
echo "Check unused import"
python .github/default/unused_import_check/check_unused_imports.py .