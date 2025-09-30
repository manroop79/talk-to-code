import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for path in Path(".").rglob("*.md"):
        base, ext = os.path.splitext(path)
        out_path = base + ".pdf"
        logger.info(f"Converting file '{path}' to '{out_path}'.")
        os.system(f"md2pdf {path} {out_path}")