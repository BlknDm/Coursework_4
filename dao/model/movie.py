from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from setup_db import db


class Movie(db.Model):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(255))
    trailer = Column(String(255))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey("genre.id"))
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey("director.id"))
    director = relationship("Director")


class MovieSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    trailer = fields.Str(required=True)
    year = fields.Int(required=True)
    rating = fields.Float(required=True)
