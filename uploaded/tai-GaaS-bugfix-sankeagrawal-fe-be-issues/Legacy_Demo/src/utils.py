# General
import base64
import datetime
import json
import os
import time
# Typing
from typing import List

import boto3
import streamlit as st

import boto3
def get_secret():
    secret_name = "dev/GenAI/core/AzureOpenAI"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(

        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return json.loads(get_secret_value_response['SecretString'])


def add_logo(config):
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


def add_footer():
    """
    Add a footer comment to the bottom of a page with markdown and HTML

    Returns:
        None
    """
    st.markdown(
        """<style>footer {visibility: visible;} footer:after{content:", powered by SFL Scientific, a Deloitte business"}</style>""",
        unsafe_allow_html=True,
    )


def add_llm_options(config: dict,
                    expanded: bool = False,
                    default_model: str = None,
                    use_memory: bool = True) -> dict:
    """
    Add a menu (typically to the sidebar) that contains options for selecting
    a LLM and parameters.

    Args:
        expanded (bool, optional): Whether to initially show the menu expanded
        or collapsed. Defaults to False.
        default_model_index (int, optional)
        use_memory(bool, optional) Whether to include conversational memory in
        the model. Defaults to True

    Returns:
        dict: model options in key, value pairs
    """
    available_models = config["MODELS"]["OPENAI"]

    if default_model and default_model in available_models:
        model_index = available_models.index(default_model)
    else:
        model_index = 0

    with st.expander("Options", expanded=expanded):
        llm_model_name = st.selectbox("LLM Model",
                                      available_models,
                                      index=model_index)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)

        if use_memory:
            include_memory = st.checkbox("Include conversation memory", value=True)
        else:
            include_memory = st.checkbox("Include conversation memory", value=False)

        options = {
            "llm_model_name": llm_model_name,
            "temperature": temperature,
            "include_memory": include_memory
        }

    return options


def display_text_word_by_word(text, placeholder=None, style="markdown", delay=0.05):
    """
    Display text word by word.

    This function takes a text and displays it word by word, either using Markdown or a text area.

    Args:
        text (str): The text to display word by word.
        placeholder (streamlit object, optional): The placeholder object to use. If not provided,
            a new placeholder will be created.
        style (str, optional): The display style to use. It can be "markdown" (default) or "text_area".
        delay (float): The delay (in units of seconds) between consecutive display of text.

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

    Args:
        folder (str): The path of the folder.

    Returns:
        List[str]: A list of sub-folder names.

    """
    sub_folders = [
        name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))
    ]
    return sub_folders


def initialize_logging(config) -> dict:
    """
    Initialize the logging directory and return the paths for the day's log files.


    The function determines the base directory based on the settings in '/config/config.toml'.

    Returns:
        dict: Paths for debug and info log files.
    """

    # Determine the base path based on the configuration
    if config.get("DGX") and config["DGX"].get("LOG_OUT_ON", False):
        base_path = config["DGX"].get("LOG_OUT_DIR", os.getcwd())
    else:
        base_path = os.getcwd()

    log_folder_path = os.path.join(base_path, "logs")

    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)

    date_str = datetime.datetime.now().strftime("%Y%m%d")

    paths = {
        "debug": os.path.join(log_folder_path, f"log_debug_{date_str}.txt"),
        "info": os.path.join(log_folder_path, f"log_info_{date_str}.txt"),
    }
    return paths


def log_interaction(log_file_path: str, user_query: str, model_response: str) -> None:
    """
    Log the interaction (user query and model response) to the specified log file.

    Args:
        log_file_path (str): Path to the file where interactions are logged.
        user_query (str): User's query or message.
        model_response (str): Model's response or answer.

    Returns:
        None
    """

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Time: {datetime.datetime.now()}\n")
        log_file.write(f"User Query: {user_query}\n")
        log_file.write(f"Model Response: {model_response}\n")
        log_file.write("=" * 50 + "\n")
