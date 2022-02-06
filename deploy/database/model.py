from werkzeug.security import generate_password_hash, check_password_hash
import db
from sqlalchemy import Column, Integer, String, Float, DateTime
# from datetime import datetime
import os
import json
from datetime import *

def datetime_parser(o):
    if isinstance(o, datetime):
        return o.__str__()

class UserSongFeedback(db.Base):
    __tablename__ = 'user_song_feedback'

    id = Column(Integer, primary_key=True)
    song_uri = Column(String(255), nullable=False)
    song_id = Column(String(255), nullable=False)
    song_name = Column(String(255), nullable=False)
    song_artist = Column(String(255), nullable=False)
    request_user_id = Column(String(255), nullable=False)
    feedback = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, song_uri, song_id, song_name, song_artist, user_id, feedback):
        self.song_uri = song_uri
        self.song_id = song_id
        self.feedback = feedback
        self.song_name = song_name
        self.song_artist = song_artist
        self.request_user_id = user_id
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<UserSongFeedback %r>' % self.song_id

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_feedback_by_user_id(request_user_id):
        return db.session.query(UserSongFeedback).filter_by(request_user_id=request_user_id).first()

    @staticmethod
    def get_last_entry():
        return db.session.query(UserSongFeedback).order_by(UserSongFeedback.timestamp.desc()).first() 

    @staticmethod
    def get_unique_count():
        return db.session.query(UserSongFeedback).distinct(UserSongFeedback.song_id).count()
    
    @staticmethod
    def get_unique_count_today():
        """
            Gets the unique count of songs added today
        """
        today = datetime.now().date()
        return db.session.query(UserSongFeedback).filter(UserSongFeedback.timestamp.between(today, today + timedelta(days=1))).distinct(UserSongFeedback.song_id).count()

class DataEntry(db.Base):
    __tablename__ = 'data_entries'
    id = Column(String(256), primary_key=True)
    model_updated_accuracy = Column(Float)
    model_updated_precission = Column(Float)
    model_updated_recall = Column(Float)
    model_updated_f1_score = Column(Float)
    
    model_updated_new_songs_number = Column(Float)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.id}>'

    def set_id(self, id):
        self.id = id

    def set_name(self, id):
        self.id = id
           
    def save(self):
        db.session.add(self)
        db.session.commit()
        #self.save_json()
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # this functions gets the object as a dictionary and saves it to a json file
    def save_json(self):
        #write json file on path where file is located
        json_file_path = "./controller"+ os.path.dirname(self.file_path) + '/{0}.json'.format(self.id)
        print(json_file_path)
        with open(json_file_path, 'w') as f:
            json.dump(self.as_dict(), f, default = datetime_parser)

    def delete(self):
        print(self.file_path)
        db.session.query(DataEntry).filter(DataEntry.id == self.id).delete()
        db.session.commit()
        return True

    def get_last_entry(self):
        return db.session.query(DataEntry).order_by(DataEntry.created_date.desc()).first()
        
    @staticmethod
    def get_by_id(id):
        return db.session.query(DataEntry).get(id)
    
    @staticmethod
    def get_all():
        return db.session.query(DataEntry).all()

    @staticmethod
    def get_unique_count():
        return db.session.query(DataEntry).distinct(DataEntry.id).count()