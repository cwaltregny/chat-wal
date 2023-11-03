import streamlit as st
import openai
import os

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit page configuration
st.set_page_config(page_title="TradWal - Traduire en Wallon", layout="wide")

# Customizing the colors using Streamlit's color theme options
primaryColor = "#d33682"
backgroundColor = "#f0f0f0"
secondaryBackgroundColor = "#e0e0e0"
textColor = "#262730"
font = "sans serif"

# Use Streamlit's themes feature to customize colors, fonts, etc.
st.markdown(
    """
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .streamlit-input {
        font-size: 18px !important;
    }
    .streamlit-button {
        background-color: #0083B8;
        color: white;
        font-size: 18px;
        height: 3em;
        width: 10em;
        border-radius: 5px;
        border: 1px solid #0083B8;
    }
    .streamlit-button:hover {
        background-color: #005f73;
        border-color: #005f73;
    }
    .streamlit-button:active {
        position: relative;
        top: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Pre-prompt to attempt to direct GPT-3.5 to respond in Walloon.
# This would be an experimental approach, as GPT-3.5 is not specifically trained on Walloon.
pre_prompt = """The following is a text in French with the translation in Walloon:

French: Le rifondou walon (appellation en wallon), appelé en français wallon unifié, est une forme normalisée du wallon lancée par le mouvement du même nom dans les années 1990 sans statut officiel et dont la légitimité, depuis sa création, l'objet d'avis divergents aussi bien au sein des dialectologues que des autres associations wallophones.
Son système orthographique propre se caractérise par l'introduction de graphèmes spécialement conçus pour qu'un même phonème puisse être prononcé conformément à la prononciation de chaque région.
Walloon:El rifondou walon u li rfondou walon, c' est on sistinme di scrijhaedje unifyî do walon, enondé pa l' UCW eyet porshuvou et spårdou pa l' SNR Li Rantoele dins les anêyes 1990.
Les djins k' î ont bråmint bouté sont lomés les «rfondeus». C' est l' prumî sistinme unifyî k' a stî vormint eployî pa sacwantès djins, et ki s' diswalpêye todi dpus.

Here is another example: 

French: Bonjour! Comment puis-je vous aider aujourd'hui?
Walloon: Bondjou! Comint vos édî oûy?

Your turn, the user will enter a text in French, translate to Walloon. """

# Function to ask the API
def ask_gpt(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

# Main app layout
st.title('TradWal - Traduire en Wallon', anchor=None)

st.markdown(
    "<div style='font-size:20px; font-weight:bold; color: {primaryColor};'>Bienvenue! Ecrivez un texte en français et recevez la traduction en Wallon.</div>".format(primaryColor=primaryColor),
    unsafe_allow_html=True,
)

user_input = st.text_area("Ecrivez votre phrase en français ici pour la traduire en wallon:",
                          placeholder="J'aimerais traduire cette phrase en Wallon",
                          key="user_question",
                          max_chars=500,
                          help="Ecrivez une phrase en français et l'IA tentera de la traduire en Wallon.")

if st.button('Traduire en Wallon', key='translate_button'):
    if user_input:
        with st.spinner('Génération de la traduction en Wallon...'):
            prompt = pre_prompt + user_input
            answer = ask_gpt(prompt)
            st.text_area("Traduction en Wallon:", value=answer, height=150, help="La traduction générée en Wallon.", key="response_area")
    else:
        st.error("S'il vous plaît, entrez une question en français.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>Ce service a été créé par la famille Waltregny et utilise l'IA pour traduire vos phrases du Français au Wallon. Les réponses sont basées sur les informations disponibles jusqu'en avril 2023 et peuvent ne pas être parfaites.</div>",
    unsafe_allow_html=True,
)

# Add some spacing at the bottom of the page
st.markdown("<br><br>", unsafe_allow_html=True)
