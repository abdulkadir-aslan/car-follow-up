# Vehicle Tracking Management

Reporting of the daily, weekly, and monthly fuel loading indices of the vehicles loaded into the system.

## Features

- User login and logout
- User authorization
- Filtering

## Installation

1. **Clone the repository**

    ```sh
    git clone https://github.com/abdulkadir-aslan/car-follow-up
    cd car-follow-up
    ```

2. **Create a virtual environment and activate it**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser to access the admin panel**

    ```sh
    python manage.py createsuperuser
    ```
    Note: After the user is created, it is necessary to log into the admin panel and set the user status to **'Active'**.

6. **Start the development server**

    ```sh
    python manage.py runserver
    ```

7. **Access the application**

    Open your browser and navigate to `http://127.0.0.1:8000/` to access the application. You can access the admin panel at `http://127.0.0.1:8000/admin/`.

## Project Structure

- `core/`: Main project directory.
  - `settings`: Main project settings.
    - `base.py`: Basic configuration
    - `development.py`: Development configuration
    - `production.py`: publish configuration
  - `urls.py`: URL routing.
  - `wsgi.py`: WSGI configuration.
- `account/`: User actions directory.
  - `admin.py`: Admin configuration.
  - `models.py`: Database models.
  - `urls.py`: URL routing for the application.
  - `views.py`: View functions.
  - `forms.py`: Form functions.
- `page/`: Home operations directory.
    - `admin.py`: Admin configuration.
    - `models.py`: Database models.
    - `views.py`: View functions.
    - `decorators.py/`: Decorators function.
    - `urls.py`: URL routing for the 
- `report/`: Report operations directory.
    - `admin.py`: Admin configuration.
    - `models.py`: Database models.
    - `views.py`: View functions.
    - `filters.py/`: Filter function.
    - `urls.py`: URL routing for the 



## Static and Media Files

- `STATIC_URL`: URL for static files.
- `MEDIA_URL`: URL for media files.
- `MEDIA_ROOT`: Root directory for media files.

## Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/en/3.2/)
