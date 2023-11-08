from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

# to define routes which we would access on the web

@app.route('/')  # this will be the home page
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        city = "Seoul"

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200: # If our weather code is not 200
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

if __name__ == "__main__":
    # to go to local host port 8000 to see the app
    serve(app, host="0.0.0.0", port=8000)
