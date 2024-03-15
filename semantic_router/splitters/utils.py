import regex
import spacy
import tiktoken


def split_to_sentences(text: str) -> list[str]:
    """
    Enhanced regex pattern to split a given text into sentences more accurately.

    The enhanced regex pattern includes handling for:
    - Direct speech and quotations.
    - Abbreviations, initials, and acronyms.
    - Decimal numbers and dates.
    - Ellipses and other punctuation marks used in informal text.
    - Removing control characters and format characters.

    Args:
        text (str): The text to split into sentences.

    Returns:
        list: A list of sentences extracted from the text.
    """
    regex_pattern = r"""
        # Negative lookbehind for word boundary, word char, dot, word char
        (?<!\b\w\.\w.)
        # Negative lookbehind for single uppercase initials like "A."
        (?<!\b[A-Z][a-z]\.)
        # Negative lookbehind for abbreviations like "U.S."
        (?<!\b[A-Z]\.)
        # Negative lookbehind for abbreviations with uppercase letters and dots
        (?<!\b\p{Lu}\.\p{Lu}.)
        # Negative lookbehind for numbers, to avoid splitting decimals
        (?<!\b\p{N}\.)
        # Positive lookbehind for punctuation followed by whitespace
        (?<=\.|\?|!|:|\.\.\.)\s+
        # Positive lookahead for uppercase letter or opening quote at word boundary
        (?="?(?=[A-Z])|"\b)
        # OR
        |
        # Splits after punctuation that follows closing punctuation, followed by
        # whitespace
        (?<=[\"\'\]\)\}][\.!?])\s+(?=[\"\'\(A-Z])
        # OR
        |
        # Splits after punctuation if not preceded by a period
        (?<=[^\.][\.!?])\s+(?=[A-Z])
        # OR
        |
        # Handles splitting after ellipses
        (?<=\.\.\.)\s+(?=[A-Z])
        # OR
        |
        # Matches and removes control characters and format characters
        [\p{Cc}\p{Cf}]+
    """
    sentences = regex.split(regex_pattern, text, flags=regex.VERBOSE)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences


def split_to_sentences_spacy(text: str) -> list[str]:
    """
    Use SpaCy to split a given text into sentences. Supported languages: English.

    Args:
        text (str): The text to split into sentences.

    Returns:
        list: A list of sentences extracted from the text.
    """ 
    nlp = spacy.load("en_core_web_sm") 
    doc = nlp(text)
    sentences = [sentence.text.strip() for sentence in doc.sents]
    return sentences

def check_and_download_spacy_model(model_name="en_core_web_sm"):
    """
    Checks if the specified SpaCy language model is installed, and if not, attempts to download and install it.

    Args:
    - model_name (str): The name of the SpaCy model to check and download. Defaults to 'en_core_web_sm'.

    """
    try:
        # Try loading the model to see if it's already installed
        spacy.load(model_name)
        print(f"Spacy model '{model_name}' is installed.")
    except OSError:
        print(f"Spacy model '{model_name}' not found, downloading...")
        from spacy.cli import download
        download(model_name)
        print(f"Downloaded and installed model '{model_name}'.")


def tiktoken_length(text: str) -> int:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)
