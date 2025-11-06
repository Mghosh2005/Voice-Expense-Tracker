from .stt_tts import speech_to_text, text_to_speech
from .llm_handler import parse_expense
from .models import Transaction

def run_voice_logger(user_id="demo_user"):
    text_to_speech("Say your expense.")
    text = speech_to_text()
    if not text:
        text_to_speech("Sorry, I didn't catch that.")
        return
    parsed = parse_expense(text)
    confirm_line = f"Save {parsed['amount_minor']/100:.2f} rupees for {parsed['description']} under {parsed['category']}?"
    text_to_speech(confirm_line)
    ans = input("Confirm? (y/n): ")
    if ans.lower().startswith('y'):
        Transaction.objects.create(user_id=user_id, **parsed)
        text_to_speech("Saved successfully.")
    else:
        text_to_speech("Okay, not saved.")

