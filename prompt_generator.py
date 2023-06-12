import streamlit as st

templates = {}
templates["francais"] = {
"role_template" : "tu dois agir comme un {key}",
"style_template" : "avec un ton {key}",
"format_template" : "pour un {key}",
"purpose_template" : "dont l'objetif est de {key}",
"context_template" : "le contexte concerne une {key}",
"scope_template" : "pour une portee {key}",
"example_template" : "voici un exemple {key}",
"target_template" : ".{key}.",
"language_template" : "dont la réponse doit être en {key}"}

templates["español"] = {
"role_template" : "debes actuar como un {key}",
"style_template" : "con un tono {key}",
"format_template" : "para un {key}",
"purpose_template" : "cuyo objetivo es {key}",
"context_template" : "el contexto se refiere a un {key}",
"scope_template" : "para un alcance de {key}",
"example_template" : "este es un ejemplo de {key}",
"target_template" : ".{key}.",
"language_template" : "cuya respuesta debe ser en {key}"}

templates["english"] = {
"role_template": "you must act as a {key}",
"style_template": "with a tone of {key}",
"format_template": "for a {key}",
"purpose_template": "whose purpose is {key}",
"context_template": "the context refers to a {key}",
"scope_template": "for a scope of {key}",
"example_template": "this is an example of {key}",
"target_template": ".{key}.",
"language_template": "whose response should be in {key}"}

def template_build(template,key, context):
    if len(key):
        return templates[st.session_state["language"]][template].format(key=key)
    return ""

def build_text(context):
    return " ".join(" ".join([
            "ChatGPT",
            template_build("role_template",context['role'], context),
            template_build("style_template",context['style'], context),
            template_build("format_template",context['format'], context),
            template_build("purpose_template",context['purpose'], context),
            template_build("language_template",context['language_'], context),
            template_build("target_template",context['target'], context),
            template_build("context_template",context['context'], context),
            template_build("scope_template",context['scope'], context),
            template_build("example_template",context['example'], context),
            context['limitations'],
            context['citations'],
            context['pointview'],
            context['counterarg'],
            context['terminology']
            ]).split())
