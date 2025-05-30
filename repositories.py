from sqlalchemy.orm import sessionmaker
from models import Base, FormSubmission, User

# 数据库交互
class FormRepository:
    def __init__(self, engine):
        self.engine = engine
        # 创建表
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def save_form(self,form_data):
        # 打开数据库连接
        session = self.Session()
        submission = FormSubmission(**form_data)
        session.add(submission)
        session.commit()
        session.close()

class UserRepository:
    def __init__(self, engine):
        self.engine = engine
        # 创建表
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def save_user(self,user_data):
        # 打开数据库连接
        session = self.Session()
        try:
            user = User(
                username=user_data['username'], 
                password=user_data['password']
                        )
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    def get_user(self, username):
        session = self.Session()
        try:
            user = session.query(User).filter(User.username == username).first()
            return user
        finally:
            session.close()
