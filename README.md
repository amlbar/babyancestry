# Getting started:

This steps for setting up the project on your local machine assumes you already have the requirements installed and that you are using Ubuntu as your Operating System.

# Requirements:

 * Virtualenv
 * python-dev
 * git

# Steps:

Open up a terminal and type the following commands.
```bash
virtualenv babyancestry
cd babyancestry
git clone https://github.com/amlbar/babyancestry.git
source bin/activate
cd babyancestry
pip install -r requirements.txt
touch babyancestry/local_settings.py
gedit babyancestry/local_settings.py
```

Put this code inside the file 'local_settings.py'.

```python
from settings import *

COMPRESS_ENABLED = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'database.sqlite'),
    }
}
```
Close the editor and then continue the following commands but not including comments:

```bash
python manage.py syncdb
# COMMENT: Then a superuser
python manage.py runserver
# COMMENT: Click the link of your development server that shows in the terminal or Copy and Paste it to your browser.
# COMMENT: Done
```
