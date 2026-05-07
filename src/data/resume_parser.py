import re


def clean_text(text: str) -> str:

    if text is None:
        return ""

    text = text.lower()

    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def parse_resume(resume_text):

    cleaned = clean_text(resume_text)

    return cleaned