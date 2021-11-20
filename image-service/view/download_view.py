from flask import Blueprint,Response,request,abort
from config.config import Config
import requests
# https://ddolcat.tistory.com/690 

class DownloadView:
    path = '/download'
    router = Blueprint('download_view',__name__,url_prefix='/api/image')
    @router.route(f'{path}',methods=["GET"])
    def get_images():
        bucket_key = request.args.get('bucket_key')
        if not bucket_key:
            return  abort(400,description ='bucket key not found')
        s3 = Config.get_connection()
        try:
            file = s3.get_object(Bucket='ywoosang-s3',Key=bucket_key)
            # json 응답
            return Response(
                file['Body'].read(), # bytes  
                mimetype= 'text/plain',
                headers={"Content-Disposition": f'attachment;filename=original.png'}
            )
        except Exception as e:
            print(e) 
            return abort(400,description ='file not exist in bucket')
    
    @router.route(f'{path}/scrapped',methods=["GET"])
    def get_scraped_image():
        # https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python 
        try:
            scrapped_url = request.args.get('url')
            image = requests.get(scrapped_url,stream=True).raw
            return Response(
                image,
                mimetype= 'text/plain',
                headers={"Content-Disposition": f'attachment;filename=original.jpeg'}
            )
        except Exception as e:
            print(e) 
            return abort(400,description ='file location is incorrect')
    



        

    