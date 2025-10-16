from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Connect to the database
def db_com():
    conn = psycopg2.connect(
        dbname="workshop",
        user="postgres",
        password="K@sinamb1",
        host="localhost",
        port="5432"
    )
    return conn

# create table
def create_table():
    conn = db_com()
    curr = conn.cursor()
    curr.execute("DROP TABLE IF EXISTS tasks;")

    curr.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
                 id SERIAL PRIMARY KEY,
                 assignment TEXT NOT NULL,
                 classname TEXT,
                 done BOOLEAN DEFAULT FALSE);
    """)

    conn.commit()
    curr.close()
    conn.close()

create_table()

@app.route('/')
def index():
    conn = db_com()
    curr = conn.cursor()

    curr.execute("SELECT id, assignment, classname, done FROM tasks ORDER BY done ASC;")

    tasks = curr.fetchall()

    curr.close()
    conn.close()

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_tasks():
    # connect to html
    assignment = request.form['title']
    year = request.form.get('year', '')

    conn = db_com()
    curr = conn.cursor()

    curr.execute("INSERT INTO tasks (assignment, classname) VALUES (%s, %s);", (assignment, year))
    conn.commit()

    curr.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    conn = db_com()
    curr = conn.cursor()

    curr.execute("UPDATE tasks SET done = NOT done WHERE id = %s;", (id,))
    conn.commit()

    curr.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    conn = db_com()
    curr = conn.cursor()

    curr.execute("DELETE FROM tasks WHERE id = %s;", (id,))
    conn.commit()

    curr.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)