import base64
import json
import os
import re

import numpy as np
import tensorflow as tf
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from skimage import measure


def load_labels(labels_path: str) -> list[str]:
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    return labels


def load_model(model_path: str) -> tf.lite.Interpreter:
    return tf.lite.Interpreter(model_path=model_path)


def preprocess_image(image: str) -> tf.Tensor:
    img = ContentFile(image)
    img = Image.open(img).convert('L')
    img_array = np.array(img)

    strokes = find_strokes(img_array)
    min_x, min_y, max_x, max_y = get_stroke_bounding_box(strokes)
    cropped_img_array = img_array[min_y:max_y + 1, min_x:max_x + 1]
    img_resized = Image.fromarray(cropped_img_array).resize((28, 28))
    img_tensor = tf.expand_dims(img_resized, axis=-1)
    img_tensor = tf.expand_dims(img_tensor, axis=0)
    img_tensor = tf.cast(img_tensor, tf.float32)
    return img_tensor


def find_strokes(img_array: np.ndarray) -> list[list[tuple[int, int]]]:
    img_array = 255 - img_array

    threshold = 128
    img_binary = (img_array > threshold).astype(np.uint8)

    contours = measure.find_contours(img_binary, 0.5)

    strokes = []
    for contour in contours:
        stroke = [(int(coord[1]), int(coord[0])) for coord in contour]
        strokes.append(stroke)

    return strokes


def get_stroke_bounding_box(strokes: list[list[tuple[int, int]]]) -> tuple[int, int, int, int]:
    min_x = min(coord[0] for stroke in strokes for coord in stroke)
    min_y = min(coord[1] for stroke in strokes for coord in stroke)
    max_x = max(coord[0] for stroke in strokes for coord in stroke)
    max_y = max(coord[1] for stroke in strokes for coord in stroke)
    return min_x, min_y, max_x, max_y


def predict_drawing(model: tf.lite.Interpreter, image: str, labels: list[str]) -> str:
    input_tensor = preprocess_image(image)
    model.allocate_tensors()
    input_details = model.get_input_details()
    output_details = model.get_output_details()
    model.set_tensor(input_details[0]['index'], input_tensor)
    model.invoke()
    output_data = model.get_tensor(output_details[0]['index'])
    top_prediction = np.argmax(output_data)
    return labels[top_prediction]


def main(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse('Only POST requests are supported', status=400)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    image_data = body['image']
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_file = base64.b64decode(image_data)

    labels_path = os.path.join(settings.BASE_DIR, 'drawmatch_app', 'ai_testing', 'data', 'labels.txt')
    model_path = os.path.join(settings.BASE_DIR, 'drawmatch_app', 'ai_testing', 'data', 'model.tflite')

    labels = load_labels(labels_path)
    model = load_model(model_path)
    prediction = predict_drawing(model, image_file, labels)
    print("Prediction:", prediction)

    return HttpResponse(prediction)


if __name__ == '__main__':
    main()
