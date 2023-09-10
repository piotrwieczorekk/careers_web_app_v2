import sqlalchemy
import os
from sqlalchemy import create_engine,text

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
            row_dict = {col: val for col, val in zip(columns, row)}
            jobs.append(row_dict)  # Append each job to the list
        return jobs

def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs where id = :val"), {"val":id})
    columns = result.keys()  # Get the column names
    jobs = []
    for row in result:
      row_dict = {col: val for col, val in zip(columns, row)}
      jobs.append(row_dict)  # Append each job to the list
    if len(jobs) == 0:
      return None
    else:
      return jobs[0]