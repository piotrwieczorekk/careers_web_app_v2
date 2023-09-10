from flask import Flask, render_template,jsonify
from database import engine, get_jobs_from_db
from sqlalchemy import text

app = Flask(__name__)


@app.route("/")
def home():
  jobs = get_jobs_from_db()
  return render_template('home2.html', 
                         jobs=jobs)

@app.route('/about')
def about_us():
    return render_template('about.html')

@app.route('/questions')
def frequently_asked_questions():
    return render_template('questions.html')

@app.route('/features')
def features():
    return render_template('features.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


