import boto3
from boto3.dynamodb.types import TypeDeserializer

from shared.config import config
from shared.logging import getLogger

log = getLogger(__name__)


def init_dynamodb_client(dynamodb_client=None):
    if dynamodb_client is None:
        return boto3.client(
            "dynamodb",
            aws_access_key_id=config.aws.access_key_id,
            aws_secret_access_key=config.aws.secret_access_key,
            aws_session_token=config.aws.session_token,
        )
    else:
        return dynamodb_client


def list_dynamodb_tables(dynamodb_client=None):
    client = init_dynamodb_client(dynamodb_client)

    res = client.list_tables()
    return res["TableNames"]


def describe_dynamodb_table(table_name: str, dynamodb_client=None):
    client = init_dynamodb_client(dynamodb_client)
    res = client.describe_table(TableName=table_name)
    return res["Table"]


# ---------------------------------------------------
#  DynamoDB Table Data
def get_dynamodb_table_data(table_name: str, query="", dynamodb=None):
    client = init_dynamodb_client(dynamodb)
    paginator = client.get_paginator("scan")
    page_iterator = paginator.paginate(TableName=table_name)

    type_deserializer = TypeDeserializer()

    data = []
    for page in page_iterator:
        log.info(f"Scanning page {page['ScannedCount']}/{page['Count']}")
        for item in page["Items"]:
            clean = {k: type_deserializer.deserialize(v) for k, v in item.items()}
            data.append(clean)

    log.success(f"Scanned {len(data)} items")
    return data
