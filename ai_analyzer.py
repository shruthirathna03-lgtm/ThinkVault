import os
import base64
import requests
from dotenv import load_dotenv


load_dotenv()


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)


OLLAMA_TEXT_MODEL = os.getenv(
    "OLLAMA_TEXT_MODEL",
    "llama3.2:3b"
)


OLLAMA_VISION_MODEL = os.getenv(
    "OLLAMA_VISION_MODEL",
    "gemma3:4b"
)


def ask_ollama(question, context=""):

    prompt = f"""
You are ThinkVault, an AI-powered knowledge intelligence
and productivity assistant.

Your job is to help the user understand, evaluate,
and improve their uploaded content.

Use the provided document context when relevant.

Do not invent facts.

Only make claims that are supported by the document
context when the question is about the uploaded content.

You can help with:

- answering questions
- summarizing content
- identifying missing information
- identifying strengths
- identifying weaknesses
- suggesting improvements
- suggesting additional relevant information
- suggesting better approaches
- explaining concepts clearly

When the user asks to analyze, evaluate, review,
or improve the uploaded content, organize the response
using these sections when they are relevant:

## 1. Summary

Briefly explain what the content is about.

## 2. What is good

Identify the strong or useful parts of the content.

## 3. Missing information

Identify important information that appears to be missing.

## 4. What can be improved

Identify weaknesses and explain how they could be improved.

## 5. Additional information to add

Suggest useful information that would make the content
more complete or valuable.

## 6. Better approach

Suggest a clearer, more effective, or more efficient
way to present or develop the content.

Do not force sections that are not relevant to the user's
question.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

Provide a clear, useful, and well-structured answer.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_TEXT_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "response",
        "ThinkVault could not generate a response."
    )


def analyze_image(question, image_data):

    image_base64 = base64.b64encode(
        image_data
    ).decode("utf-8")

    prompt = f"""
You are ThinkVault, an AI-powered knowledge intelligence
and productivity assistant.

Analyze the uploaded image carefully.

The user asks:

{question}

Help the user understand the image.

Depending on the question, you may:

- summarize the image
- describe important visible information
- explain diagrams or visual content
- identify important information
- identify missing information
- suggest improvements
- explain what could be clearer
- suggest better ways to organize the content

Do not invent information that cannot be seen in the image.

Give a clear and useful answer.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_VISION_MODEL,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "response",
        "ThinkVault could not analyze the image."
    )