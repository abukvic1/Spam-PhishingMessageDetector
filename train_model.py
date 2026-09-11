import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
df = pd.read_csv(
    "data/SMSSpamCollection",
    sep="\t",
    names=["label", "text"]
)

print(df.head())
print(df.shape)
print(df["label"].value_counts())



X = df["text"] # podaci koje model dobija kao ulaz
y = df["label"] # oznake koje model treba da predvidi
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.33,
    random_state=42,
    stratify=y
)
vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression(class_weight="balanced")
model.fit(X_train_tfidf, y_train)
predictions = model.predict(X_test_tfidf)

print("\nConfusion matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification report:")
print(classification_report(y_test, predictions))
print("Predikcije:")
print(predictions)

print("Tačni odgovori:")
print(y_test.values)
accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy)
nova_poruka = ["Congratulations! You have won free money"]

nova_poruka_tfidf = vectorizer.transform(nova_poruka)

rezultat = model.predict(nova_poruka_tfidf)

print("Nova poruka:", nova_poruka[0])
print("Model kaže:", rezultat[0])

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
#print(df)