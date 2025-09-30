"""
Usage: `streamlit run genai_app.py`

Entrypoint and home page for Generic GenAI App.

Dependencies: PIL, streamlit, streamlit_extras, st_pages, toml, utils.py
"""

import argparse

import streamlit as st
from PIL import Image
from st_pages import Page, show_pages
from streamlit_extras.switch_page_button import switch_page

from app_logger import LoggerManager
from env import load_config
from utils import add_logo

parser = argparse.ArgumentParser(description='This app lists animals')
parser.add_argument('-c', '--config',
                    help='Name of configuration file.',
                    default='config/config.toml')
args = parser.parse_args()
config_filename = args.config
print(config_filename)

config = load_config(config_filename)
st.session_state['config'] = config

st.set_page_config(
    page_title=config["TEXT"]["CLIENT_NAME"], page_icon=config["IMAGES"]["ICON_IMAGE"]
)
page_details = config["PAGES"]
page_selections = config["SUBSET"]["SELECTION"]
page_details = {k: v for k, v in page_details.items() if (k in page_selections)}

# initialize logger
if "logger" not in st.session_state:
    logger_manager = LoggerManager(
        "genai_app",
        log_out_on=config["LOCAL"]["LOG_OUT_ON"],
        log_out_dir=config["LOCAL"]["LOG_OUT_DIR"],
    )
    st.session_state["logger"] = logger_manager.get_logger()
logger = st.session_state["logger"]


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
    add_logo(config)

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
    st.session_state.logger.info("Starting ........")

    make_sidebar()
    make_buttons()


if __name__ == "__main__":
    main()
