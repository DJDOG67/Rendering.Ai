import cv2
import numpy as np


def cleanup_image(path: str) -> str:
    """Return path to cleaned-up image. This function performs simple denoising
    and contrast adjustment. The result is stored next to the original image
    with `_clean` suffix."""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(path)

    denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    lab = cv2.merge((l, a, b))
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    out_path = path.rsplit('.', 1)[0] + '_clean.png'
    cv2.imwrite(out_path, result)
    return out_path
