import numpy as np
import cv2
import sys, os
from PIL import Image
from tqdm import tqdm


#[y座標][x座標][ページ番号]

def main(argv):

    if len(argv) == 1:
        image_path = 'Boson_Capture.tiff'
    else:
        image_path = argv[1]
        save_path = argv[2]
    # open_multipage_tiff(image_path)
    convert_tiff_to_mp4(image_path, save_path)



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
    FITC = FITC.transpose(1,2,0)
    print('----tiff(video) info----')
    print(f'(height, width) : ({FITC.shape[0]}, {FITC.shape[1]})')
    print(f'The number of frames : {num_frames}')
    return FITC


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
        frame = (frame - frame.min()) / (frame.max() - frame.min()) * 255
        out.write(frame.astype(np.uint8))

    out.release()



if __name__ == "__main__":
    main(sys.argv)
