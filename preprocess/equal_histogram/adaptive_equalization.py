import numpy as np
import cv2

CLAHE = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

def equalization(
    img: np.ndarray
)->np.ndarray:
    # region Histogram equalization
    img_yuv = cv2.cvtColor(
        src = img,
        code = cv2.COLOR_BGR2YUV
    )
    img_yuv[:,:,0] = CLAHE.apply(
        src= img_yuv[:,:,0]
    )
    
    out = cv2.cvtColor(
        src= img_yuv,
        code= cv2.COLOR_YUV2BGR
    )
    return out


if __name__ == "__main__":
    IMG_PATH = 'img/0012.jpg'
    img = cv2.imread(IMG_PATH)

    out = equalization(img)

    cv2.imwrite(
        filename='output/0012_adaptive_equalization.jpg',
        img= out
    )
    cv2.imshow(winname= 'out', mat= out)

    cv2.waitKey(0)
    cv2.destroyAllWindows()