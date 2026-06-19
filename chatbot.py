import requests
import re


GROQ_API_KEY = "YOUR_API_KEY_HERE"  

def get_bot_response(user_message):
    """
    Interact with Groq API and get chatbot response.
    """

    # Extract vitals
    heart_rate = extract_heart_rate_from_message(user_message)
    blood_pressure = extract_blood_pressure_from_message(user_message)

    print(f"Debug: Extracted Heart Rate: {heart_rate}")
    print(f"Debug: Extracted Blood Pressure: {blood_pressure}")

    # Validate vitals
    if heart_rate and not validate_heart_rate(heart_rate):
        return "Invalid heart rate format. Please enter a valid heart rate (e.g., 75 bpm)."
    if blood_pressure and not validate_blood_pressure(blood_pressure):
        return "Invalid blood pressure format. Please enter a valid blood pressure (e.g., 120/80)."

    # Prepare API call
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",  
        "messages": [
            {"role": "system", "content": "You are a helpful and empathetic mental health chatbot."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    print("Sending payload to Groq API...")

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        return f"Error: {e} | Details: {error_detail}"
    except KeyError:
        return "Error: Unexpected response format from Groq API."
    except Exception as e:
        return f"Error: {str(e)}"

def validate_heart_rate(heart_rate):
    try:
        heart_rate = int(heart_rate)
        return 30 <= heart_rate <= 200
    except ValueError:
        return False

def validate_blood_pressure(bp):
    try:
        systolic, diastolic = map(int, bp.split('/'))
        return (90 <= systolic <= 200) and (60 <= diastolic <= 120)
    except ValueError:
        return False

def extract_heart_rate_from_message(msg):
    match = re.search(r'(\d{2,3})\s*(bpm|beats per minute|heart rate)?', msg.lower())
    return match.group(1) if match else None

def extract_blood_pressure_from_message(msg):
    match = re.search(r'\b(\d{2,3})/(\d{2,3})\b', msg)
    return match.group(0) if match else None

# Local testing (optional)
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply = get_bot_response(user_input)
        print("Bot:", reply)
