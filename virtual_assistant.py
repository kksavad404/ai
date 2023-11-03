import openai
import pyttsx3
import speech_recognition as sr

# Replace with your OpenAI API key
api_key = "Your_api_key_here"

openai.api_key = api_key

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None

def chat_with_openai():
    conversation = []

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Adjust the rate (speed) and voice
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)  # Adjust the rate (words per minute)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Select a female voice

    print("You: (Say 'exit' to end the conversation)")

    while True:
        user_input = recognize_speech()
        if user_input is None:
            continue
        if user_input.lower() == 'exit':
            break

        conversation.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        assistant_reply = response["choices"][0]["message"]["content"]
        print("Assistant:", assistant_reply)
        conversation.append({"role": "assistant", "content": assistant_reply})

        # Speak the assistant's reply
        engine.say(assistant_reply)
        engine.runAndWait()

    # Use the engine to speak a polite "Thank you for using my service. Have a great day!" message
    engine.say("Thank you for using my service. Have a great day!")
    engine.runAndWait()


if __name__ == "__main__":
    chat_with_openai()
