

print("Le script démarre")


import json

from google import genai
from google.genai import types
import time

MODELE="gemini-3.1-flash-lite"

client = genai.Client()


prompt=""" 
Profil : étudiante en informatique, connaît Python et Java.
Offre : Werkstudent Softwareentwicklung, Python, Git et Docker souhaités.

Réponds uniquement en JSON avec ce format :
{"score": 0, "competences_presentes": [], "competences_manquantes": []}
"""




reponse = client.models.generate_content(
   model=MODELE,
  contents=prompt,
  config=types.GenerateContentConfig(
        response_mime_type="application/json",
        http_options=types.HttpOptions(timeout=30000)  # 30 secondes max
    ),
)







print(reponse.text)

donnees=json.loads(reponse.text)

print(type(donnees))
print(donnees["score"])
print(donnees["competences_manquantes"])

