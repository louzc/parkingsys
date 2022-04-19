DROP TABLE IF EXISTS cars;

CREATE TABLE cars (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  car_plate TEXT NOT NULL,
  checkin_time TEXT NOT NULL,
  checkout_time Text
);
