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
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
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


def generate_response(messages):
    completions = openai.ChatCompletion.create(
        model=selected_model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        temperature=temperature,
    )

    message = completions.choices[0].message.content
    return message


with st.form("chat_form", clear_on_submit=True):
    message_input = st.text_area("You: ", "", key="message_input")
    assistant_input = st.text_area("Assistant: ", "", key="assistant_input")
    submitted = st.form_submit_button("Send")
    if submitted and message_input:
        messages = [{"role": "user", "content": message_input}]
        if assistant_input:
            messages.append({"role": "assistant", "content": assistant_input})
        output = generate_response(messages)
        # store the output
        st.session_state.past.append(message_input)
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
