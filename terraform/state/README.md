# Add Tags to Terraform State

This Python script, `add_tags_to_state.py`, updates a specified Terraform state file stored in AWS S3 by adding a new tag or updating the value of an existing tag for all resources. It also creates a backup of the state file before making any modifications.

## Features

- Tag Addition and Update: Adds a new tag or updates an existing tag across all resources in the Terraform state file.
- Automatic Backup: Creates a backup of the Terraform state file with a unique timestamp before making any changes.
- Support for AWS S3: Works directly with Terraform state files stored in AWS S3.

## Requirements

- Python 3.x
- Boto3 library
- AWS CLI (optional, for AWS credentials configuration)

## Setup

1. Install Boto3: Boto3 is required to interact with AWS services. Install it using pip:

   ```bash
   pip install boto3
   ```

2. AWS Credentials: Ensure your AWS credentials are configured. You can do this by setting environment variables, using the AWS CLI ("aws configure"), or by any other method supported by Boto3 and your AWS setup.

## Usage

Run the script from the command line, specifying the S3 bucket and path to the Terraform state file, as well as the tag name and value you wish to add or update.

```bash
./add_tags_to_state.py --state=s3://your-bucket/path/to/terraform.tfstate --tag-name=yourTagName --tag-value=yourTagValue
```

### Parameters

- --state: The S3 URL of the Terraform state file. Format: s3://bucket/key.
- --tag-name: The name of the tag to add or update in the state file.
- --tag-value: The value of the tag to add or update in the state file.

### Example

```bash
./add_tags_to_state.py --state="s3://mybucket/terraform/state/prod.tfstate" --tag-name="Environment" --tag-value="Production"
```

This command will update the prod.tfstate file in the mybucket S3 bucket, setting the Environment tag to Production for all resources. It will also create a backup of the original state file.

## AWS Credentials Configuration

The script uses Boto3 to interact with AWS S3. Boto3 will automatically use the AWS credentials configured on your system. You can set up your credentials in several ways:

- Environment Variables: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
- AWS Credentials File: Located at `~/.aws/credentials`.
- AWS CLI: Run "aws configure" to set up your credentials.

Ensure that the IAM role or user associated with these credentials has permissions to read from and write to the specified S3 bucket.

## Caution

Directly manipulating Terraform state files can lead to inconsistencies between your infrastructure and state data. Always ensure you have a backup and understand the changes being made.

