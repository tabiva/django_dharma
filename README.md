# Django Dharma

Django Dharma is a Django library designed to facilitate running checks on models. It provides a structured way to perform and manage checks on your Django models.

## Project Structure

The project consists of two main components:

- `django_dharma/`: The core library containing logic for running model checks.
- `test_project/`: A test Django project used to perform migrations and test the library with different Django versions.

## Installation

To install and set up the project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/django-dharma.git
   cd django-dharma
   ```

2. **Install dependencies:**

   Make sure you have [Poetry](https://python-poetry.org/) installed. Then run:

   ```bash
   poetry install
   ```

3. **Add Django to the test project:**

   ```bash
   poetry add django
   ```

## Usage

To run model checks, execute the following commands in the test project:

1. **Run migrations:**

   ```bash
   cd test_project
   poetry run python manage.py migrate
   ```

2. **Run tests:**

   ```bash
   poetry run python manage.py test
   ```

## Contributing

If you would like to contribute to the project, please follow these steps:

1. **Fork the repository.**
2. **Create a branch for your change:**

   ```bash
   git checkout -b my-feature
   ```

3. **Add and commit your changes:**

   ```bash
   git add .
   git commit -m "Add a new feature"
   ```

4. **Push your branch and open a pull request.**

## Testing

The project uses `flake8` for linting, `black` for code formatting, and `isort` for import sorting. You can run linting and formatting checks with the following commands:

```bash
poetry run flake8 django_dharma/
poetry run black --check django_dharma/
poetry run isort --check-only django_dharma/
```
