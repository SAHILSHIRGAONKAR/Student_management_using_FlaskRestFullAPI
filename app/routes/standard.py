from flask import Blueprint, jsonify, request
from ..models import Teacher, Standard
from . import db

standard_bp = Blueprint('standards', __name__, url_prefix='/standards')

@standard_bp.route('', methods=['GET'])
def get_standards():
    standards = Standard.query.all()
    standard_data = []
    for standard in standards:
        standard_info = {
            'id': standard.id,
            'name': standard.name
        }
        standard_data.append(standard_info)
    return jsonify(standard_data)

@standard_bp.route('/<int:id>', methods=['GET'])
def standards_by_(id):
    try:
        standard = Standard.query.get_or_404(id)
        standard_info = {
            'name': standard.name,
            'id': standard.id,
            'class_teacher': standard.teacher.name,
            'students': [student.name for student in standard.students]
        }
        return jsonify(standard_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@standard_bp.route('', methods=['POST'])
def create_new_standard():
    data = request.json
    name = data.get('name')
    teacher_id = data.get('teacher_id')

    try:
        # Create a new Teacher object
        new_standard = Standard(name=name, teacher_id=teacher_id)

        # Add the new Teacher object to the session
        db.session.add(new_standard, teacher_id)

        # Commit the session to persist the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'New standard created successfully'}), 201
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        # Return an error message
        return jsonify({'error': str(e)}), 400


@standard_bp.route('/<int:id>', methods=["DELETE"])
def delete_standard(id):
    try:
        standard = Standard.query.get_or_404(id)

        # Delete associated marks for the student
        db.session.delete(standard)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400