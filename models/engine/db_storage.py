#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        if cls is not None:
            dict_obj = {}
            result = self.__session.query(cls).all()
            for obj in result:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                dict_obj[key] = obj
            return dict_obj
        if cls is None:
            from models.city import City
            from models.amenity import Amenity
            from models.place import Place
            from models.review import Review
            from models.user import User
            classes = [State, City, Amenity, Place, Review, User]
            dict_obj = {}
            for c in classes:
                result = self.__session.query(c).all()
                for obj in result:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    dict_obj[key] = obj
            return dict_obj

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """A method to retrieve one object."""
        obj = self.all(cls)
        key = f"{cls}.{id}"
        return obj.get(key, None)

    def count(self, cls=None):
        """A method to count the number of objects in storage."""
        obj = self.all()
        count = 0
        if cls is not None:
            for item in obj.values():
                if item.__class__.__name__ == cls:
                    count += 1
            return count
        else:
            for item in obj.values():
                count += 1
            return count
