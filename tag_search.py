"""Creates a CSV file of all Ec2Instances' tags in a region.
CSV contains Region name, Instance ID, Instance Name, and Owner_Email."""
import sys
import argparse
import json

import re

from ec2_instance import Ec2Instance
import aws_auth
from olympus_patterns import patterns

def write_output_csv(file, rgn, inst:Ec2Instance) -> None:
    """Writes to output.csv in csv format. Columns align with parameter names."""
    with open("output.csv", 'w', encoding="UTF-8") as outfile:
        # CSV Column names
        outfile.write("Region,ID,Name,Email\n")
        # Region
        file.write(rgn + ",")
        # Instance id
        file.write(inst.id +  ",")
        # Name
        file.write(inst.instance_name + ",")
        # Owner_Email
        file.write(inst.instance_email + ",")
        # End of row
        file.write("\n")

def write_output_json(resp:dict):
    """Writes to output.json in json format."""
    with open("output.json", 'w', encoding="UTF-8") as outfile:
        outfile.write(json.dumps(resp, default=str))

def check_for_match(ptrn:str, val:str) -> bool:
    """Checks for Olympus naming conventions given a value and a pattern category.
    Returns True if value is found within the pattern category.
    See olympus_patterns.py for pattern categories."""
    match_flag = False
    for pattern in patterns[ptrn]:
        if re.search(patterns[ptrn].get(pattern), val):
            # print(f'Match on {pattern}.')
            match_flag = True
    # if not match_flag:
        # print(f'No matches for {val}.')
    return match_flag

def parse_args(args:list):
    parser = argparse.ArgumentParser()
    """
    parser.add_argument(
        "-n", "--no-proxy", default=False, action="store_true", help="do not use proxy"
    )
    """
    return parser.parse_args()

def main(args):
    parse_args(args)
    region = {
    "east1" : 'us-east-1',
    "east2" : 'us-east-2'
    }
    response = aws_auth.botosesh.client('ec2', region_name=region["east1"]).describe_instances()
    if aws_auth.check_response_code(response):
        instances = response["Reservations"]
        region = aws_auth.botosesh.region_name
    else:
        print("Invalid Request Status Code.")

if __name__ == "__main__":
    args = print(parse_args(sys.argv))
    main(args)

"""
To do list
TODO: create arg parsing for passing this as a CLI script
        make functionality for:
        print output
        csv output
        json output
        region switching
        all regions
TODO: look at pandas for better csv and json exports
        we need to know usage for naming AND sizing.
"""