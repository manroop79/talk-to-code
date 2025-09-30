# tai-GaaS
## Frontend setup instructions
The frontend was initially created using https://create-react-app.dev/

I used the following command to initialize a basic react app: ```npx create-react-app my-app``` [no need to run this now though]

When first checking out this app, you need to install the packages. ```cd``` into the frontend folder (e.g. tai-GaaS/frontend)

Then, run the command ```npm install```. That should install the needed packages that are listed in package.json

Finally, you can verify the install and start the app locally with the command ```npm start```. You should see a web browser open and display the front end.
## Backend setup instructions
Have Python installed on your machine. You can (usually) verify this in the CMD/terminal with ```python --version```. Proceed if you see an output like: Python 3.X.Y
### Virtual Environment Setup
It's generally a good practice to install python packages in a virtual environment (venv for short) rather than your normal directory. This allows for less conflicts with other Python projects on your machine. Plus, it allows for easier cleanup if you need to rebuild your working environment. You can simply delete the venv folder and start over.

```cd``` into the API folder (e.g. tai-GaaS/API)

Run the following: ```python -m venv venv``` - it should complkete in a few seconds. This command calls the built in venv functionality in Python create a folder called venv in the current directory

Now, we need to activate the venv. This should be done whenever you work on the app. Some editors like VSCode may automatically activate the venv.

The command to activate the venv for Windows: ```venv\Scripts\activate```

The command to activate the venv for Mac: ```source venv\activate.bat```

You will know the venv is activated if you see venv in parentheses in you CMD/terminal window.
### Python Package Setup
At this point, you should be in the API folder (e.g. tai-GaaS/API) with the venv activated. To install the required libraries, use the following: ```pip install -r requirements.txt```. This may take a few minutes.
### Run FastAPI
"uvicorn <api_file_name>:app --host <IP_address> –-port <port_number>".
Replace <api_file_name> with the app file name, <IP_address> and <port_number> with the relevant IP address and port number.
Use the following command: ```uvicorn app:app --host localhost --port 8000 --reload```

Then, in the browser navigate to http://127.0.0.1:8000/docs. Replace the port number with the relevant one if it is different. Click the required end point and click try it now. Then add the payload needed and click execute. 

You can also use Postman tool and provide the end point needed (all the end points are available in app.py file)

You can access the endpoints as the following example: http://127.0.0.1:8000/run_input_scanners/