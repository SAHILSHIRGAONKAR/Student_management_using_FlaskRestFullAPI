from app import create_app, db
from app.models import Student, Standard, Subject, Teacher, Mark
from random import randint

app = create_app()

def populate_database():
    def create_subject_if_not_exists(subject_name):
        subject = Subject.query.filter_by(name=subject_name).first()
        if subject:
            return subject
        else:
            new_subject = Subject(name=subject_name)
            db.session.add(new_subject)
            db.session.commit()
            return new_subject

    from random import randint


    # Your population code here
    # Create subjects
    english = create_subject_if_not_exists('English')
    hindi = create_subject_if_not_exists('Hindi')
    marathi = create_subject_if_not_exists('Marathi')
    sanskrit = create_subject_if_not_exists('Sanskrit')

    # Create teachers
    ravi_shastri = Teacher(name='Ravi Shastri')
    sanika_tadvi = Teacher(name='Sanika Tadvi')
    jose_portila = Teacher(name='Jose Portila')
    ram_subramanian = Teacher(name='Ram Subramanian')

    # Assign subjects to teachers
    ravi_shastri.subjects_taught.append(hindi)
    sanika_tadvi.subjects_taught.append(marathi)
    jose_portila.subjects_taught.append(english)
    ram_subramanian.subjects_taught.append(sanskrit)

    # Create classes and assign class teachers
    class_xii = Standard(name='XII', teacher=ravi_shastri)
    class_x = Standard(name='X', teacher=sanika_tadvi)
    class_xi = Standard(name='XI', teacher=jose_portila)
    class_ix = Standard(name='IX', teacher=ram_subramanian)

    # Add classes to the session
    db.session.add_all([class_xii, class_x, class_xi, class_ix])
    db.session.commit()

    # Define student data
    students_data = [
        {'roll_no': 1, 'name': 'John Doe', 'standard': 'X', 'city': 'Delhi', 'gender': 'M', 'dob': '2004-01-01'},
        {'roll_no': 2, 'name': 'Jane Smith', 'standard': 'XII', 'city': 'Mumbai', 'gender': 'F', 'dob': '2003-05-15'},
        {'roll_no': 3, 'name': 'Alice Johnson', 'standard': 'IX', 'city': 'Kolkata', 'gender': 'F', 'dob': '2005-07-20'},
        {'roll_no': 4, 'name': 'Bob Brown', 'standard': 'XI', 'city': 'Chennai', 'gender': 'M', 'dob': '2003-11-10'},
        {'roll_no': 5, 'name': 'Michael Clark', 'standard': 'X', 'city': 'Bangalore', 'gender': 'M', 'dob': '2004-03-25'}
    ]

    # Iterate over student data to create and add students to the session
    for student_info in students_data:
        standard_name = student_info['standard']  # Corrected from 'class_' to 'standard'
        # Query the class by name
        student_standard = Standard.query.filter_by(name=standard_name).first()
        if student_standard:
            # Create and add student
            student = Student(
                roll_no=student_info['roll_no'],
                name=student_info['name'],
                standard=student_standard,  # Using the queried standard object
                city=student_info['city'],
                gender=student_info['gender'],
                dob=student_info['dob']
            )
            db.session.add(student)
            db.session.commit()
            # Assuming `subjects` is a list of all subjects, which you need to define or query from the database
            for subject in [english, hindi, marathi, sanskrit]:
                mark = Mark(student_id=student.id, subject_id=subject.id, marks_obtained=randint(60, 100))
                db.session.add(mark)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        populate_database()