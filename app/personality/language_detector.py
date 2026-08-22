from dataclasses import dataclass
ENGLISH_WORDS = {
    "the","is","are","you","what","where","when","why",
    "how","hello","thanks","please","this","that","and","but",
    "for","with","have","has","was","were",
}
ROMANIZED_HINDI_WORDS = {
    "kya","hai","haan","nahi","nahin","kaise","kaisa","kaisi","kyun",
    "kyon","mera","meri","mere","tum","tumhe","tumhara","aap","aapka",
    "kal","abhi","acha","achha","accha","bahut","mujhe","jana","aa","aana",
    "mujhse","tera","teri","tere","kar","karo","karna","ja","jaana"
}
@dataclass
class LanguageResult:
    language: str
    script: str
    confidence: float
class LanguageDetector:
    def detect(self, message):
        if not message or not message.strip():
            return LanguageResult(
                language="unknown",
                script="unknown",
                confidence=0.0
            )
        has_devnagari = any(
           "\u0900" <= character <= "\u097F"
            for character in message
        )
        if has_devnagari:
            return LanguageResult(
                language="hindi",
                script="devanagari",
                confidence=0.9
            )
        has_bengali = any(
            "\u0980" <= character <= "\u09FF"
            for character in message
        )
        if has_bengali:
            return LanguageResult(
                language="bengali",
                script="bengali",
                confidence=0.9
            )
        words = message.lower().split()
        hindi_matches = sum(
            word in ROMANIZED_HINDI_WORDS
            for word in words
        )
        if hindi_matches > 0:
            return LanguageResult(
                language="romanized_hindi",
                script="latin",
                confidence=0.8
            )
        words = message.lower().split()
        english_matches = sum(
            word in ENGLISH_WORDS
            for word in words 
        )
        if english_matches>0:
            return LanguageResult(
                language="english",
                script="latin",
                confidence=0.8
            )