from flask import Flask, render_template, request, redirect,url_for
import sqlite3
from Artwork import Artwork 
# importing module
import logging
 
# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

#global variables
app = Flask(__name__)
database = "./test.db"
table_name = "test"
table_columns = "ID,NAME,YEAR,LINK"
port = 5000
 

@app.route('/',methods=["GET"]) 
def home_page():
    return render_template("./Home_page.html",port = port)

@app.route('/query',methods=["POST","GET"])
def query_result_page():
    if request.method == "GET":
        return render_template("Lookup_page.html",port=port)

    query_text = request.form["query"]
    query_type = request.form["Search by:"].upper()

    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(f"""SELECT * FROM {table_name}
                WHERE {query_type} like "%{query_text}%";""")
    results = c.fetchone()
    query_result = []
    counter = 0
    while results is not None:
        query_result.append(Artwork(database,table_name,table_columns))
        query_result[-1].load_from_SQL(results)
        counter += 1
        results = c.fetchone()

    #Handle Case of no results
    if len(query_result) == 0:
        error_art = Artwork(database,table_name,table_columns)
        error_art.artwork_name = "None found"
        query_result.append(error_art)
    
    return render_template("Lookup_page.html",entries = query_result,port = port)


@app.route("/write", methods = ["POST","GET"])
def write_to_db():
    if request.method == "POST":
        try:
            art_to_add = Artwork(database,table_name,table_columns)
            art_to_add.load_from_user(request.form["painting"],request.form["artist"],\
                                      request.form["year"],request.form["link"])
            art_to_add.insert_object_into_db()
            return redirect("/write",port = port)        
        except AttributeError as ae:
            return redirect(url_for('error_page', message = ae),port=port)
    else:
        return render_template("./Write_page.html",port = port)
    
@app.route("/delete/<id>", methods = ["POST"])
def delete_from_db(id):
    a = Artwork(database,table_name,table_columns)
    try:
        a.delete_from_db(id)
        return render_template("Lookup_page.html",message = f"Deleted entry {id}",port=port)
    except KeyError:
        return render_template("Lookup_page.html",message = f"Deletion error. Could not find file {id}",port=port)


    
@app.route('/error/<message>',methods = ["POST","GET"])
def error_page(message):
    return_string = "An Unexpected Error has occured. Please try again. \n {message}".format(message = message,end='\n')
    return return_string



if __name__ == "__main__":
    app.run(debug=True,port=port)
