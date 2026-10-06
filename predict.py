import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

print("Spam detector pokrenut.")
print("Za izlaz upiši: exit")

while True:
    poruka = input("\nUnesi poruku: ")

    if poruka.lower() == "exit":
        print("Program završen.")
        break

    poruka_vector = vectorizer.transform([poruka])

    rezultat = model.predict(poruka_vector)[0]

    vjerovatnoce = model.predict_proba(poruka_vector)[0]

    indeks = list(model.classes_).index(rezultat)
    sigurnost = vjerovatnoce[indeks] * 100

if rezultat == "spam":
    print("Rezultat: SPAM")
else:
    print("Rezultat: NORMALNA PORUKA")

print(f"Sigurnost: {sigurnost:.2f}%")

if sigurnost < 70:
    print("Upozorenje: Model nije potpuno siguran u ovu procjenu.")