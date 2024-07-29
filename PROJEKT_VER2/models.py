from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

def init_db():
    db.create_all()

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surface_area = db.Column(db.Float, nullable=False)
    tile_length = db.Column(db.Float, nullable=False)
    tile_width = db.Column(db.Float, nullable=False)
    sublayer_thickness = db.Column(db.Float, nullable=False)
    base_thickness = db.Column(db.Float, nullable=False)
    sand_layer_thickness = db.Column(db.Float, nullable=False)
    excavation_depth = db.Column(db.Float, nullable=False)
    joint_width = db.Column(db.Float, nullable=False)
    joint_depth = db.Column(db.Float, nullable=False)
    border_length = db.Column(db.Float, nullable=False)
    border_subs = db.Column(db.Float, nullable=False)
    border_earth = db.Column(db.Float, nullable=False)
    tiles = db.Column(db.Float)
    fugue = db.Column(db.Float)
    sublayer = db.Column(db.Float)
    base = db.Column(db.Float)
    sand = db.Column(db.Float)
    excavation = db.Column(db.Float)

# models.py 
def calculate_materials(surface_area, tile_length, tile_width, sublayer_thickness, base_thickness, sand_layer_thickness, excavation_depth, joint_width, joint_depth, border_length, border_subs, border_earth):
    if any(value <= 0 for value in [surface_area, tile_length, tile_width, sublayer_thickness, base_thickness, sand_layer_thickness, excavation_depth, joint_width, joint_depth, border_length, border_subs, border_earth]):
        raise ValueError("Wartości muszą byc większe lub równe 0!")

    tiles = (surface_area / ((tile_length / 100) * (tile_width / 100)))
    fugue = (surface_area * joint_width * joint_depth) / 1000
    sublayer = surface_area * sublayer_thickness / 1000
    base = surface_area * base_thickness / 1000
    sand = surface_area * sand_layer_thickness / 1000
    excavation = surface_area * excavation_depth / 1000

    return tiles, fugue, sublayer, base, sand, excavation

