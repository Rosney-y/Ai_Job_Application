import json
import streamlit as st
import pdfplumber
from google import genai
from google.genai import types

# Configuration de la page Streamlit
st.set_page_config(page_title="AI Job Application", page_icon="", layout="centered")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    div.stButton > button {
        background-color: #f4ecd8;
        color: #3b2f2f;
        border: 2px solid #3b2f2f;
        border-radius: 0;
        box-shadow: 4px 4px 0 #3b2f2f;
        font-family: 'Special Elite', 'Courier New', monospace;
        font-size: 1.1rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.6rem 1.6rem;
        transition: all 0.1s ease;
    }
    div.stButton > button p {
        font-family: 'Special Elite', 'Courier New', monospace;
        color: #3b2f2f;
    }
    div.stButton > button:hover {
        background-color: #e8dcc0;
        border-color: #3b2f2f;
        color: #3b2f2f;
    }
    div.stButton > button:active {
        box-shadow: 0 0 0 #3b2f2f;
        transform: translate(4px, 4px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI Job Application - Analyse de CV")
st.write("Dépose ton CV au format PDF et colle l'offre d'emploi pour obtenir une analyse détaillée et un plan d'action personnalisé.")

# --- 1. INTERFACE UTILISATEUR (Formulaire) ---
uploaded_file = st.file_uploader("1. Dépose ton CV (PDF)", type=["pdf"])

offre_text = st.text_area("2. Colle le texte de l'offre d'emploi ici", height=200, placeholder="Ex: Software Engineer Werkstudent (m/w/d)...")

# Charger ton prompt de base depuis ton fichier local
try:
    with open("prompt.txt", encoding="utf-8") as f:
        modele_prompt = f.read()
except FileNotFoundError:
    st.error("Erreur : Le fichier `prompt.txt` est introuvable dans le dossier du projet.")
    modele_prompt = ""

# --- 2. TRAITEMENT LORSQUE L'UTILISATEUR CLIQUE ---
if st.button("Lancer l'analyse", type="primary"):
    if not uploaded_file:
        st.warning("Veuillez téléverser un CV au format PDF.")
    elif not offre_text.strip():
        st.warning("Veuillez coller le texte de l'offre d'emploi.")
    elif not modele_prompt:
        st.error("Impossible de lancer l'analyse sans le fichier `prompt.txt`.")
    else:
        with st.spinner("Analyse en cours par l'IA... Patientez quelques secondes..."):
            
            # A. Extraction du texte du PDF uploadé
            cv_text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    cv_text += page.extract_text() or ""
                    cv_text += "\n"

            # B. Construction du prompt final
            prompt = modele_prompt.replace("{cv}", cv_text).replace("{offre}", offre_text)

            try:
                # C. Appel à l'API Gemini
                client = genai.Client()
                MODELE = "gemini-3.1-flash-lite"  # Utilisation d'un modèle flash stable et rapide

                reponse = client.models.generate_content(
                    model=MODELE,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        http_options=types.HttpOptions(timeout=30000)
                    ),
                )

                # D. Décodage du JSON
                donnees = json.loads(reponse.text)

                # --- 3. AFFICHAGE DES RÉSULTATS SUR LE SITE ---
                st.write("Analyse terminée avec succès !")

                # Score global
                score = donnees.get("score", 0)
                st.metric(label="Score de correspondance", value=f"{score} / 100")
                
                st.info(donnees.get("justification_score", ""))

                # Colonnes pour les compétences
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Compétences présentes")
                    for c in donnees.get("competences_presentes", []):
                        st.markdown(f"- {c}")

                with col2:
                    st.subheader(" Compétences manquantes")
                    for c in donnees.get("competences_manquantes", []):
                        st.markdown(f"- {c}")

                # Points d'alerte
                st.subheader(" Points d'alerte !!")
                for p in donnees.get("points_alerte", []):
                    st.markdown(f"- {p}")

                # Plan d'action
                st.subheader("Plan d'action")
                plan = donnees.get("plan_action", {})

                with st.expander("Cette semaine (Corrections rapides)", expanded=True):
                    for a in plan.get("cette_semaine", []):
                        st.markdown(f"- {a}")

                with st.expander(" 1 à 2 mois (Compétences prioritaires)"):
                    for a in plan.get("un_a_deux_mois", []):
                        st.markdown(f"- {a}")

                with st.expander(" 3 à 6 mois (Objectifs long terme)"):
                    for a in plan.get("trois_a_six_mois", []):
                        st.markdown(f"- {a}")

            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse : {e}")