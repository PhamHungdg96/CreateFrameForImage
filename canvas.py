import cv2
import math
import numpy as np

def canvas_right(img, alpha, size=30):
    h, w, _ =img.shape
    img_crop=img[:, w-size:w,:]
    h, w, c=img_crop.shape
    img_crop=cv2.flip(img_crop, 1)
    img_blend=np.zeros((h, w, c), dtype=np.uint8)
    img_crop = cv2.addWeighted(img_crop, 0.6, img_blend, 0.4, 0.0)

    alpha=math.pi/4-alpha
    pts_src=[]
    pts_src.append([0,0])
    pts_src.append([0,h])
    pts_src.append([w,0])
    pts_src.append([w,h])

    pts_dst=[]
    pts_dst.append([0,0])
    pts_dst.append([0,h])
    pts_dst.append([w*math.cos(alpha),w*math.sin(alpha)])
    pts_dst.append([w*math.cos(alpha),h-w*math.sin(alpha)])

    homo, status = cv2.findHomography(np.array(pts_src), np.array(pts_dst))
    im_mask = cv2.warpPerspective(img_crop, homo, (int(w*math.cos(alpha)),h), borderValue=(255,255,255))
    return im_mask

def canvas_left(img, alpha):
    h, w, _ = img.shape
    pts_src=[]
    pts_src.append([0,0])
    pts_src.append([0,h])
    pts_src.append([w,0])
    pts_src.append([w,h])

    pts_dst=[]
    pts_dst.append([w*(1-math.cos(alpha)),w*math.sin(alpha)])
    pts_dst.append([w*(1-math.cos(alpha)),h-w*math.sin(alpha)])
    pts_dst.append([w,0])
    pts_dst.append([w,h])

    homo, status = cv2.findHomography(np.array(pts_src), np.array(pts_dst))
    im_mask = cv2.warpPerspective(img, homo, (int(w*(1-math.cos(alpha))),h), borderValue=(255,255,255))
    return im_mask

def append_img(imgl, imgr):
    hl,wl,cl=imgl.shape
    hr,wr,cr=imgr.shape
    assert hl==hr
    assert cl==cr
    new_img=np.ones((hl,wl+wr, cl), dtype=np.uint8)*255
    new_img[:,:wl,:]=imgl
    new_img[:,wl:,:]=imgr
    return new_img

if __name__ == "__main__":
    img=cv2.imread("data/img2.png")
    h, w, c = img.shape
    alpha=math.pi/180*max(h, w)/min(h,w)
    _canvas_left=canvas_left(img, alpha)
    _canvas_right=canvas_right(img, alpha)
    result=append_img(_canvas_left, _canvas_right)
    print(result)
    cv2.imwrite("output.png",result)
    cv2.imshow("input", result)
    cv2.waitKey()

