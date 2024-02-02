import os
from google.cloud import vision
from typing import Text, List, Dict
from pred_ppocr_baseline import PredictionPPOCR
import argparse

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key/apikey.json'
os.environ['GRPC_DNS_RESOLVER'] = 'native'
CH_FONT = 'D:/Master/OCR_Nom/experiments/str_vietnam_temple/font/NomKhai.ttf'
CLIENT = vision.ImageAnnotatorClient()

class PredictionGGVision(PredictionPPOCR):
    def __init__(
        self,
        image_path: Text,
        json_name: Text,
        debug: bool = True
    ) -> None:
        self.image_path = image_path
        self.out_path = json_name
        self.model = CLIENT
        self.debug = debug
        self.data = self.read_data()

        if self.debug:
            print(f'**** INIT *****')
            print(f'image_path: {image_path}')
            print(f'json_name: {json_name}')

    def ocr(
        self,
        img_path : Text,
        img_name: Text
    )-> List[Dict]:
        """Finds the document bounds given an image and feature type.

        Args:
            image_file: path to the image file.

        Returns:
            List of coordinates for the corresponding feature type.
        """
        bounds = []

        # region 1: Open Image
        with open(img_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        # endregion

        # region 2: Call API
        response = CLIENT.text_detection(image=image)

        # endregion

        # region 3: Get list of text
        texts = response.text_annotations
        description_text = texts[0].description.split("\n")

        # endregion

        # region 4: Get list of bbox
        document = response.full_text_annotation
        for page in document.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    bounds.append(paragraph.bounding_box)

        # endregion

        # region 5: Convert to dictionary
        res = []
        for text, b in zip(description_text, bounds):
            bbox = [
                [b[0].x, b[0].y],
                [b[1].x, b[1].y],
                [b[2].x, b[2].y],
                [b[3].x, b[3].y]
            ]
            res.append(
                {
                'transcription': text,
                'points': bbox,
            }
        )

        # endregion
        
        if self.debug:
            print(f'Result inference {img_name} : {res}')
        return res

if __name__ == '__main__':
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

    PredictionGGVision(
        image_path= args.img_path,
        json_name= args.json_path,
        debug = False
    ).convert_to_format_mAP(
        path = args.pred_path
    )

