import logging
import re
from typing import Dict, List

import streamlit as st
from llm_guard.input_scanners import (
    Anonymize,
    BanSubstrings,
    BanTopics,
    Code,
    Language,
    PromptInjection,
    Regex,
    Secrets,
    Sentiment,
    TokenLimit,
    Toxicity,
)
from llm_guard.input_scanners.anonymize import default_entity_types
# from llm_guard.input_scanners.anonymize_helpers.analyzer import (
#     RECOGNIZER_SPACY_EN_PII_DISTILBERT,
#     RECOGNIZER_SPACY_EN_PII_FAST,
# )
from llm_guard.vault import Vault
from streamlit_tags import st_tags

LANGUAGES = ["af", "ar", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en",
"es", "et", "fa", "fi", "fr", "gu", "he", "hi", "hr", "hu", "id",
"it", "ja", "kn", "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl",
"no", "pa", "pl", "pt", "ro", "ru", "sk", "sl", "so", "sq", "sv",
"sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi", "zh-cn",
"zh-tw"]

INPUT_FILTERS = {
    "Privacy": {
        "Anonymize": """The Anonymize Scanner acts as your digital
                    guardian, ensuring your user prompts remain confidential
                    and free from sensitive data exposure.""",
        "Secrets": """This scanner diligently examines user inputs,
                        ensuring that they don't carry any secrets before they
                        are processed by the language model.""",
    },
    "Fair & Impartial": {
        "Sentiment": """It scans and evaluates the overall sentiment of
                    prompts using the SentimentIntensityAnalyzer from the
                    NLTK (Natural Language Toolkit) library.""",
    },
    "Responsible": {
        "BanSubStrings": """Ensure that specific undesired substrings never
                    make it into your prompts with the BanSubstrings
                    scanner.""",
        "BanTopics": """It is a proactive tool aimed at restricting
                        specific topics, such as religion, from being introduced
                        in the prompts. This ensures that interactions remain
                        within acceptable boundaries and avoids potentially
                        sensitive or controversial discussions.""",
        "Toxicity": """It provides a mechanism to analyze and gauge the
                        toxicity of prompt, assisting in maintaining the health
                        and safety of online interactions by preventing the
                        dissemination of potentially harmful content.""",
    },
    "Robust & Reliable": {
        "TokenLimit": """It ensures that prompts do not exceed a
                    predetermined token count, helping prevent
                    resource-intensive operations and potential denial of
                    service attacks on large language models (LLMs).""",
    },
    "Safe & Secure": {
        "Code": """It is specifically engineered to inspect user
                    prompts and discern if they contain code snippets.
                    It can be particularly useful in platforms that wish to
                    control or monitor the types of programming-related
                    content being queried or in ensuring the appropriate
                    handling of such prompts.""",
        "Language": """This scanner identifies and assesses the
                        authenticity of the language used in prompts.""",
        "PromptInjection": """It is specifically tailored to guard against
                        crafty input manipulations targeting large language models
                        (LLM). By identifying and mitigating such attempts,
                        it ensures the LLM operates securely without succumbing
                        to injection attacks.""",
        "Regex": """This scanner designed to scrutinize the prompt
                        based on predefined regular expression patterns. With the
                        capability to define desirable ("good") or undesirable
                        ("bad") patterns, users can fine-tune the validation of
                        prompts."""
    }
}

ANONYMIZE_SUGGESTIONS = default_entity_types + ["DATE_TIME", "NRP", "LOCATION", "MEDICAL_LICENSE", "US_PASSPORT"]

logger = logging.getLogger("llm-guard-playground")


def camel2snake(name: str):
    """convert camel case to snake case

    Args:
        name (str): name to convert

    Returns:
        str: output in snake case
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class TrustworthyControls():
    """Class for managing trustworthy controls."""

    def __init__(self):
        """ Initialize the controls object.
        """
        self.settings = {}

    def make_anonymize_controls(self):
        """Create the controls for the Anonymize input prompt filter."""
        st_settings = {}
        st_anon_expander = st.expander(
            "Anonymize",
            expanded=False,
        )

        with st_anon_expander:
            st_settings["entity_types"] = st_tags(
                label="Anonymize entities", text="Type and press enter",
                value=default_entity_types, suggestions=ANONYMIZE_SUGGESTIONS,
                maxtags=30, key="anon_entity_types",
            )
            st.caption(
                "Check all supported entities: https://microsoft.github.io/presidio/supported_entities/#list-of-supported-entities"
            )
            st_settings["hidden_names"] = st_tags(
                label="Hidden names to be anonymized", text="Type and press enter",
                value=[], suggestions=[],
                maxtags=30, key="anon_hidden_names",
            )
            st.caption("These names will be hidden e.g. [REDACTED_CUSTOM1].")
            st_settings["allowed_names"] = st_tags(
                label="Allowed names to ignore", text="Type and press enter",
                value=[], suggestions=[], maxtags=30, key="anon_allowed_names",
            )
            st.caption("These names will be ignored even if flagged by the detector.")
            st_settings["preamble"] = st.text_input(
                "Preamble", value=""
            )
            st_settings["use_faker"] = st.checkbox(
                "Use Faker", value=False, help="Use Faker library to generate fake data"
            )
            st_settings["threshold"] = st.slider(
                label="Threshold", value=0.0, min_value=0.0, max_value=1.0,
                step=0.1, key="anon_threshold",
            )
            # st_settings["recognizer"] = st.selectbox(
            #     "Recognizer",
            #     [RECOGNIZER_SPACY_EN_PII_DISTILBERT, RECOGNIZER_SPACY_EN_PII_FAST],
            #     index=1,
            # )
        self.settings["Anonymize"] = st_settings

    def make_ban_sub_strings_controls(self):
        """ Create the controls for the ban substrings filter.
        """
        st_bs_expander = st.expander(
            "Ban Substrings",
            expanded=False,
        )

        with st_bs_expander:
            st_bs_substrings = st.text_area(
                "Enter substrings to ban (one per line)",
                value="test\nhello\nworld",
                height=200,
            ).split("\n")

            st_bs_match_type = st.selectbox("Match type", ["str", "word"])
            st_bs_case_sensitive = st.checkbox("Case sensitive", value=False)
            st_bs_redact = st.checkbox("Redact", value=False)
            st_bs_contains_all = st.checkbox("Contains all", value=False)

        self.settings["BanSubStrings"] = {
            "substrings": st_bs_substrings,
            "match_type": st_bs_match_type,
            "case_sensitive": st_bs_case_sensitive,
            "redact": st_bs_redact,
            "contains_all": st_bs_contains_all,
        }

    def make_ban_topics_controls(self):
        """Create the controls for the ban substrings filter.
        """
        st_bt_expander = st.expander(
            "Ban Topics",
            expanded=False,
        )

        with st_bt_expander:
            st_bt_topics = st_tags(
                label="List of topics",
                text="Type and press enter",
                value=["violence"],
                suggestions=[],
                maxtags=30,
                key="bt_topics",
            )

            st_bt_threshold = st.slider(
                label="Threshold",
                value=0.6,
                min_value=0.0,
                max_value=1.0,
                step=0.05,
                key="ban_topics_threshold",
            )

        self.settings["BanTopics"] = {
            "topics": st_bt_topics,
            "threshold": st_bt_threshold,
        }

    def make_code_controls(self):
        """Create the controls for the code controls filter.
        """
        st_cd_expander = st.expander(
            "Code",
            expanded=False,
        )

        with st_cd_expander:
            st_cd_languages = st.multiselect(
                "Programming languages",
                ["python", "java", "javascript", "go", "php", "ruby"],
                default=["python"],
            )

            st_cd_mode = st.selectbox("Mode", ["allowed", "denied"], index=0)

        self.settings["Code"] = {
            "languages": st_cd_languages,
            "mode": st_cd_mode,
        }

    def make_language_controls(self):
        """Create the controls for the language filter
        """
        st_lan_expander = st.expander(
            "Language",
            expanded=False,
        )

        with st_lan_expander:
            st_lan_valid_language = st.multiselect(
                "Languages",
                LANGUAGES,
                default=["en"],
            )

        self.settings["Language"] = {
            "valid_languages": st_lan_valid_language,
        }

    def make_prompt_injection_controls(self):
        """Create the controls for the prompt injection filter
        """
        st_pi_expander = st.expander(
            "Prompt Injection",
            expanded=False,
        )

        with st_pi_expander:
            st_pi_threshold = st.slider(
                label="Threshold",
                value=0.75,
                min_value=0.0,
                max_value=1.0,
                step=0.05,
                key="prompt_injection_threshold",
            )

        self.settings["PromptInjection"] = {
            "threshold": st_pi_threshold,
        }

    def make_regex_controls(self):
        """create the controls for the regex filter"""
        st_regex_expander = st.expander(
            "Regex",
            expanded=False,
        )

        with st_regex_expander:
            st_regex_patterns = st.text_area(
                "Enter patterns to ban (one per line)",
                value="Bearer [A-Za-z0-9-._~+/]+",
                height=200,
            ).split("\n")

            st_regex_type = st.selectbox(
                "Match type",
                ["good", "bad"],
                index=1,
                help="good: allow only good patterns, bad: ban bad patterns",
            )

            st_redact = st.checkbox(
                "Redact", value=False, help="Replace the matched bad patterns with [REDACTED]"
            )

        self.settings["Regex"] = {
            "patterns": st_regex_patterns,
            "type": st_regex_type,
            "redact": st_redact,
        }

    def make_secrets_controls(self):
        """Create the controsl for the secrets filter
        """
        st_sec_expander = st.expander(
            "Secrets",
            expanded=False,
        )

        with st_sec_expander:
            st_sec_redact_mode = st.selectbox("Redact mode", ["all", "partial", "hash"])

        self.settings["Secrets"] = {
            "redact_mode": st_sec_redact_mode,
        }

    def make_sentiment_controls(self):
        """Create the controls for the sentiment filter"""
        st_sent_expander = st.expander(
            "Sentiment",
            expanded=False,
        )

        with st_sent_expander:
            st_sent_threshold = st.slider(
                label="Threshold",
                value=-0.1,
                min_value=-1.0,
                max_value=1.0,
                step=0.1,
                key="sentiment_threshold",
                help="Negative values are negative sentiment, positive values are positive sentiment",
            )

        self.settings["Sentiment"] = {
            "threshold": st_sent_threshold,
        }

    def make_token_limit_controls(self):
        """Create the controls for the limit filter"""
        st_tl_expander = st.expander(
            "Token Limit",
            expanded=False,
        )

        with st_tl_expander:
            st_tl_limit = st.number_input(
                "Limit", value=4096, min_value=0, max_value=10000, step=10
            )
            st_tl_encoding_name = st.selectbox(
                "Encoding name",
                ["cl100k_base", "p50k_base", "r50k_base"],
                index=0,
                help="Read more: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb",
            )

        self.settings["TokenLimit"] = {
            "limit": st_tl_limit,
            "encoding_name": st_tl_encoding_name,
        }

    def make_toxicity_controls(self):
        """Create the controls for the toxicity filter
        """
        st_tox_expander = st.expander(
            "Toxicity",
            expanded=False,
        )

        with st_tox_expander:
            st_tox_threshold = st.slider(
                label="Threshold",
                value=0.75,
                min_value=0.0,
                max_value=1.0,
                step=0.05,
                key="toxicity_threshold",
            )

        self.settings["Toxicity"] = {
            "threshold": st_tox_threshold,
        }

    def get_settings(self, setting: str) -> dict:
        """Return the group of configuration options corresponding to a given
        setting

        Args:
            setting (str): key of the filter

        Returns:
            dict: dict of the corresponding filter setting values
        """

        return self.settings[setting]

    def create_filter_settings_ui(self, filter_name: str):
        """ Create the appropriate ui based on the filter name.  Enables this
        creation function to be called in a loop.

        Args:
            filter_name (str): name of filter ui to create

        Raises:
            Exception: if filter name not found
        """
        function_name = f"make_{camel2snake(filter_name)}_controls"

        # get the function object from the object namespace
        if hasattr(self, function_name):
            create_settings = getattr(self, function_name)
            create_settings()
        else:
            raise Exception(f"Error, filter {filter_name} not found.")


def get_scanner(scanner_name: str, vault: Vault, settings: Dict):
    """Return configured scanner based on input string key

    Args:
        scanner_name (str): key of the scanner to config
        vault (Vault): vault object
        settings (Dict): setting values from the UI

    Raises:
        ValueError: if scanner name is unknown

    Returns:
        Scanner: configured scanner of the proper type
    """
    logger.debug(f"Initializing {scanner_name} scanner")

    if scanner_name == "Anonymize":
        return Anonymize(
            vault=vault,
            **settings
        )

    if scanner_name == "BanSubstrings":
        return BanSubstrings(**settings)

    if scanner_name == "BanTopics":
        return BanTopics(**settings)

    if scanner_name == "Code":
        mode = settings["mode"]

        allowed_languages = None
        denied_languages = None
        if mode == "allowed":
            allowed_languages = settings["languages"]
        elif mode == "denied":
            denied_languages = settings["languages"]

        return Code(allowed=allowed_languages, denied=denied_languages)

    if scanner_name == "Language":
        return Language(valid_languages=settings["valid_languages"])

    if scanner_name == "PromptInjection":
        return PromptInjection(threshold=settings["threshold"])

    if scanner_name == "Regex":
        match_type = settings["type"]

        good_patterns = None
        bad_patterns = None
        if match_type == "good":
            good_patterns = settings["patterns"]
        elif match_type == "bad":
            bad_patterns = settings["patterns"]

        return Regex(
            good_patterns=good_patterns, bad_patterns=bad_patterns, redact=settings["redact"]
        )

    if scanner_name == "Secrets":
        return Secrets(redact_mode=settings["redact_mode"])

    if scanner_name == "Sentiment":
        return Sentiment(threshold=settings["threshold"])

    if scanner_name == "TokenLimit":
        return TokenLimit(**settings["limit"])

    if scanner_name == "Toxicity":
        return Toxicity(threshold=settings["threshold"])

    raise ValueError("Unknown scanner name")


def scan_without_ui(
        vault: Vault, enabled_scanners: List[str], settings: Dict, text: str, fail_fast: bool = False
) -> (str, Dict[str, bool], Dict[str, float]):
    """Apply filters to the given input prompt

    Args:
        vault (Vault): vault object?
        enabled_scanners (List): list of enabled scanners
        settings (dict): config settings for filters
        text (str): the text to be analyzed
        fail_fast (bool): whether to quit  once one filter fails

    Returns:
        tuple: sanitized promt, flag if results are value, the risk scores
    """
    sanitized_prompt = text
    results_valid = {}
    results_score = {}

    for scanner_name in enabled_scanners:
        scanner = get_scanner(scanner_name, vault, settings[scanner_name])
        sanitized_prompt, is_valid, risk_score = scanner.scan(sanitized_prompt)
        results_valid[scanner_name] = is_valid
        results_score[scanner_name] = risk_score

        if fail_fast and not is_valid:
            break

    return sanitized_prompt, results_valid, results_score


def setup_trustworthy_controls():
    """ setup the trustworthy control interface
    """
    settings = {}
    enabled_scanners = []

    if "tai_controls" not in st.session_state:
        tai_controls = TrustworthyControls()
    else:
        tai_controls = st.session_state.tai_controls

    st.markdown('### Prompt Filters')

    for filter_topic in INPUT_FILTERS.keys():
        st.markdown(f'<span style="color:#87bc1f;">{filter_topic}</span>', unsafe_allow_html=True)
        topic_filters = INPUT_FILTERS[filter_topic]
        for filter_name in topic_filters.keys():
            with st.container():
                col1, col2, col3 = st.columns([1, 15, 1])
                if col1.toggle(f"Enable {filter_name}", label_visibility="collapsed"):
                    enabled_scanners.append(filter_name)
                with col2:
                    tai_controls.create_filter_settings_ui(filter_name)
                    settings[filter_name] = tai_controls.get_settings(filter_name)
                col3.markdown("", help=topic_filters[filter_name])

    st.session_state.enabled_scanners = enabled_scanners
    st.session_state.settings = settings
    st.session_state.tai_controls = tai_controls
