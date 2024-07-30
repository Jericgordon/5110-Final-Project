import sqlite3
import re

class Artwork:
    def __init__(self,database,table_name) -> None:
        self._database = database
        self._table_name = table_name
        self._column_names = self._get_column_names(database)
        self.index = -1
        self.objectid = -1
        self.locationid = -1
        self.title = None
        self.displaydate = -1
        self.beginyear = -1
        self.endyear = -1
        self.medium = None
        self.dimensions = None
        self.attribution = None
        self.classification = None
        self.parentid = -1
        self.imageurl = None
        self.site = None

    def load_from_index(self,index:int):
        conn = sqlite3.connect(self._database)
        c = conn.cursor()
        c.execute(
        f""" SELECT * FROM {self._table_name}
        WHERE "index" = {index};
        """)
        result = c.fetchone()

        #Ensure there was actually a valid result for that index
        if result == None:
            raise IndexError("Index not found in SQL database")
        # object_attributes = self._parse_sql_response(result)
        object_attributes = []
        for item in result:
            object_attributes.append(str(item))
        # print(len(object_attributes),type(object_attributes))
        conn.close()
        self.index = object_attributes[0] 
        self.objectid = object_attributes[1] 
        self.locationid = object_attributes[2] 
        self.title = object_attributes[3]
        self.displaydate = object_attributes[4]
        self.beginyear = object_attributes[5]
        self.endyear = object_attributes[6] 
        self.medium = object_attributes[7] 
        self.dimensions = object_attributes[8] 
        self.attribution = object_attributes[9] 
        self.classification = object_attributes[10]
        self.parentid = object_attributes[11]
        self.imageurl = object_attributes[12]
        self.site = object_attributes[-1] 

    def _get_image_link(self,tuple):
        pattern = r"http.+\.jpg"
        link = re.findall(pattern,str(tuple))
        if len(link) > 0:
            return link[-1]
        else:
            return None
        


    #returns a copy of the column names for the table
    def get_column_names(self) ->list:
        return self._column_names
             
    def load_from_search_result(self,tuple):
        self.load_from_index(int(tuple[0]))


    
    def delete_from_db(self,ID:int):
        conn = sqlite3.connect(self._database)
        c = conn.cursor()
        c.execute(
        f""" DELETE FROM {self._table_name} WHERE index = {ID}""")
        conn.commit()
        conn.close()

    def create_new_entry(self,elements:dict)->None:
        #validate user provided data
        self.index = elements[self._column_names[0]]
        self.objectid = elements[self._column_names[1]]
        self.locationid = elements[self._column_names[2]]
        print("objid",self.objectid)
        self.title = elements[self._column_names[3]]
        self.displaydate = elements[self._column_names[4]]
        self.beginyear = elements[self._column_names[5]]
        self.endyear = elements[self._column_names[6]]
        self.medium = elements[self._column_names[7]]
        self.dimensions = elements[self._column_names[8]]
        self.attribution = elements[self._column_names[9]]
        self.classification = elements[self._column_names[10]]
        self.parentid = elements[self._column_names[11]]
        self.imageurl = elements[self._column_names[12]]
        self.site = elements[self._column_names[13]]

    
    def insert_object_into_db(self):
        conn = sqlite3.connect(self._database)
        c = conn.cursor()
        #check_if_new_or_update
        if int(self.index) == -1:
            c.execute(f"""SELECT MAX("index") FROM {self._table_name};""")
            self.index = int(c.fetchone()[0]) + 1 #Get a uniqueID for the new Entry
            c.execute(
            f""" INSERT INTO {self._table_name}
            VALUES({self.index},
            {self._fill_if_not_null(self.objectid,-1)},
            {self._fill_if_not_null(self.locationid,-1)},
            "{self._fill_if_not_null(self.title,"No Title")}",
            {self._fill_if_not_null(self.displaydate,-1)},
            {self._fill_if_not_null(self.beginyear,-1)},
            {self._fill_if_not_null(self.endyear,-1)},
            "{self._fill_if_not_null(self.medium,"No Medium")}",
            "{self._fill_if_not_null(self.dimensions,"No Dimensions")}",
            "{self._fill_if_not_null(self.attribution,"No Attribution")}",
             "{self._fill_if_not_null(self.classification,"No Classification")}",
             {self._fill_if_not_null(self.parentid,-1)},
             "{self._fill_if_not_null(self.imageurl,"No Image Link")}",
             "{self._fill_if_not_null(self.site,"Not on display")}");""")
            conn.commit()
            conn.close()
        else:
            c.execute(
            f""" UPDATE {self._table_name}
            SET
            "{self._column_names[1]}" = {self._fill_if_not_null(self.objectid,-1)},
            "{self._column_names[2]}" = {self._fill_if_not_null(self.locationid,-1)},
            "{self._column_names[3]}" = "{self._fill_if_not_null(self.title,"No Title")}",
            "{self._column_names[4]}" = {self._fill_if_not_null(self.displaydate,-1)},
            "{self._column_names[5]}" = {self._fill_if_not_null(self.beginyear,-1)},
            "{self._column_names[6]}" = {self._fill_if_not_null(self.endyear,-1)},
            "{self._column_names[7]}" = "{self._fill_if_not_null(self.medium,"No Medium")}",
            "{self._column_names[8]}" = "{self._fill_if_not_null(self.dimensions,"No Dimensions")}",
            "{self._column_names[9]}" = "{self._fill_if_not_null(self.attribution,"No Attribution")}",
            "{self._column_names[10]}" = "{self._fill_if_not_null(self.classification,"No Classification")}",
            "{self._column_names[11]}" = {self._fill_if_not_null(self.parentid,-1)},
            "{self._column_names[12]}" = "{self._fill_if_not_null(self.imageurl,"No Image Link")}",
            "{self._column_names[13]}" = "{self._fill_if_not_null(self.site,"Not on display")}"
            WHERE "index" = {self.index};""")
            conn.commit()
            conn.close()

    #removes the characters ",(,) and ' from a string
    def _remove_SQL_extras(self,string:str) -> str:
        removal_table = {ord("("):None,ord(")"):None,ord(","):None,ord("'"):None}
        return string.translate(removal_table)

    def _fill_if_not_null(self,val1,val2):
        if len(str(val1)) > 0:
            return val1
        return val2

    def _get_column_names(self,database):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        table_column_names = []
        rows = c.execute("SELECT * FROM objects LIMIT 1;")
        for entry in rows.description:
            table_column_names.append(str(entry[0])) 
        conn.close()
        return table_column_names
    
    def delete_from_index(self,index):
        conn = sqlite3.connect(self._database)
        c = conn.cursor()
        c.execute(f"""DELETE FROM {self._table_name} WHERE "index" == {index};""")
        conn.commit()
        conn.close()






# #Testing Code



# database = "Art.db"
# table_name = "objects"


# conn = sqlite3.connect(database)
# c = conn.cursor()
# a = Artwork(database,table_name)

# # print(a._column_names)

# c.close()

# # a = Artwork(database,table_name)
# a.load_from_index(135434)

# a.load_from_index(1)
# mona_lisa_link = "www.google.com"
# new_entry = {
# 'index':141431, 'objectid':-1, 'locationid':-1, 
#  'title':"The Mona Lista", 'displaydate':1776, 'beginyear':1776, 
#  'endyear':1992, 'medium':"Oil and Canvas", 'dimensions':"2/1", 'attribution':"u", 
#  'classification':"t", 'parentid':1, 'imageurl':"www.google.com", 'site':"my palace"
# }
# a.create_new_entry(new_entry)
# print(a.index)
# a.insert_object_into_db()







# a.create_new_entry(new_entry)
# print(a.index)
# print(a._column_names)
# print(a.title)
# a.insert_object_into_db()
# id_test = a.index
# print(id_test)

# b = Artwork(database,table_name)
# b.load_from_index(id_test)
# print(b.title)
