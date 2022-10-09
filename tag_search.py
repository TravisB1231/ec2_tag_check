"""Creates a CSV file of all EC2 instances' tags in a region.
CSV contains Region name, Instance ID, Instance Name, and Owner_Email."""
import re
from aws_auth import botosesh
from olympus_patterns import patterns

def _check_response_code(resp:dict) -> bool:
    status = resp["ResponseMetadata"]["HTTPStatusCode"]
    if 200 <= status < 400:
        return True
    print("Invalid response.")
    return False

def write_output(file, rgn:str, inst_id:str, inst_name:str, inst_email:str) -> None:
    """Writes to outputfile in csv format. Columns align with parameter names."""
    # Region
    file.write(rgn + ",")
    # Instance id
    file.write(inst_id +  ",")
    # Name
    file.write(inst_name + ",")
    # Owner_Email
    file.write(inst_email + ",")
    # End of row
    file.write("\n")

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

# print(check_for_match("os", "windows2012"))

if __name__ == "__main__":
    region = {
    "east1" : 'us-east-1',
    "east2" : 'us-east-2'
    }
    response = botosesh.client('ec2', region_name=region["east1"]).describe_instances()
    if _check_response_code(response):
        instances = response["Reservations"]
        region = botosesh.region_name
        with open("output.csv", 'w', encoding="UTF-8") as outfile:
            # CSV Column names
            outfile.write("Region,ID,Name,Email\n")
            # Instance loop - Loop through each individual instance
            for i in enumerate(instances):
                instanceName = '<<< NO "Name" TAG FOUND >>>'
                instanceEmail = '<<< NO "Owner_Email" TAG FOUND >>>'
                instanceId = instances[i[0]]["Instances"][0]["InstanceId"]
                instanceTags = instances[i[0]]["Instances"][0]["Tags"]
                # Tag loop - Loop through each of the individual instance's tags
                for j in enumerate(instanceTags):
                    tagKey = instanceTags[j[0]]["Key"]
                    if tagKey == "Name":
                        # TODO: Function for checking for naming convention with regex.
                        # Pass which pattern as argument
                        instanceName = instanceTags[j[0]]["Value"]
                    elif tagKey == "Owner_Email":
                        instanceEmail = instanceTags[j[0]]["Value"]
                write_output(outfile, region, instanceId, instanceName, instanceEmail)
    else:
        print("Invalid Request Status Code.")

"""
# For testing only:
import json
    with open("output.json", 'w') as outputfile:
        outputfile.write(json.dumps(response, default=str))

TODO: make new string from Owner_Email tag value and strip everything from and after '@'
        afterward:
        owner_name = [Owner_Email][0] + [Owner_Email][1:]
TODO: translate OS from PlatformDetails:
        Linux/UNIX = Ubuntu (Inferred)
        find a match from this and create instanceOS based on this
TODO: find out if there's any usage pattern match.
        if not, add to a list to message creator.
        we need to know usage for naming AND sizing.
f'{owner_name}-support-{instanceOS}-{usage_patterns[match]}'
"""