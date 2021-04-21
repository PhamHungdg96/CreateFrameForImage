from flask import Flask, request
from flask_cors import CORS, cross_origin
from frame_prints import load_imgs_frame,add_padding, add_frame
from utils import img2base64, crop
import os
from skimage import io
import cv2
import numpy as np
app = Flask(__name__,static_url_path='/static')
cors = CORS(app)

@app.route('/', methods=['GET'])
def helloworld():
    return "helloworld"

@app.route('/framed_prints', methods=["POST"])
@cross_origin()
def framed_prints():
    padding_size=20
    padding_color=(255,255,255)
    frame_size=20
    frame_name='frame2'
    padding_type=0
    prints_z=1
    print(request.json)
    if not request.json or not "url" in request.json:
        abort(400)
    img_src=io.imread(request.json['url'])
    img_src=cv2.cvtColor(img_src, cv2.COLOR_RGB2BGR)
    h_img, w_img, c_img=img_src.shape
    if 'prints' in request.json:
        prints=request.json['prints']
        if 'zoom' in prints and prints['zoom']>1:
            prints_z=float(prints['zoom'])
        if 'imgW' in prints:
            prints_w=prints['imgW']
        else: prints_w=None
        if 'imgH' in prints:
            prints_h=prints['imgH']
        else: prints_h=None
        if 't' in prints:
            prints_t=prints['t']
        else: prints_t=None
        if 'l' in prints:
            prints_l=prints['l']
        else: prints_l=None
    img_src=crop(img_src,prints_z, prints_w, prints_h, prints_t, prints_l)
    if 'frame' in request.json:
        frame=request.json['frame']
        if 'name' in frame:
            frame_name=frame['name']
        if 'size' in frame:
            frame_size=frame['size']
    if 'padding' in request.json:
        padding=request.json['padding']
        if 'size' in padding:
            padding_size=padding['size']
        if 'color' in padding:
            padding_color=[int(v) for v in str(padding['color']).split(',')]
        if 'type' in padding:
            padding_type=padding['type']
    frames={"T":"top_center", "L":"center_left", "B":"bottom_center", "R":"center_right",
        "TL":"top_left", "BL":"bottom_left", "BR":"bottom_right", "TR":"top_right"}
    frame_name_s=os.listdir('data')
    if not frame_name in frame_name_s:
        abort(400)
    frame_load_imgs=load_imgs_frame(frame_name, frames)
    
    new_img_padding=add_padding(img_src,padding_size, padding_color)
    result=add_frame(new_img_padding, frame_load_imgs, frame_size)
    result=cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return 'data:image/png;base64,'+img2base64(result)

if __name__=="__main__":
    app.run(debug=True, port=5000)