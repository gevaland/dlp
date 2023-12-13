import sys

import os

from sqlalchemy_utils import database_exists, create_database, drop_database

from typing import Optional
from sqlalchemy import (
    delete,
    ARRAY,
    create_engine,
    Column,
    Integer,
    String,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import numpy as np
from io import BytesIO

sys.path.append("../configs/")

from postgre_config import (
    sql_alchemy_engine,
)
from main_config import resume_storage, job_storage

Base = declarative_base()


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    vector = Column(ARRAY(Float))


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    vector = Column(ARRAY(Float))


def get_engine():
    return create_engine(sql_alchemy_engine)


def get_session():
    return Session(get_engine())


async def add_file_to_db(file, file_name, option, vector):
    session = get_session()
    file_path = None
    adding_subject = None
    if option == "Resume":
        file_path = os.path.join(os.getcwd(), resume_storage, file_name)
        adding_subject = Resume(file_path=file_path, vector=vector)
    elif option == "Job":
        file_path = os.path.join(os.getcwd(), job_storage, file_name)
        adding_subject = Job(file_path=file_path, vector=vector)
    redundant_resumes = delete(Resume).where(Resume.vector == vector)
    session.execute(redundant_resumes)
    session.commit()
    redundant_resumes = delete(Job).where(Job.vector == vector)
    session.execute(redundant_resumes)
    session.commit()
    session.add(adding_subject)
    session.commit()
    return adding_subject.id


def get_all_jobs():
    session = get_session()
    jobs = session.query(Job).all()
    return jobs


def get_all_resumes():
    session = get_session()
    resumes = session.query(Resume).all()
    return resumes


def get_job_by_id(id):
    session = get_session()
    job = session.query(Job).get(id)
    return job


def get_resume_by_id(id):
    session = get_session()
    resume = session.query(Resume).get(id)
    return resume


def create_db():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)


def create_tables_in_db():
    os.system(f"mkdir -p /app/{resume_storage}")
    os.system(f"mkdir -p /app/{job_storage}")
    engine = get_engine()
    Base.metadata.create_all(engine)


def drop_db():
    engine = get_engine()
    if database_exists(engine.url):
        drop_database(engine.url)


def walk_directory(directory, vector_generator):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            vector = vector_generator(file_path)
            yield file_path, vector


def populate_resumes_or_job(directory, model, db, vector_generator):
    for file_path, vector in walk_directory(directory, vector_generator):
        db_object = model(file_path=file_path, vector=vector)
        db.add(db_object)
    db.commit()


def populate_resumes(directory: str, db=get_session(), vector_generator=None):
    populate_resumes_or_job(directory, Resume, db, vector_generator)


def populate_jobs(directory: str, db=get_session(), vector_generator=None):
    populate_resumes_or_job(directory, Job, db, vector_generator)
