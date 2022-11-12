"""Data class for EC2 instance data."""
class Ec2Instance:
    """
    Filters out irrelevant boto3 EC2 data. Adds custom/enriches current EC2 data.
    Makes tag data easier to work with.
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
        self.do_not_stop = False
        self.tags = self._enumerate_instance_tags(instance_data["Tags"])

    def _enumerate_instance_tags(self, tags_list:list) -> dict:
        tags = {}
        for tag in tags_list:
            tag_key = tag["Key"].lower()
            tag_val = tag["Value"]
            tags[tag_key] = tag_val
            if tag_key == "name":
                self.instance_name = tag_val
            elif tag_key == "owner_email":
                self.instance_email = tag_val
            elif tag_key == "olympus_do_not_stop":
                self.do_not_stop = True
        return tags
    