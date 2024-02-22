from flask import Flask
from app.database import db
from app.routes.students import students_bp
from app.routes.subjects import subjects_bp
from app.routes.teachers import teachers_bp
from app.routes.standard import standard_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(students_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(standard_bp)

    return app
