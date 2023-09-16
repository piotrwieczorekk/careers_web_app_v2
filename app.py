from flask import Flask, render_template,jsonify,request, redirect, url_for, session
from database import engine, get_jobs_from_db, load_job_from_db,add_application_to_db,filter_jobs_from_db,add_user_to_db,check_user,load_user_from_db,load_application_from_db, add_job_ad_to_db,load_job_ad_from_db,delete_job_ad_from_db,update_job_ad_from_db
from sqlalchemy import text
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


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


@app.route("/register",methods=['POST'])
def user_registration():
  return render_template('register.html')

@app.route("/account")
def account():
    user = session.get('user')
    user_data = None
    user_job_app = None
    job = load_job_from_db(id)
    if user:
        user_data = load_user_from_db(user['user_id'])
        user_job_app = load_application_from_db(user['user_id'])
        user_job_ads = load_job_ad_from_db(user['user_id'])
        # User is logged in, display account information
        return render_template('account.html', user=user, user_data=user_data, user_job_app = user_job_app,job=job,user_job_ads = user_job_ads)
    else:
        # User is not logged in, display registration and login forms
        return render_template('account.html', user=None)

@app.route("/job/<id>/delete")
def delete_job_ad(id):
    # Call your delete_job_ad_from_db function here with the provided id
    delete_job_ad_from_db(id)
    # Redirect back to the account page or any other appropriate page
    return redirect(url_for('account'))

def get_user_info(id):
  user_data = load_user_from_db(id)
  return user_data


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


@app.route('/account/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    user = check_user(email, password)
    if user is None:
        return render_template('login_failure.html')
    else:
        # Do something with the user's information
        session['user'] = user
        return render_template('login_success.html')


@app.route('/job/<id>/form')
def application_form(id):
    job = load_job_from_db(id)  # Load the job object based on the 'id'
    user = session.get('user')
    if job:
      if user:
        return render_template('application_form.html', job=job,user=user)
      else: 
        return render_template('account.html')
    else:
        return 'There is either no such job ID', 404

@app.route('/job/<id>/form/submit',methods=['POST'])
def submit_application(id):
    data = request.form
    job = load_job_from_db(id)  # Load the job object based on the 'id'
    user = session.get('user')
    user_data = None
    if user:
      user_data = load_user_from_db(user['user_id'])
      add_application_to_db(id, data,user_data)
      return render_template('application_form_submitted.html', job=job,application=data, user_data = user_data)



@app.route('/account/job/<id>/update',methods=['GET'])
def update_job_advertisement(id):
    job_elements = load_job_from_db(id)  # Load the job object based on the 'id'
    return render_template('update_job_ad_form.html', job_elements=job_elements)

@app.route('/account/job/<id>/update/submit',methods=['POST'])
def update_job_advertisement_submit(id):
    job = load_job_from_db(id)
    data = request.form
    update_job_ad_from_db(id, data)
    return render_template('update_job_ad_form_submit.html',updated_data=data,job=job)




@app.route('/addjob/form')
def job_ad_form():
    user = session.get('user')
    if user:
      return render_template('job_ad_form.html',user=user)
    else: 
      return render_template('account.html')



@app.route('/addjob/form/submit',methods=['POST'])
def submit_job_ad():
    data = request.form
    user = session.get('user')
    user_data = None
    if user:
      user_data = load_user_from_db(user['user_id'])
      add_job_ad_to_db(data,user_data)
      return render_template('job_ad_form_submitted.html',ad=data, user_data = user_data)




@app.route('/filter', methods=['POST'])
def filter_jobs():
    title_filter = request.form.get('title-filter')
    location_filter = request.form.get('location-filter')
    currency_filter = request.form.get('currency-filter')
    salary_filter = request.form.get('salary-filter')
    filtered_jobs = filter_jobs_from_db(title_filter,
                                        location_filter,
                                        currency_filter,
                                        salary_filter)

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


@app.route('/account/register', methods=['POST'])
def register_user():
    data = request.form
    add_user_to_db(data)
    # Return a response or render a template as needed
    return render_template('register.html')


@app.route('/account/logout')
def logout():
    # Clear the user's session
    session.pop('user', None)
    # Redirect to the home page or any other appropriate page
    return redirect(url_for('home'))




@app.route('/account/register/check_login', methods=['POST'])
def check_login():
    email = request.form['email']
    password = request.form['password']
    user = check_user(email, password)
    if user is None:
        return render_template('login_failure.html')
    else:
        # Do something with the user's information
        session['user'] = user
        return render_template('login_success.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


