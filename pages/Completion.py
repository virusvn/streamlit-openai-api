import streamlit as st
import helpers
import openai
from streamlit_chat import message

from streamlit_extras.switch_page_button import switch_page

if (
    "organization" not in st.session_state
    or "api_key" not in st.session_state
    or st.session_state["organization"] == ""
    or st.session_state["api_key"] == ""
):
    switch_page("app")

# OpenAI API
helpers.init()


models = [
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]

selected_model = st.sidebar.selectbox("Select a model", models)
temperature = st.sidebar.slider(
    "Temperature", min_value=0, max_value=1, key="temperature"
)
max_tokens = st.sidebar.slider(
    "Maximum length",
    min_value=1,
    max_value=4000,
    key="maximum_length",
    value=1024,
)
top_p = st.sidebar.slider("Top P", min_value=0, max_value=1, key="top_p")
frequency_penalty = st.sidebar.slider(
    "Frequency penalty", min_value=0, max_value=2, key="frequency_enalty"
)
presence_penalty = st.sidebar.slider(
    "Presence penalty", min_value=0, max_value=2, key="presence_penalty"
)
best_of = st.sidebar.slider("Best of", min_value=1, max_value=20, key="best_of")


def generate_response(prompt):
    completions = openai.Completion.create(
        engine=selected_model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        temperature=temperature,
        best_of=best_of,
    )
    message = completions.choices[0].text
    return message


with st.form("completion_form", clear_on_submit=True):
    user_input = st.text_area("You: ", "", key="completion_input")
    submitted = st.form_submit_button("Send")
    if submitted:
        output = generate_response(user_input)
        # store the output
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)


# Storing the chat
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
