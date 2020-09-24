import numpy as np
import cv2
import sys, os
from PIL import Image
import utils.tiff_utils as tu
import utils.raw2temp as rt
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

"""
s押下：一時停止　何かキー押すと再生
q押下：終了
"""


def main():
    compare_temp_value()


def compare_temp_value():

    image_path = os.path.join('..','data', '0006_0915','0001')
    save_path = os.path.join('..','data', '0006_0915','black_T.mp4')
    save_flag = True

    #image = tu.open_multipage_tiff(image_path)
    image = tu.open_sequense_tiff(image_path)

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
        x = 130
        w = 120

        y = 200
        h = 150

        dx = 190

        temp = rt.raw2temp(img,47.0)

        ROI_A = temp[y:y+h, x:x+w]
        ROI_B = temp[y:y+h, x+dx+w :x+ (2*w)+dx]

        im = tu.convert_16bit_to_8bit(img)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(im, (x, y), (x+w,y+h), 255)
        cv2.rectangle(im, (x+dx+w, y), (x+(2*w)+dx, y+h),255)

        cv2.putText(im,str(round(ROI_A.mean(),1)),(x,y), font, 0.7,255,1,cv2.LINE_AA)
        cv2.putText(im,str(round(ROI_B.mean(),1)),(x+w+dx,y), font, 0.7,255,1,cv2.LINE_AA)
        cv2.putText(im,str(i),(20, 20), font, 1,255,1,cv2.LINE_AA)

        print("-------page " + str(i) + " ----------")
        print("ROI_A mean = " + str(math.floor(ROI_A.mean())))
        print("ROI_B mean = " + str(math.floor(ROI_B.mean())) + "\n")


        cv2.imshow('image',im)
        key = cv2.waitKey(1)&0xff
        if save_flag:
            out.write(im)

        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.waitKey(0)

        sun_vals.append(round(ROI_A.mean(),1))
        non_sun_vals.append(round(ROI_B.mean(),1))

    #np.save('data/0006_0925/sun_vals_' + os.path.basename(image_path).split('.')[0],sun_vals)
    #np.save('data/0006_0925/non_sun_vals_' + os.path.basename(image_path).split('.')[0],non_sun_vals)
    #np.save('../data/0006_0915/sun_vals_0001.npy',sun_vals)
    #np.save('../data/0006_0915/non_sun_vals_0001.npy',non_sun_vals)
    np.save(os.path.join('..','data', '0006_0915','sun_vals_0001.npy'),sun_vals)
    np.save(os.path.join('..','data', '0006_0915','non_sun_vals_0001.npy'),non_sun_vals)
    out.release()




def compare_raw_value(): 

    image_path = os.path.join('..','data', '0006_0915','0000')
    save_path = os.path.join('..','data', '0006_0915','white_T.mp4')
    save_flag = True

    #image = tu.open_multipage_tiff(image_path)
    image = tu.open_sequense_tiff(image_path)

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
        x = 130
        w = 120

        y = 200
        h = 150

        dx = 120

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

        im = tu.convert_16bit_to_8bit(img)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(im, (x, y), (x+w,y+h), 255)
        cv2.rectangle(im, (x+dx+w, y), (x+(2*w)+dx, y+h),255)

        cv2.putText(im,str(math.floor(ROI_A.mean())),(x,y), font, 0.7,255,1,cv2.LINE_AA)
        cv2.putText(im,str(math.floor(ROI_B.mean())),(x+w+dx,y), font, 0.7,255,1,cv2.LINE_AA)
        cv2.putText(im,str(i),(20, 20), font, 1,255,1,cv2.LINE_AA)

        print("-------page " + str(i) + " ----------")
        print("ROI_A mean = " + str(math.floor(ROI_A.mean())))
        print("ROI_B mean = " + str(math.floor(ROI_B.mean())) + "\n")


        cv2.imshow('image',im)
        key = cv2.waitKey(3)&0xff
        if save_flag:
            out.write(im)

        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.waitKey(0)

        sun_vals.append(math.floor(ROI_A.mean()))
        non_sun_vals.append(math.floor(ROI_B.mean()))

    #np.save('data/0006_0925/sun_vals_' + os.path.basename(image_path).split('.')[0],sun_vals)
    #np.save('data/0006_0925/non_sun_vals_' + os.path.basename(image_path).split('.')[0],non_sun_vals)
    #np.save('../data/0006_0915/sun_vals_0001.npy',sun_vals)
    #np.save('../data/0006_0915/non_sun_vals_0001.npy',non_sun_vals)
    np.save('..','data', '0006_0915','sun_vals_0000.npy',sun_vals)
    np.save('..','data', '0006_0915','non_sun_vals_0000.npy',non_sun_vals)
    out.release()


if __name__ == "__main__":
    main()
