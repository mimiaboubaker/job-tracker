from flask import Flask


app = Flask(__name__)

@app('/')

@app("/add_job", method=["POST"])

@app("/edit_job", method=["POST"])

@app("/view_job")