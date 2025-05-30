from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
#定义数据表结构
class FormSubmission(Base):
    __tablename__ = 'form_submissions'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    sex = Column(String(10))
    hobby = Column(String(50))
    email = Column(String(50))
    message = Column(Text)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True,nullable=False)
    password = Column(String(50),nullable=False)