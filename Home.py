import nltk
import streamlit as st

nltk.download('stopwords')
st.sidebar.title("Indy News Search")


st.markdown(
    """
# Indy News Search
### Uses a database of 83 media outlets that get enriched with entries from [mediabiasfactcheck.com](https://mediabiasfactcheck.com) data (if found)
#### Source code: [morriz/indy-news](https://github.com/morriz/indy-news)
##### Media sources used: [libguides.rowan.edu](https://libguides.rowan.edu), [localfutures.org](https://localfutures.org), [trustworthymedia.org](https://trustworthymedia.org)
##### (I also included some individuals and teams that I esteem and follow myself ;)
"""
)
