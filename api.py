from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import re

app = FastAPI()

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


class Poruka(BaseModel):
    message: str


def provjeri_phishing(poruka):
    poruka = poruka.lower()

    sumnjive_fraze = [
        "verify your account",
        "verify account",
        "confirm your account",
        "update your account",
        "your account has been suspended",
        "account suspended",
        "enter your password",
        "confirm your password",
        "login immediately",
        "click the link",
        "click here to login",
        "bank account",
        "credit card",
        "urgent action required"
    ]

    broj_indikatora = 0

    for fraza in sumnjive_fraze:
        if fraza in poruka:
            broj_indikatora += 1

    if re.search(r"https?://|www\.", poruka):
        broj_indikatora += 1

    return broj_indikatora


@app.get("/")
def home():
    return {"status": "Spam & Phishing Detector API radi"}


@app.post("/predict")
def predict(poruka: Poruka):

    phishing_indikatori = provjeri_phishing(poruka.message)

    if phishing_indikatori >= 2:
        return {
            "prediction": "phishing",
            "phishing_indicators": phishing_indikatori
        }

    poruka_vector = vectorizer.transform([poruka.message])

    rezultat = model.predict(poruka_vector)[0]

    vjerovatnoce = model.predict_proba(poruka_vector)[0]

    indeks = list(model.classes_).index(rezultat)
    sigurnost = vjerovatnoce[indeks] * 100

    return {
        "prediction": rezultat,
        "confidence": round(sigurnost, 2),
        "phishing_indicators": phishing_indikatori
    }