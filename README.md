- Download all the requirements from requirements.txt
- Make a MySQL DB with name "db1" and a wallet table
	```
	CREATE TABLE IF NOT EXISTS wallet (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL,
	amount INT DEFAULT 0
	);
	```
- Run flask application app.py
