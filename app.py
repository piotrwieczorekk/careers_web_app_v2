from flask import Flask, render_template,jsonify,request
from database import engine, get_jobs_from_db, load_job_from_db,add_application_to_db,filter_jobs_from_db
from sqlalchemy import text
app = Flask(__name__)


@app.route("/")
def home():
    jobs = get_jobs_from_db()
    unique_titles = get_unique_values('title')
    unique_locations = get_unique_values('location')
    unique_currencies = get_unique_values('currency')
    
    return render_template('home2.html', 
                           jobs=jobs,
                           unique_titles=unique_titles,
                           unique_locations=unique_locations,
                           unique_currencies=unique_currencies)

@app.route('/job/<id>')
def job(id):
  job = load_job_from_db(id)
  if job:
    print(job)
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


@app.route('/job/<id>/form')
def application_form(id):
    job = load_job_from_db(id)  # Load the job object based on the 'id'
    if job:
        return render_template('application_form.html', job=job)
    else:
        return 'There is no such job id.', 404

@app.route('/job/<id>/form/submit',methods=['POST'])
def submit_application(id):
    data = request.form
    job = load_job_from_db(id)  # Load the job object based on the 'id'
    add_application_to_db(id, data)
    return render_template('application_form_submitted.html', job=job,application=data)

@app.route('/filter', methods=['POST'])
def filter_jobs():
    title_filter = request.form.get('title-filter')
    location_filter = request.form.get('location-filter')
    currency_filter = request.form.get('currency-filter')

    filtered_jobs = filter_jobs_from_db(title_filter, location_filter, currency_filter)

    return render_template('filtered_jobs.html', jobs=filtered_jobs)

def get_unique_values(column_name):
    jobs = get_jobs_from_db()
    unique_values = set()
    
    for job in jobs:
        if column_name in job:
            # Split the column value by comma and get the first part
            value_parts = job[column_name].split(',')
            if value_parts:
                unique_values.add(value_parts[0].strip())  # Add the part before the first comma
    
    return sorted(list(unique_values))  # Sort and convert to a list


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


