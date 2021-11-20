import os
import boto3
 
class Config:
    @staticmethod
    def get_connection():
        s3 = boto3.client(
            "s3",
            aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.getenv('AWS_SECRET_KEY_ID')
        )
        return s3

    
    

    