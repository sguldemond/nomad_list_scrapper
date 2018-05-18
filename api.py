from flask import Flask, request, Response, json
import main

app = Flask(__name__)


@app.route('/')
def base():
    return "Hello world from Nomad List Scrapper!"


@app.route('/get_cities')
def get_cities():
    req_countries = request.get_json()['countries']
    amount = request.get_json()['amount']

    cached_countries = main.get_saved_countries(req_countries)
    print("Cached countries: " + cached_countries)

    countries = []
    countries.extend(cached_countries)

    req_countries = main.edit_countries(req_countries)

    main.start_driver()
    countries.extend(main.get_cities_from_multiple_countries(req_countries, amount))
    main.end_driver()

    return json_response(countries)


def json_response(data):
    response = Response(
        response=json.dumps(data),
        status=200,
        mimetype='application/json',
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    print('REST service is starting...')
    app.run()
