"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, session, redirect
from WebPipeline import app, Modules

#score: [Right, Wrong, Exercises completed]
#currentScore = [Right, Wrong]
#currentAssignment

@app.route('/')
@app.route('/home')
@app.errorhandler(404)
def home(e=None):
    
    if 'score' in session:
      score = session['score']
    else:
      session['score'] = [0,0]
      score = [0,0]
    """Renders the home page."""
    return render_template(
        'index.html',
        items=Modules.modules.module,
        year=datetime.now().year,
    )
    


@app.route('/module/<name>')
def module(name):
  isBusy = [False,None]
  if 'currentAssignment' in session:
    isBusy = [True,session['currentAssignment']]
  if Modules.modules.find(name) != False:
    return render_template(
          'module.html',
          level=name,
          items=Modules.modules.find(name).data,
          isBusy=isBusy,
          year=datetime.now().year,
    )
  return redirect("/")

@app.route('/check/<name>/<type>')
def setAssignment(name,type):
  session['currentScore'] = [0,0]
  session['currentAssignment'] = [name,type,0]
  session.modified = True
  return redirect("/assignment")

@app.route('/assignment')
@app.route('/assignment')
@app.route('/assignment/<result>/<word>')
def assignment(result=None,word=None):
  if 'currentAssignment' in session:
    if session['currentAssignment'][2] != -1:
      cur = session['currentAssignment']
      if result != None and word != None:
        setResult = ["Too bad!","You guessed '" + word + "', but it was '" + Modules.modules.find(cur[0]).find(cur[1]).data[cur[2]-1][1] + "'"]
        if result == 'True':
          setResult = ["Good job!","You guessed '" + word + "' correctly!"]
      else:
        setResult = ["Start!","Good luck on the test!"]
      return render_template(
        'assignment.html',
        result=setResult,
        item=Modules.modules.find(cur[0]).find(cur[1]).data[cur[2]],
        titles=Modules.modules.find(cur[0]).find(cur[1]).description,
        year=datetime.now().year
        )
    else:
      return redirect("/results")
  return redirect("/")
#@app.route('/module/')
#def redirectHome():
#  return redirect("/")

@app.route("/grade/<inp>")
def gradeAssignment(inp):
  if 'currentAssignment' in session:
    cur = session['currentAssignment']
    result = False
    if Modules.grader.grade(cur,inp):
      session['currentScore'][0] += 1
      session['score'][0] += 1
      result = True
    else:
      session['currentScore'][1] += 1
      session['score'][1] += 1

    if len(Modules.modules.find(cur[0]).find(cur[1]).data) - 1 >= cur[2] + 1: #If reached end of list
      session['currentAssignment'][2] += 1
    else:
      session['currentAssignment'][2] = -1 #Done with exercise
    session.modified = True
    
    return redirect("/assignment/" + str(result) + "/" + inp)
  return redirect("/")

@app.route('/results')
def results():
  if 'currentScore' not in session:
    session['currentScore'] = [0,0]
  if 'score' not in session:
    session['score'] = [0,0,0]

    
  return render_template(
    'result.html',
    previous=session['currentScore'],
    total=session['score'],
    year=datetime.now().year
  )

@app.route('/clearSessionStorage')
def clear():
  session['score'] = [0,0]
  session.pop("currentAssignment",None)
  session['currentScore'] = [0,0]
  session.modified = True
  return redirect("/results")

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Loughton Languages suite 1.0'
    )


