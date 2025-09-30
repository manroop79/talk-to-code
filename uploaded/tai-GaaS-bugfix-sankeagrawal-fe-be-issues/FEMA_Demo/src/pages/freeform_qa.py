import os

from dotenv import find_dotenv, load_dotenv
import logging
import toml

import openai
import streamlit as st

from utils import add_logo

CONFIG_PATH = os.path.join("config", "config.toml")
config = toml.load(CONFIG_PATH)
page_details = config["PAGES"]["FREEFORM"]

# retrieve OpenAI API key from local .env
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = openai_api_key


def generate_summary(question: str) -> str:
    """
    Construct the messages for OpenAI input and generate the conversation
    summary using OpenAI's ChatGPT model

    Args:
        question (str): user input text

    Returns:
        str: summary if successful, default appology if not
    """
    try:
        messages = [
            {"role": "user", "content": question},
        ]
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4-32k", messages=messages
        )
        summary = chat_completion.choices[0].message.content
        # Accounting for LaTeX sensitive characters
        summary = summary.replace("$", "dollars")
        return summary

    except Exception as e:
        logging.warning(e)
        return page_details["ERROR_RESPONSE"]


def format_output(input_question: str, summary_response: str) -> str:
    """
    Format input question and response for output in Streamlit
    
    Args:
        input_question (str): user input question
        summary_response (str): model-generated summary answer

    Returns:
        str: formatted string question/answer response
    """

    response = f"""
    \n**User Query:**
    \n{input_question}
    \n**:blue[Summary:]**\n
    \n{summary_response}
    \n___\n
    """

    return response


def main():
    """
    Streamlit app for direct ChatGPT query
    """
    # setup streamlit header & sidebar
    st.title(page_details["TITLE_TEXT"])
    st.write(page_details["SUBTITLE_TEXT"])
    with st.sidebar:
        add_logo()
        if "freeform_responses" not in st.session_state.keys():
            st.session_state["freeform_responses"] = []
        clear_screen = st.button("Clear Screen", use_container_width=True)
        if clear_screen:
            st.session_state["freeform_responses"] = []
        history_on = st.checkbox(label = page_details['CHECKBOX_TEXT'])

    # setup textbox and button for question input
    input_question = st.text_area(label=f"**{page_details['MESSAGE_BOX_TEXT']}**")
    generate_answer = st.button(
        label=page_details["SEARCH_BUTTON_LABEL"],
        use_container_width=True,
    )
    if generate_answer == True:
        st.session_state["generate_search"] = True

    spinner_placeholder = st.empty()
    history_placeholder = st.empty()
    if "freeform_responses" in st.session_state.keys():
       history_placeholder.write(" \n".join(st.session_state["freeform_responses"]))

    # generate and format page output
    if input_question != "":
        if "generate_search" in st.session_state.keys():
            if st.session_state["generate_search"]:
                with spinner_placeholder:
                    with st.spinner(text=page_details["SPINNER_TEXT"]):
                        summary_response = generate_summary(input_question)
                        response = format_output(input_question, summary_response)
                        if not history_on:
                            st.session_state["freeform_responses"] = []
                        st.session_state["freeform_responses"].insert(0, str(response))
                        st.session_state["generate_search"] = False

                history_placeholder.write(" \n".join(st.session_state["freeform_responses"]))


if __name__ == "__main__":
    st.set_page_config(page_title=page_details["NAME"])
    main()
