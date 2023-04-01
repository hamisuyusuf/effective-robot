from sqlalchemy import create_engine, text
from dataclasses import dataclass, asdict 

@dataclass
class Job:
    id: int
    title: str
    salary: int
    requirements: str
    responsibilities: str
    location: str
    currency: str  

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
        column_names = result.keys()
        rows = result.fetchall()
        jobs = [dict(zip(column_names, row)) 
      for row in rows]
        return jobs




def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, title, salary, requirements, responsibilities, location, currency FROM jobs WHERE id = :val"), {"val": id})
        
    rows = result.fetchall()
    if len(rows) == 0:
        return None
    else:
        jobs = [Job(*row) for row in rows]
        return [asdict(job) for job in jobs]








