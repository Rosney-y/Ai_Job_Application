
import json
from google import genai
from google.genai import types
import time
import pdfplumber


#creation du cv en texte
with pdfplumber.open("le.pdf") as pdf:
    cv=""

    for page in pdf.pages:
        cv+=page.extract_text() or ""
        cv +="\n"






with open("offre.txt", encoding="utf-8") as f:
    offre = f.read()


with open("prompt.txt", encoding="utf-8") as f:
    modele_prompt = f.read()


prompt = modele_prompt.replace("{cv}", cv).replace("{offre}", offre)

#ca commence ici
print("Le script démarre")

MODELE="gemini-3.1-flash-lite"

client = genai.Client()

#lecture du prompt pour le transformer en tableau grace a lia 
reponse = client.models.generate_content(
   model=MODELE,
  contents=prompt,
  config=types.GenerateContentConfig(
        response_mime_type="application/json",
        http_options=types.HttpOptions(timeout=30000)  # 30 secondes max
    ),
)




donnees=json.loads(reponse.text)

print("Score :", donnees["score"])
print(donnees["justification_score"])

print("\nCompétences présentes :")
for c in donnees["competences_presentes"]:
    print("-", c)

print("\nCompétences manquantes :")
for c in donnees["competences_manquantes"]:
    print("-", c)

print("\nPoints d'alerte :")
for p in donnees["points_alerte"]:
    print("-", p)

plan = donnees["plan_action"]
print("\n=== PLAN D'ACTION ===")
print("\nCette semaine :")
for a in plan["cette_semaine"]:
    print("-", a)
print("\n1 à 2 mois :")
for a in plan["un_a_deux_mois"]:
    print("-", a)
print("\n3 à 6 mois :")
for a in plan["trois_a_six_mois"]:
    print("-", a)