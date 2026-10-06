# Spam & Phishing Message Detector

A Python application for detecting spam and phishing messages using machine learning.

The application allows the user to enter a message through a graphical interface. The message is sent to a local API, where a trained machine learning model analyzes it and returns a prediction together with a confidence score.

## Features

- Spam/phishing message detection
- Machine learning classification
- Confidence score for predictions
- Simple graphical user interface built with Tkinter
- REST API for communication between the GUI and the model
- Input validation and error handling

## Technologies

- Python
- Scikit-learn
- Pandas
- FastAPI
- Tkinter
- Requests
- Pickle

## Project Structure

```text
SpamPhishingDetector/
├── data/
├── api.py
├── gui.py
├── predict.py
├── train_model.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
├── .gitignore
└── README.md