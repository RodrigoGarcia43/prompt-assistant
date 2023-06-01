import streamlit as st

ANOTHER_OPTION = '+'
REMOVE = '-'
DEFAULT = '---'

import yaml

def select(label:str,options:list[str], key, config):
    # select_options = [DEFAULT] + options
    # st.session_state[key] = [DEFAULT] + options
    
    if st.session_state["authentification_status"] and key in config["credentials"]["usernames"][st.session_state["username"]].keys():
        st.session_state[key] = [DEFAULT] + config["credentials"]["usernames"][st.session_state["username"]][key]

    if key not in st.session_state:
        st.session_state[key] = [DEFAULT] + options

    

    # if "loaded" in st.session_state and not st.session_state["loaded"]:
    #     st.session_state[key] = [DEFAULT] + options

    #     if key == "terminology":
    #         st.session_state["loaded"] = True

    selection = st.selectbox(label,st.session_state[key],index=0)

    if selection == DEFAULT:
        return ""
                
    else:
        return selection
    
def clean():
    del st.session_state["citations"]
    del st.session_state["context"]
    del st.session_state["counterarg"]
    del st.session_state["format"]
    del st.session_state["language"]
    del st.session_state["limitations"]
    del st.session_state["pointview"]
    del st.session_state["purpose"]
    del st.session_state["role"]
    del st.session_state["scope"]
    del st.session_state["target"]
    del st.session_state["terminology"]
    del st.session_state["style"]
    


def lang_select(label:str,options:list[str], config):
    select_options = options
    if st.session_state["authentification_status"]:
        if "lan" in config["credentials"]["usernames"][st.session_state["username"]].keys():
            index = config["credentials"]["usernames"][st.session_state["username"]]["lan"]
        else:
            index = 0
    else:
        index = 0

    selection = st.selectbox(label,select_options,index=index, on_change=clean, key="lenguage_selector")

    ind = {"español":0, "francais":1, "english":2}
    if st.session_state["authentification_status"]:
        config["credentials"]["usernames"][st.session_state["username"]]["lan"] = ind[selection]
        with open('./config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

    return selection
