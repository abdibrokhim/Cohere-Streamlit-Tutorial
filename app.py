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

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Define functions for text completion
def complete(text, max_tokens, temperature, stop_sequences):
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

    if not text:
        st.session_state.text_error = "Please enter a text to complete."
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your text is being completed..."):
            compeletion = Completion()
            st.session_state.text_error = ""
            st.session_state.n_requests += 1
            st.session_state.complete = (
                compeletion.complete(text, max_tokens, temperature, [stop_sequences])
            )
            logging.info(
                f"""
                Info: 
                Text: {text}
                Max tokens: {max_tokens}
                Temperature: {temperature}
                Stop_sequences: {stop_sequences}\n
                """
            )



# Configure Streamlit page and state
st.set_page_config(page_title="Co-Complete", page_icon="🍩")


if "complete" not in st.session_state:
    st.session_state.complete = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0


# Force responsive layout for columns also on mobile
st.write(
    """<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>""",
    unsafe_allow_html=True,
)


# Render Streamlit page
st.title("Complete Text")

st.markdown(
    "This mini-app completes Sentences using Cohere's based [Model](https://docs.cohere.ai/) for texts."
)

st.markdown(
    "You can find the code on [GitHub](https://github.com/abdibrokhim/CoComplete) and the author on [Twitter](https://twitter.com/abdibrokhim)."
)

# input text
text = st.text_area(label="Enter text", placeholder="Example: I want to play")

# input max tokens
max_tokens = st.slider('Pick max tokens', 0, 1024)

# input temperature
temperature = st.slider('Pick a temperature', 0.0, 1.0)

# input stop sequences
stop_sequences = st.text_input(label="Enter stop sequences", placeholder="Example: --")


st.button(
    label="Complete",
    key="complete",
    help="Press to Complete text", 
    type="primary", 
    on_click=complete,
    args=(text, max_tokens, temperature, stop_sequences),)


text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)


if st.session_state.complete:
    st.markdown("""---""")
    st.text_area(label="Completed Text", value=st.session_state.complete,)