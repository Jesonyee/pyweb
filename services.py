from pydantic import BaseModel, root_validator, validator, EmailStr
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
    

# class RegisterData(BaseModel):
#     username: str
#     password: str
#     repassword: str
    
#     @validator('password')
#     def validate_password(cls, password):
#         """验证密码强度"""
#         if len(password) < 8:
#             raise ValueError('密码长度至少为8个字符')
#         if not any(char.isdigit() for char in password):
#             raise ValueError('密码必须包含至少一个数字')
#         if not any(char.isalpha() for char in password):
#             raise ValueError('密码必须包含至少一个字母')
#         return password
    
#     @root_validator
#     def validate_passwords_match(cls, values):
#         """验证两次输入的密码是否一致"""
#         password = values.get('password')
#         repassword = values.get('repassword')
        
#         if password != repassword:
#             raise ValueError('两次输入的密码不一致')
#         return values
    
#     @validator('username')
#     def validate_username(cls, username):
#         """验证用户名格式"""
#         if len(username) < 3:
#             raise ValueError('用户名长度至少为3个字符')
#         if ' ' in username:
#             raise ValueError('用户名不能包含空格')
#         return username
    

# class LoginData(BaseModel):
#     username: str
#     password: str



# 协调验证和存储
class FormService:
    def __init__(self, form_repo):
        self.repo = form_repo

    def submit_form(self,form_data):
        try:
            #验证提交表单数据
            validated_data = FormData(**form_data).dict()
            # 存储表单数据到数据库
            self.repo.save_form(validated_data)
            return {"status": "success"}
        except ValueError as e:
            return {"status": "error", "message": str(e)}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "database_error"}

# class RegisterService:
#     def __init__(self, register_repo):
#         self.repo = register_repo

#     def register(self,register_data):
#         try:
#             #验证提交注册数据
#             validated_reg = RegisterData(**register_data).dict()
#             # 存储注册数据到数据库
#             self.repo.save_user(validated_reg)
#             return {"status": "success"}
#         except ValueError as e:
#             return {"status": "error", "message": str(e)}
        


