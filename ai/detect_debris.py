
import os
import sys
import cv2
import numpy as np
import onnxruntime as ort

MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.onnx")
IMAGE_SIZE = 416
CONFIDENCE_THRESHOLD = 0.15
IOU_THRESHOLD = 0.45


def letterbox(image, size=416):
    height, width = image.shape[:2]
    scale = min(size / width, size / height)

    new_width = int(round(width * scale))
    new_height = int(round(height * scale))

    resized = cv2.resize(image, (new_width, new_height))

    pad_x = (size - new_width) / 2
    pad_y = (size - new_height) / 2

    left = int(round(pad_x - 0.1))
    right = int(round(pad_x + 0.1))
    top = int(round(pad_y - 0.1))
    bottom = int(round(pad_y + 0.1))

    padded = cv2.copyMakeBorder(
        resized, top, bottom, left, right,
        cv2.BORDER_CONSTANT, value=(114, 114, 114)
    )

    return padded, scale, left, top


def detect_debris(image_path):
    if not os.path.isfile(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not open image: {image_path}")

    session = ort.InferenceSession(
        MODEL_PATH,
        providers=["CPUExecutionProvider"]
    )
    print("Model inputs:", [(i.name, i.shape, i.type) for i in session.get_inputs()])
    print("Model metadata:", session.get_modelmeta().custom_metadata_map)

    original_height, original_width = image.shape[:2]

    prepared, scale, pad_x, pad_y = letterbox(image, IMAGE_SIZE)

    rgb = cv2.cvtColor(prepared, cv2.COLOR_BGR2RGB)
    tensor = rgb.astype(np.float32) / 255.0
    tensor = np.transpose(tensor, (2, 0, 1))[None, ...]

    output = session.run(
        None, {session.get_inputs()[0].name: tensor}
    )[0]

    predictions = np.squeeze(output).T
    print("Raw output shape:", output.shape)
    print("Top 10 raw scores:", np.sort(predictions[:, 4])[-10:][::-1])
    top_indices = np.argsort(predictions[:, 4])[-10:][::-1]
    for i in top_indices:
        print("Candidate:", predictions[i])

    boxes = []
    scores = []

    for prediction in predictions:
        center_x, center_y, width, height, score = prediction[:5]

        if not np.isfinite(score) or score < CONFIDENCE_THRESHOLD:
            continue

        x1 = (center_x - width / 2 - pad_x) / scale
        y1 = (center_y - height / 2 - pad_y) / scale
        x2 = (center_x + width / 2 - pad_x) / scale
        y2 = (center_y + height / 2 - pad_y) / scale

        x1 = int(np.clip(x1, 0, original_width - 1))
        y1 = int(np.clip(y1, 0, original_height - 1))
        x2 = int(np.clip(x2, 0, original_width - 1))
        y2 = int(np.clip(y2, 0, original_height - 1))

        if x2 <= x1 or y2 <= y1:
            continue

        boxes.append([x1, y1, x2 - x1, y2 - y1])
        scores.append(float(score))

    indices = cv2.dnn.NMSBoxes(
        boxes, scores, CONFIDENCE_THRESHOLD, IOU_THRESHOLD
    )

    results = []

    if len(indices) > 0:
        for index in np.array(indices).flatten():
            x, y, width, height = boxes[index]
            score = scores[index]

            cv2.rectangle(
                image, (x, y), (x + width, y + height),
                (0, 200, 0), 2
            )
            cv2.putText(
                image, f"Marine Debris | {score:.1%}",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 200, 0), 2
            )

            results.append({
                "class": "marine_debris",
                "confidence": round(score, 4),
                "bbox": [x, y, x + width, y + height]
            })

    output_path = os.path.splitext(image_path)[0] + "_detected.jpg"

    if not cv2.imwrite(output_path, image):
        raise RuntimeError("Could not save the result image.")

    print(f"Detections: {len(results)}")
    for result in results:
        print(result)

    print(f"Annotated image saved to: {output_path}")
    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ai/detect_debris.py path_to_image.jpg")
        sys.exit(1)

    try:
        detect_debris(sys.argv[1])
    except Exception as error:
        print(f"Detection failed: {error}")
        sys.exit(1)
