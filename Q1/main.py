import pandas 
import random

DataFrames = {} # To store the dataframes(Tables)
last_is_error = False # To check if the last operation was successful or not

def AddTable():
    """
    Add a table to the database
    """
    global last_is_error
    table_name = input("\nEnter the name of the table: ")
    try:
        num_columns = int(input("\nEnter the number of columns: "))
    except:
        print("\n\033[1;31mError:\033[0m Invalid number of columns")
        last_is_error = True
        return
    columns = {}
    for i in range(num_columns):
        column_name = input("\nEnter the name of the column " + str(i+1) + " : ")
        column_type = input("\nEnter the type of the column " + str(i+1) + " (int, real, str, bool): ")
        
        if column_type == "int":
            columns[column_name] = pandas.Series([], dtype = "int")
        elif column_type == "real":
            columns[column_name] = pandas.Series([], dtype = "float")
        elif column_type == "str":
            columns[column_name] = pandas.Series([], dtype = "str")
        elif column_type == "bool":
            columns[column_name] = pandas.Series([], dtype = "bool")
        else:
            print("\n\033[1;31mError:\033[0m Invalid column type")
            last_is_error = True
            return
    DataFrames[table_name] = pandas.DataFrame(columns)
    print("\nTable added to the database.")
    last_is_error = False

def LoadFile():
    global last_is_error
    file_name = input("\nEnter the name of the file: ")
    if not file_name.endswith(".csv"):
        file_name += ".csv"
    table_name = file_name.split(".")[0]
    try:
        DataFrames[table_name] = pandas.read_csv(file_name)
        print("\nData loaded from " + file_name)
        last_is_error = False
    except FileNotFoundError:
        last_is_error = True
        print("\n\033[1;31mError:\033[0m File not found")

def ShowSchema():
    global last_is_error
    table_name = input("\nEnter the name of the table: ")
    try:
        print(DataFrames[table_name].info())
        last_is_error = False
    except:
        last_is_error = True
        print("\n\033[1;31mError:\033[0m Table not found")

def ShowData():
    global last_is_error
    table_name = input("\nEnter the name of the table: ")
    try:
        print(DataFrames[table_name].to_string(index = False))
        last_is_error = False
    except:
        last_is_error = True
        print("\n\033[1;31mError:\033[0m Table not found")

def transform_value(value: str):
    if value.isdigit():
        return int(value)
    return value

def SelectRows():
    """
    Select rows from a table based on a condition
    """
    table_name = input("\nEnter the name of the table: ")
    value_or_column1 = input("\nEnter the value or column name: ")
    value_or_column1 = transform_value(value_or_column1)
    operator = input("\nEnter the operator(=, !=, >, <, >=, <=): ")
    value_or_column2 = input("\nEnter the value or column name: ")
    value_or_column2 = transform_value(value_or_column2)
    global last_is_error
    if isinstance(value_or_column1, str):
        if(len(value_or_column1) > 0 and value_or_column1[0] == "'" and value_or_column1[-1] == "'") or (value_or_column1[0] == '"' and value_or_column1[-1] == '"'):
            value_or_column1 = value_or_column1[1:-1]
        else:
            try:
                value_or_column1 = DataFrames[table_name][value_or_column1]
            except:
                print("\n\033[1;31mError:\033[0m Column not found")
                last_is_error = True
                return
        

    if isinstance(value_or_column2, str):
        if(len(value_or_column2) > 0 and value_or_column2[0] == "'" and value_or_column2[-1] == "'") or (value_or_column2[0] == '"' and value_or_column2[-1] == '"'):
            value_or_column2 = value_or_column2[1:-1]
        else:
            try:
                value_or_column2 = DataFrames[table_name][value_or_column2]
            except:
                print("\n\033[1;31mError:\033[0m Column not found")
                last_is_error = True
                return
    result = None
    try:
        if operator == "=":
            result = DataFrames[table_name][value_or_column1 == value_or_column2]
        elif operator == "!=":
            result = DataFrames[table_name][value_or_column1 != value_or_column2]
        elif operator == ">":
            result = DataFrames[table_name][value_or_column1 > value_or_column2]
        elif operator == "<":
            result = DataFrames[table_name][value_or_column1 < value_or_column2]
        elif operator == ">=":
            result = DataFrames[table_name][value_or_column1 >= value_or_column2]
        elif operator == "<=":
            result = DataFrames[table_name][value_or_column1 <= value_or_column2]
        else:
            print("\n\033[1;31mError:\033[0m Invalid operator")
            last_is_error = True
            return
        save = input("\nDo you want to save the result? (y/n): ")
        print(result.to_string(index = False))
        if save.lower() == "y":
            new_table = input("\nEnter the name of the new table: ")
            DataFrames[new_table] = result
            print("\nResult stored in " + new_table)

        last_is_error = False
    except:
        print("\n\033[1;31mError:\033[0m Table not found")
        last_is_error = True



def ProjectColumn():
    global last_is_error
    table_name = input("\nEnter the name of the \033[1;32mtable\033[0m: ")
    column_name = input("\nEnter the name of the \033[1;32mcolumn\033[0m: ")
    save = input("\nDo you want to save the result? (y/n): ")
    result = None
    try:
        result = DataFrames[table_name][column_name]
        print(result.to_string(index = False))
        if save.lower() == "y":
            new_table = input("\nEnter the name of the new table: ")
            DataFrames[new_table] = result
            print("\nResult stored in " + new_table)

        last_is_error = False
    except:
        print("\n\033[1;31mError:\033[0m Table or column not found")
        last_is_error = True

def RenameTable():
    global last_is_error
    table_name = input("\nEnter the name of the table: ")
    new_name = input("\nEnter the \033[1;32mnew\033[0m name of the table: ")
    try:
        DataFrames[new_name] = DataFrames.pop(table_name)
        print("Table renamed to " + new_name)
        last_is_error = False
    except:
        last_is_error = True
        print("\n\033[1;31mError:\033[0m Table not found")

def SaveTable():
    global last_is_error
    table_name = input("\nEnter the name of the \033[1;32mtable\033[0m: ")
    if table_name.endswith(".csv"):
        table_name = table_name[:-4]
    file_name = table_name + ".csv"

    try:
        DataFrames[table_name].to_csv(file_name, index = False)
        print("\nData saved to " + file_name)
        last_is_error = False
    except:
        last_is_error = True
        print("\n\033[1;31mError:\033[0m Table not found")

def InsertRow():
    global last_is_error
    table_name = input("\nEnter the name of the table: ")
    row = []
    try:
        for column in DataFrames[table_name].columns:
            printDtype = DataFrames[table_name][column].dtype
            if printDtype == "object":
                printDtype = "str"
            value = input(f"\nEnter the value for {column} ({printDtype}): ")
            # check the type of the column
            if DataFrames[table_name][column].dtype == "int":
                value = int(value)
            elif DataFrames[table_name][column].dtype == "float":
                value = float(value)
            elif DataFrames[table_name][column].dtype == "bool":
                value = bool(value)
            row.append(value)


        DataFrames[table_name].loc[len(DataFrames[table_name])] = row
        
        last_is_error = False
    except KeyError:
        last_is_error = True
        print("\033[1;31mError:\033[0m Table not found")
    except ValueError:
        last_is_error = True
        print("\033[1;31mError:\033[0m Invalid value")

def DeleteRow():
    global last_is_error
    table_name = input("\nEnter the name of the table: ")
    row = {}
    try:
        for column in DataFrames[table_name].columns:
            value = input("\nEnter the value for " + column + ": ")
            row[column] = value
        DataFrames[table_name] = DataFrames[table_name].replace(row, pandas.NA)
        DataFrames[table_name] = DataFrames[table_name].dropna()
        print("\nRow deleted from " + table_name)
        last_is_error = False
    except:
        last_is_error = True
        print("\033[1;31mError:\033[0m Table not found")


def UpdateRow():
    global last_is_error
    table_name = input("\nEnter the name of the table: ")
    row = {}
    for column in DataFrames[table_name].columns:
        value = input(f"\nEnter the value for {column} ({DataFrames[table_name][column].dtype}): ")
        try:
            if DataFrames[table_name][column].dtype == "int":
                value = int(value)
            elif DataFrames[table_name][column].dtype == "float":
                value = float(value)
            elif DataFrames[table_name][column].dtype == "bool":
                value = bool(value)
        except:
            last_is_error = True
            print("\n\033[1;31mError:\033[0m Invalid value")
            return
        row[column] = value
    new_row = {}
    for column in DataFrames[table_name].columns:
        value = input(f"\nEnter the new value for {column} ({DataFrames[table_name][column].dtype}): ")
        try:
            if DataFrames[table_name][column].dtype == "int":
                value = int(value)
            elif DataFrames[table_name][column].dtype == "float":
                value = float(value)
            elif DataFrames[table_name][column].dtype == "bool":
                value = bool(value)
        except:
            last_is_error = True
            print("\n\033[1;31mError:\033[0m Invalid value")
            return
        new_row[column] = value
    DataFrames[table_name] = DataFrames[table_name].replace(row, new_row)
    print("\nRow updated in " + table_name)
    
    last_is_error = False

    

def ProductTables():
    global last_is_error
    table1 = input("\nEnter the name of the first table: ")
    table2 = input("\nEnter the name of the second table: ")
    result = None
    try:
        result = pandas.merge(DataFrames[table1], DataFrames[table2], how = "cross")
        save = input("\nDo you want to save the result? (y/n): ")
        print(result.to_string(index = False))
        if save.lower() == "y":
            new_table = input("\nEnter the name of the new table: ")
            DataFrames[new_table] = result
            print("\nResult stored in " + new_table)

        last_is_error = False
    except:
        
        last_is_error = True
        print("\033[1;31mError:\033[0m Table not found")

def UnionTables():
    global last_is_error
    table1 = input("\nEnter the name of the first table: ")
    table2 = input("\nEnter the name of the second table: ")
    result = None
    try:
        result = pandas.concat([DataFrames[table1], DataFrames[table2]]).drop_duplicates()
        save = input("\nDo you want to save the result? (y/n): ")
        print(result.to_string(index = False))
        if save.lower() == "y":
            new_table = input("\nEnter the name of the new table: ")
            DataFrames[new_table] = result
            print("\nResult stored in " + new_table)
        last_is_error = False
    except:
        last_is_error = True
        print("\033[1;31mError:\033[0m Table not found")

def DiffTables():
    global last_is_error
    table1 = input("\nEnter the name of the first table: ")
    table2 = input("\nEnter the name of the second table: ")
    result = None
    try:
        result = DataFrames[table1][~DataFrames[table1].apply(tuple, 1).isin(DataFrames[table2].apply(tuple, 1))]
        save = input("\nDo you want to save the result? (y/n): ")
        print(result.to_string(index = False))
        if save.lower() == "y":
            new_table = input("\nEnter the name of the new table: ")
            DataFrames[new_table] = result
            print("\nResult stored in " + new_table)

        last_is_error = False
    except:
        last_is_error = True
        print("\033[1;31mError:\033[0m Table not found")

def JoinTables(): # Natural Join
    global last_is_error
    table1 = input("\nEnter the name of the first table: ")
    table2 = input("\nEnter the name of the second table: ")
    result = None
    try:
        result = pandas.merge(DataFrames[table1], DataFrames[table2], how = "inner")
        save = input("\nDo you want to save the result? (y/n): ")
        print(result.to_string(index = False))
        if save.lower() == "y":
            new_table = input("\nEnter the name of the new table: ")
            DataFrames[new_table] = result
            print("\nResult stored in " + new_table)
        last_is_error = False
    except:
        last_is_error = True
        print("\033[1;31mError:\033[0m Table not found")

def ListTables():
    print("\nTables in the database:")
    for table in DataFrames:
        print(table, end = ", " if table != list(DataFrames.keys())[-1] else "\n")
    global last_is_error
    last_is_error = False

def IntersectTables():
    global last_is_error
    table1 = input("\nEnter the name of the first table: ")
    table2 = input("\nEnter the name of the second table: ")
    result = None
    try:
        
        result = pandas.concat([DataFrames[table1], DataFrames[table2]]).drop_duplicates(keep = False)
        result = DataFrames[table1][~DataFrames[table1].apply(tuple, 1).isin(result.apply(tuple, 1))]
        save = input("\nDo you want to save the result? (y/n): ")
        print(result.to_string(index = False))
        if save.lower() == "y":
            new_table = input("\nEnter the name of the new table: ")
            DataFrames[new_table] = result
            print("\nResult stored in " + new_table)
        last_is_error = False
    except KeyError:
        last_is_error = True
        print("\033[1;31mError:\033[0m Table not found")



def DivideTables():
    global last_is_error
    table1 = input("\nEnter the name of the first table: ")
    table2 = input("\nEnter the name of the second table: ")
    result = None
    try:
        
        # Find the columns of table1 that are not in table2 (project)
        columns1 = []
        for column in DataFrames[table1].columns:
            if column not in DataFrames[table2].columns:
                columns1.append(column)
        table1_prime = DataFrames[table1][columns1]

        # 2. Drop duplicates from table1_prime
        table1_prime = table1_prime.drop_duplicates()

        # 3. Perform Cartesian Product of table1_prime and table2
        cproduct = pandas.merge(table1_prime, DataFrames[table2], how = "cross")
        # print("\n", cproduct.to_string(index = False))
        
        # 4. Perform cproduct - table1
        diff = cproduct[~cproduct.apply(tuple, 1).isin(DataFrames[table1].apply(tuple, 1))]
        # print("\n", diff.to_string(index = False))

        # 5. Project the columns of table1 from diff
        diff = diff[columns1].drop_duplicates()
        # print("\n", diff.to_string(index = False))

        # 6. result = table1_prime - diff
        result = table1_prime[~table1_prime.apply(tuple, 1).isin(diff.apply(tuple, 1))]
        # print("\n", result.to_string(index = False))

        

        save = input("\nDo you want to save the result? (y/n): ")
        print(result.to_string(index = False))
        if save.lower() == "y":
            new_table = input("\nEnter the name of the new table: ")
            DataFrames[new_table] = result
            print("\nResult stored in " + new_table)
        last_is_error = False
    except KeyError:
        last_is_error = True
        print("\033[1;31mError:\033[0m Table not found")


def WriteMenu():
    colors = ["\033[31m", # Red
              "\033[32m",  # Green
              "\033[33m",  # Yellow
              "\033[34m", # Blue
              "\033[35m", # Purple
              "\033[36m", # Cyan
              "\033[37m", # White
              "\033[1;31m", # Bold Red
              "\033[1;32m", # Bold Green
              "\033[1;33m", # Bold Yellow
              "\033[1;34m", # Bold Blue
              "\033[1;35m", # Bold Purple
              "\033[1;36m", # Bold Cyan
              "\033[1;37m" # Bold White
            ]
    menu = [
            "help - Show This Menu",
            "add - Add Table", 
            "load - Load File", 
            "schema - Show Schema",
            "show - Show All Data", 
            "select - Select Rows", 
            "project - Project Column", 
            "rename - Rename Table", 
            "save - Save Table", 
            "product - Perform Cartesian Product of two Tables", 
            "union - Perform Union of two Tables", 
            "diff - Perform Difference of two Tables", 
            "join - Perform Natural Join of two Tables",
            "intersect - Perform Intersection of two Tables",
            "insert - Insert Row into Table",
            "delete - Delete Row from Table",
            "update - Update Row in Table",
            "divide - Perform Division of two Tables",
            "list - List Tables",
            "quit - Quit"]

    random.shuffle(colors)
    color = random.randint(0, len(colors) - 1)
    print("\n")
    print("-"*30 + " Database Operations " + "-" * 30)
    for value in range(len(menu)):
        print(colors[color] + str(value+1) + ". " + menu[value] + "\033[0m")
        color = (color + 1) % len(colors)
    print("-" * 80)
    global last_is_error
    last_is_error = False

def main():
    global last_is_error
    last_is_error = False
    WriteMenu()
    while True:
        choice = input(("\033[1;31m" if last_is_error else "\033[1;32m") + "→\033[0m ")
        if choice == "1" or choice.startswith("help"):
            WriteMenu()
            continue
        elif choice == "2" or choice.startswith("add"):
            AddTable()
        elif choice == "3" or choice.startswith("load"):
            LoadFile()
        elif choice == "4" or choice.startswith("schema"):
            ShowSchema()
        elif choice == "5" or choice.startswith("show"):
            ShowData()
        elif choice == "6" or choice.startswith("select"):
            SelectRows()
        elif choice == "7" or choice.startswith("project"):
            ProjectColumn()
        elif choice == "8" or choice.startswith("rename"):
            RenameTable()
        elif choice == "9" or choice.startswith("save"):
            SaveTable()
        elif choice == "10" or choice.startswith("product"):
            ProductTables()
        elif choice == "11" or choice.startswith("union"):
            UnionTables()
        elif choice == "12" or choice.startswith("diff"):
            DiffTables()
        elif choice == "13" or choice.startswith("join"):
            JoinTables()
        elif choice == "14" or choice.startswith("intersect"):
            IntersectTables()
        elif choice == "15" or choice.startswith("insert"):
            InsertRow()
        elif choice == "16" or choice.startswith("delete"):
            DeleteRow()
        elif choice == "17" or choice.startswith("update"):
            UpdateRow()
        elif choice == "18" or choice.startswith("divide"):
            DivideTables()
        elif choice == "19" or choice.startswith("list"):
            ListTables()
        elif choice == "20" or choice.startswith("quit"):
            break
        else:
            print("\n\033[1;31mError:\033[0m Invalid choice")
            last_is_error = True
            continue
        


main()


    