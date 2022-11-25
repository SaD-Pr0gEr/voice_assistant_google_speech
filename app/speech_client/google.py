import os

from google.cloud import texttospeech
from google.cloud.texttospeech_v1 import AudioConfig


class AssistantSpeechGoogleClient(texttospeech.TextToSpeechClient):

    def __init__(self, config_file_path: str, language: str = "ru"):
        self.config_file = config_file_path
        self.request_config = None
        self.voice_config = None
        self.__load_client_config()
        self.__load_voice_config(language)
        super().__init__()

    def __load_client_config(self) -> None:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.config_file
        self.request_config = AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

    def __load_voice_config(self, language: str = "ru") -> None:
        self.voice_config = texttospeech.VoiceSelectionParams(
            language_code=language,
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )

    def speech_request(self, audio_text: str):
        synthesis_input = texttospeech.SynthesisInput(text=audio_text)
        response = self.synthesize_speech(
            input=synthesis_input,
            voice=self.voice_config,
            audio_config=self.request_config
        )
        return response

    def get_and_save_speech(self, audio_text: str, voice_file_path: str) -> str:
        content = self.speech_request(audio_text)
        with open(voice_file_path, "wb") as file:
            file.write(content.audio_content)
        return voice_file_path
