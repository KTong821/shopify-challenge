from .constants import ROLE_ARN, ROLE_SESSION_NAME
import os
import boto3

s3 = None

sts = boto3.client("sts")

def assume_role(web_token) -> None:
    assumed_role_object = sts.assume_role_with_web_identity(
        RoleArn=os.environ[ROLE_ARN],
        RoleSessionName=os.environ[ROLE_SESSION_NAME],
        WebIdentityToken=web_token,
        DurationSeconds=3600
    )

    credentials = assumed_role_object["Credentials"]

    global s3
    s3 = boto3.client("s3", aws_access_key_id=credentials["AccessKeyId"],
                      aws_secret_access_key=credentials["SecretAccessKey"], aws_session_token=credentials["SessionToken"])


def list_obj(bucket_name, folder_prefix) -> any:
    if (s3 is None):
        print("S3 not yet connected.")
        return
    res = s3.list_objects(Bucket=bucket_name, Prefix=folder_prefix)
    return res


def get_obj(bucket_name, key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    return obj["Body"]

def download_obj(bucket_name, object_name, file_path):
    s3.download_file(bucket_name, object_name, file_path)

def upload_obj(file_path, folder_prefix, file_name):
    s3.upload_file(file_path, folder_prefix, file_name)
