from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
from flask import Flask, send_file

from scripts.hierarchy_gen import list_files_and_directories_in_camel_case

app = Flask(__name__)
# load the sqlite database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)


# create a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


class Hierarchy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level1 = db.Column(db.String(80), nullable=False)
    level2 = db.Column(db.String(80), nullable=False)
    level3 = db.Column(db.String(80), nullable=True)
    title = db.Column(db.String(120), nullable=False)
    date_modified = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Hierarchy %r>' % self.title


def generate_data():
    # Create a new Hierarchy object
    new_hierarchy = Hierarchy(
        level1='Level 1',
        level2='Level 2',
        level3='Level 3',
        title='Title',
        date_modified=datetime.utcnow()
    )

    # Add the new Hierarchy object to the database
    db.session.add(new_hierarchy)
    db.session.commit()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/generate_data', methods=['POST', 'GET'])
def generate_data_route():
    generate_data()
    return 'Data generated successfully', 200


@app.route('/get_file/<path:file_path>', methods=['GET'])
def get_file(file_path):
    try:
        return send_file('assets/' + file_path, as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/get_hierarchy', methods=['GET'])
def get_hierarchy():
    hierarchy = list_files_and_directories_in_camel_case('assets')
    return hierarchy


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
