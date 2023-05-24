import numpy as np
import tensorflow as tf
from PIL import Image
from skimage import measure


def load_labels(labels_path):
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    return labels


def load_model(model_path):
    return tf.lite.Interpreter(model_path=model_path)


def preprocess_image(image_path, image_name):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    strokes = find_strokes(img_array)
    min_x, min_y, max_x, max_y = get_stroke_bounding_box(strokes)
    cropped_img_array = img_array[min_y:max_y + 1, min_x:max_x + 1]
    img_resized = Image.fromarray(cropped_img_array).resize((28, 28))
    img_resized.save(f'images/cropped_{image_name}')  # debug to see the resized image
    img_tensor = tf.expand_dims(img_resized, axis=-1)
    img_tensor = tf.expand_dims(img_tensor, axis=0)
    img_tensor = tf.cast(img_tensor, tf.float32)
    return img_tensor


def find_strokes(img_array):
    img_array = 255 - img_array

    threshold = 128
    img_binary = (img_array > threshold).astype(np.uint8)

    contours = measure.find_contours(img_binary, 0.5)

    strokes = []
    for contour in contours:
        stroke = [(int(coord[1]), int(coord[0])) for coord in contour]
        strokes.append(stroke)

    return strokes


def get_stroke_bounding_box(strokes):
    min_x = min(coord[0] for stroke in strokes for coord in stroke)
    min_y = min(coord[1] for stroke in strokes for coord in stroke)
    max_x = max(coord[0] for stroke in strokes for coord in stroke)
    max_y = max(coord[1] for stroke in strokes for coord in stroke)
    return min_x, min_y, max_x, max_y


def predict_drawing(model, image_path, image_name, labels):
    input_tensor = preprocess_image(image_path, image_name)
    model.allocate_tensors()
    input_details = model.get_input_details()
    output_details = model.get_output_details()
    model.set_tensor(input_details[0]['index'], input_tensor)
    model.invoke()
    output_data = model.get_tensor(output_details[0]['index'])
    top_prediction = np.argmax(output_data)
    return labels[top_prediction]


def main():
    model_path = 'data/model.tflite'
    labels_path = 'data/labels.txt'
    image_path = 'images/'
    image_name = 'face.png'  # must be 1000x1000

    image_path += image_name

    labels = load_labels(labels_path)
    model = load_model(model_path)
    prediction = predict_drawing(model, image_path, image_name, labels)
    print("Prediction:", prediction)


if __name__ == '__main__':
    main()
