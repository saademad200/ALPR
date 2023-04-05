"""
This module contains the ALPR (Automatic License Plate Recognition) class that performs OCR
and object detection on images of vehicles to extract license plate information.

The ALPR class utilizes PaddleOCR and YOLOv5 models to perform OCR and object detection,
respectively. It also provides a `process_image` method that accepts an image and returns
the image with bounding boxes around detected license plates and their corresponding OCR text.

Example usage:

    alpr = ALPR()
    image = cv2.imread("image.jpg")
    processed_image, detections = alpr.process_image(image)
"""
import re
import torch
import cv2
from paddleocr import PaddleOCR
import numpy as np
from constants import MODEL_PATH, THRESHOLD
from user_interface.utils import crop_image, resize_image


class ALPR:
    """
    Automatic License Plate Recognition (ALPR) class.
    """

    def __init__(self):
        """
        Initializes the PaddleOCR and YOLOv5 models for ALPR.
        """
        self.paddleocr = PaddleOCR(lang="en", det_db_score_mode="slow")
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)
        self.model.to(self.device)

    def process_image(self, image):
        """
        Processes the input image for automatic license plate recognition.
        Args:
            image: The input image to be processed.
        Returns:
            image: The processed image with detected license plate numbers and text.
            detections: An array of detected license plates with their respective confidence scores
            and cropped images.
        """
        # Perform object detection with YOLOv5.
        predictions = self.model(image)
        predictions = predictions.pred[0]
        detections = []
        height, _, _ = image.shape

        # Loop through detected objects and perform OCR.
        for _, prediction in enumerate(predictions):
            x1, y1, x2, y2 = prediction[:4]
            crop_coord = [int(x1), int(y1), int(x2), int(y2)]

            cropped_image = crop_image(image, crop_coord)

            txt, conf = self._ocr(cropped_image)
            rectangle_size = height // 720 + 1
            if txt is not None:
                detections.append([txt, conf, cropped_image])
                # Draw bounding box around detected object
                cv2.rectangle(image, (crop_coord[0], crop_coord[1]), (crop_coord[2], crop_coord[3]),
                              (0, 0, 255), rectangle_size)

        # Resize image and add OCR results as text.
        image = resize_image(image)
        for idx, detection in enumerate(detections):
            cv2.putText(
                image, detection[0],
                (40, 40 + 40 * idx),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (255, 0, 0),
                1,
                lineType=cv2.LINE_AA,
                bottomLeftOrigin=False,
            )

        detections = np.array(detections)

        return image, detections

    def _ocr(self, image: np.ndarray):
        """
        Performs OCR with PaddleOCR.
        Args:
            image: The input image for OCR.
        Returns:
            A tuple of the OCR result with the highest confidence score and its corresponding score.
        """
        # Perform OCR with PaddleOCR.
        result = self.paddleocr.ocr(image)
        result = result[0]

        if len(result):
            # Extract OCR results with confidence scores above threshold.
            texts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            short_listed_texts = []
            short_listed_scores = []
            short_listed_items = []
            for i, txt in enumerate(texts):
                if scores[i] > THRESHOLD:
                    short_listed_texts.append(txt)
                    short_listed_scores.append(scores[i])

            # Filter out non-alphanumeric OCR results.
            for i, txt in enumerate(short_listed_texts):
                txt = ''.join([x for x in txt if x.isalnum()])
                match = re.match(r'^(?=.*\d)[a-zA-Z0-9]+$', txt)
                if match:
                    short_listed_items.append((txt, scores[i]))

            # Return OCR result with the highest confidence score.
            if len(short_listed_items) == 0:
                return None, None

            max_conf = float('-inf')
            max_conf_ind = 0
            for i, _ in enumerate(short_listed_items):
                if short_listed_items[i][1] > max_conf:
                    max_conf = short_listed_items[i][1]
                    max_conf_ind = i
                if not re.match(r'^\d+$', short_listed_items[i][0]):
                    return short_listed_items[i]
            return short_listed_items[max_conf_ind]

        else:
            return None, None
