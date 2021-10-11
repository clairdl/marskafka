import os
from dotenv import load_dotenv
import boto3

if __name__ == "__main__":
    load_dotenv()
    # Retrieve the list of existing buckets
    s3 = boto3.client(
        "s3",
        aws_access_key_id= os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key= os.environ.get('AWS_ACCESS_SECRET'),
    )
    response = s3.list_buckets()

    # Output the bucket names
    print("Existing buckets:")
    for bucket in response["Buckets"]:
        print(f'  {bucket["Name"]}')
