# rabbitmq.py

from google.cloud import storage

import sys
import numpy as np
import cv2
import os


def singleBlobUpload(_bucket_name, _source_file_name, _destination_blob):
    """
    Uploads a file to the bucket:
    _bucket_name: The ID of your GCS bucket
    _source_file_name: The path to the file to upload
    _destination_blon: The path to the file in GCS bucket
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(_bucket_name)
    destination_blob_name = _destination_blob
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    try:
        blob.upload_from_filename(
            _source_file_name, if_generation_match=generation_match_precondition)
    except Exception as e:
        print(f"Error when upload {_source_file_name} to bucket: {e}")
        return False

    print(f"File {_source_file_name} uploaded to bucket: {destination_blob_name}")
    return True
