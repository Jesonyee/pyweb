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


@app.route('/',methods=['GET','POST'])
def form():
    if request.method == 'POST':
        try:
            result = form_service.submit_form(request.form)
            return render_template("success.html",result=result)
        except ValueError as e:
            return render_template("form.html",error=str(e))
    return render_template("form.html")


if __name__ == '__main__':
    app.run(debug=True)
