# This script automatically populates documentation with docstrings
from pathlib import Path
import mkdocs_gen_files

repo_root = Path(__file__).parents[1]
src_root = repo_root / 'src'
for path in src_root.glob("**/*.py"):
    if "__init__" in str(path):
        continue

    doc_path = Path("reference", path.relative_to(src_root)).with_suffix(".md")

    # Make docs requires relative imports
    path = path.relative_to(repo_root)
    with mkdocs_gen_files.open(doc_path, "w") as f:
        ident = ".".join(path.with_suffix("").parts)
        f.write("::: " + ident)