from pydantic import BaseModel, validator, EmailStr
from sqlalchemy.exc import SQLAlchemyError


# 数据类型验证
class FormData(BaseModel):
    name: str
    age: int
    sex: str
    hobby: str
    email: EmailStr
    message: str

    @validator('age')
    def validate_age(cls, age):
        if age < 0 or age > 120:
            raise ValueError('Age must be between 0 and 120')
        return age
# 协调验证和存储
class FormService:
    def __init__(self, form_repo):
        self.repo = form_repo

    def submit_form(self,form_data):
        try:
            validated_data = FormData(**form_data).dict()
            self.repo.save_form(validated_data)
            return {"status": "success"}
        except ValueError as e:
            return {"status": "error", "message": str(e)}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "database_error"}

