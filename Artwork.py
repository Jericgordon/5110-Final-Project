import sqlite3

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
        object_attributes = self._parse_sql_response(c.fetchone())
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
        self.site = object_attributes[13] 

    #returns a copy of the column names for the table
    def get_column_names(self) ->list:
        return self._column_names
    
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
        if self.id == -1:
            c.execute(f"SELECT MAX(ID) FROM {self._table_name};")
            self.id = self.format_SQL_int(c.fetchone()) + 1 #Get a uniqueID for the new Entry
            c.execute(
            f""" INSERT INTO {self._table_name}
            VALUES({self._column_names[0]}
            {self._column_names[1]},
            {self._column_names[2]},
            {self._column_names[3]},
            {self._column_names[4]},
            {self._column_names[5]},
            {self._column_names[6]},
            {self._column_names[7]},
            {self._column_names[8]},
            {self._column_names[9]},
            {self._column_names[10]},
            {self._column_names[11]},
            {self._column_names[12]},
            {self._column_names[13]}");""")
            conn.commit()
            conn.close()
        else:
            c.execute(
            f""" UPDATE {self._table_name}
            SET(
            "{self._column_names[1]}" = {self.objectid},
            "{self._column_names[2]}" = {self.locationid},
            "{self._column_names[3]}" = {self.title},
            "{self._column_names[4]}" = {self.displaydate},
            "{self._column_names[5]}" = {self.beginyear},
            "{self._column_names[6]}" = {self.endyear},
            "{self._column_names[7]}" = {self.medium},
            "{self._column_names[8]}" = "{self.dimensions}",
            "{self._column_names[9]}" = "{self.attribution}",
            "{self._column_names[10]}" = "{self.classification}",
            "{self._column_names[11]}" = {self.parentid},
            "{self._column_names[12]}" = "{self.imageurl}",
            "{self._column_names[13]}" = "{self.site}" ");""" )
            conn.commit()
            conn.close()

        
        #Takes a response from an SQL query, and strips the results of any of the markings
    def _parse_sql_response(self,sql_result) -> list:
        return [self._remove_SQL_extras(entry) for entry in str(sql_result).split(",")]

    #removes the characters ",(,) and ' from a string
    def _remove_SQL_extras(self,string:str) -> str:
        removal_table = {ord("("):None,ord(")"):None,ord(","):None,ord("'"):None}
        return string.translate(removal_table)

    def _get_column_names(self,database):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        table_column_names = []
        rows = c.execute("SELECT * FROM OBJECTS LIMIT 1;")#.format(table=table))
        #print((rows.description))
        column_names_unprocessed = str(rows.description).split()
        #print(column_names_unprocessed)
        for entry in column_names_unprocessed:
            processed_entry = self._remove_SQL_extras(entry)
            if (processed_entry == "None"):
                continue
            else:
                table_column_names.append(processed_entry)
        return table_column_names              

    def _get_sql_values(self) -> str:
        returnstr = ""
        for name in self._column_names:
            returnstr += "\""
            returnstr += name
            returnstr += "\""
            returnstr += ","
        return returnstr[0:-1]


database = "./Art.db"
table_name = "objects"


#,"locations","images"]
# conn = sqlite3.connect(database)
# c = conn.cursor()
# c.execute("select * from images limit 10;")

a = Artwork(database,table_name)
a.load_from_index(1)
