from flask_wtf import form
from application import app,db
# from application import api
from sqlalchemy import desc
from flask import render_template,request, Response, json, redirect, flash, url_for, session, jsonify
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
# from flask_restplus import Resource

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]


#################################################
# @api.route('/api','/api/')
# class GetAndPost(Resource):
    

#     def get(self):
#         return jsonify(User.query.all())
    
#     def post(self):
#         data = api.payload
#         user = User( email = data['email'], first_name = data['first_name'], last_name = data['last_name'])
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         return jsonify(User.query.filter_by(user_id = idx).first())
         


# @api.route('/api/<idx>')
# class GetUpdateDelete(Resource):
    
#     def get(self,idx):
#         return jsonify(User.query.filter_by(user_id = idx).first())

#     def put(self, idx):
#         User.query.filter_by(user_id = idx).first()

#     def delete(self, idx):
#         User.query.filter_by(user_id = idx).first()






###################################################


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', index = True)


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term = None):
    if term is None:
        term = "Spring 2019"
    courseData = Course.query.order_by(desc("title")).all()
    return render_template('courses.html', courseData = courseData, courses = True, term = term)

@app.route("/register",methods = ["GET","POST"])
def register():
    if not session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User( email = email, first_name = first_name, last_name = last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('You are successfully registered',"success")
        return redirect(url_for('index'))
    return render_template('register.html', title = "Register", form = form, register = True)


@app.route("/login", methods = ["GET","POST"])
def login():
    title = "Login"
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        if user and user.get_password(password):
         session["user_id"] = user.user_id
         session["username"] = user.first_name
         flash(f"{user.first_name} You are successflully logged in!!!", "success")
         return redirect('/index')
        else:
            flash("Something went wrong", "danger")
    return render_template('login.html', title = title, form = form, login = True)

@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('index'))
    else:
     user_id = session.get('user_id')
     course_id = request.form.get('course_id')
     title = request.form.get('title')
     if course_id:
        enrollment_data = Enrollment.query.filter_by(user_id = user_id, course_id = course_id).first()
        print(enrollment_data)
        if enrollment_data:
            flash(f"Oops you have already registered for this course {title}!", "danger")
            return redirect(url_for("courses"))
        else:
            enrollment = Enrollment(user_id = user_id, course_id = course_id)
            db.session.add(enrollment)
            db.session.commit()
            flash(f"You are enrolled in {title}!","success ")
     classes = Enrollment.query.filter_by(user_id = user_id).all()
     return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)    


# @app.route("/api/")
# @app.route("/api/<id>")
# def api(id = None):
#     if id is None:
#         resData = courseData
#     else:
#         resData = courseData[int(id)]
#     return Response(json.dumps(resData),mimetype="application/json")

@app.route("/users")
def user():
    users = User.query.all()
    # resData = {"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}
    return render_template('users.html',users = users)
    # return Response(json.dumps(resData), mimetype="application/json")
  

@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))