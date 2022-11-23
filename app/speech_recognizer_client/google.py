import os

from google.api_core.exceptions import GoogleAPICallError
from google.cloud.speech import SpeechClient
from google.cloud.speech_v1 import RecognitionAudio, RecognitionConfig


class AssistantSpeechRecognizerGoogleClient(SpeechClient):

    audio_data = None

    def __init__(self, audio_content: bytes, config_file_path: str, language: str = "ru"):
        self.config_file = config_file_path
        self.request_config = None
        self.__load_user_audio_data(audio_content)
        self.__load_client_config(language)
        super().__init__()

    def __load_user_audio_data(self, content: bytes) -> None:
        self.audio_data = RecognitionAudio(content=content)

    def __load_client_config(self, lang: str) -> None:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.config_file
        self.request_config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=44100,
            language_code=lang
        )

    def speech_recognize_request(self):
        request = self.long_running_recognize(
            config=self.request_config,
            audio=self.audio_data
        )
        try:
            response = request.result(timeout=60)
            return response.results
        except GoogleAPICallError:
            return False
