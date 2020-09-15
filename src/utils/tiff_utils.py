import numpy as np
import cv2
import sys, os
from PIL import Image
from tqdm import tqdm
import glob

#[y座標][x座標][ページ番号]

def main(argv):

    if len(argv) == 1:
        image_path = os.path.join('..','..','data', '0006_0915','0000.tiff')
    else:
        image_path = argv[1]
        save_path = argv[2]
    open_multipage_tiff(image_path)
    #convert_tiff_to_mp4(image_path, save_path)
    #open_sequense_tiff(os.path.join('..','..','data', '0006_0915','0000'))



def open_multipage_tiff(image_path):
    """ マルチページTiffをnumpy.arrayにして返す．

    Args:
        image_path: tiffファイルのパス
    Return:
        画像の配列. [height][width][frame]
    """
    print(f'load tiff file... {image_path}')
    img_pil = Image.open(image_path)
    FITC = []
    num_frames = img_pil.n_frames # 何枚取り出すか


    try:
        for i in tqdm(range(num_frames)):
            img_pil.seek(i)
            img = np.asarray(img_pil)
            # img.flags.writeable = True
            # img = cv2.resize(img, (512, 512))
            FITC.append(img)

    except EOFError:
        pass

    
    print('loding done!!')
    FITC = np.array(FITC)
    print(FITC.shape)

    FITC = FITC.transpose(1,2,0)
    print('----tiff(video) info----')
    print(f'(height, width) : ({FITC.shape[0]}, {FITC.shape[1]})')
    print(f'The number of frames : {num_frames}')
    return FITC

def open_sequense_tiff(dir_path,npy_save = False):
    """ シーケンスTiffをnumpy.arrayにして返す．

    Args:
        dir_path: シーケンスtiffが入っているフォルダのパス
    Return:
        画像の配列. [height][width][frame]
    """
    image = []

    file_names = glob.glob(dir_path + "\\*.tif")
    for i in tqdm(range(len(file_names))):
        #ファイル名昇順にした方がいい
        file_names[i] = os.path.basename(file_names[i])
        img = cv2.imread(dir_path + "\\" + file_names[i],-1)
        image.append(img)

    image = np.array(image)
    image = image.transpose(1,2,0)

    if npy_save == True:
        np.save(dir_path + "\\0000.npy",image)

    return image



def convert_tiff_to_mp4(image_path, save_path):
    """ マルチページTiffをmp4に変換する

    Args:
        image_path: tiffファイルのパス
        save_path: 変換したmp4ファイルを保存するパス
    """
    # フレーム列を取得
    imgs = open_multipage_tiff(image_path)

    # 保存するためのwriter等の定義
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(save_path, fourcc, 30.0, imgs.shape[:-1][::-1], 0)

    for i in range(imgs.shape[2]):
        frame = imgs[:, :, i]
        #frame = (frame - frame.min()) / (frame.max() - frame.min()) * 255
        #out.write(frame.astype(np.uint8))
        out.write(convert_16bit_to_8bit(frame))
    out.release()

def convert_16bit_to_8bit(image):
    """ 16bit 1ch画像を8bit 1ch画像に変換する

    Args:
        image: 16bit 1ch画像 ndarray.uint16
    Retuern:
        8bit 1ch画像 ndarray.uint8
    """
    frame = (image - image.min()) / (image.max() - image.min()) * 255
    return frame.astype(np.uint8)




def convert_1ch_to_3ch(image):
    """ 16bit 1ch画像を 8bit 3ch画像に拡張する関数です．ピクセル値をチャンネル方向にコピーしてます．
        multipage_tiffの場合は何フレーム目かを指定するのを忘れずに．

    Args:
        image: 16bit 1ch画像　ndarray.uint16
    Retuern:
        8bit 3ch画像 ndarray.uint8
    """

    image = np.repeat(image[:,:,np.newaxis],3,axis=2)
    image = convert_16bit_to_8bit(image)

    return image



if __name__ == "__main__":
    main(sys.argv)
