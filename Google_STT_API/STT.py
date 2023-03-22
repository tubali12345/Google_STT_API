from pathlib import Path

from google.cloud import speech
from tqdm import tqdm

from config import Config
from diar_text_format import formatter


def write_text_to_file(txt: str,
                       directory: Path,
                       name: str) -> None:
    out_file = directory / name.replace(".wav", ".txt")
    out_file.write_text(txt)


def make_directory(dir_name: str,
                   destination_path: str = Config.DESTINATION_PATH) -> Path:
    directory = Path(destination_path) / dir_name
    directory.mkdir(exist_ok=True, parents=True)
    return directory


class GCSpeech:
    def __init__(self, key: str):
        self.client = speech.SpeechClient.from_service_account_file(key)

    def transcribe(self, gcs_uri: str, enable_diarization: bool = Config.enable_diarization):
        diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=enable_diarization,
            min_speaker_count=Config.diarization_config['min_speaker_count'],
            max_speaker_count=Config.diarization_config['max_speaker_count'],
        )

        audio_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # expects wav
            sample_rate_hertz=Config.sample_rate,
            language_code=Config.LANGUAGE,
            enable_automatic_punctuation=Config.enable_automatic_punctuation,
            diarization_config=diarization_config,
            model=Config.model
        )
        audio = speech.RecognitionAudio(uri=gcs_uri)
        operation = self.client.long_running_recognize(config=audio_config, audio=audio)  # max 480s
        return operation.result()

    def get_transcribed_text(self, gcs_uri: str) -> str:
        return "\n".join([result.alternatives[0].transcript for result in self.transcribe(gcs_uri).results])

    def get_transcribed_text_with_diarization(self, gcs_uri: str) -> str:
        return formatter([f"{word_info.word}, {word_info.speaker_tag}" for word_info in
                          self.transcribe(gcs_uri).results[-1].alternatives[0].words])

    def transcribe_all_wav_from_directory(self,
                                          directory,
                                          out_dir: str,
                                          diarization: bool = False) -> None:
        for file in tqdm(Path(directory).rglob('*.wav')):
            if diarization:
                text = self.get_transcribed_text_with_diarization(f"gs://{Config.BUCKET_NAME}/{file.name}")
            else:
                text = self.get_transcribed_text(f"gs://{Config.BUCKET_NAME}/{file.name}")
            write_text_to_file(text, make_directory(out_dir), file.name)
