import React, {createContext, useReducer} from "react";

const Reducer = (state, action) => {
    switch(action.type) {
        case "prompt":
            return {...state, prompt: action.value}
        case "PROMPT_HELPERS":
            if (action.hasOwnProperty("is_valid")) {
                return {...state, prompt_helpers: {...state.prompt_helpers, is_valid: action.is_valid}}
            }
            if (action.hasOwnProperty("SanitizedPrompt")) {
                return {...state, prompt_helpers: {...state.prompt_helpers, SanitizedPrompt: action.SanitizedPrompt}}
            }
            if (action.hasOwnProperty("GeneratedText")) {
                return {...state, prompt_helpers: {...state.prompt_helpers, GeneratedText: action.GeneratedText}}
            }
            if (action.hasOwnProperty("InvalidPrompt")) {
                return {...state, prompt_helpers: {...state.prompt_helpers, InvalidPrompt: action.InvalidPrompt}}
            }
            break;
        case "ANONYMIZE":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Anonymize: {...state.Anonymize, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("entity_types")) {
                return {...state, Anonymize: {...state.Anonymize, entity_types: action.entity_types}}
            }
            if (action.hasOwnProperty("hidden_names")) {
                return {...state, Anonymize: {...state.Anonymize, hidden_names: action.hidden_names}}
            }
            if (action.hasOwnProperty("allowed_names")) {
                return {...state, Anonymize: {...state.Anonymize, allowed_names: action.allowed_names}}
            }
            if (action.hasOwnProperty("preamble")) {
                return {...state, Anonymize: {...state.Anonymize, preamble: action.preamble}}
            }
            if (action.hasOwnProperty("use_faker")) {
                return {...state, Anonymize: {...state.Anonymize, use_faker: action.use_faker}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, Anonymize: {...state.Anonymize, threshold: action.threshold}}
            }
            break;
        case "SECRETS":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Secrets: {...state.Secrets, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("redact_mode")) {
                return {...state, Secrets: {...state.Secrets, redact_mode: action.redact_mode}}
            }
            break;
        case "SENTIMENT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Sentiment: {...state.Sentiment, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, Sentiment: {...state.Sentiment, threshold: action.threshold}}
            }
            break;
        case "SENTIMENT_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Sentiment_OUTPUT: {...state.Sentiment_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, Sentiment_OUTPUT: {...state.Sentiment_OUTPUT, threshold: action.threshold}}
            }
            break;
        case "SUBSTRINGS":
            if (action.hasOwnProperty("enabled")) {
                return {...state, BanSubstrings: {...state.BanSubstrings, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("substrings")) {
                return {...state, BanSubstrings: {...state.BanSubstrings, substrings: action.substrings}}
            }
            if (action.hasOwnProperty("match_type")) {
                return {...state, BanSubstrings: {...state.BanSubstrings, match_type: action.match_type}}
            }
            if (action.hasOwnProperty("case_sensitive")) {
                return {...state, BanSubstrings: {...state.BanSubstrings, case_sensitive: action.case_sensitive}}
            }
            if (action.hasOwnProperty("redact")) {
                return {...state, BanSubstrings: {...state.BanSubstrings, redact: action.redact}}
            }
            if (action.hasOwnProperty("contains_all")) {
                return {...state, BanSubstrings: {...state.BanSubstrings, contains_all: action.contains_all}}
            }
            break;
        case "SUBSTRINGS_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, BanSubstrings_OUTPUT: {...state.BanSubstrings_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("substrings")) {
                return {...state, BanSubstrings_OUTPUT: {...state.BanSubstrings_OUTPUT, substrings: action.substrings}}
            }
            if (action.hasOwnProperty("match_type")) {
                return {...state, BanSubstrings_OUTPUT: {...state.BanSubstrings_OUTPUT, match_type: action.match_type}}
            }
            if (action.hasOwnProperty("case_sensitive")) {
                return {...state, BanSubstrings_OUTPUT: {...state.BanSubstrings_OUTPUT, case_sensitive: action.case_sensitive}}
            }
            if (action.hasOwnProperty("redact")) {
                return {...state, BanSubstrings_OUTPUT: {...state.BanSubstrings_OUTPUT, redact: action.redact}}
            }
            if (action.hasOwnProperty("contains_all")) {
                return {...state, BanSubstrings_OUTPUT: {...state.BanSubstrings_OUTPUT, contains_all: action.contains_all}}
            }
            break;
        case "TOPICS":
            if (action.hasOwnProperty("enabled")) {
                return {...state, BanTopics: {...state.BanTopics, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("topics")) {
                return {...state, BanTopics: {...state.BanTopics, topics: action.topics}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, BanTopics: {...state.BanTopics, threshold: action.threshold}}
            }
            break;
        case "TOPICS_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, BanTopics_OUTPUT: {...state.BanTopics_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("topics")) {
                return {...state, BanTopics_OUTPUT: {...state.BanTopics_OUTPUT, topics: action.topics}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, BanTopics_OUTPUT: {...state.BanTopics_OUTPUT, threshold: action.threshold}}
            }
            break;
        case "TOXICITY":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Toxicity: {...state.Toxicity, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, Toxicity: {...state.Toxicity, threshold: action.threshold}}
            }
            if (action.hasOwnProperty("match_type")) {
                return {...state, Toxicity: {...state.Toxicity, match_type: action.match_type}}
            }
            break;
        case "TOXICITY_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Toxicity_OUTPUT: {...state.Toxicity_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, Toxicity_OUTPUT: {...state.Toxicity_OUTPUT, threshold: action.threshold}}
            }
            if (action.hasOwnProperty("match_type")) {
                return {...state, Toxicity_OUTPUT: {...state.Toxicity_OUTPUT, match_type: action.match_type}}
            }
            break;
        case "TOKEN_LIMIT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, TokenLimit: {...state.TokenLimit, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("encoding_name")) {
                return {...state, TokenLimit: {...state.TokenLimit, encoding_name: action.encoding_name}}
            }
            if (action.hasOwnProperty("limit")) {
                return {...state, TokenLimit: {...state.TokenLimit, limit: action.value}}
            }
            break;
        case "CODE":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Code: {...state.Code, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("languages")) {
                return {...state, Code: {...state.Code, languages: action.languages}}
            }
            if (action.hasOwnProperty("is_blocked")) {
                return {...state, Code: {...state.Code, is_blocked: action.is_blocked}}
            }
            break;
        case "CODE_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Code_OUTPUT: {...state.Code_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("languages")) {
                return {...state, Code_OUTPUT: {...state.Code_OUTPUT, languages: action.languages}}
            }
            if (action.hasOwnProperty("is_blocked")) {
                return {...state, Code_OUTPUT: {...state.Code_OUTPUT, is_blocked: action.is_blocked}}
            }
            break;
        case "LANGUAGE":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Language: {...state.Language, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("valid_languages")) {
                return {...state, Language: {...state.Language, valid_languages: action.valid_languages}}
            }
            break;
        case "LANGUAGE_OUTPUT":
        if (action.hasOwnProperty("enabled")) {
            return {...state, Language_OUTPUT: {...state.Language_OUTPUT, enabled: action.enabled}}
        }
        if (action.hasOwnProperty("valid_languages")) {
            return {...state, Language_OUTPUT: {...state.Language_OUTPUT, valid_languages: action.valid_languages}}
        }
        break;
        case "PROMPT_INJECTION":
            if (action.hasOwnProperty("enabled")) {
                return {...state, PromptInjection: {...state.PromptInjection, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, PromptInjection: {...state.PromptInjection, threshold: action.threshold}}
            }
            break;
        case "REGEX":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Regex: {...state.Regex, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("patterns")) {
                return {...state, Regex: {...state.Regex, patterns: action.patterns}}
            }
            if (action.hasOwnProperty("match_type")) {
                return {...state, Regex: {...state.Regex, match_type: action.match_type}}
            }
            if (action.hasOwnProperty("is_blocked")) {
                return {...state, Regex: {...state.Regex, is_blocked: action.is_blocked}}
            }
            if (action.hasOwnProperty("redact")) {
                return {...state, Regex: {...state.Regex, redact: action.redact}}
            }
            break;
        case "REGEX_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Regex_OUTPUT: {...state.Regex_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("patterns")) {
                return {...state, Regex_OUTPUT: {...state.Regex_OUTPUT, patterns: action.patterns}}
            }
            if (action.hasOwnProperty("match_type")) {
                return {...state, Regex_OUTPUT: {...state.Regex_OUTPUT, match_type: action.match_type}}
            }
            if (action.hasOwnProperty("is_blocked")) {
                return {...state, Regex_OUTPUT: {...state.Regex_OUTPUT, is_blocked: action.is_blocked}}
            }
            if (action.hasOwnProperty("redact")) {
                return {...state, Regex_OUTPUT: {...state.Regex_OUTPUT, redact: action.redact}}
            }
            break;
        case "BIAS_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Bias_OUTPUT: {...state.Bias_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, Bias_OUTPUT: {...state.Bias_OUTPUT, threshold: action.threshold}}
            }
            if (action.hasOwnProperty("match_type")) {
                return {...state, Bias_OUTPUT: {...state.Bias_OUTPUT, match_type: action.match_type}}
            }
            break;
        case "DEANONYMIZE_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Deanonymize_OUTPUT: {...state.Deanonymize_OUTPUT, enabled: action.enabled}}
            }
            break;
        case "FactualConsistency_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, FactualConsistency_OUTPUT: {...state.FactualConsistency_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, FactualConsistency_OUTPUT: {...state.FactualConsistency_OUTPUT, threshold: action.threshold}}
            }
            break;
        case "ReadingTime_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, ReadingTime_OUTPUT: {...state.ReadingTime_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("max_time")) {
                return {...state, ReadingTime_OUTPUT: {...state.ReadingTime_OUTPUT, max_time: action.max_time}}
            }
            if (action.hasOwnProperty("truncate")) {
                return {...state, ReadingTime_OUTPUT: {...state.ReadingTime_OUTPUT, truncate: action.truncate}}
            }
            break;
        case "Relevance_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Relevance_OUTPUT: {...state.Relevance_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, Relevance_OUTPUT: {...state.Relevance_OUTPUT, threshold: action.threshold}}
            }
            break;
        case "LanguageSame_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, LanguageSame_OUTPUT: {...state.LanguageSame_OUTPUT, enabled: action.enabled}}
            }
            break;
        case "MaliciousURLs_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, MaliciousURLs_OUTPUT: {...state.MaliciousURLs_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, MaliciousURLs_OUTPUT: {...state.MaliciousURLs_OUTPUT, threshold: action.threshold}}
            }
            break;
        case "NoRefusal_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, NoRefusal_OUTPUT: {...state.NoRefusal_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("threshold")) {
                return {...state, NoRefusal_OUTPUT: {...state.NoRefusal_OUTPUT, threshold: action.threshold}}
            }
            break;
        case "URLReachability_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, URLReachability_OUTPUT: {...state.URLReachability_OUTPUT, enabled: action.enabled}}
            }
            break;
        case "Sensitive_OUTPUT":
            if (action.hasOwnProperty("enabled")) {
                return {...state, Sensitive_OUTPUT: {...state.Sensitive_OUTPUT, enabled: action.enabled}}
            }
            if (action.hasOwnProperty("entity_types")) {
                return {...state, Sensitive_OUTPUT: {...state.Sensitive_OUTPUT, entity_types: action.entity_types}}
            }
            if (action.hasOwnProperty("redact")) {
                return {...state, Sensitive_OUTPUT: {...state.Sensitive_OUTPUT, redact: action.redact}}
            }
            break;
        default:
            console.log("hitting the default case");
            return state;
    };
};

const initialState = {
    prompt_helpers: {is_valid: true, SanitizedPrompt: "", GeneratedText: "", InvalidPrompt: false},
    prompt: "",
    fail_fast: true,
    Anonymize: {enabled: false, entity_types: [], hidden_names: [], allowed_names: [], preamble: "", use_faker: false, threshold: 0},
    BanSubstrings: {enabled: false, substrings: ["Test", "Hello"], match_type: "str", case_sensitive: false, redact: false, contains_all: false},
    BanTopics: {enabled: false, topics: ["violence"], threshold: 0.60},
    Code: {enabled: false, languages: [], is_blocked: true},
    Language: {enabled: false, valid_languages: ["en"]},
    PromptInjection: {enabled: false, threshold: 0.75},
    Regex: {enabled: false, patterns: ["Bearer1 [A-Za-z0-9-._~+/]+"], match_type: "search", is_blocked: true, redact: false},
    Secrets: {enabled: false, redact_mode: "all"},
    Sentiment: {enabled: false, threshold: 0},
    TokenLimit: {enabled: false, encoding_name: "cl100k_base", limit: 1000},
    Toxicity: {enabled: false, threshold: 0.75, match_type: "full"},
    BanSubstrings_OUTPUT: {enabled: false, substrings: ["Test", "Hello", "World"], match_type: "str", case_sensitive: false, redact: false, contains_all: false},
    BanTopics_OUTPUT: {enabled: false, topics: ["violence"], threshold: 0.60},
    Bias_OUTPUT: {enabled: false, threshold: 0.50, match_type: "full"},
    Code_OUTPUT: {enabled: false, languages: [], is_blocked: true},
    Deanonymize_OUTPUT: {enabled: false},
    FactualConsistency_OUTPUT: {enabled: false, threshold: 0.50},
    Language_OUTPUT: {enabled: false, valid_languages: ["en"]},
    LanguageSame_OUTPUT: {enabled: false},
    MaliciousURLs_OUTPUT: {enabled: false, threshold: 0.50},
    NoRefusal_OUTPUT: {enabled: false, threshold: 0.50},
    Regex_OUTPUT: {enabled: false, patterns: ["Bearer2 [A-Za-z0-9-._~+/]+"], match_type: "search", is_blocked: true, redact: false},
    Relevance_OUTPUT: {enabled: false, threshold: 0.50},
    ReadingTime_OUTPUT: {enabled: false, max_time: 5, truncate: true},
    Sensitive_OUTPUT: {enabled: false, entity_types: ["US_SSN"], redact: false},
    Sentiment_OUTPUT: {enabled: false, threshold: 0},
    Toxicity_OUTPUT: {enabled: false, threshold: 0.50, match_type: "full"},
    URLReachability_OUTPUT: {enabled: false, success_status_codes: [200, 201, 202, 301, 302], timeout: 5},
};

const Store = ({children}) => {
    const [globalState, globalDispatch] = useReducer(Reducer, initialState);
    return (
        <Context.Provider value={[globalState, globalDispatch]}>{children}</Context.Provider>
    )
};
export const Context = createContext(initialState);
export default Store;