"""Creates a CSV file of all Ec2Instances' tags in a region.
CSV contains Region name, Instance ID, Instance Name, and Owner_Email."""
import sys
import argparse
import json

import re

from ec2_instance import Ec2Instance
import aws_auth
from olympus_patterns import patterns

def print_output(rgn, inst_list:list) -> None:
    """Writes to olympus_output.csv in csv format. Columns align with parameter names."""
    print("Index\tRegion\t\tID\t\t\tName\t\t\t\tEmail\t\t\t\tDo Not Stop")
    i = 1
    for inst in inst_list:
        print(f'{i}\t{rgn}\t{inst.id}\t{inst.instance_name}\t{inst.instance_email}\t{inst.do_not_stop}')
        i += 1

def write_output_csv(rgn, inst_list:list) -> None:
    """Writes to olympus_output.csv in csv format. Columns align with parameter names."""
    with open("olympus_output.csv", 'w', encoding="UTF-8") as outfile:
        # CSV column names
        outfile.write("Region,ID,Name,Email,Do Not Stop\n")
        # CSV rows
        for inst in inst_list:
            outfile.write(f"{rgn},{inst.id},{inst.instance_name},{inst.instance_email},{inst.do_not_stop}\n")

def write_output_json(resp:dict) -> None:
    """Useful for testing to get raw boto3 output.
    Writes to olympus_output.json in json format."""
    with open("olympus_output.json", 'w', encoding="UTF-8") as outfile:
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

def _parse_args(_args_:list):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--region", default="us-east-1",
        help="specifies the single AWS region.\
            \nDefault is 'us-east-1'."
    )
    parser.add_argument(
        "-o", "--output", default="none",
        help="selects output type.\
            \nOptions are none (default), print, csv, and json. Filename is olumpus_output."
    )
    return parser.parse_args()

def main(args):
    # Creates a boto3 session using aws_auth.botosesh and the region specified in command args.
    response = aws_auth.botosesh.client('ec2', region_name=args.region).describe_instances()
    if aws_auth.validate_response_code(response):
        _raw_response_data = response["Reservations"]
        if _raw_response_data is not None:
            # Checks if region has any instances.
            ec2_instances = []
            for i in enumerate(_raw_response_data, 0):
                # Reformats raw boto3 response data into Ec2Instance objects.
                # If this is ever changed, use '--output json' to help troubleshoot.
                ec2_instances.append(Ec2Instance(_raw_response_data[i[0]]["Instances"][0]))
        # Checks command arg for output type. See --output in _parse_args().
        output = args.output.lower()
        if output == "none":
            pass
        elif output == "print":
            print_output(args.region, ec2_instances)
        elif output == "csv":
            write_output_csv(args.region, ec2_instances)
        elif output == "json":
            write_output_json(response)
        else:
            print("Invalid output type. Please use --help for valid output types.")
    else:
        print("Invalid Request Status Code.")

if __name__ == "__main__":
    _args = _parse_args(sys.argv)
    print(_args)
    main(_args)

"""
To do list
TODO: Ec2Instance.owner_name
TODO: finish function to check for naming convention with regex.
TODO: look at pandas for better csv and json exports
        we need to know usage for naming AND sizing.
TODO: find out if there's any usage pattern match.
        if not, add to a list to message creator.
TODO: future arg functionality:
        multiple regions
        all regions?
        pattern?
        pattern file?
"""