from flask import request, render_template, redirect, url_for, flash
import requests
from app import app, db
from app.forms import LoginForm, SignupForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


def load_user(user_id):
    return User.query.get(int(user_id))



#home   
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


REGISTERED_USERS = {
    'maria@pokepedia.com':{
    'name': 'Maria',
    'password': 'test'
    }
}




#search
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
    



#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email= form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f"Hello, {REGISTERED_USERS[email]['name']}! You've successfully logged into Poképedia!🎉 Happy searching and may your Poképedia be filled with exciting discoveries!", 'success')
            return redirect(url_for('home'))
        else:
            return "Sorry, Trainer! Seems like the email or password is not quite right... Double-check and try again!"
    else:
        return render_template('login.html', form=form)
    



#signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data


        user = User(first_name, last_name, email, password)

        db.session.add(user)
        db.session.commit()

        flash("Congratulations, {first_name}! You've successfully joined our Poképedia community!🎉 Your journey to become a Pokémon master is just beginning!")
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)   
    

#log out
@app.route('/logout')
@login_required
def logout():
    flash('Until your next adventure, Trainer! ⚡', 'success')
    logout_user()
    return redirect(url_for('login'))