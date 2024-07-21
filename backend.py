from flask import Flask, render_template, request, redirect,url_for
import sqlite3

app = Flask(__name__)
database = "./test.db"
table_name = "test"
table_columns = "ID,NAME,YEAR,LINK"
 


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


@app.route("/write", methods = ["POST","GET"])
def write_to_db():
    if request.method == "POST":
        painting = request.form["painting"]
        artist = request.form["artist"]
        year = request.form["year"]
        link = request.form["link"]
        valid,message = validate_write_data(painting,artist,year,link)
        if not valid: #Check for validity
            return redirect(url_for('error_page', message = message))
        insert_data_into_tables(painting,artist,year,link)
        return redirect("/write")        
    else:
        return render_template("./Write_page.html")
    
@app.route('/error/<message>',methods = ["POST","GET"])
def error_page(message):
    return_string = "An Unexpected Error has occured. Please try again. \n {message}".format(message = message,end='\n')
    return return_string



def validate_write_data(painting, artist, year, link):
    if len(painting) == 0:
        return False,"Must have painting name"
    if len(artist) == 0:
        return False,"Must have artist name"
    try:
        int(year)
    except TypeError:
        return False, "Must have valid year"
    if len(year) == 0:
        return False,"Must have painting year"
    if int(year) < 0:
        return False,"Cannot have negative year"
    return True,""

def get_number_from_tuple(tuple):
    string_version = str(tuple)
    number = ""
    for char in string_version:
        try:
            if char == ",": #make sure to only return a single number
                return int(number)
            int(char)
            number += char
        except ValueError:
            pass
    return int(number)
            

def insert_data_into_tables(painting, artist, year, link):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(f"SELECT MAX(ID) FROM {table_name};")
    max = get_number_from_tuple(c.fetchone()) + 1 #This line gets the max ID and adds 1
    c.execute(
        f""" INSERT INTO {table_name}({table_columns})
        VALUES({max},"{painting}",{year},"{link}");
""")
    conn.commit()
    conn.close()



if __name__ == "__main__":
    app.run(debug=True)
    #insert_data_into_tables("Mona Lisa","Divinchi",1667,"http://www.google.com")
