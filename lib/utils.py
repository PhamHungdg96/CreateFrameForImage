from PIL import Image
from io import BytesIO
import base64
import cv2
import re
def img2base64(img):
    pil_img = Image.fromarray(img)
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return "data:image/png;base64," + new_image_string
def crop(img_src, zoom, prints_w, prints_h, top=None, lelf=None):
    img_h, img_w, _=img_src.shape
    if zoom is None: zoom=1
    new_sh, new_sw=int(img_h*zoom), int(img_w*zoom)
    if zoom>1:
        img_src=cv2.resize(img_src, (new_sw, new_sh),interpolation = cv2.INTER_AREA)
    if prints_w is None: prints_w=new_sw
    if prints_h is None: prints_h=new_sh
    assert(prints_w<=new_sw and prints_h<=new_sh)
    if top is None: top=(new_sh-prints_h)//2
    if lelf is None: lelf=(new_sw-prints_w)//2
    return img_src[top:top+prints_h,lelf:lelf+prints_w,:]
def load_img_from_url(url):
    img_src=io.imread(url)
    img_src=cv2.cvtColor(img_src, cv2.COLOR_RGB2BGR)
    return img_src
def load_imgs_frame_url(frames):
    return {"T":load_img_from_url(frames['T']), 
                 "L":load_img_from_url(frames['L']), 
                 "B":load_img_from_url(frames['B']), 
                 "R":load_img_from_url(frames['R']),
                 "TL":load_img_from_url(frames['TL']), 
                 "BL":load_img_from_url(frames['BL']), 
                 "BR":load_img_from_url(frames['BR']), 
                 "TR":load_img_from_url(frames['TR'])}
def de_parse_color(_type):
    result=(255,255,255)
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', _type):
        result=hex_to_rgb(_type)
    elif re.search(r"(\d+),\s*(\d+),\s*(\d+)", _type):
        result=tuple([int(v) for v in _type.split(',')])
    else:
        return _type
    return result

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))