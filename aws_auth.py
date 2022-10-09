"""Handles boto3 authentication and session creation.
Assumes AWS_PROFILE environment variable is used for session"""
from os import environ

from boto3 import Session

botosesh = Session(
    region_name="us-east-1",
    profile_name=environ.get('AWS_PROFILE')
)

def validate_response_code(resp:dict) -> bool:
    """Sifts through boto3 return data. Returns True if response is 2xx or 3xx."""
    status = resp["ResponseMetadata"]["HTTPStatusCode"]
    if 200 <= status < 400:
        return True
    print("Invalid response.")
    return False
    