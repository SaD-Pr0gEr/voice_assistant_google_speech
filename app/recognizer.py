from abc import ABC

from speech_recognition import Recognizer, AudioData, Microphone

from config import MICROPHONE_AUDIO_FILES_PATH


class AssistantRecognizer(Recognizer, ABC):
    user_audio_filename = MICROPHONE_AUDIO_FILES_PATH / "user_audio.flac"

    def __init__(self):
        super().__init__()

    def listen_user(self) -> AudioData:
        with Microphone() as microphone:
            print("Слушаю...")
            audio = self.listen(microphone)
        return audio

    def listen_and_save_audio(self) -> str:
        audio = self.listen_user()
        self.raw_write(audio.get_flac_data())
        return self.user_audio_filename

    def raw_write(self, content: bytes) -> str:
        with open(self.user_audio_filename, "wb") as file:
            file.write(content)
        return self.user_audio_filename
