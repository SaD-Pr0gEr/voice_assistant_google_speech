import os.path
import time
from abc import ABC
from pathlib import WindowsPath

from app.utils.audio import AudioPlayer
from app.utils.recognizer import AssistantRecognizer
from app.speech_client.google import AssistantSpeechGoogleClient
from app.speech_recognizer_client.google import AssistantSpeechRecognizerGoogleClient
from app.utils.file import FileManager
from config import (
    MICROPHONE_AUDIO_FILES_PATH, GOOGLE_JSON_CREDENTIALS,
    MICROPHONE_USER_AUDIO_FILES_PATH, AUDIO_FILES_PATH,
    MICROPHONE_ASSISTANT_AUDIO_FILES_PATH
)


class JarvisAssistant(AssistantSpeechGoogleClient):

    def __init__(self, google_config_json_file_path: str):
        self.__configure_paths()
        super().__init__(google_config_json_file_path)

    @staticmethod
    def __configure_paths() -> None:
        for path in (
                AUDIO_FILES_PATH,
                MICROPHONE_AUDIO_FILES_PATH,
                MICROPHONE_USER_AUDIO_FILES_PATH,
                MICROPHONE_ASSISTANT_AUDIO_FILES_PATH
        ):
            FileManager.get_or_create_path(path)

    @staticmethod
    def play_audio(audio_file_path: WindowsPath | str) -> None:
        if isinstance(audio_file_path, str):
            AudioPlayer().open_and_play_audio(audio_file_path)
        else:
            AudioPlayer().open_and_play_audio(str(audio_file_path))

    def speech_audio(self, audio_file_path: WindowsPath | str, audio_text: str = None):
        if not os.path.exists(audio_file_path):
            self.get_and_save_speech(
                audio_text,
                str(audio_file_path)
            )
        self.play_audio(audio_file_path)

    @staticmethod
    def audio_path_generator(path: str) -> str:
        return str(MICROPHONE_ASSISTANT_AUDIO_FILES_PATH / path)

    def welcome_speech(self):
        welcome_audio = self.audio_path_generator("welcome.wav")
        self.speech_audio(welcome_audio, "Вас приветствует голосовой ассистент Джарвис!")
        time.sleep(1)
        welcome_audio = self.audio_path_generator("listening.wav")
        self.speech_audio(welcome_audio, "Я вас слушаю, произнесите команду")

    def run(self):
        self.welcome_speech()

        listener_assistant = AssistantRecognizer()
        user_audio_file = listener_assistant.listen_and_save_audio()
        audio_input_content = FileManager.raw_load(user_audio_file)
        self.speech_audio(
            self.audio_path_generator("analyzing.wav"),
            "Анализирую... Прошу подождать"
        )
        google_recognize_assistant = AssistantSpeechRecognizerGoogleClient(
            str(GOOGLE_JSON_CREDENTIALS)
        )
        response = google_recognize_assistant.speech_recognize_request(audio_input_content)
        if not response:
            self.speech_audio(
                self.audio_path_generator("error_understand.wav"),
                "Я вас не понял..."
            )
            return
        user_command = None
        for result in response:
            user_command = result.alternatives[0].transcript
            self.speech_audio(
                self.audio_path_generator("user_audio.wav"),
                f"Вы сказали: {user_command}",
            )
        if user_command.lower().strip() == "привет":
            self.speech_audio(
                self.audio_path_generator("hello_too.wav"),
                "И вам привет"
            )
        else:
            self.speech_audio(
                self.audio_path_generator("trouble.wav"),
                "Неправильная команда, или я вас не понял"
            )
