import json

from flask import Blueprint, jsonify, request
from app import db
from app.models import Student, Mark, Subject, Teacher, Standard

students_bp = Blueprint('students', __name__, url_prefix='/students')

# GET ALL STUDENTS
@students_bp.route('', methods=['GET'])

def get_students():
    try:
        students = Student.query.all()
        student_data = []
        for student in students:
            student_info = {
                'name': student.name,
                'roll_no': student.roll_no,
                'standard': None,
                'class_teacher': None,
                'city': student.city,
                'gender': student.gender,
                'dob': student.dob,
                'subjects': []
            }

            # Get the name of the standard
            standard_name = student.standard.name if student.standard else None
            student_info['standard'] = standard_name

            # Get the class teacher's name for the student's standard
            class_teacher_name = student.standard.teacher.name if student.standard and student.standard.teacher else None
            student_info['class_teacher'] = class_teacher_name

            for mark in student.marks:
                subject_name = mark.subject.name
                teacher_name = mark.subject.teacher.name
                student_info['subjects'].append({
                    'subject_name': subject_name,
                    'subject_id': mark.subject_id,
                    'teacher_name': teacher_name,
                    'marks': mark.marks_obtained
                })
            student_data.append(student_info)

        return jsonify(student_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# GET STUDENT BY ID
@students_bp.route('/<int:id>', methods=['GET'])
def get_student_by_id(id):
    try:
        student = Student.query.get_or_404(id)
        student_info = {
            'name': student.name,
            'roll_no': student.roll_no,
            'standard': None,
            'class_teacher': None,
            'city': student.city,
            'gender': student.gender,
            'dob': student.dob,
            'subjects': []
        }

        # Get the name of the standard
        standard_name = student.standard.name if student.standard else None
        student_info['standard'] = standard_name

        # Get the class teacher's name for the student's standard
        class_teacher_name = student.standard.teacher.name if student.standard and student.standard.teacher else None
        student_info['class_teacher'] = class_teacher_name

        for mark in student.marks:
            subject_name = mark.subject.name
            teacher_name = mark.subject.teacher.name
            student_info['subjects'].append({
                'subject_name': subject_name,
                'subject_id': mark.subject_id,
                'teacher_name': teacher_name,
                'marks': mark.marks_obtained
            })

        return jsonify(student_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# CREATE STUDENT
@students_bp.route('', methods=['POST'])
def create_student():
    try:
        data = request.json
        new_student = Student(name=data['name'], roll_no=data['roll_no'], city=data['city'], gender=data['gender'], dob=data['dob'])

        # Add the student's standard
        standard_name = data.get('standard')
        if standard_name:
            standard = Standard.query.filter_by(name=standard_name).first()
            if standard:
                new_student.standard = standard
            else:
                return jsonify({'error': 'Standard not found'}), 404

        for subject_data in data.get('subjects', []):
            subject_name = subject_data['name']
            marks_obtained = subject_data['marks']

            # Check if subject already exists, otherwise create it
            subject = Subject.query.filter_by(name=subject_name).first()
            if not subject:
                subject = Subject(name=subject_name)
                db.session.add(subject)

            # Add mark for the subject
            mark = Mark(marks_obtained=marks_obtained, subject=subject)
            new_student.marks.append(mark)

        db.session.add(new_student)
        db.session.commit()

        # Print JSON format for the created student
        created_student_info = {
            'name': new_student.name,
            'roll_no': new_student.roll_no,
            'standard': new_student.standard.name if new_student.standard else None,
            'city': new_student.city,
            'gender': new_student.gender,
            'dob': new_student.dob,
            'subjects': []
        }
        for mark in new_student.marks:
            created_student_info['subjects'].append({
                'subject_name': mark.subject.name,
                'marks': mark.marks_obtained
            })

        print(jsonify(created_student_info))

        return jsonify({'message': 'Student created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# UPDATE STUDENT
@students_bp.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.json
        # data_dict = json.loads(data)
        student = Student.query.get(student_id)

        if not student:
            return jsonify({'error': 'Student not found'}), 404
    #     # Update student attributes
        if 'name' in data:
            student.name = data['name']
        if 'roll_no' in data:
            student.roll_no = data['roll_no']
        if 'city' in data:
            student.city = data['city']
        if 'gender' in data:
            student.gender = data['gender']
        if 'dob' in data:
            student.dob = data['dob']
    #
    #     # Update student's standard if provided
        standard_name = data.get('standard')
        if standard_name:
            standard = Standard.query.filter_by(name=standard_name).first()
            if standard:
                student.standard = standard
            else:
                return jsonify({'error': 'Standard not found'}), 404
    #
    #     # Clear existing marks and update student's subjects and marks
        student.marks.clear()
        for subject_data in data.get('subjects', []):
            subject_name = subject_data['name']
            marks_obtained = subject_data['marks']

            # Check if subject already exists, otherwise create it
            subject = Subject.query.filter_by(name=subject_name).first()
            if not subject:
                subject = Subject(name=subject_name)
                db.session.add(subject)
                db.session.flush()  # Ensure subject is persisted before creating mark

            # Add mark for the subject and associate it with the student
            mark = Mark(marks_obtained=marks_obtained, student_id=student_id, subject=subject)
            db.session.add(mark)

        db.session.commit()

        return jsonify({'message': 'Student updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# DELETE STUDENT
@students_bp.route('/<int:id>', methods=['DELETE'])
def delete_student_by_id(id):
    try:
        student = Student.query.get_or_404(id)

        # Delete associated marks for the student
        for mark in student.marks:
            db.session.delete(mark)

        # Now delete the student
        db.session.delete(student)

        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400