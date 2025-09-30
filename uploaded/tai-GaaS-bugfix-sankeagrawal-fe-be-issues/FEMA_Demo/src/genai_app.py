"""
Usage: `streamlit run genai_app.py`

Entrypoint and home page for Generic GenAI App.

Dependencies: PIL, streamlit, streamlit_extras, st_pages, toml, utils.py
"""
import os

from PIL import Image
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages
import toml

from utils import add_logo

CONFIG_PATH = os.path.join("config", "config.toml")
config = toml.load(CONFIG_PATH)
page_details = config["PAGES"]


def make_sidebar():
    """
    Generate sidebar from configured path and sidebar label
    """
    sidebar_details = list()
    for current_page in page_details:
        sidebar_details.append(
            Page(
                page_details[current_page]["PATH"],
                page_details[current_page]["NAME"],
            )
        )

    show_pages(sidebar_details)


def make_buttons():
    """
    Generate buttons recursively from configured page name, button title,
    and button description
    """
    for current_page in page_details:
        # define columns with relative widths
        button_col, description_col = st.columns([2, 6]) 
        if page_details[current_page]["NAME"] == "Home":  # no Home button
            pass
        else:
            with button_col:
                button = st.button(
                    label=f"**{page_details[current_page]['BUTTON_LABEL']}**",
                    use_container_width=True,
                )
                if button:
                    switch_page(page_details[current_page]["NAME"])
            with description_col:
                st.write(page_details[current_page]["BUTTON_DESCRIPTION"])


def main():
    """
    Generate headers, sidebar, and buttons.
    """
    add_logo()

    # format header
    img_col, title_col = st.columns(2, gap="medium")
    with img_col:
        header_img = Image.open(config["IMAGES"]["HEADER_IMAGE"])
        st.image(
            header_img,
            width=None,
            use_column_width=True,
            clamp=False,
            channels="RGB",
            output_format="auto",
        )
    with title_col:
        st.title(config["TEXT"]["DEMO_TITLE"])

    st.write(config["TEXT"]["DEMO_TAGLINE"])

    make_sidebar()
    make_buttons()


if __name__ == "__main__":
    main()
