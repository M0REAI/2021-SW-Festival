from logging import debug
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow_hub as hub
import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
import cv2
import boto3
import os
from datetime import datetime
import shutil
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_image(img_path):
    img = tf.io.read_file(img_path)
    # 이미지 파일을 디코딩
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img 

@app.post("/api/transition")
async def fit(filename:str):
    print(filename)
    # https://stackoverflow.com/questions/53450466/how-tensorflow-read-file-from-s3-bytestream 
    # content_image, style_image 를 s3 버킷 주소로
    # bucket_name =  os.getenv('AWS_BUCKET_NAME')
    bucket_name = 'ywoosang-s3' 
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2') 
    # s3 연결
    s3 = boto3.client(
        "s3",
        aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY_ID')
    )

    # 임시폴더 생성
    basename = 'temp'
    suffix = datetime.now().strftime("%y%m%d_%H%M%S")
    foldername = '_'.join([basename,suffix])
    dir_path = f'./{foldername}'
    os.mkdir(dir_path)
    
    # s3 에서 임시폴더로 다운로드
    s3.download_file(bucket_name,filename,f'./{foldername}/original.jpeg')
    
    # 로컬에 있는 파일 로드
    content_image = load_image(f'./{foldername}/original.jpeg')
    style_image = load_image('./img/style.jpg')

    # 스타일 전이
    stylized_image = model(tf.constant(content_image),tf.constant(style_image))[0]
    
    # cvtColor(입력 이미지,색상 변환 코드, 출력 채널) 
    # 반환: 출력 이미지를 생성
    # https://076923.github.io/posts/Python-opencv-10/
    image = cv2.cvtColor(np.squeeze(stylized_image)*255, cv2.COLOR_BGR2RGB)
    # imwrite()
    # cv2.imwrite(이미지를 저장할 경로, 이미지)
    # https://iagreebut.tistory.com/70
    key = str(datetime.now()) + 'styled.png'
    image_string = cv2.imencode('.png',image)[1].tostring()
    # s3 업로드
    s3.put_object(Bucket=bucket_name ,Key=key, Body=image_string)

    # 임시폴더 지우기 
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

    # Response 로 반환할 URL
    url = f'https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{key}'
    return  {
        "url" : url,
        "key" : key
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,debug=True)