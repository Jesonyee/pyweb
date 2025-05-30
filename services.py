from pydantic import BaseModel, model_validator, validator, EmailStr
from sqlalchemy.exc import SQLAlchemyError


# 表单数据类型验证
class FormData(BaseModel):
    name: str
    age: int
    sex: str
    hobby: str
    email: EmailStr
    message: str

    @validator('name')
 
    def validate_name(cls, name):
        if not name.string.strip():  # 检查字符串是否为空或仅包含空格
            raise ValueError('姓名不能为空')
        return name
    
    @validator('age')

    def validate_age(cls, age):
        if age < 0 or age > 120:
            raise ValueError('Age must be between 0 and 120')
        return age
    

    
#注册验证
class RegisterData(BaseModel):
    username: str
    password: str
    repassword: str
    
    @validator('password')
    def validate_password(cls, password):
        """验证密码强度"""
        if len(password) < 8:
            raise ValueError('密码长度至少为8个字符')
        if not any(char.isdigit() for char in password):
            raise ValueError('密码必须包含至少一个数字')
        if not any(char.isalpha() for char in password):
            raise ValueError('密码必须包含至少一个字母')
        return password
    
    #before 验证在字段验证之前运行
    @model_validator(mode="before")
    def validate_passwords_match(cls, data):
        password = data.get('password')
        repassword = data.get('repassword')

        if password != repassword:
            raise ValueError('两次输入的密码不一致')
        return data
    
    @validator('username')
    def validate_username(cls, username):
        """验证用户名格式"""
        if len(username) < 3:
            raise ValueError('用户名长度至少为3个字符')
        if ' ' in username:
            raise ValueError('用户名不能包含空格')
        return username
    
#登录验证
class LoginData(BaseModel):
    username: str
    password: str



# 协调表单验证和存储
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
            error_message = str(e).split("[")[0].strip().split("Value error, ")[-1]
            print('error_message:',error_message)
            return {"status": "error", "message": error_message}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "database_error"}

class RegisterService:
    def __init__(self, register_repo):
        self.repo = register_repo

    def register(self,register_data):
        try:
            #验证提交注册数据
            validated_data = RegisterData(**register_data).dict()
            # 存储注册数据到数据库
            self.repo.save_user(validated_data)
            return {"status": "success","message":"注册成功"}
        except ValueError as e:
            error_message = str(e).split("[")[0].strip().split("Value error, ")[-1]
            print('error_message:',error_message)
            return {"status": "error", "message": error_message }
        except SQLAlchemyError:
            return {"status": "error", "message": "数据库出错"}

class LoginService:
    def __init__(self, register_repo):
        self.repo = register_repo

    def login(self, login_data):
        try:
            # 验证数据
            validated_data = LoginData(**login_data).dict()
            # 验证用户名是否存在
            user = self.repo.get_user(validated_data["username"])
            if not user:
                return {"status": "error", "username_error": "用户名不存在"}
            # 验证密码是否正确
            if user.password != validated_data["password"]:
                return {"status": "error","password_error": "密码错误"}
            return  {"status": "success","message": "登录成功"}
        except ValueError  as e:
            return {"status": "error","message": str(e)}

        


