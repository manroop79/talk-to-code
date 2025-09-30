# Github Actions

## Purpose

## Workflows
The workflows folder contains all .yml files which are read by github to spawn actions. These indicate which actions will be run and in what order.

## Default
Each .yml file in workflows has an associated folder with a matching name under the default folder. This folder contains everything that's needed to run the action.

## Current Actions

### Lint check
Runs on PR.
Checks for
- Commented code
- TODO and FIXME tags
- Class and function Docstring exist
- Unused import, wildcard import
- Print statement
- Unused variables
- All class variable defined in `__init__`
- Inconsistent return
- Mutable value used as function defaults
- Some common mistakes, i.e. return/yield outside function; reference variable before definition; redefine functions.

The identified violation will be annotated on the code diff page. 
Here is a list of error code one that maybe reported by flake8.

| code | Description                                                     |
| ----------- | ----------- |
| E800| Found commented out code |
| T201 | print found | 
| T203 | pprint found | 
| T204 | pprint declared | 

Here is a [full list](https://pylint.readthedocs.io/en/latest/user_guide/checkers/features.html) for checks runs by pylint.

### Commented Code Check
Checks for commented code in python files.
Runs on PR.

### Docstring Check
Checks each function for
- Docstring present
- Docstring has all applicable sections (Args, Returns, Yields, Raises) depending on function itself
- Docstring has documentation for each arg that is not 'self'

Runs on PR

### Function Length Check
Checks the length of each function and raises an issue if any function definition is longer than 40 lines of code. Empty lines, and lines that are commented out with a "#" are not considered in this count.

Runs on PR

### Lint Markdown
Runs a markdown linter on all `.md` files and will show as a status check before merging a PR (or in terminal post push [wip] )

Only runs when `.md` files are changed

### MD to PDF Conversion
Will convert all `.md` files that are titled `Readme` (case insensitive) into `.pdf` files and a new PR will be made to merge the new created files back to the branch that was pushed to

Only runs when `.md` files are changed

### MD TODO Check
Checks for TODOs in Markdown Files
Runs when markdown files are updated.

### Print Check
Checks for print statements left in python code.

Runs on PR to main or master.

### Python TODO Check
Checks for TODOs in python files, and other common short phrases (ex. fixme).

Runs on PR when there are .py files in the diff.

### Unused Import Check
Identifies imports in python files that do not occur outside of imports.

Runs on PR to master or main branches.
