#include <stdio.h>
#include <mysql/mysql.h>

// funtion connect mysql return connection
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

// test connect mysql
void test_connect_mysql() {
  MYSQL *conn = NULL;
  conn = connect_mysql();
  if (conn == NULL) {
    fprintf(stderr, "connect_mysql() failed\n");
    return;
  }
  printf("Connected to database\n");
  mysql_close(conn);
}

// function create table return 0 if success else return -1
int create_table(MYSQL *conn) {
  if (mysql_query(conn, "create table IF NOT EXISTS mytable (id int, name varchar(20))")) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Table created\n");
  return 0;
}

// function insert data return 0 if success else return -1
int insert_data(MYSQL *conn, int id, char *name) {
  char query[100];
  sprintf(query, "insert into mytable values (%d, '%s')", id, name);
  if (mysql_query(conn, query)) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Data inserted\n");
  return 0;
}

// update data return 0 if success else return -1
int update_data(MYSQL *conn, int id, char *name) {
  char query[100];
  sprintf(query, "update mytable set name = '%s' where id = %d", name, id);
  if (mysql_query(conn, query)) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Data updated\n");
  return 0;
}

// delete data return 0 if success else return -1
int delete_data(MYSQL *conn, int id) {
  char query[100];
  sprintf(query, "delete from mytable where id = %d", id);
  if (mysql_query(conn, query)) {
    fprintf(stderr, "mysql_query() failed\n");
    return -1;
  }
  printf("Data deleted\n");
  return 0;
}

// select data return data if success else return -1
char *select_data(MYSQL *conn, int id) {
  char query[100];
  sprintf(query, "select * from mytable where id = %d", id);
  if (mysql_query(conn, query)) {
    fprintf(stderr, "mysql_query() failed\n");
    return NULL;
  }
  MYSQL_RES *res = mysql_store_result(conn);
  if (res == NULL) {
    fprintf(stderr, "mysql_store_result() failed\n");
    return NULL;
  }
  MYSQL_ROW row = mysql_fetch_row(res);
  if (row == NULL) {
    fprintf(stderr, "mysql_fetch_row() failed\n");
    return NULL;
  }
  return row[1];
}



void main() {
  test_connect_mysql();

  MYSQL *conn = NULL;
  conn = connect_mysql();
  if (conn == NULL) {
    fprintf(stderr, "connect_mysql() failed\n");
    return;
  }

  create_table(conn);
  insert_data(conn, 1, "John");
  update_data(conn, 1, "John Doe");
  char *name = select_data(conn, 1);
  printf("%s\n", name);
  delete_data(conn, 1);

  mysql_close(conn);
}