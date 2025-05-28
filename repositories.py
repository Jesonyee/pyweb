from sqlalchemy.orm import sessionmaker
from models import Base, FormSubmission

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