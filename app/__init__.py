from app.recognizer import AssistantRecognizer
from app.speech_recognizer_client.google import AssistantSpeechRecognizerGoogleClient
from app.utils import FileManager
from config import MICROPHONE_AUDIO_FILES_PATH, GOOGLE_JSON_CREDENTIALS


def run():
    FileManager.get_or_create_path(MICROPHONE_AUDIO_FILES_PATH)
    print("Вас приветствует голосовой ассистент Джарвис!")
    my_recognizer = AssistantRecognizer()
    user_audio_file = my_recognizer.listen_and_save_audio()
    audio_content = FileManager.raw_load(user_audio_file)
    google_assistant = AssistantSpeechRecognizerGoogleClient(
        audio_content,
        str(GOOGLE_JSON_CREDENTIALS)
    )
    print("Анализирую...")
    response = google_assistant.speech_recognize_request()
    if not response:
        print("Я вас не понял...")
        return
    user_command = None
    for result in response:
        user_command = result.alternatives[0].transcript
        print(f"Вы сказали: {user_command}")
    if user_command.lower() == "привет":
        print("И вам привет)")
    else:
        print("Неправильная команда, или я вас не понял))")
