from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('home.html')