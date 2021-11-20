from flask import Blueprint,Response,request,abort
import json
from service.upload_service import UploadService

class UploadView:
    path = '/upload'
    router = Blueprint('upload_view',__name__,url_prefix='/api/image')
    @router.route(f'{path}',methods=["POST"])
    def upload_images():
        if 'original_image' not in request.files:
            # https://stackoverflow.com/questions/5604816/whats-the-most-appropriate-http-status-code-for-an-item-not-found-error-page
            return abort(404,description="file not found")
        # HTTP request
        file = request.files['original_image']
        [url,filename] = UploadService(file).upload_file()
        if url and filename:
            response = {
                'url' : url,
                'filename': filename 
            }
            # json 응답
            return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')
        else:
            abort(400,description = 'upload failed')
    
         