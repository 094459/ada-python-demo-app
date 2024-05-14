# URL Shortener

This is a simple Flask application that allows users to create short URLs for long URLs. The application uses a PostgreSQL database to store the short URLs and their corresponding long URLs.

## Features

- Create a short URL for a long URL
- Redirect to the long URL when visiting the short URL
- View a list of all created short URLs and their details

## Prerequisites

- Python 3.x
- PostgreSQL database

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/url-shortener.git
```

2. Create a virtual environment and activate it:

```
python3 -m venv env
source env/bin/activate
```

3. Install the required packages:

```
pip install flask psycopg2
```

4. Set the following environment variables with your PostgreSQL database credentials:

```
export DB_HOST=your_db_host
export DB_NAME=your_db_name
export DB_USER=your_db_user
export DB_PASSWORD=your_db_password
export SECRET_KEY=your_secret_key
```

5. Run the application:

```
python app.py
```

The application should now be running at `http://localhost:5000`.

## Testing

This application uses pytest for testing. To run the tests, follow these steps:

1. Install pytest if you haven't already:

```
pytest
```
The tests will automatically discover and run all test cases in the `tests` directory.

## Usage

1. Visit `http://localhost:5000/add` to create a new short URL.
2. Enter the long URL you want to shorten and submit the form.
3. The application will generate a short URL for the provided long URL and display a success message.
4. Visit `http://localhost:5000/shortcuts` to view a list of all created short URLs and their details.
5. To visit the long URL, simply append the short URL to the base URL (e.g., `http://localhost:5000/abcd123`).
