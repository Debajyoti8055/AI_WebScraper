import streamlit as st
# from scrape_using_2captcha import scrape_website
from scrape_module import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

st.title("AI WEB SCRAPPER")
url = st.text_input("Enter URL: ")

if st.button("Scrape Site"):
    st.write("Scraping...")
    result=scrape_website(url)
    body_content=extract_body_content(result)
    cleaned_content=clean_body_content(body_content)
    st.session_state.dom_content=cleaned_content

    with st.expander("View DOM content"):
        st.text_area("DOM content", cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse? ")
    if st.button("Parse content"):
        st.write("Parsing...")
        dom_chunks=split_dom_content(st.session_state.dom_content) 
        result = parse_with_ollama(dom_chunks, parse_description)
        st.write(result)
