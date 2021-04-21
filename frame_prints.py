import cv2
import numpy as np
from skimage import io
import math
from replace_image import replace_image

def frame_padding_top_or_bottom(frame_top_or_bottom, frame_size, new_w):
    img_p=frame_top_or_bottom.copy()
    img_nsize = cv2.resize(img_p, (img_p.shape[1],frame_size), interpolation = cv2.INTER_LINEAR)
    result = cv2.copyMakeBorder(img_nsize,0,0,0,new_w-img_p.shape[1],cv2.BORDER_REPLICATE)
    return result

def frame_padding_left_or_right (frame_top_or_bottom, frame_size, new_h):
    img_p=frame_top_or_bottom.copy()
    img_nsize = cv2.resize(img_p, (frame_size,img_p.shape[0]), interpolation = cv2.INTER_LINEAR)
    result = cv2.copyMakeBorder(img_nsize,0,new_h-img_p.shape[0],0,0,cv2.BORDER_REPLICATE)
    return result

def frame_coner_resize(frame_coner, frame_size):
    img_p=frame_coner.copy()
    img_nsize = cv2.resize(img_p, (frame_size,frame_size), interpolation = cv2.INTER_LINEAR)
    return img_nsize

def load_img(data_path, s_name):
    return cv2.imread('data/%s/%s_%s.jpg'%(data_path, data_path,s_name))


def add_padding(img_src, padding_size, padding_color, img_bg=None, gama=128, border_outline_img=10):
    h_img,w_img,c_img=img_src.shape
    result_border=np.full((h_img+border_outline_img*2,w_img+border_outline_img*2,c_img), padding_color, dtype=np.uint8)

    result= np.full((h_img+padding_size*2,w_img+padding_size*2,c_img), padding_color, dtype=np.uint8)

    shadow_size=padding_size//int(math.sqrt(padding_size))
    result[:shadow_size,:,:]=220
    result[:,:shadow_size,:]=220
    result[:shadow_size//2,:,:]=200
    result[:,:shadow_size//2,:]=200
    result=cv2.blur(result, (int(shadow_size*1.2),int(shadow_size*1.2)))

    if not img_bg is None:
        result_bg=replace_image(w_img+padding_size*2, h_img+padding_size*2, img_bg)
        result=cv2.bitwise_and(result_bg, result)

    
    result[padding_size-border_outline_img:h_img+padding_size+border_outline_img, padding_size-border_outline_img:w_img+padding_size+border_outline_img,:] = result_border
    result=cv2.blur(result, (3,3))
    result[padding_size:h_img+padding_size, padding_size:w_img+padding_size,:] = img_src
    # box_shadow_left=create_box_shadow(padding_size, h_img+padding_size*2, int(padding_size/2), gradient_from="left")
    # box_shadow_top=create_box_shadow(w_img+padding_size*2, padding_size, int(padding_size/2), gradient_from="top")
    # result[:, :padding_size,:]= 0
    # result[:, :padding_size,:]=cv2.add(result[:, :padding_size,:],box_shadow_left)
    # result[:padding_size, padding_size:,:]=0
    # result[:padding_size, :,:]=result[:padding_size, :,:]+box_shadow_top
    return result

def add_frame(img_src, frames, frame_size):
    h, w, c=img_src.shape
    result=np.zeros((h+frame_size*2,w+frame_size*2,c),dtype=np.uint8)
    result[frame_size:h+frame_size, frame_size:w+frame_size,:]=img_src

    result[0:frame_size, 0:frame_size,:]=frame_coner_resize(frames['TL'],frame_size)
    result[0:frame_size, frame_size:w+frame_size,:]=frame_padding_top_or_bottom(frames['T'],frame_size,w)
    result[0:frame_size, w+frame_size:,:]=frame_coner_resize(frames['TR'],frame_size)

    result[h+frame_size:, 0:frame_size,:]=frame_coner_resize(frames['BL'],frame_size)
    result[h+frame_size:, frame_size:w+frame_size,:]=frame_padding_top_or_bottom(frames['B'],frame_size,w)
    result[h+frame_size:, w+frame_size:,:]=frame_coner_resize(frames['BR'],frame_size)
    
    result[frame_size:h+frame_size, 0:frame_size,:]=frame_padding_left_or_right(frames['L'],frame_size,h)
    result[frame_size:h+frame_size, w+frame_size:,:]=frame_padding_left_or_right(frames['R'],frame_size,h)

    return result

def load_imgs_frame(data_path, frames):
    return {"T":load_img(data_path,frames['T']), 
                 "L":load_img(data_path,frames['L']), 
                 "B":load_img(data_path,frames['B']), 
                 "R":load_img(data_path,frames['R']),
                 "TL":load_img(data_path,frames['TL']), 
                 "BL":load_img(data_path,frames['BL']), 
                 "BR":load_img(data_path,frames['BR']), 
                 "TR":load_img(data_path,frames['TR'])}

if __name__ == "__main__":
    data_path='frame4'
    frames={"T":"top_center", "L":"center_left", "B":"bottom_center", "R":"center_right",
        "TL":"top_left", "BL":"bottom_left", "BR":"bottom_right", "TR":"top_right"}
    frame_load_imgs=load_imgs_frame(data_path, frames)
    # img_src=io.imread('http://127.0.0.1:5000/static/img.jpg')
    img_src=io.imread('static/img.jpg')
    img_bg=cv2.imread('data/background/PM988-square.jpg')
    img_src=cv2.cvtColor(img_src, cv2.COLOR_RGB2BGR)
    # img_src=cv2.imread('static/img2.png')
    padding_size=96
    padding_color=(255,255,255)
    frame_size=96
    img_h, img_w, _=img_src.shape
    print_size_w=30 * 96 #inch
    print_size_h=int(img_h/img_w*print_size_w)
    img_src=cv2.resize(img_src, (print_size_w, print_size_h),interpolation = cv2.INTER_AREA)

    new_img_padding=add_padding(img_src,padding_size, padding_color,img_bg=img_bg)
    result=add_frame(new_img_padding, frame_load_imgs, frame_size)
    # frame_bottom_new=frame_padding_top_or_bottom(frame_bottom, frame_size,w_img+padding_size*2 )
    # result=create_box_shadow(100,100,50, gradient_from="top")
    cv2.imshow("input", result)
    cv2.waitKey()