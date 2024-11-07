from flask import Flask, render_template, request, redirect, url_for
from models import db, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()

# Home Route - List all students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Create Route - Show form to create new student
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        email = request.form['email']
        new_student = Student(name=name, age=age, grade=grade, email=email)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

# Update Route - Edit an existing student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.grade = request.form['grade']
        student.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', student=student)

# Delete Route - Delete an existing student
@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
