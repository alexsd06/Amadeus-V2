import os
import sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QTextCursor
from PyQt6.QtCore import Qt, QEvent
import asyncio
from qasync import QEventLoop, asyncSlot
from dotenv import load_dotenv
from natsort import os_sorted
from characterai import aiocai, sendCode, authUser
from sprites import get_sprite_code, emotions
import nltk.data
import time
from transformers import pipeline
from translate import Translator
from voice import tts, play_audio
from tqdm import tqdm

class AmadeusWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        load_dotenv()
        self.email = os.getenv("EMAIL")
        self.chai_token = os.getenv("CHAI_TOKEN")
        self.amadeus_id = os.getenv("AMADEUS_ID")

        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.client = aiocai.Client(self.chai_token)

        self.classifier = pipeline(
            "text-classification",
            model='bhadresh-savani/distilbert-base-uncased-emotion',
            top_k=None,
            device='cuda'
        )

        self.target_lang = 'ja'
        self.src_lang = 'en'
        self.translator = Translator(from_lang=self.src_lang, to_lang=self.target_lang)

        self.body = "amadeus"
        self.body_idx = 0
        self.font_size = 20
        self.setWindowTitle("Amadeus")
        self.setFixedSize(1280, 720)

        self.layout = QVBoxLayout()
        self.widget = QWidget()

        self.widget.setStyleSheet(
            """
            QLabel {
                background-image: url(sprites/background.png);
            }
            """
        )

        self.amadeus = QLabel()
        self.amadeus.setFixedSize(self.width(), self.height())

        sprite_code = get_sprite_code("medium", "very default")
        self.set_sprite(sprite_code + '00')

        self.text_input = QTextEdit()
        self.text_input.setStyleSheet(
            f"""
            background-color: white;
            color: black;
            font-size: {self.font_size}px;
            font-weight: bold;
            text-align: center;
            """
        )

        self.text_input.installEventFilter(self)

        self.send_button = QPushButton()
        self.send_button.setText("Send")
        self.send_button.setStyleSheet(
            f"""
            font-weight: bold;
            font-size: {self.font_size}px;
            """
        )
        self.send_button.clicked.connect(self.send_clicked)

        self.input_layout = QHBoxLayout()
        self.input_layout.addWidget(self.text_input)
        self.input_layout.addWidget(self.send_button)
        self.input_widget = QWidget()
        self.input_widget.setLayout(self.input_layout)

        self.layout.addWidget(self.amadeus)
        self.layout.addWidget(self.input_widget)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layout)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self.text_input:
            if event.key() == Qt.Key.Key_Return and self.text_input.hasFocus():
                text = self.text_input.toPlainText()
                self.text_input.clear()
                asyncio.create_task(self.send_to_amadeus(text))
                return True  # Indicate that the event is handled
        return super().eventFilter(obj, event)

    def send_clicked(self):
        text = self.text_input.toPlainText()
        self.text_input.clear()
        asyncio.create_task(self.send_to_amadeus(text))

    async def show_text(self, text):
        sentences = self.tokenizer.tokenize(text)
        wavs = []
        for sentence in sentences:
            jp_text = self.translator.translate(sentence)
            wav = tts(jp_text)
            wavs.append(wav)

        text_to_show = ""
        for idx in range(len(sentences)):
            sentence = sentences[idx]
            wav = wavs[idx]
            sentiments = self.classifier(sentence)[0]
            sentiment = sentiments[0]
            print (sentence, sentiment)
            if sentiment['score'] < 0.95:
                sentiment = 'very default'
            else:
                sentiment = sentiment['label']
            sprite_code = get_sprite_code("medium", sentiment)
            play_audio(wav)

            prev_letter = '.'
            list_sentence = list(sentence)
            vowels = ['a', 'e', 'i', 'o', 'u']
            delay_chars = [' ', '.', '!', '?']

            delay_time = 0.05

            for i in range(len(list_sentence)):
                letter = list(sentence)[i]
                text_to_show += letter
                self.text_input.clear()
                self.text_input.setText(text_to_show)
                self.text_input.verticalScrollBar().setValue(self.text_input.verticalScrollBar().maximum())
                if i > 0:
                    prev_letter = list_sentence[i - 1]
                if letter in vowels:
                    if prev_letter in vowels:
                        self.set_sprite(sprite_code + '02')
                    else:
                        self.set_sprite(sprite_code + '01')
                else:
                    if prev_letter in vowels:
                        self.set_sprite(sprite_code + '01')
                    else:
                        self.set_sprite(sprite_code + '00')
                self.repaint()
                if letter in delay_chars:
                    await asyncio.sleep(delay_time)
                await asyncio.sleep(delay_time)
            text_to_show += ' '
        await asyncio.sleep(1)
        sprite_code = get_sprite_code("medium", "very default")
        self.set_sprite(sprite_code + '00')
        self.repaint()

    async def send_to_amadeus(self, text):
        sprite_code = get_sprite_code("medium", "sleep")
        self.set_sprite(sprite_code + '00')
        self.repaint()

        print(f"User: {text}")
        async with await self.client.connect() as chat:
            chat_data = await self.client.get_chat(self.amadeus_id)
            message = await chat.send_message(
                self.amadeus_id, chat_data.chat_id, text
            )
            print(f"Amadeus: {message.text}")  # message.name
            await self.show_text(message.text)

        # await self.show_text('I am Amadeus, a copy of Makise Kurisu! Nice to meet you!')

    def set_sprite(self, sprite_code):
        sprite_path = f"sprites/{self.body}/{sprite_code}.png"
        pixmap = QPixmap(sprite_path)
        pixmap = pixmap.scaledToHeight(720)
        self.amadeus.setPixmap(pixmap)
        self.amadeus.setAlignment(Qt.AlignmentFlag.AlignCenter)

async def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = AmadeusWindow()
    window.show()

    with loop:
        loop.run_forever()

if __name__ == '__main__':
    asyncio.run(main())
