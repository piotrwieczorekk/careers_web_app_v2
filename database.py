import os
import sqlalchemy
from sqlalchemy import create_engine, text, and_, select
import bcrypt

db_connection_string = os.environ['DB_CONNECTION_STRING']


engine = create_engine(db_connection_string,
                      connect_args={
            "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
                      })

print(sqlalchemy.__version__)

#connect to the engine

def get_jobs_from_db(limit=10, offset=0):
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs ORDER BY id DESC LIMIT :limit OFFSET :offset"), {"limit": limit, "offset": offset})
        columns = result.keys()  # Get the column names
        jobs = []
        for row in result:
            row_dict = dict(zip(columns, row))
            jobs.append(row_dict)  # Append each job to the list
        return jobs


def check_user(user_email, password):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM app_users WHERE user_email = :user_email"), {"user_email": user_email})
        columns = result.keys()  # Get the column names
        users = []
        for row in result:
            row_dict = dict(zip(columns, row))
            users.append(row_dict)  # Append each user to the list

        if len(users) == 0:
            return None
        else:
            user = users[0]
            hashed_password = user['user_password']

            # Compare the entered password with the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return user
            else:
                return None



def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs where id = :val"), {"val":id})
    columns = result.keys()  # Get the column names
    jobs = []
    for row in result:
      row_dict = dict(zip(columns, row))
      jobs.append(row_dict)  # Append each job to the list
    if len(jobs) == 0:
      return None
    else:
      return jobs[0]


def load_user_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("select user_email, created_at, user_id from app_users where user_id = :val"), {"val":id})
    columns = result.keys()  # Get the column names
    users = []
    for row in result:
      row_dict = dict(zip(columns, row))
      users.append(row_dict)  # Append each job to the list
    if len(users) == 0:
      return None
    else:
      return users[0]


def load_application_from_db(user_id):
  with engine.connect() as conn:
    result = conn.execute(text("""
    SELECT t1.job_id,
    t1.full_name,
    t1.email,
    t1.linkedin_url,
    t1.education,
    t1.work_experience,
    t1.resume_url,
    t1.created_at,
    t2.title
    FROM application t1
    INNER JOIN jobs t2
    ON t1.job_id = t2.id 
    WHERE t1.user_id = :val"""), {"val":user_id})
    columns = result.keys()  # Get the column names
    job_app = [dict(zip(columns, row)) for row in result]

    return job_app if job_app else []  # Return an empty list if no job applications are found

def load_job_ad_from_db(user_id):
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs where user_id = :val"), {"val":user_id})
    columns = result.keys()  # Get the column names
    job_ad = [dict(zip(columns, row)) for row in result]

    return job_ad if job_ad else []  # Return an empty list if no job applications are found


def delete_job_ad_from_db(id):
  with engine.connect() as conn:
    conn.execute(text("""DELETE FROM jobs WHERE id = :val"""), {"val":id})

def update_job_ad_from_db(id,data):
  with engine.connect() as conn:
    conn.execute(text("""UPDATE jobs
    SET company_name = :company_name,
    title = :title, 
    location = :location,
    salary = :salary,
    currency = :currency,
    responsibilities = :responsibilities,
    requirements = :requirements
    WHERE id = :val"""), {"val":id,"company_name":data['company_name'],
              "title":data['title'],
              "location":data['location'],
              "salary":data['salary'],
              "currency":data['currency'],
              "responsibilities":data['responsibilities'],
              "requirements":data['requirements']})



def add_application_to_db(job_id, data, user_data):
  with engine.connect() as conn:
    query = text("""
            INSERT INTO application (job_id, 
            user_id,
            full_name, 
            email, 
            linkedin_url, 
            education,
            work_experience, 
            resume_url)
            VALUES (:job_id,
            :user_id,
            :full_name,
            :email,
            :linkedin_url,
            :education,
            :work_experience,
            :resume_url)
        """)

    params = {
            "job_id": job_id,
            "user_id": user_data['user_id'],
            "full_name": data['full_name'],
            "email": data['email'],
            "linkedin_url": data['linkedin_url'],
            "education": data['education'],
            "work_experience": data['work_experience'],
            "resume_url": data['resume_url']
        }

        # Use parameter binding to safely insert data into the query
    conn.execute(query, params)

def add_job_ad_to_db(data, user_data):
  with engine.connect() as conn:
    query = text("""
            INSERT INTO jobs (
            user_id,
            title, 
            company_name, 
            location, 
            salary,
            currency,
            responsibilities,
            requirements)
            VALUES (
            :user_id,
            :title,
            :company_name,
            :location,
            :salary,
            :currency,
            :responsibilities,
            :requirements)
        """)
    params = {
            "user_id": user_data['user_id'],
            "title": data['title'],
            "company_name": data['company_name'],
            "location": data['location'],
            "salary": data['salary'],
            "currency": data['currency'],
            "responsibilities": data['responsibilities'],
            "requirements": data['requirements']
        }
    conn.execute(query, params)

def add_user_to_db(data):
  with engine.connect() as conn:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'), salt)
    query = text("""
            INSERT INTO app_users (
            user_email, 
            user_password)
            VALUES (
            :user_email,
            :user_password)
        """)

    params = {
            "user_email": data['user_email'],
             "user_password": hashed_password.decode('utf-8')
        }
        # Use parameter binding to safely insert data into the query
    conn.execute(query, params)





def filter_jobs_from_db(title_filter, location_filter, currency_filter, salary_filter):
    conditions = []
    params = {}

    if title_filter:
        conditions.append(text("title LIKE :title"))
        params["title"] = f"%{title_filter}%"

    if location_filter:
        conditions.append(text("location LIKE :location"))
        params["location"] = f"%{location_filter}%"

    if currency_filter:
        conditions.append(text("currency = :currency"))
        params["currency"] = currency_filter

    query = select(("*")).select_from(text("jobs"))

    if conditions:
        condition = and_(*conditions)
        query = query.where(condition)

    if salary_filter:
        if salary_filter == "Ascending":
            query = query.order_by(text("salary ASC"))
        else:
            query = query.order_by(text("salary DESC"))

    with engine.connect() as conn:
        result = conn.execute(query, params)

        columns = result.keys()
        jobs = [dict(zip(columns, row)) for row in result]

    return jobs





