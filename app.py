from flask import Flask, render_template, request
from sqlalchemy import create_engine

from repositories import FormRepository, UserRepository
from services import FormService, LoginService, RegisterService

app = Flask(__name__)
#创建数据库连接
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/form_db")
#数据库操作，表单存储
form_repo = FormRepository(engine)
# 验证表单数据
form_service = FormService(form_repo)

user_repo =  UserRepository(engine)

register_service = RegisterService(user_repo)
login_service = LoginService(user_repo)

@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            result = register_service.register(request.form)
            if  result["status"] == "success":
                print("Register result:", result)
                return render_template("login.html",message=result["message"])
            else:
                print("Registration failed:", result["message"])
                return render_template("register.html",error=result["message"])
        except Exception as e:
            return render_template("register.html",error=str(e))
    #如果是GET请求
    return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        try:
            print("Login data:", request.form)
            result = login_service.login(request.form)
            print("Login result:", result)
            if result["status"] == "success":
                return render_template("form.html")
            else:
                return render_template(
                    "login.html",
                    username_error=result.get("username_error"),
                    password_error=result.get("password_error")
                )
        except ValueError as e:
            print("Login error:", str(e))
            return render_template("login.html",error=str(e))
    #如果是GET请求
    return render_template("login.html")


@app.route('/submit',methods=['GET','POST'])
def form():
    if request.method == 'POST':
        try:
            result = form_service.submit_form(request.form)
            if result["status"] == "success":
                print("Form submission result:", result)
                return render_template("success.html",result=result)
            else:
                print("Form submission failed:", result["message"])
                return render_template("form.html",error=result["message"])            
        except ValueError as e:
            return render_template("form.html",error=str(e))
    #如果是GET请求
    return render_template("form.html")


if __name__ == '__main__':
    app.run(debug=True)
