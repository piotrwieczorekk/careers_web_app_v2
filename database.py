import os

import sqlalchemy
from sqlalchemy import create_engine, text

db_connection_string = os.environ['DB_CONNECTION_STRING']


engine = create_engine(db_connection_string,
                      connect_args={
            "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
                      })

print(sqlalchemy.__version__)

#connect to the engine

def get_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        columns = result.keys()  # Get the column names
        jobs = []
        for row in result:
            row_dict = dict(zip(columns, row))
            jobs.append(row_dict)  # Append each job to the list
        return jobs

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

def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text("""
            INSERT INTO application (job_id, 
            full_name, 
            email, 
            linkedin_url, 
            education,
            work_experience, 
            resume_url)
            VALUES (:job_id,
            :full_name,
            :email,
            :linkedin_url,
            :education,
            :work_experience,
            :resume_url)
        """)

    params = {
            "job_id": job_id,
            "full_name": data['full_name'],
            "email": data['email'],
            "linkedin_url": data['linkedin_url'],
            "education": data['education'],
            "work_experience": data['work_experience'],
            "resume_url": data['resume_url']
        }

        # Use parameter binding to safely insert data into the query
    conn.execute(query, params)