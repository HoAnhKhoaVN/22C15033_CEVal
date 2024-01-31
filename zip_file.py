import os
import zipfile
from typing import Text, List
import argparse

_TYPE = ['txt']

class ZipTxtFile(object):
    def __init__(
        self,
        fd_path : Text,
        zip_path : Text
    ) -> None:
        self.fd_path = fd_path
        self.zip_path = zip_path
        self.lst_img_fn = self.get_image_file(os.listdir(self.fd_path))
        os.chdir(path= self.fd_path)

    @staticmethod
    def get_image_file(
        lst_fn : List[Text]
    )-> List[Text]:
        return list(filter(
            lambda x: x.split('.')[-1].lower() in _TYPE,
            lst_fn
        ))

    def __call__(self) -> None:
        with zipfile.ZipFile(self.zip_path, 'w') as zip:
            for file in self.lst_img_fn:
                zip.write(
                    filename=file,
                    compress_type= zipfile.ZIP_DEFLATED
                )
                
if __name__ == "__main__":
    # region get argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-fp', 
        '--fd_path', 
        help="Path to folder contain txt file"
    )
    parser.add_argument(
        '-zp', 
        '--zip_path',  
        help="Path to zip file"
    )

    args = parser.parse_args()
    # endregon

    obj = ZipTxtFile(
        fd_path = args.fd_path,
        zip_path=  args.zip_path
    )

    obj()
