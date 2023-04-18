import helpers
import streamlit as st

organization_id = st.text_input("Organization ID:", value="", type="password")
api_key = st.text_input("Api key:", value="", type="password")

params = st.experimental_get_query_params()
if "team" in params and params["team"][0] == "knights":
    organization_id = st.secrets["openai_organization_id"]
    api_key = st.secrets["openai_api_key"]

disabled_sumit_button = organization_id == "" or api_key == ""
submit_button = st.button("Save", disabled=disabled_sumit_button, key="submit_button")

if submit_button or (organization_id != "" and api_key != ""):
    st.session_state["organization"] = organization_id
    st.session_state["api_key"] = api_key
    helpers.init()
    try:
        helpers.getModels()
        st.write("Hi knights, you are logged in!")
    except:
        st.write("Wrong credentials!")
