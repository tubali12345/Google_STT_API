class Config:
    SOURCE_PATH = '/home/turib/diar_test'
    DESTINATION_PATH = '/home/turib/diar_test_text2'
    LANGUAGE = 'en-US'
    KEY_PATH = 'key.json'
    BUCKET_NAME = 'regens-speech-to-text-bucket'
    model = 'latest_long'
    sample_rate = 44100
    enable_automatic_punctuation = True
    enable_diarization = True
    diarization_config = {
        'min_speaker_count': 2,
        'max_speaker_count': 2,
    }
