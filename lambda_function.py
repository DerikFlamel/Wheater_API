import json
import urllib.request
import os
from urllib.parse import quote

def lambda_handler(event, context):
    # Get city name from query string
    city = event.get("queryStringParameters", {}).get("city", "São Paulo")

    # Read API key from environment variable (or fallback)
    api_key = os.environ.get("OPENWEATHER_API_KEY", "d15b2ebff5af19a1fe99d05ffbd00fdc")

    # Encode city for URL
    encoded_city = quote(city)
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={api_key}&units=metric"

    try:
        # Fetch weather data
        with urllib.request.urlopen(base_url) as response:
            data = json.loads(response.read())

        current_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()

        # Simple prediction
        tomorrow_temp = round(current_temp + 1.5, 1)

        # Prepare HTML page
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Weather Forecast — {city}</title>
            <style>
                body 
                {{
                    margin: 0;
                    padding: 0;
                    font-family: "Poppins", Arial, sans-serif;
                    color: #fff;
                    text-align: center;
                    background: linear-gradient(to bottom, #003366 0%, #0099cc 100%);
                    overflow-x: hidden;
                }}

                header 
                {{
                    background-color: rgba(0, 51, 102, 0.6);
                    padding: 20px 0;
                    font-size: 2em;
                    font-weight: 600;
                    letter-spacing: 1px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                }}

                .container {{
                    margin-top: 60px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}

                table 
                {{
                    border-collapse: collapse;
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 10px;
                    overflow: hidden;
                    width: 320px;
                    font-size: 1.1em;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                }}

                th {{
                    background-color: rgba(0, 51, 102, 0.6);
                    padding: 15px;
                    font-size: 1.2em;
                }}

                td 
                {{
                    padding: 12px 15px;
                    border-bottom: 1px solid rgba(255,255,255,0.2);
                }}

                tr:last-child td 
                {{
                    border-bottom: none;
                }}

                footer 
                {{
                    margin-top: 80px;
                    font-size: 0.9em;
                    color: rgba(255,255,255,0.7);
                }}

                /* Decorative animated waves */
                .wave 
                {{
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    width: 200%;
                    height: 100px;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 1000px / 100px;
                    animation: wave 8s infinite linear;
                }}
                .wave:nth-child(2) 
                {{
                    bottom: 10px;
                    background: rgba(255, 255, 255, 0.2);
                    animation-duration: 10s;
                }}
                .wave:nth-child(3) 
                {{
                    bottom: 20px;
                    background: rgba(255, 255, 255, 0.15);
                    animation-duration: 12s;
                }}
                @keyframes wave 
                {{
                    from {{ transform: translateX(0); }}
                    to {{ transform: translateX(-50%); }}
                }}
            </style>
        </head>
        <body>
            <header>Weather ⛅ Forecast</header>

            <div class="container">
                <h2>{city}</h2>
                <table>
                    <tr><th colspan="2">Current Conditions</th></tr>
                    <tr><td><strong>Temperature</strong></td><td>{current_temp} °C</td></tr>
                    <tr><td><strong>Humidity</strong></td><td>{humidity}%</td></tr>
                    <tr><td><strong>Description</strong></td><td>{description}</td></tr>
                    <tr><th colspan="2">Prediction</th></tr>
                    <tr><td><strong>Tomorrow</strong></td><td>{tomorrow_temp} °C</td></tr>
                </table>
            </div>

            <footer>
                Data provided by OpenWeatherMap • Generated by AWS Lambda
            </footer>

            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
        </body>
        </html>
        """

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/html"},
            "body": f"<h1>Error</h1><p>{str(e)}</p>"
        }