import sqlite3, os

def createTable():
    try:
        conn = sqlite3.connect(r'mazes.db')
        cursor = conn.cursor()
        create_table = """CREATE TABLE mazes
        (id int(3),
        name string,
        photo BLOB,
        object BLOB,
        solved_photo BLOB,
        solved_object BLOB,
        time2gen real,
        time2solve real
        )"""
        cursor.execute(create_table)
        conn.commit()
        print('yes')
        cursor.close()

    except sqlite3.Error as error:
        print('fail', error)
    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")
                  
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(empId, name, photo, obj, time2gen):
    if os.path.isfile('mazes.db'):
        pass
    else:
        createTable()
    try:
        conn = sqlite3.connect(r'mazes.db')
        cursor = conn.cursor()
        print("connected")
        sqlite_insert = """ INSERT INTO mazes (id, name, photo, obj, time2gen) VALUES (?, ?, ?, ?, ?) """
        empPhoto = convertToBinaryData(photo)
        os.remove(photo)
        empObj = convertToBinaryData(obj)
        open(obj, "w").close()
        data = (empId, name, empPhoto, empObj, time2gen)
        cursor.execute(sqlite_insert, data)
        conn.commit()
        print('yes')
        cursor.close()
    except sqlite3.Error as error:
        print('fail', error)
    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")

def insertBLOBsolved(photo, obj, ID, time2solve):
    try:
        conn = sqlite3.connect(r'mazes.db')
        cursor = conn.cursor()
        print("connected")
        sqlite_insert = """UPDATE mazes SET solved_obj = ?, solved_photo = ?, time2solve = ? WHERE id = ?;"""
        empPhoto = convertToBinaryData(photo)
        os.remove(photo)
        empObj = convertToBinaryData(obj)
        data = (empPhoto, empObj, time2solve, ID)
        cursor.execute(sqlite_insert, data)
        conn.commit()
        print('yes')
        cursor.close()
    except sqlite3.Error as error:
        print('fail', error)
    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBLOBData(empId):
    try:
        conn = sqlite3.connect(r'mazes.db')
        cursor = conn.cursor()
        print('connected')
        sql_fetch = """SELECT * from mazes where id = ?"""
        cursor.execute(sql_fetch, (empId,))
        record = cursor.fetchall()
        for row in record:
            print('ID = ', row[0], "Name = ", row[1])
            name = row[1]
            photo = row[2]
            obj = row[3]
            sobj = row[4]
            sphoto = row[5]
            print('storing')
            # Writes unsolved maze to temp file
            photoPath = r"images\{}.png".format(name)
            writeTofile(photo, photoPath)
            objPath = r"{}.pickle".format(name)
            writeTofile(obj, objPath)
            # Checks for solved mazes and writes to file if True
            if sobj == None:
                pass
            else:
                sobjPath = r"images\s{}.png".format(name)
                writeTofile(sobj, sobjPath)
                sphotoPath = r"s{}.pickle".format(name)
                writeTofile(sphoto, sphotoPath)
            return(name)
        cursor.close()
    except:
        print('OH DEAR')
    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")

def getTimes(empId):
    try:
        conn = sqlite3.connect(r'mazes.db')
        cursor = conn.cursor()
        print('connected')
        sql_fetch = """SELECT * from mazes where id = ?"""
        cursor.execute(sql_fetch, (empId,))
        record = cursor.fetchall()
        for row in record:
            print('ID = ', row[0], "Name = ", row[1])
            time2gen = row[6]
            time2solve = row[7]
            print(time2gen, time2solve)
            # Checks for solved mazes and writes to file if True
            if time2solve == None:
                return (time2gen, 'N/A')
            else:
                return (time2gen, time2solve)
        cursor.close()
    except:
        print('OH DEAR')
    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")

def deleteSqliteRecord(id):
    try:
        conn = sqlite3.connect(r'mazes.db')
        cursor = conn.cursor()
        print("connected")
        sql_query = """DELETE from mazes where id = ?"""
        cursor.execute(sql_query, (id,))
        conn.commit()
        print("deleted")
        cursor.close()
    except sqlite3.Error as error:
        print("failed", error)
    finally:
        if (conn):
            conn.close()
            print("sqlite connection is closed")

 
