# General
import os, datetime
import base64
import datetime
import streamlit as st
import docx2pdf
import time
import toml
from PIL import Image
import docx2pdf

# Typing
from typing import List

CONFIG_PATH = os.path.join("config", "config.toml")
config = toml.load(CONFIG_PATH)

        
def add_logo():
    """
    Add a logo to the sidebar using Markdown and HTML.

    This function adds custom CSS styles to the sidebar and inserts a logo image into the sidebar using base64 encoding.

    Returns:
        None
    """

    with open(config["IMAGES"]["BRAND_IMAGE"], "rb") as f:
        img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode()

    st.markdown(
        f"""<style>[data-testid="stSidebarNav"]{{background-image: url(data:image/jpeg;base64,{img_base64});background-repeat: no-repeat;background-size: 80px;padding-top: 20px;background-position: 80px 15px;}}[data-testid="stSidebarNav"]::before{{margin-left: 20px;margin-top: 20px;font-size: 30px;position: relative;top: 100px;}}</style>""",
        unsafe_allow_html=True,
    )


def display_text_word_by_word(text, placeholder=None, style="markdown", delay=0.05):
    """
    Display text word by word.

    This function takes a text and displays it word by word, either using Markdown or a text area.

    Args:
        text (str): The text to display word by word.
        placeholder (streamlit object, optional): The placeholder object to use. If not provided,
            a new placeholder will be created.
        style (str, optional): The display style to use. It can be "markdown" (default) or "text_area".

    Returns:
        None
    """
    if placeholder is None:
        placeholder = st.empty()
    word_list = text.split(" ")
    current_sentence = ""

    for word in word_list:
        current_sentence += word + " "
        if style == "markdown":
            placeholder.markdown(current_sentence, unsafe_allow_html=True)
        else:
            placeholder.text_area(current_sentence)
        time.sleep(delay)  # Adjust the sleep time to your needs



def get_domains(folder: str) -> List[str]:
    """
    Get a list of sub-folder names in a specified folder.

    Parameters:
    folder (str): The path of the folder.

    Returns:
    List[str]: A list of sub-folder names.

    """
    sub_folders = [
        name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))
    ]
    return sub_folders



def initialize_logging() -> str:
    """
    Initialize the logging directory and return the path for the day's log file.
    
    This function checks if a 'logs' directory exists in the current working 
    directory. If not, it creates one. It then returns the path to a log file
    named with the current date.
    
    Returns:
        str: Full path to the day's log file.
        
    Example:
        Output: "/path/to/current/directory/logs/log_20230905.txt"
    """
    
    # Folder path for the logs
    log_folder_path = os.path.join(os.getcwd(), "logs")

    # Create folder if it doesn't exist
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)

    # Return the full path for the log file
    log_file_path = os.path.join(log_folder_path, f"log_{datetime.datetime.now().strftime('%Y%m%d')}.txt")
    return log_file_path



def log_interaction(log_file_path: str, user_query: str, model_response: str) -> None:
    """
    Log the interaction (user query and model response) to the specified log file.

    Parameters:
        log_file_path (str): Path to the file where interactions are logged.
        user_query (str): User's query or message.
        model_response (str): Model's response or answer.

    Returns:
        None
    """
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Time: {datetime.datetime.now()}\n")
        log_file.write(f"User Query: {user_query}\n")
        log_file.write(f"Model Response: {model_response}\n")
        log_file.write("="*50 + "\n")