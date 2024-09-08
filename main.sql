PRAGMA foreign_keys = ON;
BEGIN;

CREATE TABLE bookings (
  courses_id int NOT NULL,
  customer_id int NOT NULL UNIQUE,
  spots_num int NOT NULL,
  PRIMARY KEY (customer_id, customer_id),
  FOREIGN KEY(courses_id) REFERENCES courses(course_id),
  FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE courses (
  course_id int NOT NULL UNIQUE,
  course_name varchar(255) NOT NULL,
  session_num int NOT NULL,
  room_num varchar(255) NOT NULL UNIQUE,
  start_date datetime NOT NULL,
  instructor_name varchar(255) NOT NULL,
  price int NOT NULL,
  capacity int NOT NULL,
  already_signed int NOT NULL,
  spot_calculation int NOT NULL,
  PRIMARY KEY (course_id),
);

CREATE TABLE customers (
  customer_id int NOT NULL UNIQUE,
  signed_id int NOT NULL,
  last_name varchar(255) NOT NULL,
  first_name varchar(255) NOT NULL,
  gender varchar(255) NOT NULL,
  email varchar(255) NOT NULL UNIQUE,
  PRIMARY KEY (customer_id)
);

CREATE TABLE instructors (
  ins_id int NOT NULL UNIQUE,
  age int NOT NULL,
  last_name varchar(255) NOT NULL,
  first_name varchar(255) NOT NULL,
  email varchar(255) NOT NULL UNIQUE,
  PRIMARY KEY (ins_id)
);

INSERT INTO bookings VALUES (1, 1, 1);
INSERT INTO bookings VALUES (2, 2, 1);
INSERT INTO bookings VALUES (2, 3, 1);
INSERT INTO bookings VALUES (1, 4, 1);
INSERT INTO bookings VALUES (2, 5, 1);
INSERT INTO bookings VALUES (1, 6, 1);
INSERT INTO bookings VALUES (2, 7, 1);
INSERT INTO bookings VALUES (3, 8, 1);
INSERT INTO bookings VALUES (3, 9, 1);
INSERT INTO bookings VALUES (3, 10, 1);
INSERT INTO bookings VALUES (1, 11, 1);

INSERT INTO courses VALUES ('1', 'Hip Pop', 2, 'A', '20/12/2021', 'Hannah Marin', 30, 10, 6, 4);
INSERT INTO courses VALUES ('2', 'Breaking', 1, 'B', '22/12/2021 ', 'Emily Feilds', 35, 14, 10, 4);
INSERT INTO courses VALUES ('3', 'Classic', 3, 'C', '15/11/2021', 'Spencer Hastings', 45, 3, 0, 3);


INSERT INTO customers VALUES (1, 1, 'Horan', 'Niall', 'Male', 'test1@gmail.com');
INSERT INTO customers VALUES (2, 1, 'Daniel', 'Jack', 'Male', 'test2@gmail.com');
INSERT INTO customers VALUES (3, 1, 'Payne', 'Liam', 'Male', 'test3t@gmail.com');
INSERT INTO customers VALUES (4, 1, 'Wayne', 'Jessica', 'Female', 'test4@gmail.com');
INSERT INTO customers VALUES (5, 1, 'McKate', 'Penny', 'Female', 'test5@gmail.com');
INSERT INTO customers VALUES (6, 1, 'Styles', 'Harry', 'Male', 'test6@gmail.com');
INSERT INTO customers VALUES (7, 1, 'Winters', 'Jen', 'female', 'test7@gmail.com');
INSERT INTO customers VALUES (8, 1, 'Ritz', 'Beth', 'Female', 'test8@gmail.com');
INSERT INTO customers VALUES (9, 1, 'Walls', 'Dane', 'Male', 'test9@gmail.com');
INSERT INTO customers VALUES (10, 1, 'Leraine', 'Ron', 'Female', 'test10@gmail.com');
INSERT INTO customers VALUES (11, 1, 'Malik', 'Zayn', 'Male', 'test11@gmail.com');

INSERT INTO instructors VALUES (1, 23, 'Marin', 'Hannah', '01@gmail.com');
INSERT INTO instructors VALUES (2, 24, 'Hastings', 'Spencer', '02@gmail.com');
INSERT INTO instructors VALUES (3, 25, 'Feilds', 'Emily', '04@gmail.com');

COMMIT;
