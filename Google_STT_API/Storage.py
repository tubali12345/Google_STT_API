import mimetypes
from pathlib import Path

from google.cloud import storage
from tqdm import tqdm


class GCStorage:
    def __init__(self, key_path: str):
        self.client = storage.Client.from_service_account_json(key_path)

    def get_bucket(self, bucket_name: str):
        return self.client.get_bucket(bucket_name)

    def list_buckets(self):
        return [bucket.name for bucket in self.client.list_buckets()]

    def upload_file(self,
                    bucket,
                    blob_destination: str,
                    file_path: str):
        blob = bucket.blob(blob_destination)
        blob.upload_from_filename(file_path, content_type=mimetypes.guess_type(file_path)[0])
        return blob

    def list_blobs(self, bucket_name: str):
        return self.client.list_blobs(bucket_name)

    def create_bucket(self,
                      bucket_name: str,
                      storage_class: str = 'STANDARD',
                      bucket_location: str = 'EU'):
        if bucket_name not in self.list_buckets():
            bucket = self.client.bucket(bucket_name)
            bucket.storage_class = storage_class
            return self.client.create_bucket(bucket, location=bucket_location)
        else:
            print('Bucket already exists')

    def upload_all_wav_from_path(self, path: str,
                                 bucket_name: str = 'regens-speech-to-text-bucket'):
        bucket_gcs = self.get_bucket(bucket_name)
        for file in tqdm(Path(path).rglob('*.wav')):  # '/opt/model-validation/languages/tr/data'
            self.upload_file(bucket_gcs, file.name, str(file))

    def empty_bucket(self,
                     bucket_name: str = 'regens-speech-to-text-bucket'):
        for blob in tqdm(self.list_blobs(bucket_name)):
            blob.delete()

    def download_all_from_bucket(self,
                                 destination_path: str,
                                 bucket_name: str = 'regens-speech-to-text-bucket'):
        for blob in tqdm(self.list_blobs(bucket_name)):
            blob.download_to_filename(f'{destination_path}/{blob.name}')
