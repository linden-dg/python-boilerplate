from typing import TypedDict

import boto3

from config import config
from shared.utils import get_attr


def init_cognito_client(cognito_client=None):
    if cognito_client is None:
        return boto3.client(
            "cognito-idp",
            aws_access_key_id=config.aws.access_key_id,
            aws_secret_access_key=config.aws.secret_access_key,
            aws_session_token=config.aws.session_token,
        )
    else:
        return cognito_client


# %%  List user pools in account (useful to get pool id)
def list_user_pools(cognito_client=None):
    client = init_cognito_client(cognito_client)
    return client.list_user_pools(
        # NextToken='string',
        MaxResults=10
    )


# %%  User Management functions
class User(TypedDict):
    email: str
    family_name: str
    given_name: str
    org: str


def list_users(user_pool_id: str, cognito_client=None):
    client = init_cognito_client(cognito_client)
    return client.list_users(
        UserPoolId=user_pool_id,
        Limit=50,
    )


def create_user(user: User, user_pool_id: str, cognito_client=None):
    client = init_cognito_client(cognito_client)
    res = client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=get_attr(user, "email"),
        UserAttributes=[
            {"Name": "given_name", "Value": get_attr(user, "given_name")},
            {"Name": "family_name", "Value": get_attr(user, "family_name")},
            {"Name": "email", "Value": get_attr(user, "email")},
            {"Name": "email_verified", "Value": "true"},
            {"Name": "custom:org", "Value": get_attr(user, "org")},
        ],
        # TemporaryPassword='string',
        ForceAliasCreation=False,
        # MessageAction='RESEND',  # or 'SUPPRESS'
        DesiredDeliveryMediums=["EMAIL"],
    )

    return res


def edit_user(user: User, user_pool_id: str, cognito_client=None):
    client = init_cognito_client(cognito_client)
    res = client.admin_update_user_attributes(
        UserPoolId=user_pool_id,
        Username=get_attr(user, "email"),
        UserAttributes=[{"Name": k, "Value": v} for k, v in user.items()],
    )

    return res


def resend_invite(email: str, user_pool_id: str, cognito_client=None):
    client = init_cognito_client(cognito_client)
    res = client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=email,
        MessageAction="RESEND",
        DesiredDeliveryMediums=["EMAIL"],
    )

    return res
