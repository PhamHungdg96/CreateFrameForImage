import cv2
import math
import numpy as np
def create_box_shadow(w, h, padding_size, gradient_from="left" ):
    if gradient_from == "left": 
        img=np.ones((h,w*2,3),dtype=np.uint8)*255
        img[:,:w,:]=(img[:,:w,:]-128)%256
        result=cv2.blur(img, (int(padding_size/3),int(padding_size/3)))
        result=cv2.blur(result, (int(padding_size*2/3),int(padding_size*2/3)))
        # result=cv2.blur(result, (int(padding_size),int(padding_size)))
        return result[:,w:,:]
    elif gradient_from == "top": 
        img=np.ones((h*2,w,3),dtype=np.uint8)*255
        img[:h,:,:]=(img[:h,:,:]-128)%256
        result=cv2.blur(img, (int(padding_size/3),int(padding_size/3)))
        result=cv2.blur(result, (int(padding_size*2/3),int(padding_size*2/3)))
        # result=cv2.blur(result, (int(padding_size),int(padding_size)))
        return result[h:,:,:]
    return None

if __name__ == "__main__":
    img_src=cv2.imread("static/img.jpg")
    padding_size=96*2
    padding_color=(255,255,255)
    h_img, w_img, c_img = img_src.shape
    result= np.full((h_img+padding_size*2,w_img+padding_size*2,c_img), padding_color, dtype=np.uint8)
    #replace background for result

    result_shadow=result.copy()
    shadow_size=padding_size//int(math.sqrt(padding_size))
    result_shadow[:shadow_size,:,:]=200
    result_shadow[:,:shadow_size,:]=200
    result_shadow=cv2.blur(result_shadow, (int(shadow_size*1.2),int(shadow_size*1.2)))
    result=result+result_shadow
    print(shadow_size)
    # result[]
    result[padding_size:h_img+padding_size, padding_size:w_img+padding_size,:] = img_src
    
    cv2.imshow("mask1", result)
    cv2.waitKey()