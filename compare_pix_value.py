import numpy as np
import cv2
import sys, os
from PIL import Image
import open_multipage_tiff as omt
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

"""
s押下：一時停止　何かキー押すと再生
q押下：終了


ああああ＿テスト
"""


def main():

    image_path = "../../../thermal_shade/images/Boson_Capture_4.tiff"
    image_path = os.path.join('data', 'Boson_Capture_4 2.tiff')
    save_path = os.path.join('data', 'black_T.mp4')
    save_flag = True

    image = omt.open_multipage_tiff(image_path)
    if save_flag:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(save_path, fourcc, 30.0, image.shape[:-1][::-1], 0)
    # 日向のデータ
    sun_vals = []
    # 日陰のデータ
    non_sun_vals = []


    for i in range(image.shape[2]):

        img = image[:,:,i]

        #Boson_Capture_3
        x = 60
        w = 100

        y = 160
        h = 130

        dx = 150

        """
        #Boson_Capture_4
        x = 60
        w = 100

        y = 160
        h = 160

        dx = 150
        """


        ROI_A = img[y:y+h, x:x+w]
        ROI_B = img[y:y+h, x+dx+w :x+ (2*w)+dx]

        im = (img-img.min()) / (img.max()-img.min()) * 255

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(im, (x, y), (x+w,y+h), 255)
        cv2.rectangle(im, (x+dx+w, y), (x+(2*w)+dx, y+h),255)

        cv2.putText(im,str(math.floor(ROI_A.mean())),(90, 140), font, 0.7,255,1,cv2.LINE_AA)
        cv2.putText(im,str(math.floor(ROI_B.mean())),(370, 140), font, 0.7,255,1,cv2.LINE_AA)
        cv2.putText(im,str(i),(20, 20), font, 1,255,1,cv2.LINE_AA)

        print("-------page " + str(i) + " ----------")
        print("ROI_A mean = " + str(math.floor(ROI_A.mean())))
        print("ROI_B mean = " + str(math.floor(ROI_B.mean())) + "\n")


        cv2.imshow('image',im.astype(np.uint8))
        key = cv2.waitKey(3)&0xff
        if save_flag:
            out.write(im.astype(np.uint8))



        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.waitKey(0)

        sun_vals.append(math.floor(ROI_A.mean()))
        non_sun_vals.append(math.floor(ROI_B.mean()))

    np.save('output/compare_pix_value/sun_vals_' + os.path.basename(image_path).split('.')[0],sun_vals)
    np.save('output/compare_pix_value/non_sun_vals_' + os.path.basename(image_path).split('.')[0],non_sun_vals)
    out.release()



if __name__ == "__main__":
    main()
