import os
import zipfile
from typing import Text, List

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
    FD_PATH = 'go/de_gt'
    obj = ZipTxtFile(
        fd_path = FD_PATH,
        zip_path= 'gt.zip'
    )

    obj()


    # FD_PATH = 'go/de_pred'
    # obj = ZipTxtFile(
    #     fd_path = FD_PATH,
    #     zip_path= 'pred.zip'
    # )

    # obj()