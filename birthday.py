from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from datetime import datetime, date, timedelta

app = FastAPI(title="Next Birthday Calculator")

# Home page with form
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Next Birthday Calculator</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f0f8ff; text-align: center; padding-top: 50px; }
                input { padding: 8px; width: 200px; margin: 10px; border-radius: 5px; border: 1px solid #aaa; }
                button { padding: 8px 16px; border-radius: 5px; border: none; background-color: #4CAF50; color: white; cursor: pointer; }
                button:hover { background-color: #45a049; }
                p { font-size: 18px; font-weight: bold; }
                a { display: block; margin-top: 20px; text-decoration: none; color: #333; font-weight: bold; }
            </style>
        </head>
        <body>
            <h2>Enter your Date of Birth</h2>
            <form action="/next_birthday" method="post">
                <input type="date" name="dob" required>
                <button type="submit">Calculate Next Birthday</button>
            </form>
        </body>
    </html>
    """

# POST endpoint to calculate next birthday
@app.post("/next_birthday", response_class=HTMLResponse)
def next_birthday(dob: str = Form(...)):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d").date()
        today = date.today()
        
        # Create this year's birthday
        this_year_bday = birth_date.replace(year=today.year)
        
        # If birthday has passed this year, use next year
        if this_year_bday < today:
            next_bday = this_year_bday.replace(year=today.year + 1)
        else:
            next_bday = this_year_bday

        days_until = (next_bday - today).days
        weekday = next_bday.strftime("%A")  # Name of the day

        return f"""
        <html>
            <head>
                <title>Next Birthday Result</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f0f8ff; text-align: center; padding-top: 50px; }}
                    p {{ font-size: 20px; font-weight: bold; }}
                    a {{ display: block; margin-top: 20px; text-decoration: none; color: #333; font-weight: bold; }}
                </style>
            </head>
            <body>
                <h2>Your Date of Birth: {dob}</h2>
                <p>Your next birthday is in {days_until} days! 🎉</p>
                <p>It will fall on a {weekday}.</p>
                <a href="/">Try another date</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"<p>Error: {str(e)}</p>"

