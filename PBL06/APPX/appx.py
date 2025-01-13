from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# SiteA MS1 and MS2
site_a_db_uri = 'sqlite:///SiteA/DB-A.db'

# SiteB MS3
site_b_db_uri = 'sqlite:///SiteB/DB-B.db'

# Initialize DB
app.config['SQLALCHEMY_DATABASE_URI'] = site_a_db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    return "Microservices App running!"

if __name__ == "__main__":
    app.run(port=5000)
