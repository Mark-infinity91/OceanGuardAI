# OceanGuardAI 🌊

**AI-Driven Marine Debris Detection and Mapping System for Ocean Conservation**

OceanGuardAI is a software prototype designed to detect marine debris in images, extract GPS coordinates when available, and visualise geolocated detections on an interactive map.

## Features

- AI-based marine debris detection using an ONNX model.
- Detection confidence scores displayed on annotated images.
- GPS coordinate extraction from image metadata when available.
- Interactive pollution mapping using Folium.
- Detection records can be prepared for integration with a database and dashboard.

## Technologies

- Python
- OpenCV
- ONNX Runtime
- PyTorch
- Pillow
- Folium

## Project Structure

```text
OceanGuardAI/
├── ai/
│   └── detect_debris.py
├── data/
│   ├── mapping.py
│   └── gps_reader.py
├── test_integration.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

1. Install Python 3.10 or a compatible version.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the detection script with an image:

   ```bash
   python ai/detect_debris.py marine_test.jpg
   ```

4. Run the integration test:

   ```bash
   python test_integration.py
   ```

Use your own test image paths if the sample images are not included.

## Important Limitations

- GPS coordinates are available only when supported GPS metadata exists in the image.
- Images without GPS metadata cannot be assigned a real location automatically by the current GPS reader.
- The current model detects general marine debris and does not reliably distinguish individual debris categories.
- Map markers and results from test images must not be interpreted as verified real-world pollution reports.
- Dashboard and database integration may still be in progress.

## Project Status

This repository contains the current development work. Features described as in progress must be verified before the final demonstration.

## Current Implementation Status

OceanGuard AI is a prototype for AI-assisted marine debris detection and pollution mapping.

### Components
- **AI Detection:** Debris detection pipeline using an ONNX model.
- **GPS Extraction:** Reads GPS coordinates from image EXIF metadata when available.
- **Pollution Mapping:** Displays geolocated observations on an interactive map.
- **Integration:** Dashboard, database storage, and end-to-end integration are in progress.

### Limitations
- Images without embedded GPS metadata require a separate location source or manual coordinates.
- Sample map points and demonstration charts must not be interpreted as verified marine pollution measurements.
- Detection performance depends on the model and input image quality.

### Future Work
- Connect AI detections, GPS extraction, database storage, and map visualization into one workflow.
- Validate the system using appropriately labelled marine debris images and verified locations.
