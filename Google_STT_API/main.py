from pathlib import Path

from STT import GCSpeech
from Storage import GCStorage
from config import Config


def main():
    print('Uploading to Storage...')
    storage_client = GCStorage(Config.KEY_PATH)
    storage_client.upload_all_wav_from_path(Config.SOURCE_PATH)

    print('Transcribing texts...')
    speech_client = GCSpeech(Config.KEY_PATH)
    if len(list(Path(Config.SOURCE_PATH).glob('**'))) == 1:
        speech_client.transcribe_all_wav_from_directory(Config.SOURCE_PATH,
                                                        Path(Config.SOURCE_PATH).name,
                                                        diarization=Config.enable_diarization)
    else:
        for category in Path(Config.SOURCE_PATH).glob('*/'):
            speech_client.transcribe_all_wav_from_directory(category, category.name,
                                                            diarization=Config.enable_diarization)

    print('Deleting Storage...')
    storage_client.empty_bucket()


if __name__ == '__main__':
    main()
