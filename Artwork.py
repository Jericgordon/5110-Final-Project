import sqlite3

class Artwork:
    def __init__(self,database,table_name,column_names) -> None:
        self._database = database
        self._table_name = table_name
        self._column_names = column_names
        self.id = -1
        self.artwork_name = ""
        self.artist = ""
        self.publication_date = -1
        self.image_link = ""

    def load_from_id(self,ID):
        conn = sqlite3.connect(self._database)
        c = conn.cursor()
        c.execute(
        f""" SELECT * FROM {self._table_name}
        WHERE ID = {ID};
        """)
        self.load_from_SQL(c.fetchone())
        conn.commit()
        conn.close()
    
    def delete_from_db(self,ID:int):
        conn = sqlite3.connect(self._database)
        c = conn.cursor()
        c.execute(
        f""" DELETE FROM {self._table_name} WHERE ID = {ID}""")
        conn.close()

    
    def load_from_user(self,artwork_name,artist,year:int,link)->None:
        #validate user provided data
        if len(artwork_name) == 0:
            raise AttributeError("Must have painting name")
        if len(artist) == 0:
            raise AttributeError("Must have artist name")
        if len(year) == 0:
            raise AttributeError("Must ahve painting year")
        if int(year) < 0:
            raise AttributeError("Cannot have negative year")
        
        self.artwork_name = artwork_name
        self.artist = artist
        self.year = year
        self.link = link

    def insert_object_into_db(self):
        conn = sqlite3.connect(self._database)
        c = conn.cursor()
        #check_if_new_or_update
        if self.id == -1:
            c.execute(f"SELECT MAX(ID) FROM {self._table_name};")
            self.id = self.format_SQL_int(c.fetchone()) + 1 #Get a uniqueID for the new Entry
        c.execute(
        f""" INSERT INTO {self._table_name}({self._table_name})
        VALUES({self.id},"{self.artwork_name}",{self.year},"{self.link}");
        """)
        conn.commit()
        conn.close()
        
    def load_from_SQL(self,sql_result) -> None:
        if sql_result == None:
            raise KeyError("Not found in Database")
        list_of_values = self.format_entry(str(sql_result).split(","))
        self.id = list_of_values[0]
        self.artwork_name = list_of_values[1]
        self.publication_date = list_of_values[2]
        self.image_link = list_of_values[3]

    def get_entries_from_tuple(self,tuple_list):
        return_list = []
        for tuple in tuple_list:
            #This converts the returned list
            return_list.append()
        return return_list
    
    def format_entry(self,entry):
        print(entry)
        entry[0] = self.format_SQL_int(entry[0]) #format ID
        entry[1] = self.format_SQL_string(entry[1])
        entry[2] = self.format_SQL_int(entry[2])
        entry[3] = self.format_SQL_string(entry[3])
        return entry
    
    #SQLite returns number entries like (2,). The goal of this function
    #is to change (2,) -> 2
    def format_SQL_int(self,tuple):
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
    
    #SQLite returns number entries like "'string_here'". The goal of this function
    #is to change "'string_here'" -> "string_here"
    def format_SQL_string(self,string_with_quotation_marks):
        beginning_counter = 0
        end_counter = -1
        for _ in range(len(string_with_quotation_marks)):
            if string_with_quotation_marks[beginning_counter] == "\"" or \
                string_with_quotation_marks[beginning_counter] == "\'":
                beginning_counter += 1
            else:
                break
        for _ in reversed(range(len(string_with_quotation_marks))):
            if string_with_quotation_marks[end_counter] == "\"" or \
            string_with_quotation_marks[end_counter] == "\'":
                end_counter -= 1
            else:
                break
        return  string_with_quotation_marks[beginning_counter + 2:end_counter +1]


# database = "./test.db"
# table_name = "test"
# table_columns = "ID,NAME,YEAR,LINK"

# list = [Artwork() for x in range(5)]

# for artwork  in range(1,len(list) +1):
#     print(artwork)
#     list[artwork].load_from_id(artwork,database,table_name,table_columns)

# for item in list:
#     print(item.name)

