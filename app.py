from flask import Flask, render_template,jsonify
from database import engine, get_jobs_from_db, load_job_from_db
from sqlalchemy import text

app = Flask(__name__)


@app.route("/")
def home():
  jobs = get_jobs_from_db()
  return render_template('home2.html', 
                         jobs=jobs)

@app.route('/job/<id>')
def job(id):
  job = load_job_from_db(id)
  if job:
    return render_template('job_id_page.html', 
                          job=job)
  else:
    return 'There is no such job id.',404

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


