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


def run():
    for path in (
            AUDIO_FILES_PATH,
            MICROPHONE_AUDIO_FILES_PATH,
            MICROPHONE_USER_AUDIO_FILES_PATH,
            MICROPHONE_ASSISTANT_AUDIO_FILES_PATH
    ):
        FileManager.get_or_create_path(path)
    print("Вас приветствует голосовой ассистент Джарвис!")
    my_recognizer = AssistantRecognizer()
    user_audio_file = my_recognizer.listen_and_save_audio()
    audio_content = FileManager.raw_load(user_audio_file)
    google_recognize_assistant = AssistantSpeechRecognizerGoogleClient(
        str(GOOGLE_JSON_CREDENTIALS)
    )
    print("Анализирую...")
    response = google_recognize_assistant.speech_recognize_request(audio_content)
    if not response:
        print("Я вас не понял...")
        return
    user_command = None
    for result in response:
        user_command = result.alternatives[0].transcript
        print(f"Вы сказали: {user_command}")
    google_speech_assistant = AssistantSpeechGoogleClient(str(GOOGLE_JSON_CREDENTIALS))
    if user_command.lower() == "привет":
        saved_response_audio = google_speech_assistant.get_and_save_speech("И вам привет")
        if not saved_response_audio:
            print("Я не смог перевести ваш голос((")
            return
        audioPlayer = AudioPlayer()
        audioPlayer.open_and_play_audio(str(saved_response_audio))
    else:
        print("Неправильная команда, или я вас не понял))")
