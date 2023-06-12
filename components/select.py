import streamlit as st

ANOTHER_OPTION = '+'
REMOVE = '-'
DEFAULT = '---'

import yaml

def select(label:str,options:list[str], key, config):
    select_options = [DEFAULT] + options
    if st.session_state["authentification_status"] and key in config["credentials"]["usernames"][st.session_state["username"]].keys():
        select_options = [DEFAULT] + config["credentials"]["usernames"][st.session_state["username"]][key]
    else:
        st.session_state[key] = select_options

    if key not in st.session_state:
        st.session_state[key] = select_options


    selection = st.selectbox(label,select_options,index=0)

    

    if selection == DEFAULT:
        return ""
                
    else:
        return selection
    
def clean(selection,config):
    del st.session_state["citations"]
    del st.session_state["context"]
    del st.session_state["counterarg"]
    del st.session_state["format"]
    del st.session_state["language"]
    del st.session_state["language_"]
    del st.session_state["limitations"]
    del st.session_state["pointview"]
    del st.session_state["purpose"]
    del st.session_state["role"]
    del st.session_state["scope"]
    del st.session_state["target"]
    del st.session_state["terminology"]
    del st.session_state["style"]

    ind = {"francais":0, "español":1, "english":2}
    if st.session_state["authentification_status"]:
        config["credentials"]["usernames"][st.session_state["username"]]["lan"] = ind[selection]
        with open('./config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

    st.session_state["language"] =selection
    st.write(selection)
    


def lang_select(label:str,options:list[str], config):
    select_options = options
    ind = {0:"francais", 1:"español", 2:"english"}
    if st.session_state["authentification_status"]:
        if "lan" in config["credentials"]["usernames"][st.session_state["username"]].keys():
            index = config["credentials"]["usernames"][st.session_state["username"]]["lan"]
            st.session_state["language"] = ind[index]
            
        else:
            
            index = 0
    else:
        index = 0
        

    if not "language" in st.session_state:
        st.session_state["language"] =ind[index]

    selection = st.radio("",select_options,index=index, key="lenguage_selector")

    st.button(":floppy_disk:", on_click=clean, args=[selection, config], key="lang_button")

    
    return st.session_state["language"]
