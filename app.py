"""

Streamlit app to complete text using Cohere.

"""

# Import from standard library
import logging


# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components


# Import modules
from completion import Completion
from supported_languages import SUPPORTED_LANGUAGES
from translation import Translator


# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Define functions for text completion
def complete(text, max_tokens, temperature, stop_sequences, from_lang="", to_lang=""):
    """
    Complete Text.
    """

    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before completing another Text."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

    st.session_state.complete = ""
    st.session_state.text_error = ""
    # st.session_state.visibility = ""
    # st.session_state.n_requests = 0

    if not text:
        st.session_state.text_error = "Please enter a text to complete."
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your text is being completed..."):
            
            translation = Translator()
            translated_text = translation.translate(text, "en")

            compeletion = Completion()
            completed_text = compeletion.complete(translated_text, max_tokens, temperature, [stop_sequences])

            to_lang_code = SUPPORTED_LANGUAGES[to_lang]
            result = translation.translate(completed_text, to_lang_code)

            st.session_state.text_error = ""
            st.session_state.n_requests += 1
            st.session_state.complete = (result)
            
            logging.info(
                f"""
                Info: 
                Text: {text}
                Max tokens: {max_tokens}
                Temperature: {temperature}
                Stop_sequences: {stop_sequences}\n
                From: {from_lang}
                To: {to_lang}
                """
            )


# Configure Streamlit page and state
st.set_page_config(page_title="Co-Complete", page_icon="🍩")


# Store the initial value of widgets in session state
if "complete" not in st.session_state:
    st.session_state.complete = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"


# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Render Streamlit page
st.title("Complete Text")


st.markdown(
    "This mini-app completes, summarizes and etc. using Cohere's based [Model](https://docs.cohere.ai/) for texts."
)


st.markdown(
    "You can find the code on [GitHub](https://github.com/abdibrokhim/CoComplete) and the author on [Twitter](https://twitter.com/abdibrokhim)."
)

# text
text = st.text_area(label="Enter text", placeholder="Example: I want to play")


# max tokens
max_tokens = st.slider('Pick max tokens', 0, 1024)


# temperature
temperature = st.slider('Pick a temperature', 0.0, 1.0)


# stop sequences
stop_sequences = st.text_input(label="Enter stop sequences", placeholder="Example: --")


# from to selector
col1, col2 = st.columns(2)

# from " " language
with col1:
    from_lang = st.selectbox(
        "From language",
        ([i for i in SUPPORTED_LANGUAGES]),
        label_visibility=st.session_state.visibility,
    )

# to " " language
with col2:
    to_lang = st.selectbox(
        "To language",
        ([i for i in SUPPORTED_LANGUAGES]),
        label_visibility=st.session_state.visibility,
    )

# complete button
st.button(
    label="Complete",
    key="generate",
    help="Press to Complete text", 
    type="primary", 
    on_click=complete,
    args=(text, max_tokens, temperature, stop_sequences, from_lang, to_lang),
    )


text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)


if st.session_state.complete:
    st.markdown("""---""")
    st.text_area(label="Completed Text", value=st.session_state.complete,)
