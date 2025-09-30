# Overview of the file:
#  - Purpose: Extracting insights from a set of tabular data (CSV formatted); creating plots and providing textual summary/description of the plots.
#  - Test data: Constellation Brands mock data with 4 files: sales, shipping, product list and distibutor information.
#  - Test prompts:
#           Calculate the average shipping delays based on the state/province of the distributor. Which state/province has the highest delay?
#           Is there a correlation between the promotion applied and the quantity sold or the revenue generated?
#           Examine if there is a correlation between the method of shipping (e.g. ground, air) and the frequency of shipping delays.

# General Use
import datetime, logging

from PIL import Image

import streamlit as st
import warnings
import os
import toml

# Typing
from typing import List

# Modeling
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

# Util functions
from utils import add_logo, get_domains, initialize_logging, log_interaction, display_text_word_by_word

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.warn("deprecated", DeprecationWarning)

# Handling API key
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# Loading config file
CONFIG_PATH = os.path.join("config", "config.toml")
config = toml.load(CONFIG_PATH)



# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


st.set_page_config(
    page_title=config["PAGES"]["DATA_INSIGHT"]["NAME"], page_icon=config["IMAGES"]["BRAND_IMAGE"]
)



def get_domains(folder: str) -> List[str]:
    """
    Retrieves the list of sub-folders (domains) in the specified folder.

    Args:
        folder (str): The path to the main folder.

    Returns:
        List[str]: A list of names of sub-folders (domains) present in the main folder.
    """
    sub_folders = [
        name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))
    ]
    return sub_folders



def user_queries_tabular(question: str, temp: float = config["PAGES"]["DATA_INSIGHT"]["TEMPERATURE"], max_token: int = config["PAGES"]["DATA_INSIGHT"]["MAX_TOKEN"]) -> str:
    """
    Process user's query, extract relevant information from data files, 
    and provide a summarized answer along with a visual plot saved as an image.
    
    Args:
        question (str): The question posed by the user.
        temp (float): Temperature setting for the ChatOpenAI model. Default value is 0.2, it is set by the configuration file.
        max_token (int): Maximum number of tokens for the ChatOpenAI response. Default value is 2000, it is set by the configuration file.
        
    Returns:
        str: A summarized answer to the user's question.
    """
    
    # Remove existing plot if it exists
    if os.path.exists("plot1.png"):
        os.remove("plot1.png")

    try:
        file_list = [os.path.join(config["PAGES"]["DATA_INSIGHT"]["DATA_SOURCE"], file) 
                     for file in os.listdir(config["PAGES"]["DATA_INSIGHT"]["DATA_SOURCE"]) 
                     if os.path.isfile(os.path.join(config["PAGES"]["DATA_INSIGHT"]["DATA_SOURCE"], file))]
        
        # Initialize the agent
        agent = create_csv_agent(
            ChatOpenAI(temperature=temp, max_tokens=max_token, model="gpt-4-32k"),
            file_list,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        
        # Define the full query
        full_query = (f"{question}. Write a short concluding paragraph stating the final answer "
                      "of the question based on the data along with the reasoning behind it "
                      "in summarized form and save the plot image in the current working directory "
                      "as plot1.png with x and y axis labels along with the dynamic colors and "
                      "proper legend wherever applicable.")
        
        # Get answer from the agent
        answer = agent.run(full_query)
        st.session_state['conclusion'] = answer
        return answer

    except Exception as e:
        error_message = ("Sorry, I am not able to determine the result due to technical/server error. "
                         "I apologise for the inconvenience caused.")
        st.session_state['conclusion'] = error_message
        return error_message
    
    

def print_image() -> None:
    """
    Display an image on the Streamlit app. If 'plot1.png' exists in the current directory, 
    it displays that image. Otherwise, it displays a mock image from the 'imgs' directory.
    
    Returns:
        None
    """

    if os.path.exists("plot1.png"):
        img1 = Image.open('plot1.png')
        st.image(img1, width=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
    else:
        img2 = Image.open('./imgs/mock.png')
        st.image(img2, width=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")



def main() -> None:
    """
    Defines the main execution function for the Streamlit app. It handles user input,
    processes the query, generates the required answer, and displays it along with any 
    relevant images.
    
    The function includes:
    - Sidebar with logo, domain selection, and configurations.
    - Main content area for user input, answer generation, and displaying insights.
    
    Global Variables:
        domain (str): Selected domain for the app.
        graph_text (str): User instruction for insight generation (currently commented out).
        
    Returns:
        None
    """

    # Initialize the logging setup
    log_file_path = initialize_logging()
    
    with st.sidebar:
        add_logo()
        new_chat = st.button("Clear Screen", use_container_width=True)
        if new_chat:
            logger.info("***** Screen Cleared! *****")
            st.session_state["message"] = ""

        st.session_state.domain = st.selectbox("**Domain**", tuple(get_domains(config["PAGES"]["DATA_INSIGHT"]["DATA_SOURCE"])))
    
        st.write("")
        st.write("")

    message_text = st.text_area(
        label=config["PAGES"]["DATA_INSIGHT"]["SUB_TITLE_ABOVE_TEXT_BOX2"]
    )
    st.session_state["message"] = message_text
    st.write("")
    generate_answer = st.button(label="Generate Answer", use_container_width=True)
    if generate_answer == True:
        st.session_state["generate_answer"] = True

    if message_text != '':
        if "generate_answer" in st.session_state.keys():
            if st.session_state["generate_answer"]:
                logger.info(f"\n\n NEW QUESTION: {message_text}")
                logger.info("\nStart Time - {}".format(str(datetime.datetime.now())))
                st.write("**User Query:**")
                st.write(message_text)
                st.write("")
                with st.spinner(text=config["PAGES"]["DATA_INSIGHT"]["WAITING_NOTIFICATION"]):
                    st.write("**Response:**")
                    response = user_queries_tabular(message_text, config["PAGES"]["DATA_INSIGHT"]["TEMPERATURE"], config["PAGES"]["DATA_INSIGHT"]["MAX_TOKEN"])
                        
                    # Use the display_text_word_by_word function to reveal the model's response progressively
                    response_placeholder = st.empty()  # Create an empty placeholder for the response
                    display_text_word_by_word(response, response_placeholder)  # Display the response    
                    # Logging the user's query and the model's response
                    log_interaction(log_file_path, message_text, response)
                        
                    st.write("**:green[Conclusion:]**")
                    conclusion_placeholder = st.empty()  # Create an empty placeholder for the conclusion
                    display_text_word_by_word(st.session_state['conclusion'], conclusion_placeholder)  # Display the conclusion

                    print_image()



if __name__ == "__main__":
    st.title(config["PAGES"]["DATA_INSIGHT"]["TITLE_ABOVE_TEXT_BOX"])
    st.write(config["PAGES"]["DATA_INSIGHT"]["SUB_TITLE_ABOVE_TEXT_BOX1"])
    main()
