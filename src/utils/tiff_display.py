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
import tiff_utils as tu

def main(argv):
    Bcal = 19.32029522054909
    Rcal = 1896.4810262642202
    Fcal = 1.0623746441660586
    # Get the filename
    filename = sg.popup_get_file('表示したいファイル',
                                 default_path=os.path.join('..','..','data', '0006_0915','0000'),
                                 file_types=(('Tiff Files', '.tiff'), ))
    if filename is None:
        return
    #imgs = tu.open_multipage_tiff(filename)
    #imgs = np.load(filename)
    imgs = tu.open_sequense_tiff(filename)

    # Get some Stats
    num_frames = imgs.shape[2]
    fps = 30

    sg.theme('Black')

    #画像の拡大率
    zoom_level = 1.0

    col = [[sg.Text('Max', key='max_temp', size=(10, 1), pad=((0,0),(0,int(33.3 * zoom_level))), font='Helvetica 14')],
           [sg.Text('Max', key='p5_temp', size=(10, 1), pad=((0,0),(int(33.3 * zoom_level),int(33.3 * zoom_level))), font='Helvetica 14')],
           [sg.Text('Max', key='p4_temp', size=(10, 1), pad=((0,0),(int(33.3 * zoom_level),int(33.3 * zoom_level))), font='Helvetica 14')],
           [sg.Text('Max', key='p3_temp', size=(10, 1), pad=((0,0),(int(33.3 * zoom_level),int(33.3 * zoom_level))), font='Helvetica 14')],
           [sg.Text('Max', key='p2_temp', size=(10, 1), pad=((0,0),(int(33.3 * zoom_level),int(33.3 * zoom_level))), font='Helvetica 14')],
           [sg.Text('Max', key='p1_temp', size=(10, 1), pad=((0,0),(int(33.3 * zoom_level),int(33.3 * zoom_level))), font='Helvetica 14')],
           [sg.Text('Max', key='min_temp', size=(10, 1), pad=((0,0),(int(33.3 * zoom_level),0)), font='Helvetica 14')],]



    # define the window layout
    layout = [[sg.Text('Video Viewer', size=(15, 1), font='Helvetica 20')],
              [sg.Image(filename="", key='image'),sg.Graph((500,500),(300,300),(100,100),key='graph'),sg.Image(filename="", key='colorbar'),sg.Column(col)],
              [sg.Slider(range=(0, num_frames-1),
                         size=(int(60 * zoom_level), 10), orientation='h', key='slider')],
              [sg.Button('Back', size=(7, 1), font='Helvetica 14'),
               sg.T(' ' * 30),
               sg.Button('Next', size=(7, 1), font='Helvetica 14')],
              [sg.Button('Pseudo_color', auto_size_button=True, pad=((100, 0), 3), font='Helvetica 14')],
              [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]]

    # Create the window and show it without the plot
    window = sg.Window('Video Viewer', layout, no_titlebar=False, location=(0, 0))

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window['image']
    slider_elem = window['slider']
    colorbar_elem = window['colorbar']
    max_temp_elem = window['max_temp']
    p5_temp_elem = window['p5_temp']
    p4_temp_elem = window['p4_temp']
    p3_temp_elem = window['p3_temp']
    p2_temp_elem = window['p2_temp']
    p1_temp_elem = window['p1_temp']
    min_temp_elem = window['min_temp']
    graph_elem = window['graph']

    colorbar = get_gradation_2d(255, 0, 15, int(512 * zoom_level), False)
    colorbar = cv2.applyColorMap(colorbar.astype(np.uint8),cv2.COLORMAP_HOT)
    colorbar_bytes = cv2.imencode('.png', colorbar)[1].tobytes()


    # LOOP throught video file by frame
    cur_frame = 0
    Pseudo_color_flag = False
    while True:

        # イベントの発生を検知
        event, values = window.read(timeout=0)
        if event in ('Exit', None):
            break

        # 温度を求める式
        camera_temp = 42.3
        Ocal = -142.5463107245369 * camera_temp + 25603.74739193574



        # スライダーを動かしたらその値に移動する．
        if int(values['slider']) != cur_frame:
            cur_frame = int(values['slider'])
        if event in ('Back'):
            if cur_frame > 0:
                cur_frame -= 1
        if event in ('Next'):
            cur_frame += 1
        if event in ('Pseudo_color'):
            if Pseudo_color_flag:
                Pseudo_color_flag = False
            else:
                Pseudo_color_flag = True


        # 表示するフレームを取得
        frame = imgs[:, :, cur_frame]
        temp = Bcal / np.log((Rcal / (frame * 0.98 -Ocal)) + Fcal)

        frame = tu.convert_16bit_to_8bit(frame)
        frame = cv2.resize(frame , (int(frame.shape[1] * zoom_level), int(frame.shape[0] * zoom_level)))




        if Pseudo_color_flag:
            frame = cv2.applyColorMap(frame,cv2.COLORMAP_HOT)
            colorbar = get_gradation_2d(255, 0, 15, int(512 * zoom_level), False)
            colorbar = cv2.applyColorMap(colorbar.astype(np.uint8),cv2.COLORMAP_HOT)
        else:
            colorbar = get_gradation_2d(255, 0, 15, int(512 * zoom_level), False)

        slider_elem.update(cur_frame)
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        colorbar_bytes = cv2.imencode('.png', colorbar)[1].tobytes()


        image_elem.update(data=imgbytes)
        colorbar_elem.update(data=colorbar_bytes)
        graph_elem.DrawImage(filename = "",data = imgbytes)
        max_temp_elem.update('--  ' + str(round(temp.max(),2)))
        p5_temp_elem.update('--  ' + str(round((temp.max()-temp.min())*5 / 6 + temp.min(),2)))
        p4_temp_elem.update('--  ' + str(round((temp.max()-temp.min())*4 / 6 + temp.min(),2)))
        p3_temp_elem.update('--  ' + str(round((temp.max()-temp.min())*3 / 6 + temp.min(),2)))
        p2_temp_elem.update('--  ' + str(round((temp.max()-temp.min())*2 / 6 + temp.min(),2)))
        p1_temp_elem.update('--  ' + str(round((temp.max()-temp.min())*1 / 6 + temp.min(),2)))
        min_temp_elem.update('--  ' + str(round(temp.min(),2)))


    window.Close()



def get_gradation_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T



if __name__ == '__main__':
    main(sys.argv)
