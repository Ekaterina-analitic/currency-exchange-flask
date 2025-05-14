from flask import Flask, render_template
import requests

app = Flask(__name__)

def fetch_currency_data():
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        response.raise_for_status()
        data = response.json()
        return data['Valute']
    except requests.RequestException as e:
        print(f"Ошибка при подключении: {e}")
        return None

@app.route('/')
def index():
    valutes = fetch_currency_data()
    if valutes:
        # Формируем данные для отображения
        currency_data = []
        for code, valute in sorted(valutes.items(), key=lambda x: x[1]['Value'], reverse=True):
            name = valute['Name']
            value = f"{valute['Value']:.2f}"
            previous = valute['Previous']
            change = f"{((valute['Value'] - previous) / previous) * 100:+.2f}%"
            currency_data.append((code, name, value, change))
        return render_template('index.html', currency_data=currency_data)
    else:
        return "Ошибка при получении данных. Попробуйте позже."

if __name__ == "__main__":
    app.run(debug=True)

