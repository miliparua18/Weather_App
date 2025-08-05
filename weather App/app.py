from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = 'd9fcfbebfb384766afb73755252707'

# Function to return background color based on temperature
def get_bg_color(temp):
    if temp >= 30:
        return "#ff7e67"  # Hot
    elif temp >= 20:
        return "#f7d794"  # Warm
    elif temp >= 10:
        return "#95d6f3"  # Cool
    else:
        return "#b8e0e7"  # Cold

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    bg_color = "#6294ea"  # Default color
    current_time = datetime.now().strftime('%I:%M %p')  # Example: 02:45 PM

    if request.method == 'POST':
        city = request.form['city'].strip()
        if not city:
            weather_data = {'error': 'Please enter a city name.'}
        else:
            url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
            response = requests.get(url)
            try:
                data = response.json()
                if response.status_code == 200 and 'current' in data:
                    temp = data['current']['temp_c']
                    bg_color = get_bg_color(temp)
                    weather_data = {
                        'city': data['location']['name'],
                        'temperature': temp,
                        'description': data['current']['condition']['text'],
                        'humidity': data['current']['humidity'],
                        'wind': data['current']['wind_kph'],
                        'icon': 'https:' + data['current']['condition']['icon']
                    }
                else:
                    weather_data = {'error': data.get('error', {}).get('message', 'City not found')}
            except requests.exceptions.JSONDecodeError:
                weather_data = {'error': 'Could not decode server response.'}

    return render_template('index.html',
                           weather=weather_data,
                           bg_color=bg_color,
                           current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)






