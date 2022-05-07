from flask import Flask, redirect, render_template, request,url_for
import sqlite3
import csv

app = Flask(__name__)

def connect_db():
    con = sqlite3.connect('static/db/sample.db')
    con.row_factory = sqlite3.Row
    return con

def move_to_db():
    con = connect_db()
    cur = con.cursor()
    cur.execute('''CREATE TABLE if not exists inventory
               (code text, name text, batch text, stock real, deal real, free real, mrp real, rate real,
               exp text, company text, supplier text)''')
    with open("static/uploads/new.csv", "r")as f:
        reader = list(csv.reader(f, delimiter=","))
        # print(list(reader))
        for line in reader[1:]:
            print(tuple(line))
            cur.execute(f"insert into inventory values {tuple(line)}")
    con.commit()
    cur.execute("select * from inventory")
    data = [dict(i) for i in cur.fetchall()]
    return data

@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
    # results = move_to_db()
    return render_template("home.html")

@app.route("/upload", methods=['GET','POST'])
def upload():
    data = False
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(dst="static/uploads/new.csv")

            data = True
            return redirect(url_for("home"))

    return render_template("upload.html",data=data)

def get_products(sup):
    con = connect_db()
    cur = con.cursor()
    data = cur.execute(f'''select distinct * from inventory where supplier like "%{sup}%" ''')
    return data
@app.route("/dashboard", methods=['POST'])
def dashboard():
    sup = request.form.get("search")
    data = get_products(sup)
    result = [dict(c) for c in data]
    return render_template("dashboard.html", results=result, header=list(result[0].keys()))
if __name__ == "__main__":
    app.run(debug=True)