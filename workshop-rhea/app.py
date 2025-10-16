from flask import Flask, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)



def db_con():
    conn = psycopg2.connect(
        dbname="workshop",
        user="rheamodey",
        password="password",
        host="localhost",
        port="5432"
    )
    return conn

def create_table():
    conn = db_con()
    curr = conn.cursor()
    curr.execute("""DROP TABLE IF EXISTS tasks""")

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
    conn = db_con()
    curr = conn.cursor()
    curr.execute("SELECT id, assignment, classname, done FROM tasks ORDER BY done ASC;")
    tasks = curr.fetchall()
    curr.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_tasks():
    assignment = request.form['title']
    classname = request.form.get('year','')

    conn = db_con()
    curr = conn.cursor()

    curr.execute("INSERT INTO tasks (assignment, classname) VALUES (%s,%s);", (assignment, classname))
    conn.commit()
    curr.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):

    conn = db_con()
    curr = conn.cursor()

    curr.execute("UPDATE tasks SET done = NOT done WHERE id = %s;", (id,))
    conn.commit()
    curr.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):

    conn = db_con()
    curr = conn.cursor()

    curr.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()

    curr.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

# def index():
#     conn = db_con()
#     curr = conn.cursor()
#     curr.execute("")

#     curr.close()
#     conn.close()

