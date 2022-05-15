import boto3

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIAXKDSHQRIMUFB7ZN7',
    aws_secret_access_key='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'
)

bucket = s3.Bucket('pintrst')
print(bucket)

for buck_object in bucket.objects.all():
    print(buck_object.key)

