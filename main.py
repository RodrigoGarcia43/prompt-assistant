import streamlit as st

from components.select import select, lang_select
from data.language import keys as lang_keys, label as lang_label, language
from data.citations import citations
from data.context import context as context_
from data.counterarg import conterag
from data.format import format
from data.limitations import limitations
from data.pointview import pointview
from data.purpose import purpose
from data.role import role
from data.scope import scope
from data.style import style
from data.target import target
from data.terminology import terminology
from prompt_generator import build_text

from streamlit_extras.stoggle import stoggle
from streamlit_tags import st_tags
import streamlit_authenticator as stauth

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

import yaml
from yaml.loader import SafeLoader



# Page metadata




st.set_page_config(
        page_title="GPT Prompt Assitant", page_icon="🤖", layout="wide"
)
st.markdown("""
        <style>
            .appview-container .main .block-container{
                padding-top: 1rem;    
            }
        </style>
        """, unsafe_allow_html=True)

# Print Page Title

left,middle,right = st.columns(3)
with left:
    st.write('')
with middle:
    st.image("./data/logo.jpg")
with right:
    st.write('')


st.title("🤖 GPT Prompt Assistant")




context={}

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


def submit(tags, options):
    st.session_state[options] = tags
    

    if st.session_state["authentication_status"]:
        config["credentials"]["usernames"][st.session_state["username"]][options] = tags

        with open('./config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)


        
with st.sidebar:
    with st.expander(":heavy_check_mark:"):
        name, authentication_status, username = authenticator.login('Login', 'main')
        st.session_state["authentification_status"] = authentication_status
        if st.session_state["authentication_status"]:
            authenticator.logout('Logout', 'main', key='unique_key')
            st.write(f'Welcome *{st.session_state["name"]}*')
            # if not "loaded" in st.session_state:
            #     st.session_state["loaded"] = False
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')

    with st.expander(":heavy_plus_sign:"):
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                st.success('User registered successfully')
                with open('./config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)

context["language"] = lang_select(lang_label, lang_keys, config)

left, right = st.columns([3,1])

with left:
    
    options = style[context["language"]][1]

    context["style"] = select(style[context["language"]][0], options, "style", config)

with right:
    if st.checkbox(":pencil2:", key="1_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["style"],
            maxtags=-1,
            key="style_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"style"], key="style_button")

        # st.write(config["credentials"]["usernames"][st.session_state["username"]]["style"])
    
left, right = st.columns([3,1])
with left:
    context['format'] = select(format[context["language"]][0], format[context["language"]][1], "format", config)

with right:
    if st.checkbox(":pencil2:", key="2_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["format"],
            maxtags=-1,
            key="format_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"format"], key="format_button")

left, right = st.columns([3,1])
with left:
    context["scope"] = select(scope[context["language"]][0], scope[context["language"]][1], "scope", config)
with right:
    if st.checkbox(":pencil2:", key="3_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["scope"],
            maxtags=-1,
            key="scope_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"scope"], key="scope_button")

left, right = st.columns([3,1])
with left:
    context['purpose'] = select(purpose[context["language"]][0], purpose[context["language"]][1], "purpose", config)
with right:
    if st.checkbox(":pencil2:", key="4_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["purpose"],
            maxtags=-1,
            key="purpose_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"purpose"], key="purpose_button")


left, right = st.columns([3,1])

with left:
    context['role'] = select(role[context["language"]][0], role[context["language"]][1], "role", config)

with right:
    if st.checkbox(":pencil2:", key="5_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["role"],
            maxtags=-1,
            key="role_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"role"], key="role_button")

left, right = st.columns([3,1])
with left:
    context['context'] = select(context_[context["language"]][0], context_[context["language"]][1], "context", config)
with right:
    if st.checkbox(":pencil2:", key="6_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["context"],
            maxtags=-1,
            key="context_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"context"], key="context_button")

left, right = st.columns([3,1])
with left:
    context['limitations'] = select(limitations[context["language"]][0], limitations[context["language"]][1], "limitations", config)
with right:
    if st.checkbox(":pencil2:", key="7_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["limitations"],
            maxtags=-1,
            key="limitations_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"limitations"], key="limitations_button")

exammple = {
        "francais": "écrire un exemple",
        "español" : "Ponga un ejemplo"
    }
context['example'] = st.text_input(exammple[context["language"]])

left, right = st.columns([3,1])
with left:
    context['target'] = select(target[context["language"]][0], target[context["language"]][1], "target", config)
with right:
    if st.checkbox(":pencil2:", key="8_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["target"],
            maxtags=-1,
            key="target_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"target"], key="target_button")

left, right = st.columns([3,1])
with left:
    context['language_'] = select(language[context["language"]][0], language[context["language"]][1], "language", config)
with right:
    if st.checkbox(":pencil2:", key="9_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["language"],
            maxtags=-1,
            key="language_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"language"], key="language_button")

left, right = st.columns([3,1])

with left:
    context['citations'] = select(citations[context["language"]][0], citations[context["language"]][1], "citations", config)
with right:
    if st.checkbox(":pencil2:", key="10_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["citations"],
            maxtags=-1,
            key="citations_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"citations"], key="citations_button")

left, right = st.columns([3,1])
with left:
    context['pointview'] = select(pointview[context["language"]][0], pointview[context["language"]][1], "pointview", config)
with right:
    if st.checkbox(":pencil2:", key="11_check"):
        keywords = st_tags(
            label='',
            text='Press enter to add more',
            value=st.session_state["pointview"],
            maxtags=-1,
            key="pointview_tag")
        
        st.button(":floppy_disk:", on_click=submit, args=[keywords,"pointview"], key="pointview_button")

left, right = st.columns([3,1])
with left:
    context['counterarg'] = select(conterag[context["language"]][0], conterag[context["language"]][1], "counterarg", config)
with right:
    if st.checkbox(":pencil2:", key="12_check"):
            keywords = st_tags(
                label='',
                text='Press enter to add more',
                value=st.session_state["counterarg"],
                maxtags=-1,
                key="counterarg_tag")
            
            st.button(":floppy_disk:", on_click=submit, args=[keywords,"counterarg"], key="counterarg_button")

left, right = st.columns([3,1])
with left:  
    context['terminology'] = select(terminology[context["language"]][0], terminology[context["language"]][1], "terminology", config)
with right:
    if st.checkbox(":pencil2:", key="13_check"):
            keywords = st_tags(
                label='',
                text='Press enter to add more',
                value=st.session_state["terminology"],
                maxtags=-1,
                key="terminology_tag")
            
            st.button(":floppy_disk:", on_click=submit, args=[keywords,"terminology"], key="terminology_button")

prompt = build_text(context)

with st.sidebar:
    title = {
        "francais": "Voici l'invite de ChatGPT",
        "español" : "Prompt para ChatGPT"
    }
    st.title(title[context["language"]])
    st.text_area(
            label = "",
            height=500,
            label_visibility="collapsed",
            value=prompt)
    
    st.code(prompt)
    