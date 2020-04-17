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

5. **Build the Docker Image (using docker-compose)**
	```
	docker-compose build
	```

6. **Launch the container**
	```
	docker-compose up -d
	```

7. On Startup, a setup screen will be presented where you can fill out the ENV vars for first run. This screen will not be shown again, so please ensure your details are correct.
   ```
   Note: To resetup, delete the file ```.setupcompleted``` from your folder.
   HOWEVER, THIS WILL DELETE YOUR CURRENT SECRET KEY, AND ALL ENCRYPTED DATA WILL NOT BE ABLE TO BE RECOVERED
   ```

# Contributing

There are no contributing guide lines for now. Please browse through the issues, if you find any of them interesting fork this repo, make changes and create PR.
