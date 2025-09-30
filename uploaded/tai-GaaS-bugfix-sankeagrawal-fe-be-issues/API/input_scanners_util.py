import logging
from llm_guard.vault import Vault
from llm_guard import scan_prompt
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

SCANNERS_LIST= ['Anonymize', 'BanSubstrings', 'BanTopics', 'Code', 'Language', 
                'PromptInjection', 'Regex', 'Secrets', 'Sentiment', 'TokenLimit', 'Toxicity']

logger= logging.getLogger()

class InputScannerUtil:

    def run_input_scanners(self, sanitized_prompt: str, scanner_configs: dict, fail_fast: bool):
        total_scanners= len(scanner_configs)
        current= 0
        results_valid= dict()
        results_score= dict()
        for scanner_name, scanner_params in scanner_configs.items():
            logger.info(f"Scanner Name: {scanner_name}\nScanner parameters: {scanner_params}")
            
            current+=1
            if scanner_params.get("enabled") == False:
                continue

            if scanner_name not in SCANNERS_LIST:
                logger.error(f"Unknown scanner name: {scanner_name}")
                raise ValueError(f"Unknown scanner name: {scanner_name}")
           
            try:
                if scanner_name.casefold() == "Anonymize".casefold():
                    scanner=self.Anonymize_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Code".casefold():
                    scanner=self.code_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Language".casefold():
                    scanner=self.language_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Secrets".casefold():
                    scanner=self.secrets_scanner(params=scanner_params)
                elif scanner_name.casefold() == "BanSubstrings".casefold():
                    scanner=self.BanSubstrings_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Toxicity".casefold():
                    scanner=self.toxicity_scanner(params=scanner_params)
                elif scanner_name.casefold() == "TokenLimit".casefold():
                    scanner=self.tokenLimit_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Sentiment".casefold():
                    scanner=self.sentiment_scanner(params=scanner_params)
                elif scanner_name.casefold() == "BanTopics".casefold():
                    scanner=self.BanTopics_scanner(params=scanner_params)
                elif scanner_name.casefold() == "PromptInjection".casefold():
                    scanner=self.promptInjection_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Regex".casefold():
                    scanner=self.regex_scanner(params=scanner_params)
            except Exception as error:
                e= f"An error occured: {error}"
                logger.error(e)
                raise RuntimeError(e)

            #keep updating sanitized prompt to be an input for the next scanner
            sanitized_prompt, is_valid, risk_score= scanner.scan(sanitized_prompt)

            results_valid[scanner_name]= is_valid
            results_score[scanner_name]= risk_score
            # result= {'sanitized_prompt': sanitized_prompt, 'results_valid': results_valid, 'results_score':results_score}
            result= {'sanitized_prompt': sanitized_prompt, 'results_valid': results_valid, 'results_score':results_score, 'is_valid': is_valid}
            
            if fail_fast and not is_valid:
                logger.error(f"Scanner {scanner_name} is_valid= {is_valid}. result: {result}" )
                return result
            
            logger.info(f"Scanner: {scanner_name}. Result: {result}")
            if current == total_scanners:
                return result
    

    def run_with_scan_prompt(self, prompt: str, scanner_configs: dict, fail_fast_flag: bool):
        input_scanner_list=[]
        for scanner_name, scanner_params in scanner_configs.items():
            logger.info(f"Scanner Name: {scanner_name}\nScanner parameters: {scanner_params}")
            
            if scanner_params.get("enabled") == False:
                continue

            if scanner_name not in SCANNERS_LIST:
                logger.error(f"Unknown scanner name: {scanner_name}")
                raise ValueError(f"Unknown scanner name: {scanner_name}")
           
            try:
                if scanner_name.casefold() == "Anonymize".casefold():
                    scanner=self.Anonymize_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "Code".casefold():
                    scanner=self.code_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "Language".casefold():
                    scanner=self.language_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "Secrets".casefold():
                    scanner=self.secrets_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "BanSubstrings".casefold():
                    scanner=self.BanSubstrings_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "Toxicity".casefold():
                    scanner=self.toxicity_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "TokenLimit".casefold():
                    scanner=self.tokenLimit_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "Sentiment".casefold():
                    scanner=self.sentiment_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "BanTopics".casefold():
                    scanner=self.BanTopics_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "PromptInjection".casefold():
                    scanner=self.promptInjection_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
                elif scanner_name.casefold() == "Regex".casefold():
                    scanner=self.regex_scanner(params=scanner_params)
                    input_scanner_list.append(scanner)
            except Exception as error:
                e= f"An error occured while running scanner ({scanner_name}): {error}"
                logger.error(e)
                raise RuntimeError(e)
            
        sanitized_prompt, results_valid, results_score = scan_prompt(input_scanner_list, prompt, fail_fast=fail_fast_flag)
        
        logger.info(f"Result:\n sanitized_prompt:{sanitized_prompt}\n results_valid: {results_valid}\
                    \nresults_score: {results_score}\n")
    
        return {"sanitized_prompt": sanitized_prompt, "results_valid": results_valid, 
                "results_score": results_score}

    

    def Anonymize_scanner(self, params : dict):
        entity_types= params.get("entity_types")
        hidden_names= params.get("hidden_names")
        allowed_names=params.get("allowed_names")
        preamble= params.get("preamble")
        use_faker= params.get("use_faker")
        threshold=params.get("threshold")
        vault= Vault()
        return Anonymize(vault=vault, entity_types=entity_types, hidden_names=hidden_names,allowed_names=allowed_names,
                         preamble=preamble, use_faker=use_faker, threshold=threshold)
    

    def code_scanner(self, params : dict):
        languages= params.get("languages")
        is_blocked= params.get("is_blocked")
        return Code(languages=languages, is_blocked=is_blocked)


    def language_scanner(self, params : dict):
        valid_languages= params.get("valid_languages")
        return Language(valid_languages=valid_languages)


    def secrets_scanner(self, params : dict):
        redact_mode= params.get("redact_mode")
        return Secrets(redact_mode=redact_mode)
        

    def sentiment_scanner(self, params : dict):
        threshold= params.get("threshold")
        return Sentiment(threshold=threshold)


    def BanSubstrings_scanner(self, params : dict):
        substrings= params.get("substrings")
        match_type= params.get("match_type")
        case_sensitive= params.get("case_sensitive")
        redact= params.get("redact")
        contains_all= params.get("contains_all")
        return BanSubstrings(substrings=substrings, match_type=match_type, case_sensitive=case_sensitive,
                                redact=redact, contains_all=contains_all)
    

    def BanTopics_scanner(self, params : dict):
        topics= params.get("topics")
        threshold= params.get("threshold")
        return BanTopics(topics=topics, threshold=threshold)
    
    
    def toxicity_scanner(self, params : dict):
        threshold= params.get("threshold")
        match_type= params.get("match_type")
        return Toxicity(threshold=threshold, match_type=match_type)
    

    def promptInjection_scanner(self, params : dict):
        threshold= params.get("threshold")
        return PromptInjection(threshold=threshold)
    

    def tokenLimit_scanner(self, params : dict):
        limit= params.get("limit")
        encoding_name= params.get("encoding_name")
        return TokenLimit(limit=limit, encoding_name=encoding_name)
    
   
    def regex_scanner(self, params : dict):
        patterns= params.get("patterns")
        match_type= params.get("match_type")
        is_blocked= params.get("is_blocked")
        redact= params.get("redact")
        return Regex(patterns=patterns, match_type=match_type, is_blocked=is_blocked, redact=redact)