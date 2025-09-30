import React from "react";
import { Typography } from "@mui/material";
import SecretsFilter from "./Filters/SecretsFilter";
import SentimentFilter from "./Filters/SentimentFilter";
import ToxicityFilter from "./Filters/ToxicityFilter";
import AnonymizeFilter from "./Filters/AnonymizeFilter";
import BanSubstringsFilter from "./Filters/BanSubstringsFilter";
import BanTopicsFilter from "./Filters/BanTopicsFilter";
import TokenLimitFilter from "./Filters/TokenLimitFilter";
import CodeFilter from "./Filters/CodeFilter";
import LanguageFilter from "./Filters/LanguageFilter";
import PromptInjectionFilter from "./Filters/PromptInjectionFilter";
import RegexFilter from "./Filters/RegexFilter";

export default function InputScanners(props) {
    const {CurrentPage} = props;

    return (
        <div>
            <Typography variant="h4">Input Scanners</Typography>
            <Typography variant="h6" color="#87BC1F">Privacy</Typography>
            <AnonymizeFilter filterName="Anonymize" helperText="The Anonymize Scanner acts as your digital guardian, ensuring your user prompts remain confidential and free from sensitive data exposure."/>
            <SecretsFilter filterName="Secrets" helperText="This scanner diligently examines user inputs, ensuring that they don't carry any secrets before they are processed by the language model."/>
            <Typography variant="h6" color="#87BC1F">Fair & Impartial</Typography>
            <SentimentFilter CurrentPage={CurrentPage} filterName="Sentiment" helperText="It scans and evaluates the overall sentiment of prompts using the SentimentIntensityAnalyzer from the NLTK (Natural Language Toolkit) library."/>
            <Typography variant="h6" color="#87BC1F">Responsible</Typography>
            <BanSubstringsFilter CurrentPage={CurrentPage} filterName="Ban Substrings" helperText="Ensure that specific undesired substrings never make it into your prompts with the BanSubstrings scanner."/>
            <BanTopicsFilter CurrentPage={CurrentPage} filterName="Ban Topics" helperText="It is a proactive tool aimed at restricting specific topics, such as religion, from being introduced in the prompts. This ensures that interactions remain within acceptable boundaries and avoids potentially sensitive or controversial discussions."/>
            <ToxicityFilter CurrentPage={CurrentPage} filterName="Toxicity" helperText="It provides a mechanism to analyze and gauge the toxicity of prompt, assisting in maintaining the health and safety of online interactions by preventing the dissemination of potentially harmful content."/>
            <Typography variant="h6" color="#87BC1F">Robust & Reliable</Typography>
            <TokenLimitFilter filterName="Token Limit" helperText="It ensures that prompts do not exceed a predetermined token count, helping prevent resource-intensive operations and potential denial of service attacks on large language models (LLMs)."/>
            <Typography variant="h6" color="#87BC1F">Safe & Secure</Typography>
            <CodeFilter CurrentPage={CurrentPage} filterName="Code" helperText="It is specifically engineered to inspect user prompts and discern if they contain code snippets. It can be particularly useful in platforms that wish to control or monitor the types of programming-related content being queried or in ensuring the appropriate handling of such prompts."/>
            <LanguageFilter CurrentPage={CurrentPage} filterName="Language" helperText="This scanner identifies and assesses the authenticity of the language used in prompts."/>
            <PromptInjectionFilter filterName="Prompt Injection" helperText="It is specifically tailored to guard against crafty input manipulations targeting large language models (LLM). By identifying and mitigating such attempts, it ensures the LLM operates securely without succumbing to injection attacks."/>
            <RegexFilter CurrentPage={CurrentPage} filterName="Regex" helperText={"This scanner designed to scrutinize the prompt based on predefined regular expression patterns. With the capability to define desirable (\"good\") or undesirable (\"bad\") patterns, users can fine-tune the validation of prompts."}/>
        </div>
    );
}