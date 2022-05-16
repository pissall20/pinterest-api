import os
import sys
import boto3

# To fix path issues for import
sys.path.insert(0, os.getcwd())
from settings import *

s3 = boto3.resource(
    service_name='s3',
    region_name=region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

bucket = s3.Bucket(bucket_name)
print(bucket)

# s3.Object('pintrst', 'pinpost/image_traits.csv').put(Body=open('/Users/pissall/git/general-coding/Pinterest_App/helpers/image_traits.csv', 'rb'))
# object_delete = 'pinpost/image_traits.csv'
# s3.Object("pintrst", object_delete).delete()
# print("Object deletion successful")

list_of_files = list()

for buck_object in bucket.objects.all():
    print(buck_object.key)

    if buck_object.key == f"{folder_name}/":
        continue
    list_of_files.append(buck_object.key)
    save_local_file = buck_object.key.split("/")[1]
    local_file_path = os.path.join(os.getcwd(), "json_files", save_local_file)
    bucket.download_file(buck_object.key, local_file_path)

print(len(list_of_files))
