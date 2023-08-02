import boto3


def get_session(role_arn: str) -> boto3.session.Session:
    sts_client = boto3.client("sts")
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="rank-cli",
    )
    session = boto3.session.Session(
        aws_access_key_id=assumed_role["Credentials"]["AccessKeyId"],
        aws_secret_access_key=assumed_role["Credentials"]["SecretAccessKey"],
        aws_session_token=assumed_role["Credentials"]["SessionToken"],
        region_name="eu-west-1"
    )
    return session


def get_secret(session: boto3.session.Session, secret_id: str) -> str:
    client = session.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id)
    return response["SecretString"]
