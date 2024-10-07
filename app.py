import pandas as pd
import streamlit as st
from chatgpt_excess_words import *

## Excess words list
keywords = load_keywords()

## Set page title
st.title("ChatGPT Excess Words Checker")
st.write(
    """
    Upload a text file, Word document, PDF, or directly enter 
    text to check for **excess words**.
    Based on the 14.4 million PubMed <i class="ai ai-pubmed"></i>
     abstracts analysis by *Kobak et al.* 
    [(2024)](https://arxiv.org/html/2406.07016v2).
    """,
    unsafe_allow_html=True,
)

### Add README.md content
st.write(
    f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    <details>
        <summary> <i class="fa-solid fa-circle-info"></i> About </summary>
        {readme_to_html()}
    </details>
    """,
    unsafe_allow_html=True,
)

## Option 1: File Uploader
uploaded_file = st.file_uploader(
    "Choose a file (optional)", type=["txt", "docx", "pdf"]
)

## Option 2: Text Input
text_input = st.text_area("Or enter text here:")

if uploaded_file is not None:
    text = extract_text_from_file(uploaded_file)
elif text_input:
    text = text_input.lower()
else:
    st.info("Please upload a file or enter text.")
    text = None  # Set text to None if no input is provided

if text:
    keyword_counts = {}

    # Count the occurrences of each keyword in the text
    for keyword in keywords:
        count = text.count(keyword.lower())  # Count occurrences of the keyword
        if count > 0:  # Only store keywords found in the text
            keyword_counts[keyword] = count

    if keyword_counts:
        # Sort the dictionary by count in descending order
        sorted_keywords = sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True)

        st.write("**Found Keywords (sorted by count):**")
        for keyword, count in sorted_keywords:
            st.error(f"{count} — {keyword}")
    else:
        st.success("**No keywords found in the text.**")

## Footer
github_link = """
    <div style="text-align: center; margin-top: 20px;">
        <p>Source code on 
        <a href="https://github.com/atsyplenkov/chatgpt-excess-words" target="_blank">
        <i class="fa fa-github" style="font-size:18px;"></i> GitHub</a></p>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1/css/academicons.min.css">
"""
st.write(github_link, unsafe_allow_html=True)
