import os
import openai
import streamlit as st


@st.cache
def getModels():
    return openai.Model.list().data


def init():
    openai.organization = st.session_state["organization"]
    openai.api_key = st.session_state["api_key"]
