from flask import Flask, render_template, request, redirect,url_for

    
app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def home_page():
    if (request.method == "GET"):
        return render_template("./Home_page.html")

@app.route('/query',methods=["POST","GET"])

def query_result_page():
    user_input = request.form["query"]
    if (user_input == None or user_input == ""):
        message = "Please include a valid search term"
        return redirect(url_for('error_page', message = message))
    return "{input} is what you wrote {length}".format(input = user_input,length = len(user_input))
    
@app.route('/error/<message>',methods = ["POST","GET"])
def error_page(message):
    return_string = "An Unexpected Error has occured. Please try again. \n {message}".format(message = message,end='\n')
    return return_string




    

if __name__ == "__main__":
    app.run(debug=True)