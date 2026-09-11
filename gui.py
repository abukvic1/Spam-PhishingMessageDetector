import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/predict"

def analiziraj_poruku():
    poruka = unos.get("1.0", tk.END).strip()

    if not poruka:
        messagebox.showwarning(
            "Upozorenje",
            "Unesite poruku za analizu."
        )
        return

    try:
        analiziraj_button.config(
            text="ANALIZIRAM...",
            state="disabled"
        )

        odgovor = requests.post(
            API_URL,
            json={"message": poruka},
            timeout=5
        )

        odgovor.raise_for_status()

        podaci = odgovor.json()

        rezultat = podaci["prediction"]

        if rezultat == "phishing":
            indikatori = podaci["phishing_indicators"]

            rezultat_label.config(
                text="🚨 PHISHING",
                fg="#B71C1C"
            )

            opis_rezultata.config(
                text="Poruka sadrži znakove mogućeg phishing napada.",
                fg="#B71C1C"
            )

            sigurnost_label.config(
                text=f"Phishing indikatori: {indikatori}"
            )

            upozorenje_label.config(
                text="Ne otvarajte linkove i ne unosite lične podatke."
            )

        else:
            sigurnost = float(podaci["confidence"])

            if rezultat == "spam":
                rezultat_label.config(
                    text="⚠ SPAM",
                    fg="#D32F2F"
                )

                opis_rezultata.config(
                    text="Ova poruka izgleda kao spam.",
                    fg="#D32F2F"
                )

            else:
                rezultat_label.config(
                    text="✓ NORMALNA PORUKA",
                    fg="#2E7D32"
                )

                opis_rezultata.config(
                    text="Poruka ne izgleda kao spam.",
                    fg="#2E7D32"
                )

            sigurnost_label.config(
                text=f"Sigurnost modela: {sigurnost:.2f}%"
            )

            if sigurnost < 70:
                upozorenje_label.config(
                    text="Model nije potpuno siguran u ovu procjenu."
                )
            else:
                upozorenje_label.config(text="")

    except requests.exceptions.ConnectionError:
        messagebox.showerror(
            "Greška",
            "FastAPI server nije pokrenut."
        )

    except requests.exceptions.RequestException as greska:
        messagebox.showerror(
            "Greška",
            f"Došlo je do greške:\n{greska}"
        )

    finally:
        analiziraj_button.config(
            text="ANALIZIRAJ PORUKU",
            state="normal"
        )
def obrisi():
    unos.delete("1.0", tk.END)

    rezultat_label.config(
        text="Rezultat",
        fg="#555555"
    )

    opis_rezultata.config(text="")
    sigurnost_label.config(text="")
    upozorenje_label.config(text="")


root = tk.Tk()

root.title("Spam & Phishing Detector")
root.geometry("650x700")
root.resizable(False, False)

root.configure(bg="#FFF7F2")


# NASLOV

naslov = tk.Label(
    root,
    text="SPAM & PHISHING DETECTOR",
    font=("Segoe UI", 26, "bold"),
    bg="#FFF7F2",
    fg="#E65100"
)

naslov.pack(pady=(30, 5))


podnaslov = tk.Label(
    root,
    text="Provjeri da li je poruka sigurna, phishing ili spam",
    font=("Segoe UI", 11),
    bg="#FFF7F2",
    fg="#666666"
)

podnaslov.pack(pady=(0, 25))


# GLAVNI OKVIR

kartica = tk.Frame(
    root,
    bg="white",
    padx=30,
    pady=25
)

kartica.pack(
    padx=40,
    fill="both"
)


unos_label = tk.Label(
    kartica,
    text="Unesite poruku",
    font=("Segoe UI", 12, "bold"),
    bg="white",
    fg="#333333"
)

unos_label.pack(anchor="w")


unos = tk.Text(
    kartica,
    height=8,
    width=60,
    font=("Segoe UI", 11),
    bd=1,
    relief="solid",
    wrap="word"
)

unos.pack(
    pady=(10, 20),
    fill="x"
)


# DUGMAD

dugmad_frame = tk.Frame(
    kartica,
    bg="white"
)

dugmad_frame.pack()


analiziraj_button = tk.Button(
    dugmad_frame,
    text="ANALIZIRAJ PORUKU",
    font=("Segoe UI", 11, "bold"),
    bg="#F57C00",
    fg="white",
    activebackground="#E65100",
    activeforeground="white",
    bd=0,
    padx=25,
    pady=10,
    cursor="hand2",
    command=analiziraj_poruku
)

analiziraj_button.pack(
    side="left",
    padx=5
)


obrisi_button = tk.Button(
    dugmad_frame,
    text="OČISTI",
    font=("Segoe UI", 11),
    bg="#EEEEEE",
    fg="#333333",
    bd=0,
    padx=25,
    pady=10,
    cursor="hand2",
    command=obrisi
)

obrisi_button.pack(
    side="left",
    padx=5
)


# REZULTAT

rezultat_frame = tk.Frame(
    root,
    bg="white",
    padx=25,
    pady=20
)

rezultat_frame.pack(
    padx=40,
    pady=25,
    fill="x"
)


rezultat_label = tk.Label(
    rezultat_frame,
    text="Rezultat",
    font=("Segoe UI", 20, "bold"),
    bg="white",
    fg="#555555"
)

rezultat_label.pack()


opis_rezultata = tk.Label(
    rezultat_frame,
    text="",
    font=("Segoe UI", 11),
    bg="white"
)

opis_rezultata.pack(pady=5)


sigurnost_label = tk.Label(
    rezultat_frame,
    text="",
    font=("Segoe UI", 12, "bold"),
    bg="white",
    fg="#444444"
)

sigurnost_label.pack(pady=5)


upozorenje_label = tk.Label(
    rezultat_frame,
    text="",
    font=("Segoe UI", 10),
    bg="white",
    fg="#F57C00"
)

upozorenje_label.pack()


root.mainloop()