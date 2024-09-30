import boto3
import os
from botocore.exceptions import NoCredentialsError

class S3Uploader:
    def __init__(self, bucket_name, aws_access_key, aws_secret_key):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    def upload_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_name)
        try:
            self.s3.upload_file(file_name, self.bucket_name, object_name)
            print(f"Upload successful: {object_name}")
        except FileNotFoundError:
            print(f"The file {file_name} was not found.")
        except NoCredentialsError:
            print("Credentials not available.")

    def upload_files_in_dir(self, dir_path):
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                self.upload_file(file_path)
