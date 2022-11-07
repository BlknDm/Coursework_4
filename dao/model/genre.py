from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String

from setup_db import db


class Genre(db.Model):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)


class GenreSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)