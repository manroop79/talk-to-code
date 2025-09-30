from typing import Dict, Optional

from pydantic import BaseModel, Field


class Anonymize(BaseModel):
    enabled: bool
    entity_types: list[str]
    hidden_names: list[str]
    allowed_names: list[str]
    preamble: str
    use_faker: bool
    threshold: float

class Deanonymize(BaseModel):
    enabled: float

class BanCompetitors(BaseModel):
    enabled: bool
    competitors: list[str]
    redact: bool
    threshold: float

class Bias(BaseModel):
    enabled: bool
    threshold: float
    match_type: str

class FactualConsistency(BaseModel):
    enabled: bool
    minimum_score: float

class Json(BaseModel):
    enabled: bool
    required_elements: int

class Code(BaseModel):
    enabled: bool
    languages: list[str]
    is_blocked: bool

class Language(BaseModel):
    enabled: bool
    valid_languages: list[str]

class LanguageSame(BaseModel):
    enabled: bool

class MaliciousURLs(BaseModel):
    enabled: bool
    threshold: float

class NoRefusal(BaseModel):
    enabled: bool
    threshold: float

class ReadingTime(BaseModel):
    enabled: bool
    max_time: float
    truncate: bool

class Relevance(BaseModel):
    enabled: bool
    threshold: float

class BanSubstrings(BaseModel):
    enabled: bool
    substrings: list[str]
    match_type: str
    case_sensitive: bool
    redact: bool
    contains_all: bool

class Secrets(BaseModel):
    enabled: bool
    redact_mode: str

class Sensitive(BaseModel):
    enabled: bool
    entity_types : list[str]
    redact : bool

class Sentiment(BaseModel):
    enabled: bool
    threshold: float

class Toxicity(BaseModel):
    enabled: bool
    threshold: float
    match_type: str

class URLReachability(BaseModel):
    enabled: bool
    success_status_codes: list[int]
    timeout: int

class TokenLimit(BaseModel):
    enabled: bool
    limit: int
    encoding_name: str 
    
class BanTopics(BaseModel):
    enabled: bool
    topics: list
    threshold: float

class PromptInjection(BaseModel):
    enabled: bool
    threshold: float
    
class Regex(BaseModel):
    enabled: bool
    patterns: list[str]
    match_type: str
    is_blocked: bool
    redact: bool

class InputScannerConfigs(BaseModel):
    Anonymize: Anonymize
    Secrets: Secrets
    Sentiment: Sentiment
    BanSubstrings: BanSubstrings
    BanTopics: BanTopics
    Toxicity: Toxicity
    TokenLimit: TokenLimit
    Code: Code
    Language: Language
    PromptInjection: PromptInjection
    Regex: Regex
    
class InputScannerRequest(BaseModel):
    prompt: str
    fail_fast: bool = True
    scanner_configs: InputScannerConfigs

class OutputScannerConfigs(BaseModel):
    BanCompetitors: BanCompetitors
    BanSubstrings: BanSubstrings
    BanTopics: BanTopics
    Bias: Bias
    Code: Code
    Deanonymize: Deanonymize
    FactualConsistency: FactualConsistency
    JSON: Json
    Language: Language
    LanguageSame: LanguageSame
    MaliciousURLs: MaliciousURLs
    NoRefusal: NoRefusal
    ReadingTime: ReadingTime
    Regex: Regex
    Relevance: Relevance
    Sensitive: Sensitive
    Sentiment: Sentiment
    Toxicity: Toxicity
    URLReachability: URLReachability

class OutputScannerRequest(BaseModel):
    prompt: str
    output: str
    fail_fast: bool = True
    scanner_configs: OutputScannerConfigs