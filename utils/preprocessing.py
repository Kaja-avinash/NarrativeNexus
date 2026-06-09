import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources safely
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet", quiet=True)

try:
    nltk.data.find("corpora/omw-1.4")
except LookupError:
    nltk.download("omw-1.4", quiet=True)

# Initialize resources
STOP = set(stopwords.words("english"))
LEM = WordNetLemmatizer()


def preprocess_text(text):
    """
    Clean and preprocess text for NLP tasks.
    """

    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    try:
        tokens = nltk.word_tokenize(text)
    except LookupError:
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
        tokens = nltk.word_tokenize(text)

    processed_tokens = []

    for token in tokens:
        if token not in STOP and len(token) > 2:
            processed_tokens.append(LEM.lemmatize(token))

    return " ".join(processed_tokens)


def preprocess_documents(documents):
    """
    Preprocess multiple documents.
    """

    if not documents:
        return []

    return [preprocess_text(doc) for doc in documents]


def get_word_count(text):
    """
    Return word count.
    """

    if not text:
        return 0

    return len(text.split())


def get_unique_word_count(text):
    """
    Return unique word count.
    """

    if not text:
        return 0

    return len(set(text.split()))
