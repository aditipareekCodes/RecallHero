from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import json

app = Flask(__name__)
CORS(app)

# --- RE-PASTE YOUR NEW KEY HERE ---
# If you get a 429 error, wait 60 seconds.
client = genai.Client(api_key="YOUR_API_KEY_HERE")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    notes = data.get("notes", "").strip()

    if not notes:
        return jsonify({"error": "No notes provided."}), 400

    prompt = f"""
    Return ONLY a JSON object with these keys: "the_skinny", "the_recall", "the_anchor".
    Use the notes to fill them. 
    NOTES: {notes}
    """

    try:
        # Using 1.5 Flash as it's more stable for Free Tier quotas
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        
        raw_text = response.text.strip()
        
        # Clean potential markdown fences
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()

        return jsonify(json.loads(raw_text))

    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}") # This shows in your terminal
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)