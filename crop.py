import cv2
import numpy as np
from skimage import io

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

if __name__=="__main__":
    img_src=io.imread('static/img.jpg')
    img_src=cv2.cvtColor(img_src, cv2.COLOR_RGB2BGR)
    result=crop(img_src, 1 ,None, None)
    cv2.imshow("input", result)
    cv2.waitKey()