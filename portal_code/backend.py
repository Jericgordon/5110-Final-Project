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
database = "Art.db"
table_name = "objects"
port = 4000
 

@app.route('/',methods=["POST","GET"])
def query_result_page():
    if request.method == "GET":
        return render_template("Lookup_page.html",port=port)

    #create sql connections to database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    #get user input
    query_text = request.form["query"]
    query_type = request.form["Search by:"].upper()

    #get the index of the desired files
    query_result = []
    match(query_type):
        case "INDEX": #load directly from index if possible
            try:
                a = Artwork(database,table_name)
                a.load_from_index(query_text)
                query_result.append(a)

            except IndexError:
                return render_template("Lookup_page.html",message= f"Item with index {query_text} not found ",port = port)
        
        #default case
        case _: #handle all other query types
            c.execute(f"""SELECT "index" FROM {table_name}
                        WHERE {query_type} like "%{query_text}%";""")
            results = c.fetchone()

            counter = 0
            while results is not None and counter < 20:
                query_result.append(Artwork(database,table_name))
                query_result[-1].load_from_search_result(results)
                counter += 1
                results = c.fetchone()

    if len(query_result) == 0:
        return render_template("Lookup_page.html",message= "No results found",port = port)
    return render_template("Lookup_page.html",entries = query_result,port = port)


@app.route("/write", methods = ["POST","GET"])
def write_to_db():
    match (request.method):
        case "POST":
            try:
                art_to_add = Artwork(database,table_name)
                art_to_add.load_from_user(request.form["painting"],request.form["artist"],\
                                        request.form["year"],request.form["link"])
                art_to_add.insert_object_into_db()
                return redirect("/write",port = port)        
            except AttributeError as ae:
                return redirect(url_for('error_page', message = ae),port=port)
        case _:
            return render_template("./Write_page.html",port = port)

@app.route("/edit/<id>", methods = ["POST","GET"])
def edit_page(id:int):
    match(request.method):
        case "GET":
            #if we are creating an item rather than updating one
            print(id)
            if (int(id) == -1): 
                return render_template("Creation_page.html",port = port)
            
            a = Artwork(database,table_name)
            a.load_from_index(id)
            print("debug index",a.index)
            return render_template(f"Edit_page.html",port = port,object = a)

        case "POST":
            elements_dict = {}
            elements_dict['index'] = id
            elements_dict['objectid'] = -1 
            elements_dict['locationid'] = -1 
            elements_dict['title'] = request.form["title"]
            elements_dict['displaydate'] = request.form["display_date"]
            elements_dict['beginyear'] = request.form["begin_year"]
            elements_dict['endyear'] = request.form["end_year"]
            elements_dict['medium'] = request.form["medium"] 
            elements_dict['dimensions'] = request.form["dimensions"] 
            elements_dict['attribution'] = request.form["attribution"]
            elements_dict['classification'] = request.form["classification"]
            elements_dict['parentid'] = -1
            elements_dict['imageurl'] = request.form["image_link"]
            elements_dict['site'] = request.form["site"]
            for key,value in elements_dict.items():
                print(key,value)
            a = Artwork(database,table_name)
            a.create_new_entry(elements_dict)
            a.insert_object_into_db()
            return redirect("/")

        case _:
            return "INVALID METHOD"


    
@app.route("/delete/<id>", methods = ["POST"])
def delete_from_db(id):
    a = Artwork(database,table_name)
    try:
        a.delete_from_index(id)
        return render_template("Lookup_page.html",message = f"Deleted entry {id}",port=port)
    except KeyError:
        return render_template("Lookup_page.html",message = f"Deletion error. Could not find file {id}",port=port)


    
@app.route('/error/<message>',methods = ["POST","GET"])
def error_page(message):
    return_string = "An Unexpected Error has occured. Please try again. \n {message}".format(message = message,end='\n')
    return return_string



if __name__ == "__main__":
    app.run(debug=True,port=port)
