import os
import zipfile
from typing import Any, Text, List

IMG_TYPE = ['png', 'jpg', 'jpeg']

class ZipTxtFile(object):
    def __init__(
        self,
        fd_path : Text,
        zip_path : Text
    ) -> None:
        self.fd_path = fd_path
        self.zip_path = zip_path
    
    @staticmethod
    def get_image_file(
        lst_fn : List[Text]
    )-> List[Text]:
        return list(filter(
            lambda x: x.split('.')[-1].lower() not in IMG_TYPE,
            lst_fn
        ))

    def __call__(self) -> None:

        # region 1: Get list of file
        lst_fn = os.listdir(self.fd_path)
        lst_img_fn = self.get_image_file(lst_fn)
        lst_img_full_path = list(map(lambda x: os.path.join(self.fd_path, x), lst_img_fn))
        print(f'lst_img_full_path: {lst_img_full_path}')

        # endregion

        # region 2: Zip file
        with zipfile.ZipFile(self.zip_path, 'w') as zip:
            for file in lst_img_full_path:
                zip.write(
                    filename=file,
                    compress_type= zipfile.ZIP_DEFLATED
                )

        # endregion
        


if __name__ == "__main__":
    FD_PATH = 'go/de'
    obj = ZipTxtFile(
        fd_path = FD_PATH,
        zip_path= 'demo.zip'
    )

    obj()