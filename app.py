from flask import Flask, render_template, request, flash, redirect, url_for, send_file, session
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indexFull.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
