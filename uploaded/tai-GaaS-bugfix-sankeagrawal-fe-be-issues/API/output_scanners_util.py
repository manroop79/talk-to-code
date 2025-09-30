import logging
from llm_guard.vault import Vault
from llm_guard import scan_output
from llm_guard.output_scanners import (
    BanCompetitors,
    BanSubstrings,
    BanTopics,
    Bias,
    Code,
    Deanonymize,
    FactualConsistency,
    JSON,
    Language,
    LanguageSame,
    MaliciousURLs,
    NoRefusal,
    ReadingTime,
    Regex,
    Relevance,
    Sentiment,
    Toxicity,
    Sensitive,
    URLReachability
)

SCANNERS_LIST= ['BanCompetitors', 'BanSubstrings', 'BanTopics', 'Bias', 'Code', 'Deanonymize', 'Language', 
                 'Regex', 'Sentiment', 'FactualConsistency', 'Toxicity', 'JSON', 'LanguageSame',
                 'MaliciousURLs', 'NoRefusal', 'ReadingTime', 'Relevance', 'Sensitive',
                 'URLReachability']

logger= logging.getLogger()

class OutputScannerUtil:

    def run_output_scanners(self, sanitized_prompt: str, output: str, scanner_configs: dict, fail_fast: bool):
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
                if scanner_name.casefold() == "BanCompetitors".casefold():
                    scanner=self.BanCompetitors_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Code".casefold():
                    scanner=self.code_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Language".casefold():
                    scanner=self.language_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Deanonymize".casefold():
                    scanner=self.deanonymize_scanner(params=scanner_params)
                elif scanner_name.casefold() == "BanSubstrings".casefold():
                    scanner=self.BanSubstrings_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Toxicity".casefold():
                    scanner=self.toxicity_scanner(params=scanner_params)
                elif scanner_name.casefold() == "FactualConsistency".casefold():
                    scanner=self.factualConsistency_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Sentiment".casefold():
                    scanner=self.sentiment_scanner(params=scanner_params)
                elif scanner_name.casefold() == "BanTopics".casefold():
                    scanner=self.BanTopics_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Bias".casefold():
                    scanner=self.bias_scanner(params=scanner_params)
                elif scanner_name.casefold() == "Regex".casefold():
                    scanner=self.regex_scanner(params=scanner_params)
                elif scanner_name.casefold() == "JSON".casefold():
                    scanner=self.JSON_scanner(params=scanner_params)
                elif scanner_name.casefold() == "LanguageSame".casefold():
                    scanner=self.languageSame_scanner(params=scanner_params)
                elif scanner_name.casefold() == "MaliciousURLs".casefold():
                    scanner=self.maliciousURLs_scanner(params=scanner_params)
                elif scanner_name.casefold() == "NoRefusal".casefold():
                    scanner=self.noRefusal_scanner(params=scanner_params)
                elif scanner_name.casefold() == "ReadingTime".casefold():
                    scanner=self.readingTime_scanner(params=scanner_params)
                elif scanner_name.casefold == "Relevance".casefold():
                    scanner=self.relevance_scanner(params=scanner_params)
                elif scanner_name.casefold == "Sensitive".casefold():
                    scanner=self.sensitive_scanner(params=scanner_params)
                elif scanner_name.casefold == "URLReachability".casefold():
                    scanner=self.urlReachability_scanner(params=scanner_params)
            except Exception as error:
                e= f"An error occured while running scanner {scanner_name}: {error}"
                logger.error(e)
                raise RuntimeError(e)

            #keep updating output to be an input for the next scanner
            sanitized_prompt, is_valid, risk_score= scanner.scan(sanitized_prompt, output)
            
            results_valid[scanner_name]= is_valid
            results_score[scanner_name]= risk_score
            result= {'sanitized_response': output, 'results_valid': results_valid, 'results_score':results_score}

            if fail_fast and not is_valid:
                logger.error(f"Scanner {scanner_name} is_valid result= {is_valid}. result: {result}" )
                return result
            
            logger.info(f"Scanner: {scanner_name}. Result: {result}")
            if current == total_scanners:
                return result
    

    def run_with_scan_output(self, prompt: str, output: str, scanner_configs: dict, fail_fast_flag: bool):
        output_scanners_list=[]
        for scanner_name, scanner_params in scanner_configs.items():
            logger.info(f"Scanner Name: {scanner_name}\nScanner parameters: {scanner_params}")
            
            if scanner_params.get("enabled") == False:
                continue

            if scanner_name not in SCANNERS_LIST:
                logger.info(f"Unknown scanner name: {scanner_name}")
                raise ValueError(f"Unknown scanner name: {scanner_name}")
           
            try:
                if scanner_name.casefold() == "BanCompetitors".casefold():
                    scanner=self.BanCompetitors_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "Code".casefold():
                    scanner=self.code_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "Language".casefold():
                    scanner=self.language_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "Deanonymize".casefold():
                    scanner=self.deanonymize_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "BanSubstrings".casefold():
                    scanner=self.BanSubstrings_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "Toxicity".casefold():
                    scanner=self.toxicity_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "FactualConsistency".casefold():
                    scanner=self.factualConsistency_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "Sentiment".casefold():
                    scanner=self.sentiment_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "BanTopics".casefold():
                    scanner=self.BanTopics_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "Bias".casefold():
                    scanner=self.bias_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "Regex".casefold():
                    scanner=self.regex_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "JSON".casefold():
                    scanner=self.JSON_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "LanguageSame".casefold():
                    scanner=self.languageSame_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "MaliciousURLs".casefold():
                    scanner=self.maliciousURLs_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "NoRefusal".casefold():
                    scanner=self.noRefusal_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "ReadingTime".casefold():
                    scanner=self.readingTime_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "Relevance".casefold():
                    scanner=self.relevance_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
                elif scanner_name.casefold() == "URLReachability".casefold():
                    scanner=self.urlReachability_scanner(params=scanner_params)
                    output_scanners_list.append(scanner)
            except Exception as error:
                e= f"An error occured while running scanner ({scanner_name}): {error}"
                logger.error(e)
                raise RuntimeError(e)

        sanitized_response_text, results_valid, results_score = scan_output(scanners=output_scanners_list, prompt=prompt,
                                                                     output=output, fail_fast=fail_fast_flag)
        
        logger.info(f"Result:\n sanitized_response:{sanitized_response_text}\n results_valid: {results_valid}\
                    \nresults_score: {results_score}\n")

        return {"sanitized_response": sanitized_response_text, "results_valid": results_valid, 
                "results_score": results_score}

    
    def BanCompetitors_scanner(self, params : dict):
        competitor_list= params.get("competitors")
        redact= params.get("redact")
        threshold=params.get("threshold")
        return BanCompetitors(competitors=competitor_list, redact=redact, threshold=threshold) 

    def code_scanner(self, params : dict):
        languages= params.get("languages")
        is_blocked= params.get("is_blocked")
        return Code(languages=languages, is_blocked=is_blocked)

    def language_scanner(self, params : dict):
        valid_languages= params.get("valid_languages")
        return Language(valid_languages=valid_languages)

    def Deanonymize_scanner(self, params : dict):
        vault= Vault()
        return Deanonymize(vault=vault)
        
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
    
    def bias_scanner(self, params : dict):
        threshold= params.get("threshold")
        match_type= params.get("match_type")
        return Bias(threshold=threshold, match_type=match_type)

    def factualConsistency_scanner(self, params : dict):
        minimum_score= params.get("minimum_score")
        return FactualConsistency(minimum_score=minimum_score)
    
    def regex_scanner(self, params : dict):
        patterns= params.get("patterns")
        match_type= params.get("match_type")
        is_blocked= params.get("is_blocked")
        redact= params.get("redact")
        return Regex(patterns=patterns, match_type=match_type, is_blocked=is_blocked, redact=redact)
    
    def JSON_scanner(self, params : dict):
        required_elements= params.get("required_elements")
        return JSON(required_elements=required_elements)
    
    def languageSame_scanner(self, params : dict):
        return LanguageSame()
    
    def maliciousURLs_scanner(self, params: dict):
        threshold= params.get("threshold")
        return MaliciousURLs(threshold=threshold)
    
    def noRefusal_scanner(self, params: dict):
        threshold= params.get("threshold")
        return NoRefusal(threshold=threshold)
    
    def readingTime_scanner(self, params : dict):
        max_time= params.get("max_time")
        truncate= params.get("truncate")
        return ReadingTime(max_time=max_time, truncate=truncate)
    
    def relevance_scanner(self, params : dict):
        threshold= params.get("threshold")
        return Relevance(threshold=threshold)

    def sensitive_scanner(self, params : dict):
        entity_types= params.get("entity_types")
        redact= params.get("redact")
        return Sensitive(entity_types=entity_types, redact=redact)
    
    def urlReachability_scanner(self, params : dict):
        success_status_codes= params.get("success_status_codes")
        timeout= params.get("timeout")
        return URLReachability(success_status_codes=success_status_codes, timeout=timeout)