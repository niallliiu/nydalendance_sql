from genericpath import exists
import sqlite3
from flask import Flask, render_template, redirect, url_for, request, g

app = Flask(__name__)

#I got my secret key by print(secrets.token_hex())' 
app.secret_key = 'b89690140290ca5535ddbe4ac3df3a2eb18ef9363c844d94e39f44300cf17f77'


DATABASE = 'dance.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/course")
def course():
    cursor = get_db().cursor()
    cursor.execute("""

        SELECT courses.course_id, courses.course_name, instructors.first_name, instructors.last_name
        FROM courses
        JOIN instructors ON courses.course_id=instructors.ins_id
        LIMIT 5

    """)

    return render_template('courses.html', courses=cursor)

@app.route("/instructor")
def instructor():
    cursor = get_db().cursor()
    cursor.execute("""

        SELECT instructors.first_name, instructors.last_name, instructors.email, instructors.ins_id, instructors.age, courses.course_name, courses.course_id
        FROM instructors
        JOIN courses ON courses.course_id=instructors.ins_id
        LIMIT 5

    """)
    return render_template('instructor.html', instructors = cursor)

@app.route("/cours/<int:customer_id>", methods=['GET', 'POST'])
def cours(customer_id):

    cursor = get_db().cursor()
    cursor.execute("BEGIN")
    cursor.execute("""

        SELECT courses.course_id, courses.already_signed, courses.course_name, courses.session_num, courses.room_num, courses.start_date, instructors.first_name, last_name, courses.price, courses.capacity, instructors.ins_id 
        FROM courses
        JOIN instructors ON courses.course_id=instructors.ins_id
        WHERE courses.course_id=?

    """, [customer_id])
    cours = cursor.fetchone()

    cursor.execute("""

        SELECT signed_id AS signed, customers.first_name, customers.last_name, customers.gender, customers.email
        FROM customers
        JOIN courses ON courses.course_id=customers.customer_id
        WHERE courses.course_id=?

    """, [customer_id])

    cursor.execute("""

        SELECT bookings.courses_id, bookings.customer_id
        FROM bookings
        JOIN courses ON courses.course_id = bookings.courses_id
        JOIN customers ON bookings.customer_id = customers.customer_id
        WHERE (courses.course_id=? AND bookings.courses_id=?) AND (customers.customer_id=? AND bookings.customer_id=?)

    """, [customer_id,customer_id,customer_id,customer_id])

    cursor.execute("""

        SELECT courses.already_signed AS alreadysigned, courses.spot_calculation as spots
        FROM courses
        WHERE courses.course_id=?

    """, [customer_id])
    alreadysigned = cursor.fetchone()['alreadysigned']

    feedback = None
    first_name = ""
    last_name = ""
    gender = ""
    email = ""
    if request.method == 'POST':
        email = request.form['email']
        cursor.execute("SELECT customers.email FROM customers WHERE email=?", [email])
        customer = cursor.fetchone()

        if customer:
            feedback = "The entered email address has already signed up before... each person can only sign up one of our courses!"

        else:
            if  alreadysigned == 0:
                feedback = "This class is full... ! Please contact us for an additional sign-up."

            else: 

                first_name = request.form['first_name']
                last_name = request.form['last_name']
                gender = request.form['gender']
                email = request.form['email']

                cursor.execute("""

                    INSERT INTO customers(first_name, last_name, gender, email, signed_id)

                    VALUES (?, ?, ?, ?, 1)

                """, [first_name,last_name,gender,email])

                cursor.execute("""

                    INSERT OR IGNORE INTO bookings(courses_id, customer_id, spots_num)
                    
                    VALUES (?,?,1)

                """, [customer_id,customer_id])

                cursor.execute("""

                    UPDATE courses

                    SET already_signed=already_signed - 1, spot_calculation=spot_calculation + 1

                    WHERE courses.course_id=?

                """, [customer_id])

                cursor.execute("COMMIT")

                return redirect(url_for("cours", customer_id=customer_id))
    
    html = render_template('cours.html', available_spot = cursor, email=email, cours=cours, customers = cursor, feedback=feedback, first_name = first_name, last_name = last_name, gender = gender, courses = cursor, customer_table = cursor)

    cursor.execute("COMMIT")

    return html