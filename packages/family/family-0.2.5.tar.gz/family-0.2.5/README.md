# We are family, we are microservices

## Get Started

### Installation

    pip install family

### Create your app

    family-createapp helloworld -f falcon # alternative flask

    # then step by step create your project

    cd helloworld; tree .
        ├── fabfile.py
        ├── gunicorn_development.py
        ├── gunicorn_production.py
        ├── __init__.py
        ├── requirements.txt
        ├── setup.cfg
        ├── setup.py
        ├── shell.py
        ├── supervisor.ini
        ├── yourapp
        │   ├── app.py
        │   ├── __init__.py
        │   ├── middlewares.py
        │   ├── sentry.py
        │   ├── settings.py
        │   └── wsgi.py
        └── yourapp.egg-info
            ├── dependency_links.txt
            ├── entry_points.txt
            ├── PKG-INFO
            ├── requires.txt
            ├── SOURCES.txt
            └── top_level.txt

    pip install -r requirements.txt

### Local development

    gunicorn -c gunicorn_development.py yourapp.wsgi:app
    

### Deployment

    make deploy


## TODO

    * Integrate with SLB to make the service discover and register available.
    * unify configurations
    * common logger
