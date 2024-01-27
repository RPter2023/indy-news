import asyncio

import streamlit as st

from api import search_mediabiasfactcheck

st.sidebar.title("Indy News Search")
st.title("Search MediaBiasFactCheck DB")
st.markdown(
    """
## Search for media outlets by partial name
#### Uses a snapshot of the MediaBiasFactCheck DB (5714 records) and checks wether input is found in the *NAME* only.
#### (Only records with a confidence score of "medium" or "high" are included.)
"""
)
name = st.text_input("Search by name...", value="Democracy Now", max_chars=255)

limit = st.slider("Select number of results", 1, 25, (5))

if name == "":
    st.stop()


def search_and_display_results():
    results = search_mediabiasfactcheck(name, limit)
    st.json(results, expanded=True)


search_and_display_results()
