# Search stock price web app
#### Description:
Basic Stock market web app with user registration and login forms.
Flask, Python, SQLite and IEX Stock market API.

#### flaskr/__init__.py is The application factory with create_app function which creates Flask instance.
In __init__.py we import and register the sql database functions created in db.py. 
Also, we need to import and register any blueprint, in this case that would be blueprint from
auth.py and blog.py

#### flaskr/auth.py containes the blueprint for auth and the views related to authentication.
Views:
Register:
When visiting auth/register register() function will render the template with HTML for registration auth/register.html
If request method is POST -
register() function uses request.form to receive username and password from the registration form.
Also, it generates the password hash and stores both the username and the encoded password in the sql database.
Fucntion also checks that the username isn't registered via except db.IntegrityError
After the user is registered function returns the template with HTML for login. (auth/login.html)

Login:
When visiting auth/login login() function will render the template with HTML for login auth/login.html
If request method is POST -
login() function uses request.form to receive username and password from the login form.
Function selects the user from the database, if the username doesn't exist it returns an error.
Function decoded the password with check_password_hash and returns an error if incorrect.
If username and password are correct function will add the user to the session dictionary.

Logout:
When selecting logout route the logout() function will clear the session and redirect to the index page (blog/index.html)

Login required:
login_required() function is used for in blog views as decorator to make sure createing ,editing or deleting of posts
can be done only by the logged user


#### flaskr/quote.py containes the blueprint for blog and the views related to blog displaying, creating, editing and deleting.
Views:
Index:
index() function renders the template with all the stocks user has searched for in the database. (quote/index.html)

Quote:
lookup() function is used to get the stock quote from teh IEX API. 
When visiting quote/quote quote() function will render the template with HTML for search of the stock ticker
If request method is POST -
quote() function uses request.form to receive ticker from the create form.
Function checks that ticker is entered and is correct and returns an error if not. Function uses the lookup() to get the stock information and
ionsert it into the database. Function renders the stock information on the quoted.html.


Delete:
del_all() function deletes all stocks search history from the database, for current user.

#### Installation:
Install with pip (windows):
```
$ pip install -r requirements.txt
$ pip3 install virtualenv
$py -3 -m venv venv
$venv\Scripts\activate
$pip install Flask
```

Initialize the database
```
$ flask --app flaskr init-db
```

Run in development server
```
$ flask --app flaskr --debug run
```

#### Project Directory:
```
/home/user/Projects/FLASK_BLOG
├───flaskr
│   ├───static
│   │   └───img
│   ├───templates
│   │   ├───auth
│   │   └───quote
│   └───__pycache__
├───instance
└───venv
```