import torch
import cv2
from UI.utils import crop_image, resize_image
from paddleocr import PaddleOCR
import numpy as np
from constants import MODEL_PATH


class ANPR:
    def __init__(self):
        self.paddleocr = PaddleOCR(lang="en", det_db_score_mode="slow")
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)
        self.model.to(self.device)

    def process_image(self, image):
        predictions = self.model(image)   
        predictions = predictions.pred[0]
        orig_h, orig_w, _ = image.shape
        image, new_height, new_width = resize_image(image)
        all_detections = []
        for j, prediction in enumerate(predictions):
            x1, y1, x2, y2 = prediction[:4]

            crop_coord = [int((1280-new_width)/2 + x1*new_width/orig_w),
                          int((720 - new_height)/2 + y1*new_height/orig_h),
                          int((1280-new_width)/2 + x2*new_width/orig_w),
                          int((720 - new_height)/2 + y2*new_height/orig_h)]

            cropped_image = crop_image(image, crop_coord)
            
            detections = self._ocr(cropped_image)
            if len(detections):
                cv2.rectangle(image, (crop_coord[0], crop_coord[1]), (crop_coord[2], crop_coord[3]), (0, 0, 255), 2)
            all_detections.extend(detections)

            for i, txt in enumerate(detections):
                cv2.putText(
                    image, txt,
                    (40, 30*i + 30*j + 40),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (255, 0, 0),
                    1,
                    lineType=cv2.LINE_AA,
                    bottomLeftOrigin=False,
                )
        
        return image, all_detections
    
    def _ocr(self, image: np.ndarray):
        result = self.paddleocr.ocr(image)
        result = result[0]
        txts = []
        if len(result):
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]

            # Threshold 0.9
            txts = [txts[i] for i in range(len(txts)) if scores[i] > 0.8]

        return txts
