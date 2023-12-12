This repo contains code that demonstrates the use of pytest

#### Requirements:
Install required modules:
```
pip install -r requirements.txt
```
If setting up a mysql database, need the following:
```
CREATE TABLE users
(
  user_id int unsigned not null auto_increment,
  first_name varchar(512) NOT NULL,
  last_name varchar(512) NOT NULL,
  email varchar(512) NOT NULL,
  is_subscriber tinyint DEFAULT 0,
  PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```
Update the config/db.config file to connect to the mysql db.

#### To run the main program
```
export DB_CONFIG=$(pwd)/config/db.config
src/main.py
```
Note that this will create a database error if mysql isn't setup for this demo.

#### Ways of running pytests:
###### Run all tests in tests dir
```
pytest tests
```

###### Run one test file
```
pytest tests/test_dbutil.py
```

###### Run one test file showing stdout
```
pytest -s tests/test_dbutil.py
```

###### Run one test function from a file
```
pytest tests/test_dbutil.py::test_good_connection
```

###### Run tests with coverage report
```
pytest --cov src --cov-report term-missing tests
```
Note that pytest-cov needs to be installed first.
