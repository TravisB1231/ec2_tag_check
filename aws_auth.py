"""Handles boto3 authentication and session creation.
Assumes AWS_PROFILE environment variable is used for session"""
import os
import boto3

botosesh = boto3.session.Session(
    region_name="us-east-1",
    profile_name=os.environ.get('AWS_PROFILE')
)
