import json

# import the ai platform package
import ai_server
# import the openai package
import openai
import pandas as pd
import streamlit as st
from app_logger import init_logger
from env import load_config
# Trustworthy AI scanning
from llm_guard.vault import Vault
from openai import AzureOpenAI
from trustworthy_utils import scan_without_ui
from trustworthy_utils import setup_trustworthy_controls
from utils import add_logo, add_footer
from utils import get_secret

# use your access and secret keys to authenticate and
server_connection = ai_server.RESTServer(
    access_key="665e7edd-ae2c-4222-9d10-45b996aac565",  # example: "d0033d40-ea83-4083-96ce-17a01451f831"
    secret_key="59001d7b-c7ee-4cbc-9d05-1cb70524b17a",  # example: "c2b3fae8-20d1-458c-8565-30ae935c4dfb"
    base="https://workshop.cfg.deloitte.com/cfg-ai-demo/Monolith/api"
    # example: https://{domain}/{direcotry/path segment}/Monolith/api
)

# Modify OpenAI's API key and API base to use CFG's API.
openai.api_key = "EMPTY"
openai.api_base = server_connection.get_openai_endpoint()

config = load_config(config_file="./config/config.toml")
page_details = config["PAGES"]["FREEFORM"]

# Initialize logger
logger = init_logger('genai_app', config)

secrets = get_secret()

@st.cache_data
def set_openai_api_key() -> None:
    """Retrieves OpenAI API key from local .env"""
    try:
        openai_api_key = secrets["Key1"]
        openai.api_key = openai_api_key
    except KeyError as ke:
        st.session_state.logger.warning(
            "Please set your OPENAI_API_KEY as environment variable following the instructions on ReadMe file."
        )
        st.session_state.logger.warning(ke)


def get_summary_from_model(messages, model_name="e338934d-bef1-4920-9136-dc0e37060dfa") -> str:
    """Generates the conversation summary using OpenAI's ChatGPT model.

    Args:
        messages (list): list of constructed messages for OpenAI.
        model_name (str, optional): Name of OpenAI model to use. Defaults to "gpt-4-32k".

    Returns:
        str: summary from OpenAI.
    """
    #
    # chat_completion = openai.ChatCompletion.create(
    #     model=model_name,
    #     messages=messages,
    #     headers=server_connection.get_auth_headers(),
    #     insight_id=server_connection.cur_insight
    # )
    # return chat_completion.choices[0].message.content
    client = AzureOpenAI(
        api_key=secrets["Key1"],
        api_version="2023-12-01-preview",
        azure_endpoint=secrets["url"]
    )

    completion = client.chat.completions.create(
        model=secrets["gpt-3"],
        messages=messages
    )
    # chat_completion = openai.ChatCompletion.create(model=model_name, messages=messages)
    return completion.choices[0].message.content


def generate_summary(question: str, llm_guard: bool, enabled_scanners, settings, st_fail_fast):
    """
    Construct the messages for OpenAI input and generate the conversation
    summary using OpenAI's ChatGPT model

    Args:
        question (str): user input text.
        llm_guard (bool): enable llm-guard
        enabled_scanners (list): list of activated scanner names
        settings (dict): dict of setting values
        st_fail_fast (bool): flag whether to quit on first fail


    Returns:
        str: summary if successful, default apology if not.
    """
    summary = None

    # Initialize result variables
    st_result_text = None
    st_analysis = None

    if llm_guard and enabled_scanners:

        # if toggled, init the vault
        vault = Vault()

        # Scan prompt
        st_result_text, results_valid, results_score = scan_without_ui(
            vault, enabled_scanners, settings, question, st_fail_fast
        )

        # Prepare analysis data for presentation
        st_analysis = [
            {"scanner": k, "is valid": results_valid[k], "risk score": results_score[k]}
            for k in results_valid
        ]

        messages = [{"role": "user", "content": st_result_text}]
        summary = get_summary_from_model(messages)
        summary = summary.replace("$", "dollars")

        return st_result_text, pd.DataFrame(st_analysis), summary
    else:
        messages = [{"role": "user", "content": question}]
        summary = get_summary_from_model(messages)
        summary = summary.replace("$", "dollars")

        return summary, pd.DataFrame(st_analysis), None


def format_output(input_question: str, summary_response: str, summ_unedit: str, scanner_results: pd.DataFrame = None,
                  llm_guard_toggle: bool = False):
    """Format input question and response for output in Streamlit, and add scanner results if available.

    Args:
        input_question (str): user input text.
        summary_response (str): llm response
        summ_unedit (str): llm_respone (raw)
        scanner_results (DataFrame): results of llm-guard scanning
        llm_guard_toggle (bool): turn llm-guard on/off

    """

    # Check if enabled_scanners is empty and llm_guard_toggle is on
    if llm_guard_toggle and scanner_results is not None and not scanner_results.empty:
        st.write(f"""
        \n**User Query:**
        \n{input_question}
        """)

        with st.expander("TrustworthyAI Scanner Log"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Sanitized Text:**")
                st.write(summary_response)

            with col2:
                st.write("**Scanner Results:**")
                st.table(scanner_results)

        if all(scanner_results['is valid']):
            st.write(f"""**Response**
                    \n{summ_unedit}""")
        else:
            st.error("Your request violated the LLM usage policy")
    else:
        st.write(f"""
        \n**User Query:**
        \n{input_question}
        \n**:blue[Summary:]**\n
        \n{summary_response}
        \n___\n
        """)


def main():
    """Streamlit app for direct ChatGPT query."""
    # openai key
    # set_openai_api_key()

    # Setup Streamlit header & sidebar
    add_footer()

    llm_guard_toggle = True
    st_fail_fast = False

    with st.sidebar:
        add_logo(config)
        if "freeform_responses" not in st.session_state.keys():
            st.session_state["freeform_responses"] = []
        clear_screen = st.button("Clear Screen", use_container_width=True)
        if clear_screen:
            st.session_state["freeform_responses"] = []
        history_on = st.checkbox(label=page_details["CHECKBOX_TEXT"])

    tab1, tab2 = st.tabs(["Chat", "Controls"])

    with tab2:
        setup_trustworthy_controls()

    if "enabled_scanners" not in st.session_state:
        st.session_state.enabled_scanners = None
        st.session_state.settings = None
    enabled_scanners = st.session_state.enabled_scanners
    settings = st.session_state.settings

    with tab1:
        input_question = st.text_area(label=f"**{page_details['SUB_TITLE_ABOVE_TEXT_BOX2']}**")

        if st.button(
                label=page_details["SEARCH_BUTTON_LABEL"],
                use_container_width=True,
        ):
            with st.spinner(text=page_details["SPINNER_TEXT"]):
                summary_response, scanner_results, summ_unedit = generate_summary(input_question, llm_guard_toggle,
                                                                                  enabled_scanners, settings,
                                                                                  st_fail_fast)

                st.session_state.logger.info(f"FFQA - Query: {str(input_question)}")
                st.session_state.logger.info(json.dumps(
                    {'query': input_question, 'response_history_bool': history_on, 'response': summary_response}))

            format_output(input_question, summary_response, summ_unedit, scanner_results, llm_guard_toggle)


st.set_page_config(
    page_title=config["TEXT"]["CLIENT_NAME"],
    page_icon=config["IMAGES"]["ICON_IMAGE"],
)

st.markdown('<h1>Trustworthy<span style="color:#87bc1f;">LLM</span></h1>', unsafe_allow_html=True)
st.write(page_details["SUB_TITLE_ABOVE_TEXT_BOX1"])

main()
