import os
from pred_ppocr_baseline import PredictionPPOCR
import argparse
from PIL import Image
from typing import Text, List, Dict
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

class PredPPOCRWithPreprocess(PredictionPPOCR):
    def __init__(
        self,
        image_path: Text,
        json_name: Text,

        debug: bool = True
    ) -> None:
        super().__init__(image_path, json_name, debug)

    def ocr(
        self,
        img_path : Text,
        img_name: Text
    )-> List[Dict]:
        # region 1: Preprocess
        img = preprocess(img_path= img_path)

        # endregion

        # region 2: OCR
        result = self.model.ocr(img, cls=True)[0]

        # endregion
        res= []
        # region Postprocessing
        for line in result:
            _bbox, (text, prob) = line
            bbox = [[int(bb[0]), int(bb[1])] for bb in _bbox]
            res.append({
                'transcription': text,
                'points': bbox,
                'prob': prob
            })
        # endregion
        if self.debug:
            print(f'Result inference {img_name} : {res}')
        return res

if __name__ == "__main__":
    # region get argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-ip', 
        '--img_path', 
        help="Path to folder contain images"
    )
    parser.add_argument(
        '-lb', 
        '--json_path',  
        help="Path to json"
    )

    parser.add_argument(
        '-gt', 
        '--pred_path',  
        help="Path to predicto truth"
    )

    args = parser.parse_args()
    # endregon
    PredPPOCRWithPreprocess(
        image_path= args.img_path,
        json_name= args.json_path,
        debug = False
    ).convert_to_format_mAP(
        path = args.pred_path
    )
    # IMG_PATH = 'img/0012.jpg'
    # img = preprocess(img_path= IMG_PATH)
    # cv2.imshow(
    #     winname= 'out',
    #     mat= img
    # )
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    
