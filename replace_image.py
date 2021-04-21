import cv2
import numpy as np
import math

def replace_image_x(w, img_bg):
    h_i, w_i, c_i=img_bg.shape
    assert(w>w_i)
    r_x=w//w_i+1
    # print(w, w_i, r_x)
    result=[]
    for n in range(r_x):
        if n==0:
            result=img_bg.copy()
        else:
            result=np.concatenate((result, img_bg), axis=1)
    return result[:, :w, :]
def replace_image_y(h, img_bg):
    h_i, w_i, c_i=img_bg.shape
    assert(h>h_i)
    r_y=h//h_i+1
    # print(h, h_i, r_y)
    result=[]
    for n in range(r_y):
        if n==0:
            result=img_bg.copy()
        else:
            result=np.concatenate((result, img_bg), axis=0)
    return result[:h, :, :]
def replace_image(w,h,img_bg):
    result=replace_image_x(w, img_bg)
    result=replace_image_y(h, result)
    return result
if __name__=="__main__":
    img_bg=cv2.imread('data/background/PM988-square.jpg')
    result=replace_image(1000, 800, img_bg)
    cv2.imshow("input", result)
    cv2.waitKey()