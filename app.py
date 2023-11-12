from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def welcome():
    return '<h1>Welcome, Trainer! Curious about a Pokemon? Enter its name to discover its details!</h1>'




@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        pokemon = request.form.get('pokemon')
        poke_data = get_pokemon_data(pokemon)
        return render_template('search.html', poke_data=poke_data)
    else:
        return render_template('search.html')
    


def get_pokemon_data(number):
    url = f'https://pokeapi.co/api/v2/pokemon/{number}'
    response = requests.get(url)
    data = response.json()

    pokemon = {
        'name': data['forms'][0]['name'],
        'ability' : data['abilities'][0]['ability']['name'],
        'base_experience':data['base_experience'],
        'image': data['sprites']['front_default']

}
    return pokemon