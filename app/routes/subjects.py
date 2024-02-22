from flask import Blueprint, jsonify, request
from . import db
from ..models import Subject, Teacher, Standard

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')

# GET ALL SUBJECTS
@subjects_bp.route('', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    subject_data = []
    for subject in subjects:
        teacher = Teacher.query.filter_by(id=subject.teacher_id).first()
        subject_info = {
            'id': subject.id,
            'name': subject.name,
            'teacher': {'id': teacher.id, 'name': teacher.name} if teacher else None
        }
        subject_data.append(subject_info)
    return jsonify(subject_data)


# GET SUBJECT BY ID
@subjects_bp.route('/<int:id>', methods=['GET'])
def get_subject_by_id(id):
    subject = Subject.query.get_or_404(id)
    teacher = Teacher.query.filter_by(id=subject.teacher_id).first()
    subject_info = {
        'id': subject.id,
        'name': subject.name,
        'teacher': {'id': teacher.id, 'name': teacher.name} if teacher else None
    }
    return jsonify(subject_info)


# CREATE SUBJECT
@subjects_bp.route('', methods=['POST'])
def create_subject():
    data = request.json
    teacher_id = data.get('teacher_id')
    if not teacher_id:
        return jsonify({'error': 'Teacher ID is required'}), 400

    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({'error': 'Teacher not found'}), 404

    new_subject = Subject(name=data['name'], teacher_id=teacher_id)
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({'message': 'Subject created successfully'}), 201


# UPDATE SUBJECT
@subjects_bp.route('/<int:id>', methods=['PUT'])
def update_subject(id):
    subject = Subject.query.get_or_404(id)
    data = request.json

    teacher_id = data.get('teacher_id')
    if teacher_id:
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return jsonify({'error': 'Teacher not found'}), 404
        subject.teacher_id = teacher_id

    subject.name = data.get('name', subject.name)

    db.session.commit()
    return jsonify({'message': 'Subject updated successfully'})


# DELETE SUBJECT
@subjects_bp.route('/<int:id>', methods=['DELETE'])
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted successfully'})
