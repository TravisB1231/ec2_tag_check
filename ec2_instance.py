"""Data class for EC2 instance data."""
class Ec2Instance:
    """
    Filters out irrelevant boto3 EC2 data. Makes tag data easier to work with.
    Adds custom EC2 data.
    """
    def __init__(self, instance_data:dict):
        self.id = instance_data["InstanceId"]
        # self.launch_time = instance_data["LaunchTime"]
        # self.vpc = instance_data["VpcId"]
        # self.subnet = instance_data["SubnetId"]
        # self.state = instance_data["State"]["Name"]
        self.os = instance_data["PlatformDetails"]
        if self.os == "Linux/UNIX":
            self.os = "Ubuntu"
        self.instance_name = None
        self.instance_email = None
        self.tags = self._enumerate_instance_tags(instance_data["Tags"])

    def _enumerate_instance_tags(self, tags_list:list) -> dict:
        tags = {}
        # TODO: dict comprehension
        for tag in tags_list:
            tag_key = tag["Key"]
            tag_val = tag["Value"]
            tags[tag_key] = tag_val
            if tag_key == "Name":
                self.instance_name = tag_val
            elif tag_key == "Owner_Email":
                self.instance_email = tag_val
        return tags
"""
TODO: make new string from Owner_Email tag value and strip everything
    from and after '@' afterward:
    owner_name = [Owner_Email][0] + [Owner_Email][1:]
"""
    