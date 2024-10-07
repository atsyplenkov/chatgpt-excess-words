import re
import streamlit as st
from chatgpt_excess_words import *
import altair as alt
import pandas as pd

## Excess words list
keywords = load_keywords()

## Set page title
st.title("ChatGPT Excess Words Checker")
st.write(
    """
    Checks the input text for **ChatGPT excess words**.
    Based on the words indicated by 14.4 million PubMed
    <i class="ai ai-pubmed"></i> abstracts analysis by 
    *Kobak et al.* [(2024)](https://arxiv.org/html/2406.07016v2).
    """,
    unsafe_allow_html=True,
)

### Add README.md content
st.write(
    f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    <details>
        <summary> <i class="fa-solid fa-circle-info"></i> About: </summary>
        {readme_to_html()}
    </details>
    """,
    unsafe_allow_html=True,
)

## Option 1: File Uploader
uploaded_file = st.file_uploader(
    "Upload a file (optional)", type=["txt", "docx", "pdf"]
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

## Tabs
tab1, tab2 = st.tabs(["Words", "Diagram"])

if text:
    # Count all words in the text
    all_words = re.findall(r"\b\w+\b", text)
    total_word_count = len(all_words)

    keyword_counts = {}

    # Count the occurrences of each keyword in the text
    for keyword in keywords:
        # Create a regex pattern to match the keyword as a full word (case-insensitive)
        pattern = r"\b" + re.escape(keyword) + r"\b"
        count = len(
            re.findall(pattern, text, re.IGNORECASE)
        )  # Count occurrences of the full keyword
        if count > 0:  # Only store keywords found in the text
            keyword_counts[keyword] = count

    if keyword_counts:
        # Sort the dictionary by count in descending order
        sorted_keywords = sorted(
            keyword_counts.items(), key=lambda item: item[1], reverse=True
        )

        with tab1:
            st.write("**Found Excess Words (sorted by count):**")
            for keyword, count in sorted_keywords:
                st.error(f"{count} — {keyword}")
    else:
        st.success("**No Excess Words found in the text.**")

    # Calculate good words (words that are not in the excees word list)
    good_words = total_word_count - sum(keyword_counts.values())

    # Prepare data for the pie chart
    data = pd.DataFrame(
        {
            "Category": ["Other", "Excess Words"],
            "Count": [good_words, sum(keyword_counts.values())],
            "Percentage": [
                (good_words / total_word_count) * 100,
                (sum(keyword_counts.values()) / total_word_count) * 100,
            ],
        }
    )

    # Round Percentage to one decimal place
    data["Percentage"] = data["Percentage"].round(1)
    data["Percentage"] = data["Percentage"].astype(str) + "%"

    base = alt.Chart(data).encode(
        theta=alt.Theta("Count", stack=True),
        radius=alt.Radius(
            "Count", scale=alt.Scale(type="sqrt", zero=True, rangeMin=100)
        ),
        color=alt.Color(
            field="Category",
            type="nominal",
            scale=alt.Scale(range=["#a35139", "#2c3b4e"]),
        ),
    )

    c1 = base.mark_arc(innerRadius=20, stroke="#fff")

    c2 = base.mark_text(size=18, radiusOffset=20).encode(text="Percentage")

    chart_with_labels = c1 + c2

    # Display the chart
    with tab2:
        st.write("**Excess Words distribution:**")
        st.altair_chart(chart_with_labels, use_container_width=True)

## Footer
github_link = """
    <div style="text-align: center; margin-top: 20px;">
        <p>Source code on 
        <a href="https://github.com/atsyplenkov/detect-chatgpt" target="_blank">
        <i class="fa fa-github" style="font-size:18px;"></i> GitHub</a></p>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1/css/academicons.min.css">
"""
st.write(github_link, unsafe_allow_html=True)
