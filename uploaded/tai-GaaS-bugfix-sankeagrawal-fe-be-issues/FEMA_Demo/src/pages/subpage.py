import os

import toml
import streamlit as st

from utils import add_logo

CONFIG_PATH = os.path.join("config", "config.toml")
config = toml.load(CONFIG_PATH)
page_details = config["PAGES"]["SUBPAGE"]


def main():
    """
    Basic sample streamlit app to demonstrate functionality and configs
    """
    # setup streamlit header & sidebar

    st.title(page_details["TITLE_TEXT"])
    st.write(page_details["SUBTITLE_TEXT"])
    with st.sidebar:
        add_logo()


if __name__ == "__main__":
    st.set_page_config(page_title=page_details["NAME"])
    main()
