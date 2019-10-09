# bootcamp
A Minimal social networking application using Flask

## Setup

1. **Clone this Repo**

    ``` 
    git clone https://github.com/SriNandan33/bootcamp.git 
    ```

2. **Install Python version 3.6 or greater**

	  https://www.python.org/downloads/
		
3. **Create virtual environment and activate  it**

	```
    python3 -m venv venv
	source venv/bin/activate
    ```

4. **Install requirements**

	```
    pip install -r requirements.txt
    ```
	
5. **Create .flaskenv file and add required environment variables**
	```
	FLASK_APP=run.py
	FLASK_DEBUG=true
	SECRET_KEY=<secret-key>
	ADMIN_EMAIL=<your-email-address>
	SENDGRID_API_KEY=<your-sendgrid-api-key>

	```

		Note: I am currently using google smtp service to send emails ( will be replaced soon). For testing purspose recipient might want to allow less secure apps to send emails to his account (https://myaccount.google.com/lesssecureapps).

6. **Run the application**

    You should run commands below to create and apply migrations. 
    Database and tables will be created.
    
     ```
    flask db migrate
    flask db upgrade 
    ```
	```
    flask run
    ```

    Now go to http://localhost:5000 to see it live.


# Contributing

There are no contributing guide lines for now. Please browse through the issues, if you find any of them interesting fork this repo, make changes and create PR.
