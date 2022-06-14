#include <stdio.h>
#include <mysql/mysql.h>

// function connect mysql return connection
MYSQL *connect_mysql() {
  MYSQL *conn = NULL;
  conn = mysql_init(NULL);
  if (conn == NULL) {
    fprintf(stderr, "mysql_init() failed\n");
    return NULL;
  }
  if (mysql_real_connect(conn, "localhost", "root", "31072001", "mydatabase", 0, NULL, 0) == NULL) {
    fprintf(stderr, "mysql_real_connect() failed\n");
    mysql_close(conn);
    return NULL;
  }
  return conn;
}

// create table if not exists motor default
int create_table_motor_default(MYSQL *conn) {
  if (mysql_query(conn, "create table IF NOT EXISTS MotorDefault (\
                    id INT(11) NOT NULL AUTO_INCREMENT,\
                    theta_1 FLOAT(11) NOT NULL,\
                    theta_2 FLOAT(11) NOT NULL,\
                    theta_3 FLOAT(11) NOT NULL,\
                    theta_4 FLOAT(11) NOT NULL,\
                    theta_5 FLOAT(11) NOT NULL,\
                    w_1 FLOAT(11) NOT NULL,\
                    w_2 FLOAT(11) NOT NULL,\
                    w_3 FLOAT(11) NOT NULL,\
                    w_4 FLOAT(11) NOT NULL,\
                    w_5 FLOAT(11) NOT NULL,\
                    vitri_x FLOAT(11) NOT NULL,\
                    vitri_y FLOAT(11) NOT NULL,\
                    vitri_z FLOAT(11) NOT NULL,\
                    phi FLOAT(11) NOT NULL,\
                    gramma FLOAT(11) NOT NULL,\
                    v FLOAT(11) NOT NULL,\
                    position FLOAT(11) NOT NULL,\
                    velocity FLOAT(11) NOT NULL,\
                    description VARCHAR(255) NOT NULL,\
                    PRIMARY KEY (id)\
                    )\
                    ENGINE=InnoDB;")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Connected to database\n");
  return 0;
}

// create table if not exists motor
int create_table_controll(MYSQL *conn) {
  if (mysql_query(conn, "create table IF NOT EXISTS Controll (\
                    id INT(11) NOT NULL AUTO_INCREMENT,\
                    theta_1 FLOAT(11) NOT NULL,\
                    theta_2 FLOAT(11) NOT NULL,\
                    theta_3 FLOAT(11) NOT NULL,\
                    theta_4 FLOAT(11) NOT NULL,\
                    theta_5 FLOAT(11) NOT NULL,\
                    w_1 FLOAT(11) NOT NULL,\
                    w_2 FLOAT(11) NOT NULL,\
                    w_3 FLOAT(11) NOT NULL,\
                    w_4 FLOAT(11) NOT NULL,\
                    w_5 FLOAT(11) NOT NULL,\
                    vitri_x FLOAT(11) NOT NULL,\
                    vitri_y FLOAT(11) NOT NULL,\
                    vitri_z FLOAT(11) NOT NULL,\
                    phi FLOAT(11) NOT NULL,\
                    gramma FLOAT(11) NOT NULL,\
                    v FLOAT(11) NOT NULL,\
                    PRIMARY KEY (id)\
                    )\
                    ENGINE=InnoDB;")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Connected to database\n");
  return 0;
}

// insert data to table motor
int insert_data_motor(MYSQL *conn, float theta_1, float theta_2, float theta_3, float theta_4, float theta_5, float w_1, float w_2, float w_3, float w_4, float w_5, float vitri_x, float vitri_y, float vitri_z, float phi, float gramma, float v, float position, float velocity, char *description) {
  if (mysql_query(conn, "insert into MotorDefault (theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v, position, velocity, description) values ('" + theta_1 + "', '" + theta_2 + "', '" + theta_3 + "', '" + theta_4 + "', '" + theta_5 + "', '" + w_1 + "', '" + w_2 + "', '" + w_3 + "', '" + w_4 + "', '" + w_5 + "', '" + vitri_x + "', '" + vitri_y + "', '" + vitri_z + "', '" + phi + "', '" + gramma + "', '" + v + "', '" + position + "', '" + velocity + "', '" + description + "')")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Insert data to table motor\n");
  return 0;
}

// insert data to table controll
int insert_data_controll(MYSQL *conn, float theta_1, float theta_2, float theta_3, float theta_4, float theta_5, float w_1, float w_2, float w_3, float w_4, float w_5, float vitri_x, float vitri_y, float vitri_z, float phi, float gramma, float v) {
  if (mysql_query(conn, "insert into Controll (theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v) values ('" + theta_1 + "', '" + theta_2 + "', '" + theta_3 + "', '" + theta_4 + "', '" + theta_5 + "', '" + w_1 + "', '" + w_2 + "', '" + w_3 + "', '" + w_4 + "', '" + w_5 + "', '" + vitri_x + "', '" + vitri_y + "', '" + vitri_z + "', '" + phi + "', '" + gramma + "', '" + v + "')")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Insert data to table controll\n");
  return 0;
}

// select data from table motor and return data
int select_data_motor(MYSQL *conn, float *theta_1, float *theta_2, float *theta_3, float *theta_4, float *theta_5, float *w_1, float *w_2, float *w_3, float *w_4, float *w_5, float *vitri_x, float *vitri_y, float *vitri_z, float *phi, float *gramma, float *v, float *position, float *velocity, char *description) {
  MYSQL_RES *res;
  MYSQL_ROW row;
  if (mysql_query(conn, "select * from MotorDefault")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  res = mysql_store_result(conn);
  if (res == NULL) {
    fprintf(stderr, "mysql_store_result() failed\n");
    return -1;
  }
  row = mysql_fetch_row(res);
  if (row == NULL) {
    fprintf(stderr, "mysql_fetch_row() failed\n");
    return -1;
  }
  *theta_1 = atof(row[1]);
    *theta_2 = atof(row[2]);
    *theta_3 = atof(row[3]);
    *theta_4 = atof(row[4]);
    *theta_5 = atof(row[5]);
    *w_1 = atof(row[6]);
    *w_2 = atof(row[7]);
    *w_3 = atof(row[8]);
    *w_4 = atof(row[9]);
    *w_5 = atof(row[10]);
    *vitri_x = atof(row[11]);
    *vitri_y = atof(row[12]);
    *vitri_z = atof(row[13]);
    *phi = atof(row[14]);
    *gramma = atof(row[15]);
    *v = atof(row[16]);
    *position = atof(row[17]);
    *velocity = atof(row[18]);
    strcpy(description, row[19]);
    return 0;
}

// select data from table controll and return data to controll
int select_data_controll(MYSQL *conn, float *theta_1, float *theta_2, float *theta_3, float *theta_4, float *theta_5, float *w_1, float *w_2, float *w_3, float *w_4, float *w_5, float *vitri_x, float *vitri_y, float *vitri_z, float *phi, float *gramma, float *v) {
  MYSQL_RES *res;
  MYSQL_ROW row;
  if (mysql_query(conn, "select * from Controll")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  res = mysql_store_result(conn);
  if (res == NULL) {
    fprintf(stderr, "mysql_store_result() failed\n");
    return -1;
  }
  row = mysql_fetch_row(res);
  if (row == NULL) {
    fprintf(stderr, "mysql_fetch_row() failed\n");
    return -1;
  }
  *theta_1 = atof(row[1]);
    *theta_2 = atof(row[2]);
    *theta_3 = atof(row[3]);
    *theta_4 = atof(row[4]);
    *theta_5 = atof(row[5]);

    *w_1 = atof(row[6]);
    *w_2 = atof(row[7]);
    *w_3 = atof(row[8]);
    *w_4 = atof(row[9]);
    *w_5 = atof(row[10]);
    *vitri_x = atof(row[11]);
    *vitri_y = atof(row[12]);
    *vitri_z = atof(row[13]);
    *phi = atof(row[14]);
    *gramma = atof(row[15]);
    *v = atof(row[16]);
    return 0;
}

// update data to table motor
int update_data_motor(MYSQL *conn, float theta_1, float theta_2, float theta_3, float theta_4, float theta_5, float w_1, float w_2, float w_3, float w_4, float w_5, float vitri_x, float vitri_y, float vitri_z, float phi, float gramma, float v, float position, float velocity, char *description) {
  if (mysql_query(conn, "update MotorDefault set theta_1 = '" + theta_1 + "', theta_2 = '" + theta_2 + "', theta_3 = '" + theta_3 + "', theta_4 = '" + theta_4 + "', theta_5 = '" + theta_5 + "', w_1 = '" + w_1 + "', w_2 = '" + w_2 + "', w_3 = '" + w_3 + "', w_4 = '" + w_4 + "', w_5 = '" + w_5 + "', vitri_x = '" + vitri_x + "', vitri_y = '" + vitri_y + "', vitri_z = '" + vitri_z + "', phi = '" + phi + "', gramma = '" + gramma + "', v = '" + v + "', position = '" + position + "', velocity = '" + velocity + "', description = '" + description + "'")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Update data to table motor\n");
  return 0;
}

// update data to table controll
int update_data_controll(MYSQL *conn, float theta_1, float theta_2, float theta_3, float theta_4, float theta_5, float w_1, float w_2, float w_3, float w_4, float w_5, float vitri_x, float vitri_y, float vitri_z, float phi, float gramma, float v) {
  if (mysql_query(conn, "update Controll set theta_1 = '" + theta_1 + "', theta_2 = '" + theta_2 + "', theta_3 = '" + theta_3 + "', theta_4 = '" + theta_4 + "', theta_5 = '" + theta_5 + "', w_1 = '" + w_1 + "', w_2 = '" + w_2 + "', w_3 = '" + w_3 + "', w_4 = '" + w_4 + "', w_5 = '" + w_5 + "', vitri_x = '" + vitri_x + "', vitri_y = '" + vitri_y + "', vitri_z = '" + vitri_z + "', phi = '" + phi + "', gramma = '" + gramma + "', v = '" + v + "'")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Update data to table controll\n");
  return 0;
}

// test main
int main() {
  connect_mysql();
  
  mysql_close(conn);

    return 0;
}
