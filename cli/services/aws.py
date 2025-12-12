from typing import Union, List
import boto3


def get_session(role_arn: str) -> boto3.session.Session:
    if role_arn:
        sts_client = boto3.client("sts")
        assumed_role = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="rank-cli",
        )
        session = boto3.session.Session(
            aws_access_key_id=assumed_role["Credentials"]["AccessKeyId"],
            aws_secret_access_key=assumed_role["Credentials"][
                "SecretAccessKey"
            ],
            aws_session_token=assumed_role["Credentials"]["SessionToken"],
            region_name="eu-west-1",
        )
        return session
    else:
        return boto3.session.Session(region_name="eu-west-1")


def get_secrets(
    session: boto3.session.Session,
    secret_ids: Union[str, List[str]],
    secret_prefix: str = "",
) -> dict:
    if isinstance(secret_ids, str):
        secret_ids = [secret_ids]

    secrets = {}
    client = session.client("secretsmanager")
    for secret_id in secret_ids:
        response = client.get_secret_value(SecretId=secret_prefix + secret_id)
        secrets[secret_id] = response["SecretString"]

    return secrets
