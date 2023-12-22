from flask import Flask,request, redirect, url_for
app= Flask(__name__)


user1='admin'
password1='admin'

@app.route('/success/<name>')
def success(name):
   return 'Welcome %s!' %name
   
@app.route('/unsuccess')
def unsuccess():
   return 'Login failed' 
   

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password=request.form['password']
        if (user==user1) and (password==password1):	    	
            return redirect(url_for('success', name=user))
        else:
            return redirect(url_for('unsuccessful'))
  

if __name__=='__main__':
    app.run(debug=True)
             
