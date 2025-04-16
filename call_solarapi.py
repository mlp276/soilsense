import requests
import json
import os

# Google Maps Solar API endpoint
SOLAR_API_ENDPOINT = "https://solar.googleapis.com/v1/dataLayers:get"

# Get the API key from environment variable
API_KEY = "ENTER_API_KEY"

if not API_KEY:
    print("Error: API key not found. Please set the environment variable.")
    exit(1)

def get_solar_data(latitude, longitude):
    params = {
        'location.latitude': latitude,
        'location.longitude': longitude,
        'radiusMeters': 100,
        'view': 'FULL_LAYERS',
        'requiredQuality': 'HIGH',
        'exactQualityRequired': False,  # Corrected boolean value
        'pixelSizeMeters': 0.5,
        'key': API_KEY
    }

    response = requests.get(SOLAR_API_ENDPOINT, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def download_data_layers(data, lat, lon):
    folder_name = f"data_{lat}_{lon}"
    os.makedirs(folder_name, exist_ok=True)

    imagery_keys = ['rgbUrl', 'dsmUrl', 'maskUrl', 'annualFluxUrl', 'monthlyFluxUrl', 'hourlyShadeUrls']

    for key in imagery_keys:
        url = data.get(key)
        if url:
            full_url = f"{url}&key={API_KEY}"
            file_path = os.path.join(folder_name, f"{key.replace('Url', '')}.tif")
            try:
                response = requests.get(full_url)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved {key} to {file_path}")
                else:
                    print(f"Failed to download {key}: {response.status_code}")
            except Exception as e:
                print(f"Error downloading {key}: {e}")

def main():
    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))

    solar_data = get_solar_data(latitude, longitude)

    if solar_data:
        print(json.dumps(solar_data, indent=4))
        download_data_layers(solar_data, latitude, longitude)

if __name__ == "__main__":
    main()
