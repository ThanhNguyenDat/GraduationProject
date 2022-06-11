import mysql.connector
from mysql.connector import Error

class ConnectDB:
    def __init__(self):
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()
        print("MySQL connection is closed")

    def get_connection(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='EmbServer',
                                                 user='root',
                                                 password='31072001')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                # print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Your connected to database: ", record)
            return connection
        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_table_controll(self):

        try:
            self.__init__()
            sql = """CREATE TABLE IF NOT EXISTS Controll (
                    id INT(11) NOT NULL AUTO_INCREMENT,
                    theta_1 FLOAT(11) NOT NULL,
                    theta_2 FLOAT(11) NOT NULL,
                    theta_3 FLOAT(11) NOT NULL,
                    theta_4 FLOAT(11) NOT NULL,
                    theta_5 FLOAT(11) NOT NULL,
                    w_1 FLOAT(11) NOT NULL,
                    w_2 FLOAT(11) NOT NULL,
                    w_3 FLOAT(11) NOT NULL,
                    w_4 FLOAT(11) NOT NULL,
                    w_5 FLOAT(11) NOT NULL,
                    vitri_x FLOAT(11) NOT NULL,
                    vitri_y FLOAT(11) NOT NULL,
                    vitri_z FLOAT(11) NOT NULL,
                    phi FLOAT(11) NOT NULL,
                    gramma FLOAT(11) NOT NULL,
                    v FLOAT(11) NOT NULL,
                    PRIMARY KEY (id)
                    )
                    ENGINE=InnoDB;"""
            self.cursor.execute(sql)
            self.connection.commit()
            print("Table created successfully")
            
        except Error as e:
            print("Error while creating table", e)
        finally:
            self.cursor.close()

    def create_table_motor_default(self):
        try:
            self.__init__()
            sql = """CREATE TABLE IF NOT EXISTS MotorDefault (
                    id INT(11) NOT NULL AUTO_INCREMENT,
                    theta_1 FLOAT(11) NOT NULL,
                    theta_2 FLOAT(11) NOT NULL,
                    theta_3 FLOAT(11) NOT NULL,
                    theta_4 FLOAT(11) NOT NULL,
                    theta_5 FLOAT(11) NOT NULL,
                    w_1 FLOAT(11) NOT NULL,
                    w_2 FLOAT(11) NOT NULL,
                    w_3 FLOAT(11) NOT NULL,
                    w_4 FLOAT(11) NOT NULL,
                    w_5 FLOAT(11) NOT NULL,
                    vitri_x FLOAT(11) NOT NULL,
                    vitri_y FLOAT(11) NOT NULL,
                    vitri_z FLOAT(11) NOT NULL,
                    phi FLOAT(11) NOT NULL,
                    gramma FLOAT(11) NOT NULL,
                    v FLOAT(11) NOT NULL,
                    position FLOAT(11) NOT NULL,
                    velocity FLOAT(11) NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    PRIMARY KEY (id)
                    )
                    ENGINE=InnoDB;"""
                    
            self.cursor.execute(sql)
            self.connection.commit()
            print("Table created successfully")
        except Error as e:
            print("Error while creating table", e)
        finally:
            self.cursor.close()

    def insert_data(self, data, table_name: str ="Controll", sql : str = None):
        try:
            self.__init__()
            if data:
                if type(data) != type(list):
                    data = list(data)
                if table_name == "Controll":
                    sql = """INSERT INTO Controll (theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                elif table_name == "MotorDefault":
                    sql = """INSERT INTO MotorDefault (theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v, position, velocity, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                self.cursor.execute(sql, data)
            elif sql:
                self.cursor.execute(sql)
            
            self.connection.commit()
            print("Data inserted successfully")
        except Error as e:
            print("Error while inserting data", e)
        finally:
            self.cursor.close()

    def update_data(self, id, data, name_database='Controll'):
        if type(data) != type(list):
            data = list(data)
        try:
            self.__init__()
            if name_database == "Controll":
                sql = """UPDATE Controll SET theta_1 = %s, theta_2 = %s, theta_3 = %s, theta_4 = %s, theta_5 = %s, w_1 = %s, w_2 = %s, w_3 = %s, w_4 = %s, w_5 = %s, vitri_x = %s, vitri_y = %s, vitri_z = %s, phi = %s, gramma = %s, v = %s WHERE id = """ + str(id)
            elif name_database == "MotorDefault":
                sql = """UPDATE MotorDefault SET theta_1 = %s, theta_2 = %s, theta_3 = %s, theta_4 = %s, theta_5 = %s, w_1 = %s, w_2 = %s, w_3 = %s, w_4 = %s, w_5 = %s, vitri_x = %s, vitri_y = %s, vitri_z = %s, phi = %s, gramma = %s, v = %s, position = %s, velocity = %s, description = %s WHERE id = """ + str(id)
            self.cursor.execute(sql, data)
            self.connection.commit()
            print("Data updated successfully")
        except Error as e:
            print("Error while updating data", e)
        finally:
            self.cursor.close()

    def delete_data_by_id(self, id, name_database='Controll'):
        #  convert id to list
        id = str(id)
        if type(id) != type(list):
            id = list(id)
        try:
            self.__init__()
            if name_database == 'Controll':
                sql = """DELETE FROM Controll WHERE id = %s"""
            elif name_database == 'MotorDefault':
                sql = """DELETE FROM MotorDefault WHERE id = %s"""
            self.cursor.execute(sql, id)
            self.connection.commit()
            print("Data deleted successfully")
        except Error as e:
            print("Error while deleting data", e)
        finally:
            self.cursor.close()
    
    def delete_data_by_feature(self, feature, value):
        data = [feature, value]
        try:
            self.__init__()
            sql = """DELETE FROM Controll WHERE %s = %s"""
            self.cursor.execute(sql, data)
            self.connection.commit()
            print("Data deleted successfully")
        except Error as e:
            print("Error while deleting data", e)
        finally:
            self.cursor.close()

    def select_data(self):
        try:
            self.__init__()
            sql = """SELECT * FROM Controll"""
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print("Error while selecting data", e)
        finally:
            self.cursor.close()

    def select_data_by_id(self, id):
        try:
            self.__init__()
            sql = """SELECT * FROM Controll WHERE id = %s"""
            self.cursor.execute(sql, id)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print("Error while selecting data", e)
        finally:
            self.cursor.close()

    def select_data_by_mode(self, mode):
        try:
            self.__init__()
            sql = """SELECT * FROM Controll WHERE mode = %s"""
            self.cursor.execute(sql, mode)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print("Error while selecting data", e)
        finally:
            self.cursor.close()

    def show_data(self, table_name="Controll"):
        try:
            # check if table exists
            self.__init__()
            sql = """SELECT * FROM %s""" % table_name
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print("Error while showing data", e)
        finally:
            self.cursor.close()

# ConnectDB = ConnectDB()
# ConnectDB.create_table_controll()
# ConnectDB.create_table_motor_default()
# result = ConnectDB.show_data()
# print(result)
# # insert data into table Controll
# data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "mode2", 1, 2, 3, "position2", 'velocity2']
# data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, "mode1", 1, 2, 3, "position1", 'velocity1']
# ConnectDB.insert_data(data, table_name="MotorDefault")
# data = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, "mode3", 1, 2, 3, "position3", 'velocity3']
# ConnectDB.insert_data(data, table_name="MotorDefault")
