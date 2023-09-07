from typing import TypedDict

import boto3

from config import config
from shared.logging import getLogger
from shared.utils import create_dir_if_not_exist
from shared.utils.sanitize import sanitize_folder_path, sanitize_filename

log = getLogger(__name__)


def init_s3_client(s3_client=None):
    if s3_client is None:
        return boto3.client(
            "s3",
            aws_access_key_id=config.aws.access_key_id,
            aws_secret_access_key=config.aws.secret_access_key,
            aws_session_token=config.aws.session_token,
        )
    else:
        return s3_client


def list_s3_buckets(s3_client=None):
    client = init_s3_client(s3_client)
    res = client.list_buckets()
    return [b["Name"] for b in res["Buckets"]]


class TFileMeta(TypedDict):
    filename: str
    subfolders: list[str]
    org: str
    location: str


def _handle_file_meta(s3_filepath: str, meta: TFileMeta):
    _parts = s3_filepath.split("/")
    meta["filename"] = _parts[-1]
    meta["subfolders"] = _parts[0:-1]
    return meta


def list_files_in_bucket(
    bucket_id: str, handle_file_meta=_handle_file_meta, s3_client=None
):
    client = init_s3_client(s3_client)
    s3_bucket_objects = client.list_objects_v2(
        Bucket=bucket_id,
        # Delimiter='string',
        # EncodingType='url',
        # Marker='string',
        # MaxKeys=123,
        # Prefix='string',
        # RequestPayer='requester',
        # ExpectedBucketOwner='string'
    )

    # Add metadata (e.g. uploader details to file list)
    s3_files = []
    for f in s3_bucket_objects["Contents"]:
        if f["Size"] > 0:
            _meta = client.head_object(Bucket=bucket_id, Key=f["Key"])["Metadata"]
            _meta = handle_file_meta(f["Key"], _meta)
            f["meta"] = _meta
            log.debug(f'Meta added -  {f["meta"]["filename"]}')

            s3_files.append(f)

    log.success("FETCHED LIST OF FILES FROM S3")
    return s3_files


def _get_nested_subfolders(file_path: str, meta: TFileMeta):
    subfolders = "\\".join(meta["subfolders"])
    return f"{file_path}\\{subfolders}"


def download_files_from_bucket(
    files: list[dict],
    bucket_id: str,
    data_folder: str = config.paths.raw,
    get_nested_folder_path=_get_nested_subfolders,
    s3_client=None,
):
    client = init_s3_client(s3_client)
    for file in files:
        _meta = file["meta"]
        _dir = get_nested_folder_path(data_folder, _meta)
        # Check if the file is currently accessible (hasn't been archived)
        if file["StorageClass"] != "GLACIER" and file["StorageClass"] != "DEEP_ARCHIVE":
            # sanitise the folder path & recursively create the subfolders if they don't exist
            _sanitized_dir = create_dir_if_not_exist(sanitize_folder_path(_dir))

            # sanitise the filename to remove invalid characters
            _sanitized_filename = sanitize_filename(_meta["filename"])

            # download the actual file from s3 into the filepath
            client.download_file(
                bucket_id, file["Key"], f"{_sanitized_dir}\\{_sanitized_filename}"
            )
            file["meta"]["location"] = _sanitized_dir
            log.success(f'Downloaded - {_sanitized_dir}\\{_meta["filename"]}')
        else:
            log.warning(
                f'File in long term storage & cannot be retrieved - {_dir}\\{_meta["filename"]}'
            )

    log.success("ALL FILES DOWNLOADED")
    return files


def download_all_files_from_bucket(
    bucket_id: str,
    data_folder: str = config.paths.raw,
    handle_file_meta=_handle_file_meta,
    get_nested_folder_path=_get_nested_subfolders,
    s3_client=None,
):
    client = init_s3_client(s3_client)
    files_list = list_files_in_bucket(bucket_id, handle_file_meta, s3_client=client)
    downloaded_files = download_files_from_bucket(
        files_list, bucket_id, data_folder, get_nested_folder_path, s3_client=client
    )
    return downloaded_files
