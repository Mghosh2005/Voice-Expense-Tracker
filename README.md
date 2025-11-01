# Expense-Tracker

This project focuses on building the core LLM module of a voice-interactive expense tracker. The system uses natural language understanding to process spoken or written inputs like “I spent ₹300 for dinner yesterday” and intelligently categorizes them into types such as Food, Travel, Household, or Miscellaneous. The goal is to make the model capable of understanding user intents, extracting key entities like amount, category, and date, and generating smart, context-aware responses such as “Would you like to save it under the Food category?” or “Stored ₹300 for Food on 31st October.”

The LLM module will act as the brain of the expense tracker, handling entity extraction, categorization, and dialogue management. It will later integrate with a backend or database to store and retrieve transactions. The system leverages NLP and lightweight prompt-based reasoning to classify expenses without manual intervention.

Technologies used include Python, transformers-based NLP models, and prompt-driven categorization logic. Future versions may integrate speech-to-text (STT) and text-to-speech (TTS) modules to support full voice interaction.

The folder structure includes a dedicated llm_handler.py for entity extraction and categorization logic, along with placeholders for future modules like stt_tts.py and voice_cli.py. The project aims to deliver a smart, context-aware conversational module that can be extended into a complete expense tracking system with analytics and visualization in later phases.
FOLDER STRUCTURE:
voice_expense_tracker/
├─ manage.py
├─ requirements.txt
├─ README.md
├─ .env.example
├─ voice_tracker/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
└─ expenses/
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ models.py
   ├─ serializers.py
   ├─ views.py
   ├─ urls.py
   ├─ llm_handler.py
   ├─ stt_tts.py
   ├─ voice_cli.py
   └─ migrations/
