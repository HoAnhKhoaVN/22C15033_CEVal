import os
# from pred_ppocr_baseline import PredictionPPOCR
import argparse
from PIL import Image
from typing import Text, List
import cv2
import numpy as np
from preprocess.contrast import change_contrast
from preprocess.noise import remove_noise
from preprocess.equal_histogram.simple_equalization import equalization

def get_args():
    pass


def preprocess(
    img_path: Text = 'img/0012.jpg'
)->Image:
    # region 1: Read image
    img = cv2.imread(filename= img_path)
    H, W = img.shape[:2]
    # endregion

    # region 2: Noise Removal
    img = remove_noise(img)

    # endregion

    # region 3: Change constrast
    img = change_contrast(img)
    # endregion

    # region 4: Histogram equalization
    img = equalization(img)

    # endregion
    
    return img

if __name__ == "__main__":
    # # region get argument
    # parser = argparse.ArgumentParser()WW
    # parser.add_argument(
    #     '-ip', 
    #     '--img_path', 
    #     help="Path to folder contain images"
    # )
    # parser.add_argument(
    #     '-lb', 
    #     '--json_path',  
    #     help="Path to json"
    # )

    # parser.add_argument(
    #     '-gt', 
    #     '--pred_path',  
    #     help="Path to predicto truth"
    # )

    # args = parser.parse_args()
    # # endregonIMG_PATH
    IMG_PATH = 'img/0012.jpg'
    img = preprocess(img_path= IMG_PATH)
    img = cv2.imread(IMG_PATH)

    print(f'Type img : {type(img)}')
    out = change_contrast(img)
    cv2.imshow(
        winname= 'out',
        mat= out
    )
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    
