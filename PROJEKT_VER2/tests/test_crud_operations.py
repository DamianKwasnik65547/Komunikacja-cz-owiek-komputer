# tests/test_crud_operations.py
import unittest
from flask_testing import TestCase
from app import app, db, generate_pdf
from models import Project
from sqlalchemy.orm import make_transient

class TestCRUDOperations(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.secret_key = 'your_secret_key'
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()
            self.project = Project(
                name="PDF Project",
                surface_area=100,
                tile_length=30,
                tile_width=30,
                sublayer_thickness=10,
                base_thickness=15,
                sand_layer_thickness=5,
                excavation_depth=20,
                joint_width=2,
                joint_depth=2,
                border_length=50,
                border_subs=5,
                border_earth=5,
                tiles=100,
                fugue=6,
                sublayer=0.1,
                base=0.15,
                sand=0.05,
                excavation=0.2
            )
            db.session.add(self.project)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_generate_pdf(self):
        with app.app_context():
            # Ensure the project instance is transient if needed
            make_transient(self.project)
            pdf = generate_pdf(self.project)
        self.assertIsInstance(pdf, bytes)
        self.assertGreater(len(pdf), 0)  # PDF nie jest pusty

if __name__ == "__main__":
    unittest.main()
