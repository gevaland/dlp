import sys

import os

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from typing import List, Optional
from sqlalchemy import ForeignKey, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Session

import numpy as np
from io import BytesIO

sys.path.append("../configs/")

from postgre_config import (
    posgres_user,
    posgres_user_password,
    sql_alchemy_engine,
)
from main_config import video_after_treatment, video_before_treatment


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = "video"

    video_id: Mapped[int] = mapped_column(primary_key=True)
    only_name: Mapped[Optional[str]]
    video_before_treatment: Mapped[Optional[str]]
    video_after_treatment: Mapped[Optional[str]]


def get_engine():
    return create_engine(sql_alchemy_engine)


def get_session():
    return Session(get_engine())


async def add_video(video, video_name):
    session = get_session()

    bp = os.path.join(os.getcwd(), video_before_treatment, video_name)
    ap = os.path.join(os.getcwd(), video_after_treatment, video_name)

    contents = await video.read()
    nparr = np.frombuffer(contents, np.uint8)
    buffer = BytesIO()
    buffer.write(nparr)
    bytes_data = buffer.getvalue()

    with open(bp, "wb") as file:
        file.write(bytes_data)
    video = Video(
        video_before_treatment=bp,
        video_after_treatment=ap,
        only_name=video_name,
    )

    redundant_images = delete(Video).where(Video.video_before_treatment == bp)
    redundant_images = session.execute(redundant_images)
    session.commit()
    session.add(video)
    session.commit()
    return bp, ap


def create_db():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)


def create_tables_in_db():
    os.system("mkdir -p /app/storage/videos_before_treatment")
    os.system("mkdir -p /app/storage/videos_after_treatment")
    engine = get_engine()
    Base.metadata.create_all(engine)


def drop_db():
    engine = get_engine()
    if database_exists(engine.url):
        drop_database(engine.url)


def get_db_user_credentials():
    return {
        "posgres_user": posgres_user,
        "posgres_user_password": posgres_user_password,
        "command": f"sudo -u postgres createuser --login --no-superuser --createdb --createrole -e {posgres_user} -P;",
    }
