from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in .env file!")

# Initialize Gemini client
client = genai.Client(api_key=GOOGLE_API_KEY)

# Create FastAPI app
app = FastAPI(title="Gemini Funny Name Jokes API")

# Home page with form
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Funny Name Jokes</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f0f8ff; text-align: center; padding-top: 50px; }
                input { padding: 8px; width: 200px; margin: 10px; border-radius: 5px; border: 1px solid #aaa; }
                button { padding: 8px 16px; border-radius: 5px; border: none; background-color: #4CAF50; color: white; cursor: pointer; }
                button:hover { background-color: #45a049; }
                pre { text-align: left; display: inline-block; background: #fff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px #ccc; }
                a { display: block; margin-top: 20px; text-decoration: none; color: #333; font-weight: bold; }
            </style>
        </head>
        <body>
            <h2>Enter your name to get a 2-line funny joke 😄</h2>
            <form action="/joke" method="post">
                <input type="text" name="name" placeholder="Your name" required>
                <button type="submit">Get Joke</button>
            </form>
        </body>
    </html>
    """

# POST endpoint to generate joke
@app.post("/joke", response_class=HTMLResponse)
def joke(name: str = Form(...)):
    # Prompt Gemini to give 1 unique 2-line joke about the name
    prompt = (
        f"Give 1 short, funny, witty, polite comment about the name '{name}'. "
        "It must be exactly 2 lines, focus on the name itself, not the person. "
        "Make it unique and do not repeat style for other names."
    )
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        joke_text = response.text if hasattr(response, "text") else "Oops! No joke generated."

        return f"""
        <html>
            <head>
                <title>Funny Name Joke for {name}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f0f8ff; text-align: center; padding-top: 50px; }}
                    pre {{ text-align: left; display: inline-block; background: #fff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px #ccc; }}
                    a {{ display: block; margin-top: 20px; text-decoration: none; color: #333; font-weight: bold; }}
                </style>
            </head>
            <body>
                <h2>Funny 2-line joke for the name '{name}':</h2>
                <pre>{joke_text}</pre>
                <a href="/">Try another name</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"<p>Error: {str(e)}</p>"

