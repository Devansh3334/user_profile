### Create virtual environment

```
$ virtualenv venv -p python3
```

### Activate virtual environment

```
$ source env/bin/activate
```


### Migration command

```
$ python manage.py makemigrations
$ python manage.py migrate
    
```

### Create super admin user

```
$  python manage.py createsuperuser
	>>>  email_address : admin@123.com
	>>>  username : admin
	>>>  password : admin
```

### Run django server

```
$ python3 manage.py runserver
```
# user_profile
