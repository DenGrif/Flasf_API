#импортируем Flask и библиотеку Request
from flask import Flask, render_template, request
import requests

#импортируем объект класса Flask
app = Flask(__name__)


#формируем путь и методы GET и POST
@app.route('/', methods=['GET', 'POST'])
def index():
    # создаем функцию с переменной weather, где мы будем сохранять погоду, новости, цитаты
    weather = None
    news = None
    quote = None
# формируем условия для проверки метода. Форму мы пока не создавали, но нам из неё
# необходимо будет взять только город.
    if request.method == 'POST':
        # этот определенный город мы будем брать для запроса API
        city = request.form['city']
        weather = get_weather(city)
        news = get_news()
        quote = get_random_quote()
    return render_template("index.html", weather=weather, news=news, quote=quote)


#в функции прописываем город, который мы будем вводить в форме
def get_weather(city):
   api_key = "c0e062f5ceaddc9438c305c317c0b9c2"
   #адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
   url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru&units=metric"
   #для получения результата нам понадобится модуль requests
   response = requests.get(url)
   #прописываем формат возврата результата
   return response.json()

def get_news():
    api_key = "5d2e9e15bfe166e341f20954e8fa7a95"
    url = f"http://api.mediastack.com/v1/news?languages=ru&access_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('data', [])
    return []


def get_random_quote():
    url = "http://api.forismatic.com/api/1.0/"
    params = {
        "method": "getQuote",
        "format": "json",
        "lang": "ru"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        quote_data = response.json()
        return {
            "content": quote_data['quoteText'],
            "author": quote_data.get('quoteAuthor', 'Неизвестный')
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return {
            "content": "Не удалось получить цитату.",
            "author": "Неизвестный"
        }


if __name__ == '__main__':
    app.run(debug=True)
