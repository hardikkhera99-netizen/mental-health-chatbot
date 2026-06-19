# AI-Powered Mental Health Chatbot

## Overview

The AI-Powered Mental Health Chatbot is a Python-based application designed to provide supportive and empathetic responses to users. The system combines Natural Language Processing (NLP), Sentiment Analysis, and physiological data such as heart rate and blood pressure to create a more personalized user experience.

The project consists of a Flask backend, a Tkinter-based graphical user interface, sentiment analysis using Hugging Face Transformers, and AI-generated responses through the Groq API.

---

## Features

* Sentiment Analysis using Transformers
* AI-generated responses using Groq API
* Flask Backend Integration
* Tkinter-based GUI Interface
* Voice Input using Speech Recognition
* Voice Output using Text-to-Speech
* Heart Rate Validation
* Blood Pressure Validation
* Dark Mode Support

---

## Technologies Used

* Python
* Flask
* Transformers (Hugging Face)
* Groq API
* Tkinter
* SpeechRecognition
* pyttsx3
* Requests

---

## Project Structure

```text
Mental Health Chatbot/
│
├── app.py
├── chatbot.py
├── sentiment_analysis.py
├── web_ui.py
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone the repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Groq API key in `chatbot.py`.

4. Start the Flask server:

```bash
python app.py
```

5. Run the GUI application:

```bash
python web_ui.py
```

---

## Future Enhancements

* Database Integration
* User Authentication
* Emotion Detection from Voice
* Chat History Storage
* Mental Health Analytics Dashboard
* Web-Based Deployment

---

## Author

Hardik Khera

B.Tech – Artificial Intelligence and Data Science
