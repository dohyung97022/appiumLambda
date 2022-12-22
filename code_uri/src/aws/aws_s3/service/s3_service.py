import boto3

bucket_name = 'appiumapi'


def upload_file(upload_file_name, object_name, bucket=bucket_name, is_public: bool = False):
    extra_args = {'ACL': 'public-read'} if is_public else {}
    boto3.client('s3').upload_file(upload_file_name, bucket, object_name, ExtraArgs=extra_args)


def download_file(object_name, to_file: str, bucket=bucket_name):
    boto3.client('s3').download_file(bucket, object_name, to_file)


def get_presigned_url(object_name, bucket=bucket_name):
    return boto3.client('s3', region_name='us-east-1').generate_presigned_url(
        'get_object', Params={'Bucket': bucket, 'Key': object_name}, ExpiresIn=604800)
