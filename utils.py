from PIL import Image
from io import BytesIO
import base64
import cv2
def img2base64(img):
    pil_img = Image.fromarray(img)
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return new_image_string
def crop(img_src, zoom, prints_w, prints_h, top=None, lelf=None):
    img_h, img_w, _=img_src.shape
    new_sh, new_sw=int(img_h*zoom), int(img_w*zoom)
    img_src=cv2.resize(img_src, (new_sw, new_sh),interpolation = cv2.INTER_AREA)
    if prints_w is None: prints_w=new_sw
    if prints_h is None: prints_h=new_sh
    assert(prints_w<=new_sw and prints_h<=new_sh)
    if top is None: top=(new_sh-prints_h)//2
    if lelf is None: lelf=(new_sw-prints_w)//2
    return img_src[top:top+prints_h,lelf:lelf+prints_w,:]