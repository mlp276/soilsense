import csv
import geopy.distance
from shapely.geometry import Polygon, Point

def generate_rotated_grid(corners, spacing=100):
    """
    Generate a grid of latitude and longitude points spaced 'spacing' meters apart
    within a rotated rectangular boundary defined by four corner points.
    """
    polygon = Polygon(corners)  # Create a Shapely polygon from the rectangle corners
    min_lat, min_lon, max_lat, max_lon = (
        min(p[0] for p in corners),
        min(p[1] for p in corners),
        max(p[0] for p in corners),
        max(p[1] for p in corners),
    )

    points = []
    current_lat = min_lat

    while current_lat <= max_lat:
        current_lon = min_lon
        while current_lon <= max_lon:
            test_point = Point(current_lat, current_lon)
            if polygon.contains(test_point):
                points.append((current_lat, current_lon))
            # Move longitude by approximately 'spacing' meters
            current_lon = geopy.distance.distance(meters=spacing).destination((current_lat, current_lon), 90)[1]
        # Move latitude by approximately 'spacing' meters
        current_lat = geopy.distance.distance(meters=spacing).destination((current_lat, min_lon), 0)[0]

    return points

def save_to_csv(points, filename="rotated_grid_points.csv"):
    """Save the generated points to a CSV file."""
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Latitude", "Longitude"])
        writer.writerows(points)

def main():
    print("Enter the four corner points of the rotated rectangle (in order).")
    corners = []
    for i in range(4):
        lat = float(input(f"Enter latitude for corner {i+1}: "))
        lon = float(input(f"Enter longitude for corner {i+1}: "))
        corners.append((lat, lon))

    # Generate grid
    grid_points = generate_rotated_grid(corners)

    # Save to CSV
    save_to_csv(grid_points)
    print(f"CSV file 'rotated_grid_points.csv' has been saved with {len(grid_points)} points.")

if __name__ == "__main__":
    main()
