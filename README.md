# Ai_Job_Application

I have never really known what to write or how to describe my skills in a CV, or how to adapt them to each job position ( in germany )
This website will analyze your profile and tell you how to enhance your CV, as well as what skills you should learn—and in how much time—to land the job you want.

## What it does

Upload your CV (PDF), paste a job offer, and get:

- a match score out of 100 with a short justification
- skills already present in your CV
- missing skills
- warning points (what could get your application rejected)
- an action plan split into three periods: this week, 1-2 months, 3-6 months

## How it works

1. `pdfplumber` extracts the text from the uploaded CV.
2. The CV text and the job offer are inserted into a detailed prompt (`prompt.txt`).
3. The prompt is sent to the Google Gemini API, which is instructed to answer in a strict JSON format.
4. The JSON is parsed in Python and displayed with Streamlit.

## Tech stack

- Python
- Google Gemini API (`google-genai`)
- Streamlit (interface)
- pdfplumber (PDF text extraction)


## Run it locally

```bash
git clone https://github.com/Rosney-y/Ai_Job_Application.git
cd Ai_Job_Application
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"
streamlit run app.py
```

You need your own Gemini API key (Google AI Studio). Never commit your key.

## Challenges and solutions

**Two-column CVs gave mixed-up text.** The PDF extraction reads line by line across both columns, so sections got mixed. I worked around it in the prompt by telling the model that the text order is scrambled and that it must rebuild the sections itself. An alternative would be to crop each column with pdfplumber.

**An API call took over 4 minutes.** I isolated the problem by keeping the same code and changing only the model: switching to a lighter model (`gemini-3.1-flash-lite`) brought the response time down to about 4 seconds. The slow model was probably overloaded. I also added a 30-second timeout so the app never hangs silently.

**Unreliable model output.** The JSON is read with `.get()` and default values, so a missing key does not crash the app.

## Limitations

- The score is an estimate, not an exact measure. It can vary between runs.
- The CV is sent to the Gemini API for analysis. Do not upload a CV you do not want to share with Google.
- Scanned CVs (images) are not supported.

## What I learned

Calling an API, structured JSON output, prompt design, error handling, virtual environments, protecting secrets, and Git/GitHub.
