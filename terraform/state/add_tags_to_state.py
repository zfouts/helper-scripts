#!/usr/bin/env python3
import json
import boto3
import argparse
import time
from botocore.exceptions import NoCredentialsError

class TerraformStateModifier:
    def __init__(self, s3_bucket, s3_key):
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.state_data = None

    def backup_state_file(self):
        """Create a backup of the Terraform state file."""
        backup_key = f"{self.s3_key}.backup_tagging_{int(time.time())}"
        s3 = boto3.client('s3')
        copy_source = {
            'Bucket': self.s3_bucket,
            'Key': self.s3_key
        }
        s3.copy(copy_source, self.s3_bucket, backup_key)
        print(f"Backup created: {backup_key}")

    def load_state_file(self):
        """Load the Terraform state file from S3."""
        try:
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=self.s3_bucket, Key=self.s3_key)
            self.state_data = json.loads(response['Body'].read())
        except NoCredentialsError:
            print("Error: AWS credentials not found.")
            exit(1)

    def save_state_file(self):
        """Save the modified Terraform state file back to S3."""
        try:
            s3 = boto3.client('s3')
            s3.put_object(Bucket=self.s3_bucket, Key=self.s3_key, Body=json.dumps(self.state_data, indent=2))
        except NoCredentialsError:
            print("Error: AWS credentials not found.")
            exit(1)

    def add_tag_to_resource(self, resource, tag_name, tag_value):
        """Add or update a tag for a given resource."""
        if 'tags' in resource['attributes']:
            resource['attributes']['tags'][tag_name] = tag_value
        elif 'tags_all' in resource['attributes']:
            resource['attributes']['tags_all'][tag_name] = tag_value

    def modify_state(self, new_tag_name, new_tag_value):
        """Modify the Terraform state file to include a new tag."""
        self.backup_state_file()  # Backup the original state file before modifications
        self.load_state_file()
        for module in self.state_data.get('resources', []):
            for resource in module.get('instances', []):
                self.add_tag_to_resource(resource, new_tag_name, new_tag_value)
        self.state_data['serial'] += 1  # Increment the serial number
        self.save_state_file()

def main():
    parser = argparse.ArgumentParser(description='Update Terraform state file tags in AWS S3.')
    parser.add_argument('--state', required=True, help='S3 URL of the Terraform state file (format: s3://bucket/key)')
    parser.add_argument('--tag-name', required=True, help='The name of the tag to add or update in the state file')
    parser.add_argument('--tag-value', required=True, help='The value of the tag to add or update in the state file')

    args = parser.parse_args()

    if args.state.startswith('s3://'):
        s3_path = args.state[5:].split('/', 1)
        s3_bucket, s3_key = s3_path[0], s3_path[1]
    else:
        raise ValueError("State file path must start with s3://")

    modifier = TerraformStateModifier(s3_bucket=s3_bucket, s3_key=s3_key)
    modifier.modify_state(args.tag_name, args.tag_value)

if __name__ == "__main__":
    main()

