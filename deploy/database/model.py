from werkzeug.security import generate_password_hash, check_password_hash
import db
from sqlalchemy import Column, Boolean, String, Float, DateTime, Text, Date, Time, asc, func
# from datetime import datetime
import os
import json
from datetime import *

def datetime_parser(o):
    if isinstance(o, datetime):
        return o.__str__()

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