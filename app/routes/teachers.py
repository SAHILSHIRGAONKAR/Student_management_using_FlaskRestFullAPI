from flask import Blueprint, jsonify, request
from ..models import Teacher, Standard
from . import db

teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

@teachers_bp.route('', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    teachers_data = []
    for teacher in teachers:
        teacher_info = {
            'id': teacher.id,
            'name': teacher.name
        }
        teachers_data.append(teacher_info)
    return jsonify(teachers_data)

@teachers_bp.route('/<int:id>', methods=['GET'])
def get_teachers_by_id(id):
    try:
        teacher = Teacher.query.get_or_404(id)
        teacher_info = {
            'name': teacher.name,
            'id': teacher.id,
            'subject_taught': [subject.name for subject in teacher.subjects_taught],
            'standard_taught': [standard.name for standard in teacher.standards_taught]
        }
        return jsonify(teacher_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teachers_bp.route('', methods=['POST'])
def create_teacher():
    # Extract data from the request JSON
    data = request.json
    name = data.get('name')

    try:
        # Create a new Teacher object
        new_teacher = Teacher(name=name)

        # Add the new Teacher object to the session
        db.session.add(new_teacher)

        # Commit the session to persist the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'New teacher created successfully'}), 201
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        # Return an error message
        return jsonify({'error': str(e)}), 400

@teachers_bp.route('/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        teacher = Standard.query.get_or_404(id)

        # Delete associated marks for the student
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({'message': 'teacher deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

