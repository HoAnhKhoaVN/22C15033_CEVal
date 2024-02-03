import numpy as np
import cv2

CONTRAST=2.
BRIGHTNESS=2.

def change_contrast(
    img: np.ndarray,
)->np.ndarray:
    return cv2.addWeighted(
        src1= img,
        alpha= CONTRAST, # Contrast
        src2= img,
        beta= 0,
        gamma=BRIGHTNESS, # Brightness
    )

if __name__ == "__main__":
    IMG_PATH = 'img/0012.jpg'
    img = cv2.imread(IMG_PATH)

    out = change_contrast(img)

    cv2.imshow(winname= 'out', mat= out)

    cv2.waitKey(0)
    cv2.destroyAllWindows()