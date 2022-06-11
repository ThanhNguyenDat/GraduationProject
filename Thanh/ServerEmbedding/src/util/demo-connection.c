#include <stdio.h>
#include <mysql/mysql.h>

void main() {
  MYSQL *conn = NULL;
  conn = mysql_init(NULL);
  if (conn == NULL) {
    fprintf(stderr, "mysql_init() failed\n");
    return;
  }
  if (mysql_real_connect(conn, "localhost", "root", "31072001", "mydatabase", 0, NULL, 0) == NULL) {
    fprintf(stderr, "mysql_real_connect() failed\n");
    mysql_close(conn);
    return;
  }
  printf("Connected to database\n");
  mysql_close(conn);
}