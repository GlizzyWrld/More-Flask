from flask import Flask, url_for, render_template, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetAdd, PetEdit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yolobroletsgo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Home page with list of pets"""
    pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

@app.route('/add', methods=['GET','POST'])
def pet_add():
    """Add a pet"""
    form = PetAdd
    if form.validate_on_submit():
        pet = Pet(
            name = form.name.data,
            species = form.species.data,
            photo_url = form.photo_url.data,
            age = form.age.data,
            notes = form.notes.data
        )
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('pets'))
    
    else:
        return render_template('add_pet.html', form=form)
    
@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def pet_edit(pet_id):
    """Edit a pet"""
    pet = Pet.query.get_or_404(pet_id)
    form = PetEdit(obj=pet)
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        return redirect(url_for('pets'))
    
    else:
        return render_template('edit_pet.html', pet=pet, form=form)
    
@app.route('/api/pets/<int:pet_id>', methods=['GET'])
def api_get_pet(pet_id):
    """Return JSON info about a pet"""
    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}
    return jsonify(info)