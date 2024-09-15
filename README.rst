Django Dharma
=============

Django Dharma is a Django library designed to facilitate running checks
on models. It provides a structured way to perform and manage checks on
your Django models.

Why Use Django Dharma?
----------------------

Django Dharma is useful in scenarios where you need to validate data
after it has been entered into your system. For example, if you are
importing data from an external source without validating it during the
import process (maybe you want to get them in your system as they are),
you might want to perform validation checks afterward. With Django
Dharma, you can execute checks such as:

-  How many records have been inserted?
-  Does the ``foo`` column contain values other than ``bar``?
-  Does each ``biz`` entry correspond to a ``baz`` entry?

You can save the results of these checks and then analyze them or take
necessary precautions based on the findings.

Project Structure
-----------------

The project consists of two main components:

-  ``django_dharma/``: The core library containing logic for running
   model checks.
-  ``test_project/``: A test Django project used to perform migrations
   and test the library with different Django versions.

Installation
------------

To install Django Dharma, you can use ``pip``:

1. **Install the package:**

   .. code-block:: bash

      pip install django-dharma

2. **Add ``django_dharma`` to your Django project's ``INSTALLED_APPS``
   in ``settings.py``:**

   .. code-block:: python

      INSTALLED_APPS = [
          # ... other installed apps
          'django_dharma',
      ]

Usage
-----

To use Django Dharma, you need to run the ``perform_checks`` management
command to execute the checks on your models. This command will collect
all implementations of the specified protocol and run the checks, saving
any anomalies to the ``Anomaly`` model.

1. **Run migrations:**

   .. code-block:: bash

      python manage.py migrate

2. **Create a check:**

   To create a check, define a class that implements the
   ``CheckProtocol``. The class should include a ``run_checks`` method
   and an attribute ``model`` of type ``models.MyModel``. Here is an
   example:

   .. code-block:: python

      from datetime import datetime
      from django_dharma.base import count_check
      from myapp import models

      class MyModelCheck:
          model = models.MyModel

          def run_checks(self) -> None:
              """
              Verifies that the 'foo' column contains only 'biz' and 'foo' values.
              """
              allowed_values = {'biz', 'foo'}

              # Get distinct values in the 'foo' column
              distinct_values = set(self.model.objects.values_list('foo', flat=True).distinct())

              # Check if all distinct values are in the allowed_values set
              assert distinct_values.issubset(allowed_values), (
                  f"Column 'foo' contains unexpected values: {distinct_values - allowed_values}"
              )

              # This check verifies that there are at least 30 records
              # in the MyModel model for today.
              count_check(model=self.model, filters={"date": datetime.today().date()}, count=30)

              print("All checks passed!")

3. **Run the checks:**

   .. code-block:: bash

      python manage.py perform_checks

Contributing
------------

If you would like to contribute to the project, please follow these
steps:

1. **Fork the repository.**

2. **Create a branch for your change:**

   .. code-block:: bash

      git checkout -b my-feature

3. **Add and commit your changes:**

   .. code-block:: bash

      git add .
      git commit -m "Add a new feature"

4. **Push your branch and open a pull request.**

Testing
-------

The project uses ``flake8`` for linting, ``black`` for code formatting,
and ``isort`` for import sorting. You can run linting and formatting
checks with the following commands:

.. code-block:: bash

   poetry run flake8 django_dharma/
   poetry run black --check django_dharma/
   poetry run isort --check-only django_dharma/
