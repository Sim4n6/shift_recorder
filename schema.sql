DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS shifts;

CREATE TABLE IF NOT EXISTS users (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL
    );

INSERT INTO users ( username, name, password ) VALUES ( "sim4n6", "simo", "D21ED213E3D12ED31DE");

CREATE TABLE IF NOT EXISTS shifts (
    shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_date_time DATETIME NOT NULL,
    shifter_id INTEGER, FOREIGN KEY (shifter_id) REFERENCES users(employee_id)
    );

INSERT INTO shifts ( shift_date_time ) VALUES ( '2001-10-03 15:20:02.102' );
INSERT INTO shifts ( shift_date_time ) VALUES ( '2001-10-03 16:30:02.102' );