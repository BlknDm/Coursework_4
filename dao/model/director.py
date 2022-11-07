from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String

from setup_db import db


class Director(db.Model):
    __tablename__ = 'director'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)


class DirectorSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
