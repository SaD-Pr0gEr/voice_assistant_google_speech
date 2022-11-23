from pyaudio import PyAudio
import wave


class AudioPlayer(PyAudio):

    def __init__(self, chunk_size: int = 1024):
        self.chunk_size = chunk_size
        super().__init__()

    def open_and_play_audio(self, audio_file_path: str) -> None:
        wave_file = wave.open(audio_file_path, 'rb')
        stream = self.open(
            format=self.get_format_from_width(wave_file.getsampwidth()),
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True
        )
        data = wave_file.readframes(self.chunk_size)
        while len(data):
            stream.write(data)
            data = wave_file.readframes(self.chunk_size)
        stream.stop_stream()
        stream.close()
        self.terminate()
