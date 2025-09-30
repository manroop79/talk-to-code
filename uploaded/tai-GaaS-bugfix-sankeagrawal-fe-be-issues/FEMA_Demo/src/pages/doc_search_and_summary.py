# Overview of the file:
#  - Purpose: Extracting information from the available corpus of PDF files along with comparison and summarization of information.
#  - Test data: Constellation Brands 10-K filings.
#  - Test prompts:
#        What was the company's total revenue for the last fiscal year? How does this compare to the revenue reported in the prior year's 10-K?
#        Did the company report any financial metrics related to mergers or acquisitions? If so, what was the total value of these transactions?
#        What was the company's gross profit and its corresponding margin for the fiscal year of 2022?

# Standard library
import os
import logging
import datetime
import warnings
import toml
import sys

# Third-party libraries
import streamlit as st

# Langchain
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory

# Typing
from typing import List, Dict
sys.path.append("src")

# Utility
from utils import (
    add_logo,
    initialize_logging,
    log_interaction,
    display_text_word_by_word,
)
# Handling API key
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

warnings.filterwarnings("ignore")

# Loading config file
CONFIG_PATH = os.path.join("config", "config.toml")
config = toml.load(CONFIG_PATH)

# Define global variables
NUM_OF_SIM = None  # The number of similar documents to consider for summary
NUM_OF_SIM_ORIGINAL = None  # The original number of similar documents selected
SUMMARY_TYPE = (
    None  # The selected type of summary (Short, Long, Bullet Points, User-Determined)
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_instruction() -> str:
    """
    Generates instruction based on the type of summary requested.

    Returns:
        str: The generated instruction.
    """
    return config["PAGES"]["DOC_SEARCH"]["INSTRUCTION_MAPPING"][SUMMARY_TYPE]


def prepare_response(response: Dict) -> str:
    """
    This function generates a string output based on the response from the
    query.  It unpacks the response object, styles the references and includes
    the question.

    Args:
        response (Dict): response dict from llm query

    Returns:
        str: formatted output description
    """

    output = f"**User Query:**\n{response['question']}\n\n"

    output += "\n\n**:blue[Summary:]**\n\n"
    output += response["output_text"]
    output += "\n\n---\n\n"

    output += "**:green[Relevant Documents:]**\n"
    logger.info(f"\n\n***\n\n{response}\n\ns**\n\n")
    for i, doc in enumerate(response["input_documents"]):
        output += f"\n{i+1}. **Document Name:** {doc.metadata['source']}\n"
        output += f"\n   **Page:** {doc.metadata['page']}"
        output += f"  **Relevance:** {100*doc.metadata['score']:.1f}%\n"
    return output


@st.cache_resource  # we only want to run this once so memory is persistant
def prepare_chain():
    """
    Create a qa chain to form the prompt and send to the OpenAI api.
    Initialize the chain with memory so the model 'remembers' previous queries
    """

    prompt_template = """Use the following pieces of context to answer the question at the end. If the context is empty, say that you don't know the answer. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    {instruction}
    Question: {question}\n

    """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "instruction", "question"]
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")

    chain = load_qa_chain(
        OpenAI(model_name="gpt-3.5-turbo",
               temperature=config["PAGES"]["DOC_SEARCH"]["TEMPERATURE"],
               max_tokens=config["PAGES"]["DOC_SEARCH"]["MAX_TOKEN"]),
        memory=memory,
        chain_type="stuff",
        prompt=PROMPT,
        verbose=True
    )

    return chain


def user_queries(user_query: str) -> str:
    """
    Handle the query: first, get the relevant documents (with relevance
    scores), send the request and get the response.

    Args:
    user_query (str): A question asked by the user.

    Returns:
    str: The generated summary text.

    """
    vectordb = st.session_state["vectordb"]
    chain = st.session_state["chain"]

    docs_and_scores = vectordb.similarity_search_with_relevance_scores(
        user_query,
        k=NUM_OF_SIM,
        score_threshold=config["PAGES"]["DOC_SEARCH"]["SCORE_THRESHOLD"])

    if len(docs_and_scores) == 0:
        st.write('<p style="font-size:20px; color:pink;">Sorry, this question is out of context. There are no relevant documents in the private database to answer this query reliably. Please try another query</p>',unsafe_allow_html=True)

    else:

        for doc, score in docs_and_scores:
            doc.metadata = {**doc.metadata, **{"score": score}}

        docs = [doc[0] for doc in docs_and_scores]

        instruction = get_instruction()

        response = chain(
            {
                "input_documents": docs[:NUM_OF_SIM],
                "instruction": instruction,
                "question": user_query,
            },
            return_only_outputs=False,
        )

        response_text = prepare_response(response)
        response_text = response_text.replace("$", "\$")

        return response_text


def sidebar_content():
    """
    This function defines the content of the sidebar in the Streamlit app.
    It includes a button to clear the screen, a dropdown to select the domain,
    a dropdown to select the number of relevant documents for summary,
    and a set of radio buttons to select the summary type.
    """

    global NUM_OF_SIM
    global NUM_OF_SIM_ORIGINAL
    global SUMMARY_TYPE

    add_logo()
    if "history" not in st.session_state.keys():
        st.session_state["history"] = []
    clear_screen = st.button("Clear Screen", use_container_width=True)
    if clear_screen:
        logger.info("***** Screen Cleared *****")
        st.session_state["doc_search"] = ""
        st.session_state = {}
        st.session_state["history"] = []
    NUM_OF_SIM = st.selectbox("**Relevant Documents Summary**",
                              (1, 2, 3, 4, 5, 10))
    NUM_OF_SIM_ORIGINAL = NUM_OF_SIM
    SUMMARY_TYPE = st.radio(
        "Summary Type",
        tuple(config["PAGES"]["DOC_SEARCH"]["INSTRUCTION_MAPPING"].keys()),
    )


def add_metadata(docs: List) -> List:
    """Add extra metadata to the text chunks read in. In this case,
    add the company name based on the directory name of the parent folder
    the pdf document came from. This can be used for filtering the docs
    to be used for retrieval. Obviously, this can be extended to include
    any meta-data that will be useful for returning accurate queries.

    Args:
        docs (List): List of langchain Documents

    Returns:
        List: List of langchain Documents that have modified meta-data
    """
    for doc in docs:
        filestring = doc.metadata["source"]
        company = os.path.basename(os.path.dirname(filestring))
        doc.metadata["Company"] = company

    return docs


@st.cache_resource
def setup_db() -> Chroma:
    """
    Read all pdf files in a specified directory, split the sections,
    find the embeddings, and store in a vector database.

    There is a lot going on in this function, and forms the basis of
    'document loading' pipeline.  This should probably be a centralized
    function somewhere, as it is a pattern that will appear all over and we
    will want to modify it.

    Returns:
        VectorStore: need to properly abstract the vector store type.
    """

    embeddings = OpenAIEmbeddings()

    if os.path.exists("./chroma_db"):
        logger.info("found existing database, using that...\n")
        vectordb = Chroma(
            persist_directory="./chroma_db", embedding_function=embeddings
        )
    else:
        logger.info("\n** Ingesting PDF documents...")
        with st.spinner(text="Ingesting documents and creating database..."):
            loader = PyPDFDirectoryLoader(
                config["PAGES"]["DOC_SEARCH"]["DATA_SOURCE"])
            docs = loader.load()
            logger.info(f"Length of raw docs: {len(docs)}")
            text_splitter = CharacterTextSplitter(
                separator="\n", chunk_size=1000,
                chunk_overlap=150, length_function=len
            )
            docs = text_splitter.split_documents(docs)
            logger.info(f"Length of split docs: {len(docs)}")

            docs = add_metadata(docs)

            vectordb = Chroma.from_documents(
                docs, embedding=embeddings, persist_directory="./chroma_db"
            )
            vectordb.persist()
            logger.info("...done! ** \n\n")

    return vectordb


def main_content():
    """
    This function defines the main content of the Streamlit app.
    It includes a text area for the user to enter a question,
    and a button to generate the search.

    """

    st.session_state["user_query"] = st.text_area(
        label=config["PAGES"]["DOC_SEARCH"]["SUB_TITLE_ABOVE_TEXT_BOX2"],
        key="mess"
    )
    st.session_state["generate_search"] = st.button(
        label="Generate Search", use_container_width=True, key="ans"
    )

    st.session_state["vectordb"] = setup_db()
    st.session_state["chain"] = prepare_chain()


def handle_response(log_file_path: str) -> None:
    """
    Handle the response to the user's query.

    This function checks if a message is entered by the user, constructs
    the response by including the references, summary, logs the interaction
    to a specified log file, and appends the response to the session history.
    If no search is generated, it just displays the session history.

    Parameters:
        log_file_path (str): Path to the file where interactions (user query
                             and model response) are logged.

    Returns:
        None

    Examples:
        handle_response("/path/to/log.txt")
    """
    try:
        if st.session_state["user_query"] != "":
            user_query = st.session_state["user_query"]
            if "generate_search" in st.session_state.keys():
                if st.session_state["generate_search"]:
                    logger.info(f"\n\n NEW QUESTION: {user_query}")
                    logger.info(
                        "\nStart Time - {}".format(str(datetime.datetime.now())))

                    with st.spinner(
                        text=config["PAGES"]["DOC_SEARCH"]["WAITING_NOTIFICATION"]
                    ):
                        response = user_queries(user_query)

                        # Logging the user's query and the response
                        log_interaction(log_file_path, user_query, response)

                        # Use the display_text_word_by_word function to display the response progressively
                        response_placeholder = (
                            st.empty()
                        )  # Create an empty placeholder for the response
                        display_text_word_by_word(
                            response, response_placeholder
                        )  # Display the response

                        # Move the previous current_response to past_responses
                        if "current_response" in st.session_state:
                            if "past_responses" not in st.session_state:
                                st.session_state["past_responses"] = []
                            st.session_state["past_responses"].append(
                                st.session_state["current_response"]
                            )

                        # Store the new response in current_response
                        st.session_state["current_response"] = response
                        st.session_state["generate_search"] = False
    except:
        st.write("")

    # Display past responses (if any)
    if "past_responses" in st.session_state:
        for past_response in st.session_state["past_responses"]:
            st.write(past_response)
        logger.info("Complete Time - {}".format(str(datetime.datetime.now())))


def main():
    """
    This is the main function that initializes the global variables,
    displays the sidebar and main content, and handles the response to the
    user's query.

    :func sidebar_content: displays the sidebar content
    :func main_content: displays the main content
    :func handle_response: handles the response to the user's query
    """
    with st.sidebar:
        sidebar_content()
    log_file_path = initialize_logging()
    main_content()
    handle_response(log_file_path)


if __name__ == "__main__":
    st.set_page_config(page_title=config["PAGES"]["DOC_SEARCH"]["NAME"])
    st.title(config["PAGES"]["DOC_SEARCH"]["TITLE_ABOVE_TEXT_BOX"])
    st.write(config["PAGES"]["DOC_SEARCH"]["SUB_TITLE_ABOVE_TEXT_BOX1"])
    main()
