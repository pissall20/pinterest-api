import boto3
from settings import *

s3 = boto3.resource(
    service_name='s3',
    region_name=region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

bucket = s3.Bucket('pintrst')
print(bucket)

# s3.Object('pintrst', 'pinpost/image_traits.csv').put(Body=open('/Users/pissall/git/general-coding/Pinterest_App/helpers/image_traits.csv', 'rb'))

for buck_object in bucket.objects.all():
    print(buck_object.key)


