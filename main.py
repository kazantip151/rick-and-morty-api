from flask import Flask, jsonify
import csv
import os

app = Flask(__name__)

@app.route("/api/")
def character():
    return "Welcome to Rick and Morty API"

@app.route("/api/characters", methods=["GET"])
def get_all_characters():
    try:
        characters = read_characters_from_csv()
        return jsonify(characters)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/characters/<name>", methods=["GET"])
def get_character_by_name(name):
    try:
        characters = read_characters_from_csv()

        # Handle the case where no data is available
        if isinstance(characters, dict) and "message" in characters:
            return jsonify(characters), 404

        # Find character by name (case-insensitive)
        character = next(
            (char for char in characters if char["Name"].lower() == name.lower()),
            None
        )

        if character:
            return jsonify(character)
        else:
            return jsonify({"message": f"Character '{name}' not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/locations/<location>", methods=["GET"])
def get_characters_by_location(location):

    try:
        characters = read_characters_from_csv()

        # Handle the case where no data is available
        if isinstance(characters, dict) and "message" in characters:
            return jsonify(characters), 404

        # Find all characters at the specified location (case-insensitive)
        matching_characters = [
            char for char in characters
            if "Location" in char and char["Location"].lower() == location.lower()
        ]

        if matching_characters:
            return jsonify(matching_characters)
        else:
            return jsonify({"message": f"No characters found at location '{location}'"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/refresh-data", methods=["POST"])
def refresh_data():
    try:
        from service import get_characters
        get_characters()
        return jsonify({
            "status": "success",
            "message": "Character data refreshed successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/healthcheck", methods=["GET"])
def healthcheck():
    try:
        # Check if the CSV file exists
        csv_exists = os.path.exists("characters.csv")

        # You could add more checks here like database connectivity, etc.

        return jsonify({
            "status": "healthy",
            "message": "Service is running",
            "data_available": csv_exists
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": str(e)
        }), 500

def read_characters_from_csv():
    characters = []

    # Check if file exists
    if not os.path.exists("characters.csv"):
        return {"message": "No character data available"}

    try:
        with open("characters.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                characters.append(row)
        return characters
    except OSError as e:
        raise Exception(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    app.run(debug=True)