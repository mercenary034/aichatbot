from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# Create ChatBot instance with a new database file to avoid old data
CB = ChatBot(
    'ChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///chatbot_new_db.sqlite3'  # Use a new DB file
)

# Training with your custom Q&A
conversation = [
    "hello",
    "hi there!",
    "how are you doing?",
    "i'm doing great.",
    "you're welcome.",
    "who developed you",
    "I am developed by Aashish and Shashwat",
    "how far is the sun",
    "The Sun is about 93 million miles (150 million kilometers) away from Earth."
]

trainer = ListTrainer(CB)
trainer.train(conversation)

# Also train with the English corpus for general responses
trainer_corpus = ChatterBotCorpusTrainer(CB)
trainer_corpus.train('chatterbot.corpus.english')

print("Training completed with new data.")
