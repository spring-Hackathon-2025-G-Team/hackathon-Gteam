from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sample=  {
            "ko": "password1",
            "xuyokana":"password2"
        }

        if sample[username] == password:
            return redirect("/index")
        else :
          return redirect("/login?error=ユーザー名かパスワードが違います")
    
    elif request.method == "GET":
        error = request.args.get("error")
        return render_template("login.html", error=error)

@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

#if __name__ == '__main__':
 #   print("Starting Flask application...")
  #  app.run(host='0.0.0.0', port=5000, debug=True)