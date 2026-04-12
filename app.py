from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    name = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
    return render_template('home', name=name)