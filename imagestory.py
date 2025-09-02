import os
import google.generativeai as genai
from flask import Flask, request, render_template_string

# Load Gemini API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Simple HTML page with a button to trigger story generation
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Story Generator</title>
</head>
<body>
    <h2>Generate Story from JPG Image</h2>
    <form method="post">
        <label>Enter image path (e.g. /home/user/picture.jpg):</label><br><br>
        <input type="text" name="image_path" placeholder="image.jpg" required>
        <button type="submit">Generate Story</button>
    </form>
    {% if story %}
        <h3>Generated Story:</h3>
        <p>{{ story }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    story = None
    if request.method == "POST":
        image_path = request.form["image_path"]

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Open local JPG file
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()

            # Generate story
            response = model.generate_content([
                "Write a creative short story based on this image:",
                {"mime_type": "image/jpeg", "data": image_bytes}
            ])

            story = response.text

        except Exception as e:
            story = f"Error: {str(e)}"

    return render_template_string(HTML_PAGE, story=story)

if __name__ == "__main__":
    app.run(debug=True)

