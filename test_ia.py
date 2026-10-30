

print("Le script démarre")


from google import genai
from google.genai import types
import time

MODELE="gemini-3.1-flash-lite"

client = genai.Client()
start=time.time()


reponse = client.models.generate_content(
   model=MODELE,
  contents="Explique en 2 phrases ce qu'est un Werkstudent en Allemagne.",
  config=types.GenerateContentConfig(
        http_options=types.HttpOptions(timeout=30000)  # 30 secondes max
    ),
)







print(reponse.text)
print(f"Durée : {time.time() - start:.1f} secondes")
