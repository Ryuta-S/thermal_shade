# coding=utf-8
#
# ===============================================
# Author: RyutaShitomi
# date: 2020-09-05T11:54:30.296Z
# Description: display the tiff file using PySimleGUI
# If you don't install PySimpleGUI yet, you can install below command.
# conda install -c conda-forge pysimplegui
# ===============================================

# built-in or installed packages
import PySimpleGUI as sg
from PIL import Image
import cv2
import io
import os, sys
import numpy as np

# user packages
#from open_multipage_tiff import open_multipage_tiff as omf
import open_multipage_tiff as omt

def main(argv):
    # Get the filename
    filename = sg.popup_get_file('表示したいファイル',
                                 default_path=os.path.join('data', '0000_0829/0000.tiff'),
                                 file_types=(('Tiff Files', '.tiff'), ))
    if filename is None:
        return
    imgs = omt.open_multipage_tiff(filename)

    # Get some Stats
    num_frames = imgs.shape[2]
    fps = 30

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('Video Viewer', size=(15, 1), font='Helvetica 20')],
              [sg.Image(filename="", key='image')],
              [sg.Slider(range=(0, num_frames-1),
                         size=(60, 10), orientation='h', key='slider')],
              [sg.Button('Back', size=(7, 1), font='Helvetica 14'),
               sg.T(' ' * 30),
               sg.Button('Next', size=(7, 1), font='Helvetica 14')],
              [sg.Button('Normalize', size=(7, 1), pad=((100, 0), 3), font='Helvetica 14')],
              [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]]

    # Create the window and show it without the plot
    window = sg.Window('Video Viewer', layout, no_titlebar=False, location=(0, 0))

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window['image']
    slider_elem = window['slider']

    # LOOP throught video file by frame
    cur_frame = 0
    norm_flag = True
    while True:

        # イベントの発生を検知
        event, values = window.read(timeout=0)
        if event in ('Exit', None):
            break
        # スライダーを動かしたらその値に移動する．
        if int(values['slider']) != cur_frame:
            cur_frame = int(values['slider'])
        if event in ('Back'):
            if cur_frame > 0:
                cur_frame -= 1
        if event in ('Next'):
            cur_frame += 1
        if event in ('Normalize'):
            if norm_flag:
                norm_flag = False
            else:
                norm_flag = True


        # 表示するフレームを取得
        frame = imgs[:, :, cur_frame]
        if norm_flag:
            frame = omt.convert_16bit_to_8bit(frame)
        slider_elem.update(cur_frame)
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        image_elem.update(data=imgbytes)

    window.Close()


if __name__ == '__main__':
    main(sys.argv)
