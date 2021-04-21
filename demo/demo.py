import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
im_dst=cv2.imread('frame.jpg')
h_dst, w_dst, _ =im_dst.shape
im_src=cv2.imread('img.jpg')
h_src, w_src, _ = im_src.shape

pts_src=[]
pts_src.append([0,0])
pts_src.append([w_src,0])
pts_src.append([0,h_src])
pts_src.append([w_src,h_src])
with open('info.json', 'r') as jsonfile:
    info=json.load(jsonfile)
points=info['points']
pts_dst=[]
for point in points:
    pts_dst.append([point['x'],point['y']])

h, status = cv2.findHomography(np.array(pts_src), np.array(pts_dst))
im_mask = cv2.warpPerspective(im_src, h, (w_dst,h_dst))

cv2.imshow("Warped Source Image", cv2.add(im_dst,im_mask))
cv2.waitKey(0)


# plt.figure()
# plt.imshow(img)
# plt.show()