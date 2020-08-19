

from flask import Flask, render_template, request, flash, session, redirect
from forms import SignUpForm, SignInForm, TaskForm, ProjectForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY']='HoangPN Python-Flask Web App'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
migrate=Migrate(app, db)

import models

@app.route('/')
def main():
    todolist=[
        {
            'name': 'Buy milk',
            'des': 'Buy 2 lits of milk'
        },
        {
            'name': 'Get money',
            'des': 'Get 500k from ATM'
        },
        {
            'name': 'Get money',
            'des': 'Get 500k from ATM'
        },
        {
            'name': 'Get money',
            'des': 'Get 500k from ATM'
        },
        {
            'name': 'Get money',
            'des': 'Get 500k from ATM'
        },
        {
            'name': 'Get money',
            'des': 'Get 500k from ATM'
        },
    ]
    return  render_template('index.html',todolist=todolist)

@app.route('/signUp', methods=['GET','POST'])
def showSignUp():
    form = SignUpForm()

    # Nhận giá trị từ form
    # if form.is_submitted():
    #     _name=form.inputName.data
    #     _email=form.inputEmail.data
    #     _password=form.inputPassword.data
      
    #     user={'name': _name, 'email': _email, 'password': _password}
    #     return render_template('signUpSuccess.html', user=user)

    if form.validate_on_submit():
        print("Validate on submit")
        _fname=form.inputFirstName.data
        _lname=form.inputLastName.data
        _email=form.inputEmail.data
        _password=form.inputPassword.data

        # user={'first_name': _fname,'last_name': _lname, 'email': _email, 'password_hash': _password}
        if(db.session.query(models.User).filter_by(email=_email).count() == 0):
            user = models.User(first_name = _fname, last_name = _lname, email=_email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()
            return render_template('signUpSuccess.html', user=user)
        else:
            flash('Email {} is already axists'.format(_email))
            return render_template('signup.html',form = form)
    print("Not validate on submit")
    return render_template('signup.html', form = form)

@app.route('/signIn', methods=['GET','POST'])
def signIn():
    form = SignInForm()
    
    if form.validate_on_submit():
        print("Validate on submit")
        _email=form.inputEmail.data
        _password=form.inputPassword.data

        user = db.session.query(models.User).filter_by(email=_email).first()
        if (user is None):
            flash('Wrong email address or password')
        else:
            if (user.check_password(_password)):
                session['user'] = user.user_id
                # return render_template('username.html')
                return redirect('/userHome')
            else:
                flash('Wrong email address or password')

    return render_template('signin.html', form = form)

@app.route('/userHome', methods=['GET','POST'])
def userHome():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        projects = db.session.query(models.Project).filter_by(user_id = _user_id).all()
    

        return render_template('userhome.html', user = user, projects = projects)
    else:
        return redirect('/')

@app.route('/newTask', methods=['GET','POST'])
def newTask():
    _user_id = session.get('user')
    form = TaskForm()
    form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        if form.validate_on_submit():
            _description = form.inputDescription.data
            _priority_id = form.inputPriority.data
            priority = db.session.query(models.Priority).filter_by(priority_id = _priority_id).first()
            
            _task_id = request.form['hiddenTaskId']
            _prj_id = int(session.get('project'))
    

            if (_task_id == "0"):
               
                project = db.session.query(models.Project).filter_by(project_id=_prj_id).first()
                tam = int(project.uncom_task)
                project.uncom_task = tam + 1
                task = models.Task(description = _description, priority = priority, project_id = _prj_id)
                db.session.add(task)

            else:
                task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
                task.description = _description
                task.priority = priority

            db.session.commit()
            return redirect('/listTaskDetail')

        return render_template('newtask.html',form = form, user = user)
    
    return redirect('/')

@app.route('/deleteTask', methods=['GET','POST'])
def deleteTask():
    _user_id = session.get('user')
  
    if _user_id:
        _task_id = request.form['hiddenTaskId']

        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
            db.session.delete(task)
            _prj_id=task.project_id
            project = db.session.query(models.Project).filter_by(project_id=_prj_id).first()
            project.uncom_task -= 1
            db.session.commit()

        return redirect('/userHome')
        
    return redirect('/')

@app.route('/editTask', methods=['GET','POST'])
def editTask():
    _user_id = session.get('user')
    form = TaskForm()
    form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]

  
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _task_id = request.form['hiddenTaskId']

        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
            form.inputDescription.default = task.description
            form.inputPriority.default = task.priority_id
            form.process()
            return render_template('newtask.html', form = form, user = user, task = task)
        
    return redirect('/')


@app.route('/doneTask', methods=['GET','POST'])
def doneTask():
    _user_id = session.get('user')
  
    if _user_id:
        _task_id = request.form['hiddenTaskId']

        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
            task.isCompleted = True

            _prj_id=task.project_id
            project = db.session.query(models.Project).filter_by(project_id=_prj_id).first()
            project.uncom_task -= 1

            db.session.commit()

        return redirect('/userHome')

    return redirect('/')

@app.route('/newProject', methods=['GET','POST'])
def newProject():
    _user_id = session.get('user')
    form = ProjectForm()
    
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        if form.validate_on_submit():
            _prname = form.inputProjectName.data
            _prj_id = request.form['hiddenProjectId']

            if (_prj_id == "0"):
                project = models.Project(pr_name=_prname, user_id= _user_id)
                db.session.add(project)
            else:
                project = db.session.query(models.Project).filter_by(project_id= _prj_id).first()
                project.pr_name = _prname
            
            db.session.commit()
            return redirect('/userHome')

        return render_template('newproject.html',form = form, user = user)
    
    return redirect('/')

@app.route('/listTask', methods=['GET','POST'])
def taskDetail():
    _user_id = session.get('user')
    if _user_id:
        _project_id = request.form['hiddenProjectId']
        session['project'] = _project_id
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        project = db.session.query(models.Project).filter_by(project_id = _project_id).first()
        uncompleted_tasks = db.session.query(models.Task).filter_by(project_id = _project_id, isCompleted = False)
        return render_template('taskdetail.html', tasks = uncompleted_tasks, user = user, project = project)


@app.route('/listTaskDetail', methods=['GET','POST'])
def taskDetailNew():
    _user_id = session.get('user')
    if _user_id:
        _project_id = session.get('project')
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        project = db.session.query(models.Project).filter_by(project_id = _project_id).first()
        uncompleted_tasks = db.session.query(models.Task).filter_by(project_id = _project_id, isCompleted = False)
        return render_template('taskdetail.html', tasks = uncompleted_tasks, user = user, project = project)
   
@app.route('/deleteProject', methods=['GET','POST'])
def deleteProject():
    _user_id = session.get('user')
  
    if _user_id:
        _prj_id = request.form['hiddenProjectId']

        if _prj_id:
            project = db.session.query(models.Project).filter_by(project_id = _prj_id).first()
            db.session.delete(project)
            tasks = db.session.query(models.Task).filter_by(project_id = _prj_id).all()
            for task in tasks:
                db.session.delete(task)
            
            db.session.commit()

        return redirect('/userHome')
        
    return redirect('/')

@app.route('/editProject', methods=['GET','POST'])
def editProject():
    _user_id = session.get('user')
    form = ProjectForm()
   
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _prj_id = request.form['hiddenProjectId']

        if _prj_id:
            project = db.session.query(models.Project).filter_by(project_id = _prj_id).first()
            form.inputProjectName.default = project.pr_name
            form.process()
            return render_template('newproject.html', form = form, user = user, project = project)
        
    return redirect('/')

if __name__ == '__main__':
    app.run()

         