import os
from pred_ppocr_baseline import PredictionPPOCR
import argparse
from PIL import Image
from typing import Text, List
import cv2
import numpy as np

def get_args():
    pass


def deskew(img):
    co_ords = np.column_stack(
        tup = np.where(img > 0)
    )

    angle = cv2.minAreaRect(points=co_ords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    
    H, W = img.shape[:2]
    center = (
        W //2,
        H //2
    )

    M = cv2.getRotationMatrix2D(
        center= center,
        angle= angle,
        scale= 1.0
    )

    rotated = cv2.warpAffine(
        src = img,
        M = M,
        dsize= (W, H),
        flags= cv2.INTER_CUBIC,
        borderMode= cv2.BORDER_REPLICATE
    )

    return rotated

def remove_noise(img):
    return cv2.fastNlMeansDenoisingColored(
        src= img,
        dst= None,
        h = 10,
        hColor= 10,
        templateWindowSize= 7,
        searchWindowSize= 15
    )


def preprocess(
    img_path: Text = 'img/0012.jpg'
)->Image:
    # region 1: Read image
    img = cv2.imread(filename= img_path)
    # cv2.imshow(
    #     winname= 'src',
    #     mat= img
    # )
    H, W = img.shape[:2]
    # endregiom

    # # region 2: Normalization
    # norm_img = np.zeros(shape = (H, W))
    # img = cv2.normalize(
    #     src = img,
    #     dst= norm_img,
    #     alpha= 0,
    #     beta= 255,
    #     norm_type= cv2.NORM_MINMAX
    # )
    # cv2.imshow(
    #     winname= 'normalization',
    #     mat= img
    # )

    # endregion

    # # region Skew Corection
    # img = deskew(img)
    # cv2.imshow(
    #     winname= 'skew corection',
    #     mat= img
    # )

    # # endregion

    # region Noise Removal
    img = remove_noise(img)
    # cv2.imshow(
    #     winname= 'noise_removal',
    #     mat= img
    # )   

    # endregion

    # # region skeletonization
    # kernel = np.ones(
    #     shape= (5,5),
    #     dtype= np.uint8
    # )

    # img = cv2.erode(
    #     src = img,
    #     kernel= kernel,
    #     iterations= 20
    # )

    # cv2.imshow(
    #     winname= 'skeletonization',
    #     mat= img
    # )   
    # # endregion

    # region Histogram equalization
    img_yuv = cv2.cvtColor(
        src = img,
        code = cv2.COLOR_BGR2YUV
    )
    img_yuv[:,:,0] = cv2.equalizeHist(
        src= img_yuv[:,:,0]
    )
    img = cv2.cvtColor(
        src= img_yuv,
        code= cv2.COLOR_YUV2BGR
    )

    basename = os.path.basename(img_path)
    fn = basename.split('.')[0]
    cv2.imwrite(
        filename= f'output/{fn}.png',
        img= img
    )

    # cv2.imshow(
    #     winname= 'histogram_equalization',
    #     mat= img
    # )   
    # endregion
    


if __name__ == "__main__":
    # # region get argument
    # parser = argparse.ArgumentParser()
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
    # # endregon
    preprocess(img_path='img/0019.jpg')
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
