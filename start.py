from flask import Flask,render_template,request,session,redirect,url_for
from sdk import GeetestLib
import json

app = Flask(__name__)
pc_geetest_id = "48a6ebac4ebc6642d68c217fca33eb4d"
pc_geetest_key = "4f1c085290bec5afdc54df73535fc361"

@app.route('/pc-geetest/register',methods=['GET'])
def registe():
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id,pc_geetest_key)
    status = gt.pre_process(user_id=user_id,new_captcha=0)
    session[gt.GT_STATUS_SESSION_KEY] = status
    session['user_id'] = user_id
    response = gt.get_response_str()
    return response

@app.route('/pc-geetest/validate',methods=['POST'])
def validate():
    gt = GeetestLib(pc_geetest_id,pc_geetest_key)
    challenge = request.form[gt.FN_CHALLENGE]
    seccode = request.form[gt.FN_SECCODE]
    validate = request.form[gt.FN_VALIDATE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    user_id = session['user_id']
    if status:
        result = gt.success_validate(challenge,validate,seccode,user_id)
    else:
        result = gt.failback_validate(challenge,validate,seccode)
    result = '<html><body><h1>登陆成功</h1></body></html>' if result else '<html><body><h1>登陆失败</h1></body></html>'
    return result

@app.route('/')
def login():
    return render_template('login.html')




if __name__ == '__main__':
    app.secret_key = 'i-like-python-nmba'
    app.run(debug=True)
