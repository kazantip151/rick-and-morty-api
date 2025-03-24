import requests
import csv

def get_characters():
    try:
        response = requests.get("https://rickandmortyapi.com/api/character/?species=Human&status=alive&origin=Earth")
        response.raise_for_status()
        characters = response.json()["results"]
        store_characters(characters)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching characters: {e}")


def store_characters(characters):
    try:
        with open("characters.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Write header row
            writer.writerow(["Name", "Location", "Image URL"])

            # Write character data
            for character in characters:
                writer.writerow([character["name"], character["location"]["name"], character["image"]])
    except OSError as e:
        print(f"Error to write to CSV file: {e}")

if __name__ == "__main__":
    get_characters()

