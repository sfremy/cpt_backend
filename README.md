# Project Description
- This project is a college application tracker called "CollegeApp Scout" that helps students choose colleges for their list and track each application to help with better organization in the already tedious process of college applications. By working on this project, I gained valuable information on backend and frontend development and connectivity, along with creating machine learning algorithms to predict college admission decisions.

- Students can create accounts and login with the same account credentials. This is done in order to allow independent tracking of college applications, creating a highly personalized experience. The creation of the account is done using a POST method in the API endpoint `/api/users`. These credentials are stored in the backend in an SQLite database, and are fetched using the GET method under the same endpoint.

- Upon logging in, the student is redirected to the MyScout page. Here, the student can add their initial colleges to the list. They can always add further colleges to their list in the future. Both of these features work using a PUT method under the API endpint `/api/users/edit`. There is also a college delete feature, where the user can delete specific colleges from the list. This is done using a DELETE method under the edit endpoint. 

- <strong>IMPORTANT</strong>: The colleges are saved as a list, and are fetched using this code line: `json.loads(user.college_list)`. This list is saved in the SQLite database, and is unique to each user. The third screenshot in the Personal Project Reference includes this code. While the college list might not be visible due to being stored in an SQLite database, it is being fetched in the backend and frontend nonetheless. An image of the SQLite database will be included later in the document.

- This project includes a machine learning feature that uses a linear regression model to predict the student's admission decision based on user-entered data such as their SAT score, GPA, and the number of extracurriculars. The dataset used is representative of the most competitive American universities, and is stored in a `.csv` file in the backend.

# Files/features I created

## Backend:
- DELETE function in `user.py` API file: I created the college delete function under the edit endpoint in the API. This uses the DELETE method along with sequencing, selection, and iteration to go through the user's original college list, recognize the user-entered list of colleges to delete, and delete specific colleges from the original list.
- `datamodel.py`: This code defines a data model class with methods for training a logistic regression model, making predictions, creating new data entries, reading data, updating data, and deleting data entries.
- `student_admission_dataset.csv`: This contains the college data for my machine learning program.

## Frontend:
- `website_login.html`: This file includes the simple HTML layout and the core JavaScript code for the login function that uses the POST method in the frontend under `/api/users/authenticate`.
- `2024-02-08-signUp.md`: This file includes the simple HTML layout for the sign up feature along with the core JavaScript code that uses the POST method in the frontend under `/api/users`.
- `config.js`: This creates globally defined variables for the root of the API URL, allowing for simplicity when fetching endpoints anywhere across the frontend.

# Files/features I modified or worked collaboratively on

## Backend:
- `user.py`: I created the delete colleges feature along with assisting with debugging for the PUT method under the edit endpoint.
- `sqlite.db`: Found under the relative URL `instance/sqlite.db`, this includes all the data for the project, including user login credentials, college lists, and the college list items themsevels (Harvard University, MIT, etc.). Every function that reads and commits data stores it in this file.
- `users.py`: In this model file, I integrated additional schema to the SQLite database, `_email` and `_college_list` being major ones.
- `main.py`: The only change I made here was the port number and the initialized data.

# Template code
Our teacher provided use with template code for the login and sign up feature, along with other core backend files. The list below contains all the files that include program code. Some of these files have been modified by our group according to the project requirements, while others have been left completey untouched:
- `user.py`: The login and sign up code under `class UserAPI` and `class _Security` were provided by the teacher.
- `main.py`: The majority of the code was provided by the teacher. Only the port number, initialized data, and college data was added by the group.
- `users.py`: The majority of the model code was provided by the teacher. Only schema changed were made.
- `auth_middleware.py`: The entire file was provided by the teacher. The file relates to the login feature.
- Other docker related files.


### Everything after this point is information provided by the teacher by default for the template repository
# Flask Portfolio Starter

Use this project to create a Flask Servr.

Runtime link: <https://flask.nighthawkcodingsociety.com/>
GitHub link: https://github.com/nighthawkcoders/flask_portfolio

## Conventional way to get started

> Quick steps that can be used with MacOS, WSL Ubuntu, or Ubuntu; this uses Python 3.9 or later as a prerequisite.

- Open a Terminal, clone project and cd to project area

```bash
mkdir ~/vscode; cd ~/vscode

git clone https://github.com/nighthawkcoders/flask_portfolio.git

cd flask_portfolio
```

- Install python dependencies for Flask, etc.

```bash
pip install -r requirements.txt
```

- Run from Terminal without VSCode

  - Setup database and init data
  
  ```bash
    ./migrate.sh
    ```

  - Run python server from command line without VSCode

    ```bash
    python main.py
    ```

### Open project in VSCode

- Prepare VSCode and run

  - From Terminal run VSCode

    ```bash
    code .
    ```

  - Open Setting: Ctl-Shift P or Cmd-Shift
    - Search Python: Select Interpreter
    - Match interpreter to `which python` from terminal

  - Select main.py and Play button
  - Try Play button and try to Debug

## Idea

> The purpose of project is to serve APIs.  It is the backend piece of a Full-Stack project.  Review `api` folder in project for endpoints.

### Visual thoughts

> The Starter code should be fun and practical.

- Organize with Bootstrap menu
- Add some color and fun through VANTA Visuals (birds, halo, solar, net)
- Show some practical and fun links (hrefs) like Twitter, Git, Youtube
- Build a Sample Page (Table)
- Show project specific links (hrefs) per page

### Files and Directories in this Project

These are some of the key files and directories in this project

README.md: This file contains instructions for setting up the necessary tools and cloning the project. A README file is a standard component of all properly set up GitHub projects.

requirements.txt: This file lists the dependencies required to turn this Python project into a Flask/Python project. It may also include other backend dependencies, such as dependencies for working with a database.

main.py: This Python source file is used to run the project. Running this file starts a Flask web server locally on localhost. During development, this is the file you use to run, test, and debug the project.

Dockerfile and docker-compose.yml: These files are used to run and test the project in a Docker container. They allow you to simulate the project’s deployment on a server, such as an AWS EC2 instance. Running these files helps ensure that your tools and dependencies work correctly on different machines.

instances: This directory is the standard location for storing data files that you want to remain on the server. For example, SQLite database files can be stored in this directory. Files stored in this location will persist after web application restart, everyting outside of instances will be recreated at restart.

static: This directory is the standard location for files that you want to be cached by the web server. It is typically used for image files (JPEG, PNG, etc.) or JavaScript files that remain constant during the execution of the web server.

api: This directory contains code that receives and responds to requests from external servers. It serves as the interface between the external world and the logic and code in the rest of the project.

model: This directory contains files that implement the backend functionality for many of the files in the api directory. For example, there may be files in the model directory that directly interact with the database.

templates: This directory contains files and subdirectories used to support the home and error pages of the website.

.gitignore: This file specifies elements to be excluded from version control. Files are excluded when they are derived and not considered part of the project’s original source. In the VSCode Explorer, you may notice some files appearing dimmed, indicating that they are intentionally excluded from version control based on the rules defined in .gitignore.

### Implementation Summary

#### July 2023

> Updates for 2023 to 2024 school year.

- Update README with File Descriptions (anatomy)
- Add JWT and add security features to data
- Add migrate.sh to support sqlite schema and data upgrade

#### January 2023

> This project focuses on being a Python backend server.  Intentions are to only have simple UIs an perhaps some Administrative UIs.

#### September 2021

> Basic UI elements were implemented showing server side Flask with Jinja 2 capabilities.

- Project entry point is main.py, this enables Flask Web App and provides capability to renders templates (HTML files)
- The main.py is the  Web Server Gateway Interface, essentially it contains a HTTP route and HTML file relationship.  The Python code constructs WSGI relationships for index, kangaroos, walruses, and hawkers.
- The project structure contains many directories and files.  The template directory (containing html files) and static directory (containing js files) are common standards for HTML coding.  Static files can be pictures and videos, in this project they are mostly javascript backgrounds.
- WSGI templates: index.html, kangaroos.html, ... are aligned with routes in main.py.
- Other templates support WSGI templates.  The base.html template contains common Head, Style, Body, Script definitions.  WSGI templates often "include" or "extend" these templates.  This is a way to reuse code.
- The VANTA javascript statics (backgrounds) are shown and defaulted in base.html (birds), but are block replaced as needed in other templates (solar, net, ...)
- The Bootstrap Navbar code is in navbar.html. The base.html code includes navbar.html.  The WSGI html files extend base.html files.  This is a process of management and correlation to optimize code management.  For instance, if the menu changes discovery of navbar.html is easy, one change reflects on all WSGI html files.
- Jinja2 variables usage is to isolate data and allow redefinitions of attributes in templates.  Observe "{% set variable = %}" syntax for definition and "{{ variable }}" for reference.
- The base.html uses combination of Bootstrap grid styling and custom CSS styling.  Grid styling in observe with the "<Col-3>" markers.  A Bootstrap Grid has a width of 12, thus four "Col-3" markers could fit on a Grid row.
- A key purpose of this project is to embed links to other content.  The "href=" definition embeds hyperlinks into the rendered HTML.  The base.html file shows usage of "href={{github}}", the "{{github}}" is a Jinja2 variable.  Jinja2 variables are pre-processed by Python, a variable swap with value, before being sent to the browser.
