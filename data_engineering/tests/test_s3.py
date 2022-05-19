import unittest
import os
import logging
from http import HTTPStatus
from unittest import TestCase, mock

import boto3
from botocore.exceptions import ClientError
from moto import mock_s3

import src.aws

mock_env_vars = {
    "AUDIENCE": "test_audience",
    "CLIENT_ID": "test_id",
    "AWS_ROLE_ARN": "test_arn",
    "AWS_ROLE_SESSION": "test_role_session",
    "AWS_BUCKET": "test_bucket"
}

test_bucket = "test_bucket"
test_key = "test_key"
test_file_name = "tests/test_image.jpg"
test_region = "us-east-1"

@mock_s3
class TestS3(TestCase):
    """
    Testing AWS functionality
    """

    @classmethod
    @mock.patch.dict(os.environ, mock_env_vars)
    @mock_s3
    def setup_s3(cls):
        src.aws.s3 = boto3.client("s3")

        def create_bucket(bucket_name: str):
            response = src.aws.s3.create_bucket(Bucket=bucket_name)
            HTTPStatusCode = response["ResponseMetadata"]["HTTPStatusCode"]
            assert HTTPStatusCode == HTTPStatus.OK

        def upload_file(file_name: str, bucket: str, key: str):
            try:
                _ = src.aws.s3.upload_file(
                    file_name, Bucket=bucket, Key=key)
            except ClientError as e:
                logging.error(e)
                return False
            return True

        create_bucket(test_bucket)
        upload_file(test_file_name, test_bucket, test_key)

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)

    def setUp(cls):
        cls.setup_s3()
        
    @mock.patch.dict(os.environ, mock_env_vars)
    def test_get_object_return_successfully(self):
        obj = src.aws.get_obj(test_bucket, test_key)
        self.assertIsNotNone(obj)

    def test_get_object_when_using_wrong_key_raise_error(self):
        with self.assertRaises(ClientError):
            src.aws.get_obj(test_bucket, "wrong_key")

    def test_get_object_when_using_wrong_bucket_raise_error(self):
        with self.assertRaises(ClientError):
            src.aws.get_obj("wrong_bucket", test_key)

    def test_download_obj_return_successfully(self):
        src.aws.download_obj(test_bucket,
                              test_key, test_file_name)

    def test_download_obj_with_wrong_key_raises_error(self):
        with self.assertRaises(ClientError):
            src.aws.download_obj(test_bucket,
                                  "wrong_key", test_file_name)

    def test_list_object_return_successfully(self):
        res = src.aws.list_obj(test_bucket, test_key)
        self.assertIsNotNone(res.get("Contents"))

    def test_list_object_when_using_wrong_bucket_returns_none(self):
        with self.assertRaises(ClientError):
            res = src.aws.list_obj("wrong_bucket", test_key)

    def test_list_object_when_using_wrong_key_prefix(self):
        res = src.aws.list_obj(test_bucket, "wrong_key")
        self.assertEqual(res.get("Prefix"), "wrong_key")


if __name__ == "__main__":
    unittest.main()
