# https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.utils.secure_filename
from werkzeug.utils import secure_filename
from flask import abort
from config.config import Config
from datetime import datetime

 


class UploadService:
    extensitions = ['png','jpg','jpeg']
    def __init__(self,file):
        self.file = file

    # 확장자 체크 
    def is_allowed_extension(self,filename):
        try:
            print(filename)
            extension = filename.rsplit('.',1)[1].lower()
            return  extension in self.extensitions
        except Exception as e:
            print(e)
            return False
    
    # s3 업로드 
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    def upload_file(self):
        # filename = secure_filename(self.file.filename)
        basename = self.file.filename
        prefix = datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([prefix,basename])
        print(filename)
        if not self.is_allowed_extension(filename):
            return abort(403,'file format not allowed')
        # 현재 함수 안에는 except가 없으므로 예외를 상위 코드 블록으로 넘김
        # bucket = os.getenv('AWS_BUCKET_NAME')
        bucket = 'ywoosang-s3'
        s3 = Config.get_connection()
        s3.upload_fileobj(
            self.file,
            bucket,
            filename,
        )
        # https://stackoverflow.com/questions/48608570/python-3-boto-3-aws-s3-get-object-url
        url = f'https://{bucket}.s3.ap-northeast-2.amazonaws.com/{filename}'
        # after upload file to s3 bucket, return filename of the uploaded file
        return url,filename

        



        

    


