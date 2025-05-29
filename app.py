from flask import Flask, render_template, request
from sqlalchemy import create_engine

from repositories import FormRepository
from services import FormService

app = Flask(__name__)
#创建数据库连接
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/form_db")
#数据库操作，表单存储
form_repo = FormRepository(engine)
# 验证表单数据
form_service = FormService(form_repo)

# register_repo =  UserRepository(engine)

# register_service = RegisterService(register_repo)

@app.route('/')
def index():
    return render_template("login.html")

login_data = {"admin": "123456"}

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            name=request.form.get('username')
            password=request.form.get('password')
            if name in login_data.keys():
              return render_template("register.html",error="用户名已存在")
            else:
              login_data[name] = password
              return render_template("login.html")
        except ValueError as e:
            return render_template("register.html",error=str(e))
    #如果是GET请求
    return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
     try:
        name=request.form.get('username')
        password=request.form.get('password')
        if name in login_data.keys():
            if password == login_data[name]:
                  return render_template("form.html")
            else:
                return render_template("login.html",error="密码错误")
        else:
            return render_template("login.html",error="用户名不存在")
     except ValueError as e:
            return render_template("login.html",error=str(e))
    #如果是GET请求
    return render_template("login.html")


# @app.route('/register',methods=['POST'])
# def register():
#     if request.method == 'POST':
#         try:
#             result = register_service.register(request.form)
#             return render_template("login.html",result=result)
#         except ValueError as e:
#             return render_template("register.html",error=str(e))
#     return render_template("register.html")

# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         try:
#             result = register_service.login(request.form)
#             return render_template("form.html",result=result)
#         except ValueError as e:
#             return render_template("login.html",error=str(e))
#     #如果是GET请求
#     return render_template("login.html")
    

@app.route('/submit',methods=['GET','POST'])
def form():
    if request.method == 'POST':
        try:
            result = form_service.submit_form(request.form)
            return render_template("success.html",result=result)
        except ValueError as e:
            return render_template("form.html",error=str(e))
    #如果是GET请求
    return render_template("form.html")


if __name__ == '__main__':
    app.run(debug=True)
