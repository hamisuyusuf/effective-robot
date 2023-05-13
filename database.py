from sqlalchemy import create_engine, text
import os


db_connection_string =os.environ['DB_CONNECTION_STRING']
engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
    }
)

def load_jobs_from_db():
    with engine.connect() as conn:
      
      result = conn.execute(text("select * from jobs"))
      #   column_names = result.keys()
      #   rows = result.fetchall()
      #   jobs = [dict(zip(column_names, row)) 
      # for row in rows]
      #   return jobs
      jobs =[]
      for row in result.all():
        jobs.append(dict(row._mapping))
      return jobs  




def  load_job_from_db(id):
    with engine.connect() as conn:
        
        result = conn.execute(
          text(f"SELECT * FROM jobs WHERE id = :val"),
          {"val": id}
        )
        
    rows = result.mappings().all()
    if len(rows) == 0:
        return None
    else:
      return dict(rows[0])

def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO applications (job_id, name, linkedIn_url, resume_link) VALUES (:job_id, :name, :email, :linkedIn_url, :resume_link)")

    conn.execute(query, 
             job_id=job_id,
             name=data['name'],
             email=data['email'],
             linkedIn_url=data['linkedIn_url'],
             resume_link=data['resume_link']
            )




