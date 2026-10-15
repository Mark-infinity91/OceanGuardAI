
from PIL import Image, ExifTags


def get_gps_coordinates(image_path):
    image = Image.open(image_path)
    exif = image.getexif()
    gps = exif.get_ifd(ExifTags.IFD.GPSInfo)

    if not gps or 2 not in gps or 4 not in gps:
        return None

    latitude = gps[2]
    longitude = gps[4]

    lat = float(latitude[0]) + float(latitude[1]) / 60 + float(latitude[2]) / 3600
    lon = float(longitude[0]) + float(longitude[1]) / 60 + float(longitude[2]) / 3600

    if gps.get(1) == "S":
        lat = -lat
    if gps.get(3) == "W":
        lon = -lon

    return [lat, lon]


if __name__ == "__main__":
    coordinates = get_gps_coordinates("gps_test.jpg")
    print("GPS coordinates:", coordinates)
