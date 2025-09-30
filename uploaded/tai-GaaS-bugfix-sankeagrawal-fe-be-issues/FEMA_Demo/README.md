# Generative AI Tool for Client Demos

<img src="imgs/logo.png" width=50%>

![](https://raster.shields.io/badge/python-v3.6+-blue.png)
![](https://api.travis-ci.org/anfederico/Clairvoyant.png?branch=master)
![](https://raster.shields.io/badge/dependencies-up%20to%20date-brightgreen.png)

Index
=====

1. [Project Overview](#project-overview)
2. [Usage Instructions](#usage-instructions)
3. [Overview of Tab](#overview-of-tabs)
4. [Project Notes](#project-notes)

# Project Overview
This repository is for the FEMA Demo. The developer can update **all** the free parameters of the code such as titles, company logo, source data from the configuration file (**config/config.toml**) and move immediately to the phase of testing prompts with the model.

All of the parameters in **config/config.toml** already have default values, the developer's only task is to replace these placeholders with variables that best fit the client's needs.

The repository is organized based on "tabs", which are separate Python files (one for each main functionality) that appear as separate buttons on the user interface.

**Current Functionalities**

  - **#0 Home** tab: A welcome page that the user first sees upon launching the application.

  - **#1 Document Search & Summarization** tab: Allows users to search for relevant content within a database of PDF documents.


This guide discusses in detail how to customize each of these tabs along with best practices, recommendations and known issues.

# Usage Instructions

### API setup

Unless the project has a common API key, the developer will need to obtain one.

**Step 1**: Link to the form: https://deloittesurvey.deloitte.com/Community/se/3FC11B267E706126 Last step with image uploading can be skipped. Brief description of the project is sufficient, provide name of the project technical lead.

**Step 2:** Within 24 hours the access is granted. Watch out for email with "Welcome to the OpenAI API" subject.

**Step 3:** Click on the link in the email, sign in with Deloitte email. After logging in, top right corner, click on "DeloitteUS" from menu options choose "View API Keys". Here, create an API key.

**Step 4:** Create a file named ".env" and place it into the repository's main directory. The content of the file should be:
    `OPENAI_API_KEY = "your-api-key-here"`

### Setting Up the Environment
The app can be run in one of two ways:

`Option 1`: 
After pulling the repository, navigate to the repository's home directory and execute the following commands:

    conda create -n fema_genai python=3.9
    conda activate fema_genai
    conda install pip
    pip install -r docker/installation_media/requirements.txt
    streamlit run src/genai_app.py
    
Following these steps, the application will pop up in the browser.

`Option 2`:
This project can currently dockerized, run the following command from the home directory of this repository:
```
bash scripts/build_and_run.sh
```

Then, start the app by typing the following into a browser window:
``` 
localhost:8501
```

### Source Data

   - Unzip the data file provided. After unzipping, move the `doc_search` folder to be under the `data` folder. This folder should contain documents in PDF format. 

# Overview of Tabs

## #0 Main User Interface

### Purpose
   - A welcome page that the user first sees upon starting the application. This page includes a set of buttons with descriptions that the user can choose from. From this page the user can switch to the tabs by clicking on the corresponding buttons.

### Steps to Customize the Tab    

  - The relevant section of **config/config.toml** is located under the `[IMAGES]`, `[TEXT]` and `[PAGES.HOME]` lines.

    - `HEADER_IMAGE`: The image that appears on the left top corner of the UI above the tabs. This image is also used as the icon in the browser thumbnail. This is typically the company's logo.
    - `BRAND_IMAGE`: Main image that appears on the front page when the application is started. This image contains the company's logo along with some typical products or titles.
    - `DEMO_TITLE`: Main title of the front page of the UI.
    - `DEMO_TAGLINE`: Sub-title that appears on the front page of the UI.
    - `PATH`: The path of the Python file. By default this is the `src/Overview.py` file.
    - `NAME`: Name of the welcome page. By default it is "Home".
    - `SIDEBAR_LABEL`: Tab name shown in the the left-side bar.

### Best practices

- **Appealing UI**:
    - Besides updating the header and brand images, make sure all the remaining text and titles fit the client's industry or specific use case. Try to minimize technical language.

### Known Issues
   - N/A

## #1 Document Search & Summarization

### Purpose

   - This tab allows the developer to use a corpus of PDF files and create documents summaries, comparisons or extract specific facts.
  
### Steps to Customize the Tab

  - The relevant section of **config/config.toml** is located under the `[PAGES.DOC_SEARCH]` and `[PAGES.DOC_SEARCH.INSTRUCTION_MAPPING]` lines.

  - List of parameters:
    - `PATH`: The path of the Python file.
    - `NAME`: The name of the tab that will be displayed.
    - `SIDEBAR_LABEL`: Text for the left-side bar.
    - `BUTTON_LABEL`: Text for the button.
    - `BUTTON_DESCRIPTION`: Description of the tab for the front page of the UI.
    - `TITLE_ABOVE_TEXT_BOX`: The main title that is displayed above the box where the user enters the prompt.
    - `SUB_TITLE_ABOVE_TEXT_BOX1`: Short sub-title text that is displayed above the prompt box. Its value can be "" (empty string) if the developer does not want to add this label.
    - `SUB_TITLE_ABOVE_TEXT_BOX2`: Short sub-title text that is displayed above the prompt box. Its value can be "" (empty string) if the developer does not want to add this label.
    - `WAITING_NOTIFICATION`: Text that is displayed when the model is running the query.
    - `TEMPERATURE`: The temperature that is used in the LLM. Its default value is 0.0. Accepted values are between 0 and 1. Lower values mean that the outputs are more consistent between consecutive runs.
    - `MAX_TOKEN`: The maximum number of tokens that are used in the LLM. Default value is 2000. This value works for the vast majority of use cases.
    - `DATA_SOURCE`: The folder where the PDF data is stored. By defult it is `./data/fema`. 
    - `SCORE_THRESHOLD`: The minimum relevance criteria that is used for retrieving chunk embeddings based on a given user query. Default value is 0.75 where 0 means no relevance and 1 means identical (maximum relevance) 
    - `[PAGES.DOC_SEARCH.INSTRUCTION_MAPPING]`: This is a dictionary that will give the user the option to get responses in various formats such as bullet point summary or summary in a specified number of paragraphs. This variable is composed of mapping name and instruction pairs. The default instructions are the following:  
      - "Short (In Paragraph)" = "provide the very short summary of the provided above text in two to three small paragraphs and summary response should be in accordance - with the below question"
      - "Long (In Paragraph)" = "provide the detailed summary of the provided above text in three to four detailed paragraphs and summary response should be in accordance - with the below question"
      - "Short (In Bullet Points)" = "provide the summary of the provided above text in 2 bullet points and summary response should be in accordance with the below question"
      - "Long (In Bullet Points)" = "provide the summary of the provided above text in 6 bullet points and summary response should be in accordance with the below question"
      - "User-Determined" = ""
    - These strings are passed to the LLM and instruct the model to generate the final output in the desired format.
    - The names of the instruction will appear as a bar with click-able options on the left side of the Document Search tab.   

### Source Data

   - The source data placed into the `DATA_SOURCE` folder must be PDF files, which is the only accepted data format.
   - By default the model will create a vector data base from the PDF files that is stored in the `chroma_db` folder of the repository's main directory. This allows significant reduction in response time and cost saving as well.
   - IMPORTANT: If the developer replaces the source PDF files with new ones, the previous `chroma_db` folder has to be deleted so the model can generate the updated vector data base.
   - The model can use up to 5 documents to create a response. This means that if the key information is spread across 100 PDF files, the model will not be able to answer that prompt correctly.
   - The number of documents used to answer a given prompt can be adjusted on the left side of the UI. Accepted values are 1 to 5. For example if the goal is to compare 2 documents then it is recommended to set this number to 2.

### Best practices

- **Data Size**:
    - For the demo purposes, a few hundred pages of PDF files are more than enough.

- **Synthetic Data**:
    - If absolutely no data is available (not even financial statements from the client's website), the LLM will need to be run on synthetic data.
    - For this purpose, it is recommended to use ChatGPT to generate paragraphs of text that are used as PDF files.

- **Challenges with Prompts**:
    - Identifying prompts for the Document Search is a time consuming part of creating a demo.
    - It is recommended to use ChatGPT for prompt suggestions. It is recommended to even specify the difficulty of the prompts ("show me 10 easy, medium and difficult prompts").
    - It is expected that the developer will need to test >50 prompts to identify a handful (~3) that will be used in the client demo.
    - ChatGPT's prompts usually have a higher success rate, ensuring consistent plots and summaries compared to manually crafted ones.
    - It is highly recommended to test each prompt at least 3-5 times to ensure they always work and double check that the returned page does indeed contain the information from the model's response.

### Known Issues

- **Inconsistent Responses**:
    - The model might yield varied responses for the same prompts. Test each prompt a couple of times to check consistentcy.
    - The model may have difficulty identifying the units of certain values (such as dollar vs. millions of dollars).


### Known Issues

- **Choosing Score Threshold**:
    - The score threshold has to be manually fine tuned for the vector database retrieval.

# Project Notes
The most current list of known bugs and future enhancemenets live in the github [issues](https://github.com/Deloitte/SFL_IntDev_GenAI_Demo/issues).
### Repo Contents
```
.
├── LICENSE.md
├── README.md
├── config
│   └── config.toml
├── data
├── docker
│   ├── Dockerfile
│   └── installation_media
│       ├── install_base_deps.sh
│       └── requirements.txt
├── documentation
│   ├── docs
│   │   ├── index.md
│   │   └── reference.md
│   ├── gen_doc_stubs.py
│   └── mkdocs.yml
├── imgs
│   ├── deloitte_dot_logo.png
│   ├── fema1.png
│   ├── fema2.png
│   ├── logo.png
│   └── mock.png
├── logs
├── models
├── notebooks
├── prompts
│   └── subpage.json
├── pyproject.toml
├── scripts
│   ├── build_and_run.sh
│   ├── create_md.sh
│   ├── local_action.sh
│   ├── run_formatting.sh
│   ├── run_local_actions.sh
│   ├── run_similar_code_check.sh
│   └── start_j_lab.sh
└── src
    ├── defintions.py
    ├── genai_app.py
    ├── pages
    │   ├── Data_Insight.py
    │   ├── doc_search_and_summary.py
    │   ├── freeform_qa.py
    │   └── subpage.py
    └── utils.py
```



### Contacts 

- Point of Contact: Celia Ludwinski ([cludwinksi@deloitte.com](mailto:cludwinksi@deloitte.com))
- Technical Questions: Brendon Hall ([brehall@deloitte.com](mailto:brehall@deloitte.com))
- PMD Sponsor: Michael Luk ([miluk@deloitte.com](mailto:miluk@deloitte.com))

### License

[![CC-BY-ND](https://licensebuttons.net/l/by-nd/4.0/88x31.png)](https://creativecommons.org/licenses/by-nd/4.0/)

To the extent possible under the law, and under our agreements, SFL Scientific, a Deloitte Business retains all copyright and related or neighboring rights to this work.
