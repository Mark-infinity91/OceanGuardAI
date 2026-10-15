
import folium
from folium.plugins import HeatMap


def create_map(detections=None):
    # Create the main world map
    marine_map = folium.Map(
        location=[20.0, 0.0],
        zoom_start=2
    )
    # Add OceanGuard AI title
    title_html = """
    <h3 style="text-align:center; color:#087E8B;">
        OceanGuard AI
    </h3>
    <p style="text-align:center; color:#444;">
        AI-Driven Marine Debris Detection and Mapping System
    </p>
    """

    marine_map.get_root().html.add_child(
        folium.Element(title_html)
    )

    # Sample data only - used when no detections are supplied
    if detections is None:
        detections = [
            {
                "name": "Sample Location 1",
                "coordinates": [20.0, 0.0],
                "debris_type": "Plastic bottle",
                "confidence": 0.91,
                "status": "Pending review"
            },
            {
                "name": "Sample Location 2",
                "coordinates": [10.0, 50.0],
                "debris_type": "Plastic bag",
                "confidence": 0.84,
                "status": "Verified sample"
            },
            {
                "name": "Sample Location 3",
                "coordinates": [-10.0, 100.0],
                "debris_type": "Can",
                "confidence": 0.76,
                "status": "Pending review"
            }
        ]

   
    # Group detections that share the same GPS coordinates
    grouped_detections = {}

    for item in detections:
        coordinates = item.get("coordinates")

        if not coordinates:
            print(
                f"Skipping map marker for "
                f"{item.get('name', 'Unknown detection')}: "
                "GPS coordinates unavailable."
            )
            continue

        key = tuple(coordinates)
        grouped_detections.setdefault(key, []).append(item)

    # Create one marker for each unique GPS location
    for coordinates, items in grouped_detections.items():
        popup_lines = ["<b>SAMPLE OR TEST DATA</b>"]

        for item in items:
            popup_lines.append(
                f"<hr><b>Location:</b> {item.get('name', 'Unknown')}<br>"
                f"<b>Debris type:</b> {item.get('debris_type', 'Unknown')}<br>"
                f"<b>Confidence:</b> {item.get('confidence', 0):.0%}<br>"
                f"<b>Status:</b> {item.get('status', 'Unknown')}"
            )

        popup_text = "<br>".join(popup_lines)

        folium.CircleMarker(
            location=list(coordinates),
            radius=8,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=f"{len(items)} detection(s) at this location"
        ).add_to(marine_map)


    # Prepare heatmap coordinates, skipping missing GPS
    heatmap_points = [
        item["coordinates"]
        for item in detections
        if item.get("coordinates")
    ]

    # Add heatmap only if there are valid coordinate points
    if heatmap_points:
        heatmap = HeatMap(
            heatmap_points,
            name="Detection Heatmap",
            radius=25,
            blur=15
        )
        heatmap.add_to(marine_map)

    # Add a layer control

    
    # Add detection summary panel
    total_detections = len(detections)
    gps_available = sum(
        1 for item in detections if item.get("coordinates")
    )
    gps_unavailable = total_detections - gps_available

    summary_html = f"""
    <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        width: 220px;
        background: white;
        border: 2px solid #087E8B;
        border-radius: 8px;
        padding: 14px;
        z-index: 9999;
        font-family: Arial, sans-serif;
        color: #222;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    ">
        <h4 style="margin: 0 0 12px; color: #087E8B;">
            Detection Summary
        </h4>
        <p>Total detections: <b>{total_detections}</b></p>
        <p>GPS available: <b style="color: green;">{gps_available}</b></p>
        <p>GPS unavailable: <b style="color: #c0392b;">{gps_unavailable}</b></p>
    </div>
    """

    marine_map.get_root().html.add_child(
        folium.Element(summary_html)
    )

    # Add map legend
    legend_html = """
    <div style="
        position: fixed;
        bottom: 35px;
        left: 35px;
        width: 220px;
        background-color: white;
        border: 2px solid #087E8B;
        border-radius: 8px;
        padding: 12px;
        z-index: 9999;
        font-size: 13px;
        color: #222;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    ">
        <b style="color: #087E8B;">OceanGuard AI — Legend</b>
        <hr style="margin: 8px 0;">
        <div>
            <span style="color: red;">●</span>
            AI detection with GPS
        </div>
        <div style="margin-top: 6px;">
            <span style="color: #3388ff;">●</span>
            Detection heatmap
        </div>
        <div style="margin-top: 6px;">
            <span style="color: #666;">○</span>
            GPS unavailable — no marker
        </div>
        <div style="margin-top: 8px; font-size: 11px; color: #666;">
            Test data is not a confirmed pollution report.
        </div>
    </div>
    """

    marine_map.get_root().html.add_child(
        folium.Element(legend_html)
    )

    folium.LayerControl().add_to(marine_map)

    return marine_map


if __name__ == "__main__":
    marine_map = create_map()
    marine_map.save("ocean_map.html")
    print("Ocean map created successfully!")
    print("Map markers and heatmap added where GPS coordinates exist.")
