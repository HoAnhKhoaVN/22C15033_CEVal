import numpy as np
import cv2

def remove_noise(
    img: np.ndarray
)->np.ndarray:
    return cv2.fastNlMeansDenoisingColored(
        src= img,
        dst= None,
        h = 10,
        hColor= 10,
        templateWindowSize= 7,
        searchWindowSize= 15
    )

if __name__ == "__main__":
    IMG_PATH = 'img/0012.jpg'
    img = cv2.imread(IMG_PATH)

    out = remove_noise(img)

    cv2.imshow(winname= 'out', mat= out)

    cv2.waitKey(0)
    cv2.destroyAllWindows()