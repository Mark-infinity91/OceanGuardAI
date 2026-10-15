
from ai.detect_debris import detect_debris
from data.mapping import create_map
from data.gps_reader import get_gps_coordinates

# Run AI detection on the test image
results = detect_debris("marine_test.jpg")
gps_coordinates = get_gps_coordinates("marine_test.jpg")
print("Photo GPS coordinates:", gps_coordinates)

# Convert AI results into the map's format
map_detections = []

for i, result in enumerate(results, start=1):
    map_detections.append({
        "name": f"Image detection {i}",
        "coordinates": gps_coordinates,
        "debris_type": result["class"],
        "confidence": result["confidence"],
       "status": (
    "AI detected - GPS available"
    if gps_coordinates
    else "AI detected - GPS unavailable"
)
    })

# Generate the integrated map
marine_map = create_map(detections=map_detections)
marine_map.save("integrated_ocean_map.html")

print(f"AI detections processed: {len(map_detections)}")
print("Map saved: integrated_ocean_map.html")
print("GPS coordinates:", gps_coordinates)
# Separate GPS marker test — not a real pollution location
gps_test_coordinates = get_gps_coordinates("gps_test.jpg")

gps_test_detection = [{
    "name": "GPS Reader Test",
    "coordinates": gps_test_coordinates,
    "debris_type": "GPS test only",
    "confidence": 0,
    "status": "GPS test - not a pollution report"
}]

gps_test_map = create_map(detections=gps_test_detection)
gps_test_map.save("gps_marker_test.html")

print("GPS marker test map saved: gps_marker_test.html")
print("GPS test coordinates:", gps_test_coordinates)