from constant import JSON_NAME
import json
import re
import os
from collections import defaultdict
from typing import Text
from tqdm import tqdm
import argparse

class GroundTruth:
    def __init__(
        self,
        label_path: Text,
        img_path: Text,
        debug: bool = True, 
    ):
        self.label_path = label_path
        self.img_path = img_path
        self.dir_name, self.json_path = self.get_json_path()
        self.debug = debug
        self.data = self.read_data()
    
    def get_json_path(self):
        dir_name = os.path.dirname(self.label_path)
        json_path = os.path.join(dir_name, JSON_NAME)
        return dir_name, json_path

    def txt2json(self):
        my_dict = defaultdict(list)
        lst_img_path = os.listdir(self.img_path)
        if self.debug:
            print(f'lst_img_path : {lst_img_path}')
        
        with open(self.label_path, 'r', encoding= 'UTF-8-sig') as f:
            for line in f:
                path , context_json = line.strip().split(None, maxsplit= 1)
                # region Check path have in list image file
                file_name = os.path.basename(path)
                if self.debug:
                    print(f'{file_name}')
                if file_name not in lst_img_path:
                    continue
                # endregion

                dict_context = json.loads(s = context_json)
                
                lst_new_points = []
                lst_transcription = []
                for d in dict_context:
                    transcription = d['transcription']
                    points = d['points']

                    lst_transcription.append(transcription)
                    lst_new_points.append(points)
                    
                for tran , point in zip(lst_transcription, lst_new_points):
                    my_dict[path].append(
                        {
                            'transcription': tran,
                            'points': point
                        }
                    )

        print(f'Path to json file: {self.json_path}')
        with open(self.json_path, 'w', encoding= 'UTF-8-sig') as f:
            json.dump(
                obj = my_dict,
                fp = f,
                indent= 4,
                ensure_ascii= False
            )

    def read_data(self):
        if not os.path.exists(self.json_path):
            if self.debug:
                print(f"Do not exist {self.json_path} => Process convert .txt file to .json file!!!")
            self.txt2json()

        with open(self.json_path, 'r', encoding= 'UTF-8-sig') as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def get_file_name_without_extension(file_path: Text):
        return os.path.splitext(os.path.basename(file_path))[0]

    def convert_to_format_mAP(
        self,
        out_path: Text
    )-> None:
        
        # region Create out_path
        if not os.path.exists(path = out_path):
            os.makedirs(name= out_path)
        
        # endregion


        for k, v in tqdm(self.data.items(), desc="Progress convert to format calculate mAP: "):
            if self.debug:
                print(f'key: {self.get_file_name_without_extension(k)}')
                for _v in v:
                    transcription = _v['transcription']
                    points = _v['points']
                    tl_br = points[0]+ points[2]
                    print(f'{transcription} {" ".join(list(map(str,tl_br)))}')
                break
            else:
                output_file = os.path.join(
                        out_path,
                        self.get_file_name_without_extension(k)
                    )
                with open(f'{output_file}.txt', 'w', encoding='UTF-8-sig') as f:
                    for _v in v:
                        transcription = _v['transcription']
                        points = _v['points']
                        tl_br = points[0]+ points[1]+points[2]+points[3]
                        f.write(f'{",".join(list(map(str,tl_br)))},{transcription}\n')
        

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
        '--label_txt',  
        help="Path to Label.txt"
    )

    parser.add_argument(
        '-gt', 
        '--gt_path',  
        help="Path to Ground truth"
    )

    args = parser.parse_args()
    # endregon


    gt_chieu = GroundTruth(
        label_path= args.label_txt,
        debug= False,
        img_path= args.img_path
    )
    gt_chieu.convert_to_format_mAP(
        out_path= args.gt_path
    )