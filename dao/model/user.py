from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from dao.model.genre import GenreSchema
from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    favourite_genre_id = Column(Integer, ForeignKey('genre.id'))
    favourite_genre = Column(String)


class UserSchema(Schema):
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    surname = fields.Str()
    favourite_genre = fields.Nested(GenreSchema, only=['name'])
