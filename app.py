import sqlite3

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('SQLiteDB.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('layout/dashboard.html')


@app.route('/users')
def users():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students order by id desc ').fetchall()
    conn.close()
    return render_template('layout/users.html', data=students)


@app.route('/view_user')
def view_user():
    user_data = {key: request.args.get(key) for key in ['name', 'gender', 'phone', 'email', 'address']}
    return render_template('layout/view_user.html', user_data=user_data)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (user_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        conn.execute('UPDATE students SET name = ?, gender = ?, phone = ?, email = ?, address = ? WHERE id = ?',
                     (name, gender, phone, email, address, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))

    conn.close()
    return render_template('layout/edit_user.html', data=student)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        conn = get_db_connection()

        row_count = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
        new_id = row_count + 1

        conn.execute('INSERT INTO students (name, gender, phone, email, address) VALUES (?, ?, ?, ?, ?)',
                     (name, gender, phone, email, address))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))

    return render_template('layout/add_user.html')


@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))


@app.route('/confirm_delete/<int:user_id>')
def confirm_delete(user_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    user_data = {
        'id': student['id'],
        'name': student['name'],
        'gender': student['gender'],
        'phone': student['phone'],
        'email': student['email'],
        'address': student['address']
    }
    return render_template('layout/confirm_delete.html', user_data=user_data)


if __name__ == '__main__':
    app.run()
