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

# Function to ask the API
def ask_gpt(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}],
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
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
            system_prompt = """The following is a text in French with the translation in Walloon:
            French: Le rifondou walon (appellation en wallon), appelé en français wallon unifié, est une forme normalisée du wallon lancée par le mouvement du même nom dans les années 1990 sans statut officiel et dont la légitimité, depuis sa création, l'objet d'avis divergents aussi bien au sein des dialectologues que des autres associations wallophones.
            Son système orthographique propre se caractérise par l'introduction de graphèmes spécialement conçus pour qu'un même phonème puisse être prononcé conformément à la prononciation de chaque région.
            Walloon:El rifondou walon u li rfondou walon, c' est on sistinme di scrijhaedje unifyî do walon, enondé pa l' UCW eyet porshuvou et spårdou pa l' SNR Li Rantoele dins les anêyes 1990.
            Les djins k' î ont bråmint bouté sont lomés les «rfondeus». C' est l' prumî sistinme unifyî k' a stî vormint eployî pa sacwantès djins, et ki s' diswalpêye todi dpus.

            Here is another example: 

            French: Bonjour! Comment puis-je vous aider aujourd'hui?
            Walloon: Bondjou! Comint vos édî oûy?

            Here is another example:

            French: Il existe de nombreux dictionnaires wallons, dont plusieurs sont très riches et font figure de modèles d'un point de vue lexicographique. Tout dictionnaire est un discour sur la langue, une mise à plat de l'imaginaire linguistique. Or, pratiquement tous les dictionnaires wallon-français publiés jusqu'à présent ont une optique dialectale, c.-à-d. qu'ils ne considèrent le wallon que dans sa dimension géolinguistique cloisonnée. Tous ces dictionnaires wallons sont d'abord des dictionnaires strictement locaux.
            Le présent projet de dictionnaire, au contraire, considère le wallon dans toutes ses composantes géographiques (voire historiques, sociales, etc.) et est né d'une tentative, encore largement inachevée, de compilation de plusieurs dictionnaires existant (plus de 200 répertoriés).
            Malheureusement, un tel projet exige beaucoup plus de temps et de persévérance que ce que je suis capable d'y consacrer... A supposer que d'autres veuillent s'y mettre, le travail à faire consiste maintenant à: Unifier l'orthographe et les aspect lexicographiques;
            Encoder les dictionnaires existants, surtout à partir de la lettre E.
            Techniquement parlant, il est déjà possible de faire des recherches sur plusieurs orthographes (normalisée ou Feller) et même dans le sens français-wallon. Cette fonctionnalité n'est pas implémentée dans la version en ligne (que vous avez sous les yeux) parce que le nombre d'enregistrements déjà concernés est un minuscule sous-ensemble de la base de données en son état actuel. A supposer qu'un groupe de généreux mécènes me paie pour passer ma vie à faire du wallon, le travail à faire serait simplement un fastidieux encodage. Le plus important serait, à mon sens, de terminer l'encodage simple wallon-français, qui pourrait déjà rendre de grands services.
            Beaucoup d'articles contiennent des notations bizarres du genre. Il s'agit de fichiers textes pour des articles plus longs, qui doivent être incorporés à la base de données --  et le seront peut-être un jour, qui sait?
            Malgré toutes les réserves détaillées plus haut, il n'en reste pas moins que cette tentative a produit un fichier relativement important, et que ce serait trop bête de ne pas en faire profiter le plus de monde possible...
            Walloon: I gn a des banslêyes di diccionaires walons. Sacwants sont foû ritches et passèt po des egzimpes dins l' monde del lecsicografeye.
            Mins on diccionaire est ossu, tofer, ene façon di håyner les idêyes k' on-z a sol lingaedje. Et cåzumint tos les motîs walons evont di l' idêye ki li walon est èn atroclaedje di pårlers aparintés. C' est tos diccionaires «coinreces», ki n' s' interessèt k' a leu coine do payis walon. Ci motî ci, lu, riwaite li walon come on seu lingaedje et sayî di rashonner totes les ritchesses lecsicografikes --dj' ô: tos les mots-- di ç' lingaedje la dins on seu ovraedje. C' est ene saye, co lon d' esse achevêye, di ramonçler tos les motlîs publiyîs djusk' asteure (di pus d' 200).
            Målureuzmint, po-z avni å coron d' on sfwait ovraedje, i fåt bråmint d' pus di coraedje et di tins ki dj' end a. Admetans k' i gn åreut ds ôtes po-z aidî, i fåt asteure:
            Dins l' pårteye k' est ddja fwaite, unifyî li façon di scrire eyet tot çou k' est lecsicolodjeye; Ecôder les motîs dedja publiyîs;
            Tecnicmint, i gn a moyén eto di cachî après on mot dins sins francès-walon, et co di cweri après on mot walon scrît dins tot l' minme ortografeye (Feller ou «XH»). Mins çoula n' est nén possibe dins li modêye ki vs avoz vaici pa dvant vos ouys. Cwè ki... I gn a moyén tot l' minme di cachî après on mot francès (waitîz pus bas po saveur kimint). Li scrijhaedje eployî dins les mots dedja ecôdés est (li pus sovint) on «rfondou walon» scrît dins l' ortografeye da Feller (pont di XH).
            Bon, mågré tot çou k' dji di di negatif pa dzeu, l' ovraedje k' a stî fwait est dedja foirt consecant et pout ddja esse foirt ahessåve. Ci sereut biesse, vormint, di n' è nén fé profiter ls ôtes.

            Now translate the user input in French to Walloon:"""
            user_prompt="""I'm giving the following text in French, please translate it to Walloon.
            French: {}
            Walloon: """.format(user_input)
            answer = ask_gpt(system_prompt, user_prompt)
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
