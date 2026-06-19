import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import speech_recognition as sr
import pyttsx3
import threading

# Config
FLASK_API_URL = "http://127.0.0.1:5000/chat"
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# Voice Output
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Voice Input
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            messagebox.showinfo("Voice Input", "Listening...")
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            message_entry.delete("1.0", tk.END)
            message_entry.insert(tk.END, user_input)
    except sr.UnknownValueError:
        messagebox.showerror("Voice Input", "Sorry, could not understand the audio.")
    except sr.RequestError:
        messagebox.showerror("Voice Input", "Speech recognition service unavailable.")
    except sr.WaitTimeoutError:
        messagebox.showerror("Voice Input", "Listening timed out.")

# Send Message
def send_message():
    user_message = message_entry.get("1.0", tk.END).strip()
    heart_rate = heart_rate_entry.get().strip()
    blood_pressure = blood_pressure_entry.get().strip()

    if not user_message:
        messagebox.showwarning("Input Error", "Please enter a message.")
        return
    if not heart_rate or not blood_pressure:
        messagebox.showwarning("Input Error", "Please enter both heart rate and blood pressure.")
        return

    try:
        int_heart_rate = int(heart_rate)
        systolic, diastolic = map(int, blood_pressure.split('/'))
    except ValueError:
        messagebox.showerror("Input Error", "Invalid heart rate or blood pressure format.")
        return

    full_message = f"The user's heart rate is {heart_rate} bpm and blood pressure is {blood_pressure}. Message: {user_message}"

    try:
        response = requests.post(FLASK_API_URL, json={"message": full_message})
        response.raise_for_status()
        data = response.json()
        bot_reply = data.get("response", "No response")
        sentiment_label, sentiment_score = data.get("sentiment", ("Unknown", 0.0))

        # Emoji based on sentiment
        if sentiment_label == "POSITIVE":
            emoji = "😊"
        elif sentiment_label == "NEGATIVE":
            emoji = "😟"
        else:
            emoji = "😐"

        chat_area.insert(tk.END, f"You: {user_message}\n")
        chat_area.insert(tk.END, f"Sentiment: {sentiment_label} {emoji} ({sentiment_score})\n")
        chat_area.insert(tk.END, f"Bot: {bot_reply}\n\n")

        speak_text(bot_reply)
        message_entry.delete("1.0", tk.END)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Server Error", f"Could not connect to the server.\n{str(e)}")

# Toggle Dark Mode
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode

    bg_color = "#1e1e1e" if dark_mode else "#e6ffff"
    fg_color = "#ffffff" if dark_mode else "#000000"
    entry_bg = "#2d2d2d" if dark_mode else "#ccf2f4"

    root.config(bg=bg_color)
    chat_area.config(bg=entry_bg, fg=fg_color, insertbackground=fg_color)
    message_entry.config(bg=entry_bg, fg=fg_color, insertbackground=fg_color)
    heart_rate_entry.config(bg=entry_bg, fg=fg_color, insertbackground=fg_color)
    blood_pressure_entry.config(bg=entry_bg, fg=fg_color, insertbackground=fg_color)

    for widget in label_widgets:
        widget.config(bg=bg_color, fg=fg_color)
    for widget in button_widgets:
        widget.config(bg="#00b8e6" if not dark_mode else "#444444", fg=fg_color)

# GUI Setup
root = tk.Tk()
root.title("🧠 Mental Health Chatbot")
root.geometry("800x700")
root.configure(bg="#e6ffff")
dark_mode = False

label_widgets = []
button_widgets = []

# Chat Area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=85, height=20, font=("Arial", 11), bg="#ccf2f4")
chat_area.pack(padx=10, pady=10)

# User Message
label_msg = tk.Label(root, text="Your Message:", bg="#e6ffff", font=("Arial", 10, "bold"))
label_msg.pack()
label_widgets.append(label_msg)

message_entry = tk.Text(root, height=3, width=85, bg="#ccf2f4", font=("Arial", 10))
message_entry.pack(padx=10, pady=5)

# Heart Rate
label_hr = tk.Label(root, text="Heart Rate (bpm):", bg="#e6ffff", font=("Arial", 10, "bold"))
label_hr.pack()
label_widgets.append(label_hr)

heart_rate_entry = tk.Entry(root, width=30, bg="#ccf2f4", font=("Arial", 10))
heart_rate_entry.pack(padx=10)

# Blood Pressure
label_bp = tk.Label(root, text="Blood Pressure (e.g., 120/80):", bg="#e6ffff", font=("Arial", 10, "bold"))
label_bp.pack()
label_widgets.append(label_bp)

blood_pressure_entry = tk.Entry(root, width=30, bg="#ccf2f4", font=("Arial", 10))
blood_pressure_entry.pack(padx=10)

# Button Frame
button_frame = tk.Frame(root, bg="#e6ffff")
button_frame.pack(pady=15)

send_button = tk.Button(button_frame, text="Send Message", command=send_message, bg="#00b8e6", fg="black", font=("Arial", 10, "bold"))
send_button.grid(row=0, column=0, padx=10)
button_widgets.append(send_button)

voice_button = tk.Button(button_frame, text="🎤 Speak", command=lambda: threading.Thread(target=recognize_speech).start(), bg="#66ccff", fg="black", font=("Arial", 10, "bold"))
voice_button.grid(row=0, column=1, padx=10)
button_widgets.append(voice_button)

# Dark Mode Toggle Positioned Right
dark_toggle_frame = tk.Frame(root, bg="#e6ffff")
dark_toggle_frame.pack(anchor='e', padx=20, pady=5)

dark_button = tk.Button(dark_toggle_frame, text="🌙 Toggle Dark Mode", command=toggle_dark_mode, bg="#444", fg="white", font=("Arial", 10, "bold"))
dark_button.pack()
button_widgets.append(dark_button)

# Main Loop
root.mainloop()
