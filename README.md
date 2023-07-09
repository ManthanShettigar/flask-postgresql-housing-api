


# PostgreSQL-backend Housing Data API using Flask and Psycopg2

Flask-based RESTful API that stores housing data in a PostgreSQL database and provides various queries to retrieve information about the housing data.


## Run Locally

Install dependencies

```bash
  pip install -r requirements.txt
```
### Step 1 : Creating the PostgreSQL Database and User
Log in to an interactive Postgres session 

```bash
sudo -iu postgres psql
```

 create a database 
 

```bash
CREATE DATABASE database;
```

Next, create a database user for our project.

```bash
CREATE USER manthan WITH PASSWORD 'password';
```

Replace `manthan`  and `password` with your choice of username & password

Then give this new user access to administer your new database:
```bash
GRANT ALL PRIVILEGES ON DATABASE database TO manthan;
```
Next, assign the ownership of the database to the user 

```bash
ALTER DATABASE database OWNER TO manthan;

```
Now, quit the interactive session with `\q`.

Set the environment variables, make sure it is the same username and password when creating database user

```bash
export DB_USERNAME='manthan'            
export DB_PASSWORD='password'

```

### Step 2 : Run the API

Run the application

```bash
python app.py
```
The API should now be running locally on `http://localhost:5000`

**API Endpoints**

The following endpoints are available:

- **GET /avg** - Retrieve the average sale price of houses overall.
- **GET /avglocation** - Retrieve the average sale price of houses per location.
- **GET /max** - Retrieve the maximum sale price among all houses.
- **GET /min** - Retrieve the minimum sale price among all houses.

**Example Usage**

To retrieve the average sale price overall, make a GET request to `http://localhost:5000/avg`.

To retrieve the average sale price per location, make a GET request to `http://localhost:5000/avglocation`.

To retrieve the maximum sale price, make a GET request to `http://localhost:5000/max`.

To retrieve the minimum sale price, make a GET request to `http://localhost:5000/min`.

The API will return JSON responses containing the requested information.

**Error Handling** 

- If there are no houses in the database, the API will return a `404` error with an appropriate error message.


## Demo

![](https://s11.gifyu.com/images/SWNvV.gif)


## Acknowledgements

 - [How To Use a PostgreSQL Database in a Flask Application](https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application)
 - [Python PostgreSQL Tutorial Using Psycopg2](https://pynative.com/python-postgresql-tutorial/)

