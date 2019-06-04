from flask import render_template, flash, redirect, url_for, request, session, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewProjectForm, EditProjectForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from app.models import User, Projects, Comments, CompleteProjects, CompleteComments
from werkzeug.urls import url_parse
from sqlalchemy import func, cast, Integer
from app.email import send_password_reset_email
import os
import datetime



basedir = os.path.abspath(os.path.dirname(__file__))
jfile = basedir + "/static/javascript.js"
cfile = basedir + "/static/styles.css"
c2file = basedir + "/static/indexstyles.css"
jfilesize = int(os.path.getmtime(jfile))
cfilesize = int(os.path.getmtime(cfile))
c2filesize = int(os.path.getmtime(c2file))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', jfilesize=jfilesize, cfilesize=c2filesize,)



@app.route('/allprojects')
@login_required
def allprojects():
    dev = "Projects"
    allUsers = User.query.filter(User.username != "admin").all()
    currentRole = User.query.filter_by(
        username=current_user.username).first_or_404()
    projects = []
    p2 = db.session.query(User, Projects).join(Projects).order_by(
        cast(Projects.priority, Integer).asc(), Projects.user_id.asc())
    for project in p2:
        commentMaxQ = db.session.query(func.max(Comments.id)).filter(
            Comments.comment_id == project[1].id).first()
        commentMaxInt = commentMaxQ[0]
        commentMaxCom = Comments.query.filter(
            Comments.comment_id == project[1].id, Comments.id == commentMaxInt).first()
        project[1].comment = commentMaxCom
        projects.append(project)

    return render_template('allprojects.html', title='Home', projects=projects, allUsers=allUsers, currentRole=currentRole, jfilesize=jfilesize, cfilesize=cfilesize, dev=dev)



@app.route('/login', methods=['GET', 'POST'])
def login():
    dev = "Projects"
    if current_user.is_authenticated:
        return redirect('/projects/' + current_user.username)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/projects/' + current_user.username)
    return render_template('login.html', title='Sign In', form=form, jfilesize=jfilesize, cfilesize=cfilesize, dev=dev)


@app.route('/projects/completed')
@login_required
def completed():
    page = request.args.get('page', 1, type=int)
    dev = "Projects"
    allUsers = User.query.filter(User.username != "admin").all()
    currentRole = User.query.filter_by(username=current_user.username).first_or_404()
    projects = db.session.query(User, CompleteProjects).join(CompleteProjects).order_by(
        CompleteProjects.timestamp.desc()).paginate(page, app.config['PROJECTS_PER_PAGE'], False)

    next_url = url_for('completed', page=projects.next_num) \
        if projects.has_next else None
    prev_url = url_for('completed', page=projects.prev_num) \
        if projects.has_prev else None
    return render_template('completed.html', title='Completed Projects', projects=projects.items, allUsers=allUsers, currentRole=currentRole, jfilesize=jfilesize, cfilesize=cfilesize, dev=dev, next_url=next_url, prev_url=prev_url)


@app.route('/projects/completed/<project>', methods=['GET', 'POST'])
@login_required
def completedprojectView(project):
    dev = "Projects"
    form = EditProjectForm()
    allUsers = User.query.filter(User.username != "admin").all()
    currentRole = User.query.filter_by(username=current_user.username).first_or_404()
    proj = CompleteProjects.query.filter_by(id=project).first_or_404()
    comments = CompleteComments(comment_id=proj.id).query.filter_by(comment_id=project).all()

    form.description.data = proj.description
    form.company.data = proj.company
    if proj.priority == "9999":
        proj.priority = ""
    if proj.priority_dept == "9999":
        proj.priority_dept = ""
    form.priority.data = proj.priority
    form.priority_dept.data = proj.priority_dept
    form.requester.data = proj.requester
    form.department.data = proj.department
    form.ticket.data = proj.ticket
    form.hours.data = proj.hours
        
    return render_template('viewprojects.html', title='Completed Project', form=form, comment=comments, project=proj, allUsers=allUsers, currentRole=currentRole, jfilesize=jfilesize, cfilesize=cfilesize, dev=dev)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/projects/<username>', methods=['GET', 'POST'])
@login_required
def developer(username):
    user = User.query.filter_by(username=username).first_or_404()
    allUsers = User.query.filter(User.username != "admin").all()
    currentRole = User.query.filter_by(username=current_user.username).first_or_404()
    projects = []
    p2 = Projects.query.filter_by(user_id=user.id).order_by(cast(Projects.priority, Integer).asc())
    for project in p2:
        commentMaxQ = db.session.query(func.max(Comments.id)).filter(Comments.comment_id==project.id).first()
        commentMaxInt = commentMaxQ[0]
        commentMaxCom = Comments.query.filter(Comments.comment_id==project.id, Comments.id==commentMaxInt).first()
        project.comment = commentMaxCom
        projects.append(project)

    return render_template('devprojects.html', title='Developer Projects', user=user, projects=projects, allUsers=allUsers, currentRole=currentRole, jfilesize=jfilesize, cfilesize=cfilesize, dev=username)

@app.route('/projects/<username>/new', methods=['GET', 'POST'])
@login_required
def projectNew(username):
    form = NewProjectForm()
    allUsers = User.query.filter(User.username != "admin").all()
    currentRole = User.query.filter_by(username=current_user.username).first_or_404()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        if form.priority.data == "":
            form.priority.data = "9999"
        project = Projects(description=form.description.data, company=form.company.data, requester=form.requester.data, status=form.status.data, priority=form.priority.data,
                           priority_dept=form.priority_dept.data, department=form.department.data, ticket=form.ticket.data, hours=form.hours.data, user_id=user.id)
        db.session.add(project)
        db.session.commit()
        flash('Project Added!')
        return redirect(url_for('developer', username=username))
    return render_template('newprojects.html', title='Add Projects', user=user, form=form, allUsers=allUsers, currentRole=currentRole, jfilesize=jfilesize, cfilesize=cfilesize, dev=username)


@app.route('/projects/<username>/<project>', methods=['GET', 'POST'])
@login_required
def projectView(username, project):
    form = EditProjectForm()
    allUsers = User.query.filter(User.username != "admin").all()
    currentRole = User.query.filter_by(username=current_user.username).first_or_404()
    user = User.query.filter_by(username=username).first_or_404()
    proj = Projects.query.filter_by(id=project).first_or_404()
    comments = Comments(comment_id=proj.id).query.filter_by(comment_id=project).all()
    comment = Comments(comment_id=proj.id)
    if form.validate_on_submit():
        proj.description = form.description.data
        proj.company = form.company.data
        if form.priority.data == "":
            form.priority.data = "9999"
        proj.priority = form.priority.data
        proj.priority_dept = form.priority_dept.data
        proj.requester = form.requester.data
        proj.status = form.status.data
        proj.department = form.department.data
        proj.ticket = form.ticket.data
        proj.hours = form.hours.data
        comment.comment = form.comment.data
        if comment.comment != "":
            db.session.add(comment)
        db.session.commit()
        flash('Project Updated!')
        return redirect(url_for('projectView', username=username, comment=comments, project=project))
    elif request.method == 'GET':
        form.description.data = proj.description
        form.company.data = proj.company
        if proj.priority == "9999":
            proj.priority = ""
        if proj.priority_dept == "9999":
            proj.priority_dept = ""
        form.priority.data = proj.priority
        form.priority_dept.data = proj.priority_dept
        form.requester.data = proj.requester
        form.status.data = proj.status
        form.department.data = proj.department
        form.ticket.data = proj.ticket
        form.hours.data = proj.hours
        
    return render_template('editprojects.1.html', title='Edit Project', user=user, form=form, comment=comments, project=proj, allUsers=allUsers, currentRole=currentRole, jfilesize=jfilesize, cfilesize=cfilesize, dev=username)

@app.route('/projects/<username>/devcompleted')
@login_required
def devcompleted(username):
    page = request.args.get('page', 1, type=int)
    allUsers = User.query.filter(User.username != "admin").all()
    currentRole = User.query.filter_by(username=current_user.username).first_or_404()
    projects = db.session.query(User, CompleteProjects).filter_by(username=username).join(CompleteProjects).order_by(
        CompleteProjects.timestamp.desc()).paginate(page, app.config['PROJECTS_PER_PAGE'], False)

    next_url = url_for('devcompleted', page=projects.next_num, username=username) \
        if projects.has_next else None
    prev_url = url_for('devcompleted', page=projects.prev_num, username=username) \
        if projects.has_prev else None
    return render_template('devcompleted.html', title='Completed Projects', projects=projects.items, allUsers=allUsers, currentRole=currentRole, jfilesize=jfilesize, cfilesize=cfilesize, dev=username, next_url=next_url, prev_url=prev_url)


@app.route('/register', methods=['GET', 'POST'])
def register():
    dev = "Projects"
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role="user")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, jfilesize=jfilesize, cfilesize=cfilesize, dev=dev)




@app.route('/projects/<username>/<project>/destroy', methods=['GET', 'POST'])
@login_required
def deleteProject(username, project):
    Comments.query.filter_by(comment_id=project).delete()
    Projects.query.filter_by(id=project).delete()
    db.session.commit()
    flash('Project Deleted!')
    return redirect(url_for('developer', username=username))



@app.route('/projects/<username>/<project>/complete', methods=['GET', 'POST'])
@login_required
def completeProject(username, project):
    proj = Projects.query.filter_by(id=project).first_or_404()
    comments = Comments(comment_id=proj.id).query.filter_by(comment_id=project).all()
    completeProj = CompleteProjects(description=proj.description, company=proj.company, department=proj.department, priority=proj.priority,
                                    priority_dept=proj.priority_dept, requester=proj.requester, ticket=proj.ticket, hours=proj.hours, user_id=proj.user_id)
    db.session.add(completeProj)
    db.session.commit()
    proj2 = db.session.query(func.max(CompleteProjects.id)).first_or_404()
    for c in comments:
        completeCom = CompleteComments(comment=c.comment, comment_id=proj2[0])
        db.session.add(completeCom)
    Comments.query.filter_by(comment_id=project).delete()
    Projects.query.filter_by(id=project).delete()
    db.session.commit()
    flash('Project Completed!')
    return redirect(url_for('developer', username=username))





@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form, jfilesize=jfilesize, cfilesize=cfilesize)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form, title='Reset Password', jfilesize=jfilesize, cfilesize=cfilesize)






@app.route('/projects/<username>/<project>/move', methods=['GET', 'POST'])
@login_required
def moveDev(username, project):
    uid = User.query.filter_by(username=request.form["devUsername"]).first_or_404()
    updateProject = Projects.query.filter_by(id=project).first_or_404()
    # print(updateProject.id)
    setattr(updateProject, 'user_id', uid.id)
    # print(updateProject.user_id)
    db.session.commit()
    return redirect(url_for('developer', username=username))









#*****************
#** Catch ALL
#*****************
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('index'))