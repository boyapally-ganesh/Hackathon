

# Hackathon API

This project is a Django-based API for a Hackathon API.


## Prerequisites
```bash
Before you begin, ensure you have met the following requirements:
- You have installed Python 3.8 or higher.



```
## Installation Instructions
### Clone the Repository
To get started, clone this repository to your local machine:
```bash
Follow these steps to get your development environment set up:

1. Clone the repository:
   ```bash
   https://github.com/boyapally-ganesh/Hackathon.git
   cd hackathon

```

## Setup Environment


```bash
 python -m venv env
# Activate the virtual environment
# On Windows
env\Scripts\activate
# On MacOS/Linux
source env/bin/activate


```
## 
Make sure to fill in all necessary variables like database configurations and secret keys.

## Install Dependencies
The project dependencies are listed in the requirements.txt file located at the root of the project directory. 

```bash
  pip install -r requirements.txt

```
## Configuration
Create a .env file in the root directory of the project and add the necessary environment variables

```bash
DEBUG=on
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME


```

```
This command builds the Docker images and starts the containers specified in the 'docker-compose.yml' file.

## Using the Django Development Server
 Apply the migrations:

 ```bash
   python manage.py migrate
```
## Start the development server
 ```bash
  python manage.py runserver
```
## API Usage
Once the application is running, you can use the provided Postman collection (api.postman_collection.json) to interact with the API.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
 ```bash
 
### Notes:

- Ensure you include any specific environment variables needed for your Django settings in the `.env` file example.
- You might want to provide more specific API usage details or expand the sections based on your project’s features or requirements.

This README provides a structured way to guide users through setting up and using your project, enhancing the overall accessibility and usability of your repository.

```


## Documentation

[Documentation] 

```bash
## API Endpoints

This section provides detailed examples of requests for each API endpoint using Postman. Import the provided collection into Postman to interact with the API directly.

### Importing the Collection
1. Open Postman.
2. Click on 'Import' at the top left of the application.
3. Choose 'Link' and paste the URL of the collection.
4. Click 'Continue' and then 'Import' to add the collection to your workspace.

### Available Endpoints

#### User Registration
- **Method:** POST
- **Endpoint:** 'http://127.0.0.1:8000/app/register/'
- **Body:**
  ```json
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123"
}


```
Description: Registers a new user with email, username, and password

#### User Login

##### . Method : POST
####  . Endpoint:  http://127.0.0.1:8000/app/login/
####  . Body

```bash
{
    "username": "testuser",
    "password": "password123"
}


```
After login u will get access key to perform other operations like Create Hackathon etc. 
### Create Hackathon API
#### Method: POST
#### Endpoint: http://127.0.0.1:8000/app/hackathons/
#### Header: Authorization: Bearer {token}
#### Body:

```bash
#### Create Hackathon

- **POST Method:**
  - **Endpoint:** `http://127.0.0.1:8000/app/hackathons/`
  - **Header:** Authorization: Bearer {token}
  - **Body:**
    ```json
   {
    "title": "java",
    "description": "this is java course",
    "background_image": "C:\\Users\\HOME\\Pictures\\beanedit.png",
    "hackathon_image": "C:\\Users\\HOME\\Pictures\\readme.PNG",
    "submissions_type": "image",
    "start_datetime": "2024-09-19T17:54:00Z",
    "end_datetime": "2024-09-20T17:54:00Z",
    "reward_prize": "300"
}

    ```
  - **Description:**The API is creating a new hackathon with details such as title, description, images for the hackathon (background, hackathon image), submission type, and time range (start and end date.Files are being uploaded from the user’s system (images for the hackathon)



```

###### This format clarifies the distinction between the two methods under the same endpoint, making it easier for users to understand how to use each method effectively.

### List Hackathons API
#### Method: GET
#### Endpoint: http://127.0.0.1:8000/app/hackathons/
#### Header: Authorization: Bearer {token}
#### Body:

```bash
#### List Hackathon

- **GET Method:**
  - **Endpoint:** http://127.0.0.1:8000/app/hackathons/`
  - **Header:** Authorization: Bearer {token}
  - **Description:** The API retrieves a list of all available hackathons without requiring any authentication. This is often used to display public hackathons to users..
```

###  Register for a Hackathon
#### Method: POST
#### Endpoint: http://127.0.0.1:8000/app/hackathons/{hackathon_id}/register/
#### Header: Authorization: Bearer {token}
#### Description: This endpoint allows a user to register for a specific hackathon.

```bash
####  Register for a Hackathon

- **POST Method:**
  - **Endpoint:** http://127.0.0.1:8000/app/hackathons/{hackathon_id}/register/`
  - **Header:** Authorization: Bearer {token}
  - **Description:** This endpoint allows a user to register for a specific hackathon.
```

### List User's Enrolled Hackathons
#### Method: GET
#### Endpoint: http://127.0.0.1:8000/app/user/enrolled-hackathons/
#### Header: Authorization: Bearer {token}
#### Body:

```bash
#### List User's Enrolled Hackathons

- **GET Method:**
  - **Endpoint:** http://127.0.0.1:8000/app/user/enrolled-hackathons/`
  - **Header:** Authorization: Bearer {token}
  - **Description:** This endpoint returns a list of hackathons that the user is enrolled in.
  Response:
     Returns a list of hackathons the user is registered for.
```


### Submit Hackathon Entry
#### Method: POST
#### Endpoint: http://127.0.0.1:8000/app/hackathons/{hackathon_id}/submissions/create/
#### Header: Authorization: Bearer {token}
#### Body:

```bash
#### Submit Hackathon Entry

- **POST Method:**
  - **Endpoint:** `http://127.0.0.1:8000/app/hackathons/{hackathon_id}/submissions/create/`
  - **Header:** Authorization: Bearer {token}
  - **Body:**
    ```json
   {
    "hackathon": "java",
    "submission_name": "this is java course",
    "summary": "this is the submi hackthon entry",
    "submission_image": "C:\\Users\\HOME\\Pictures\\beanedit.png",
    "submission_file": "C:\\Users\\HOME\\Pictures\\readme.PNG",
    "submission_link": "https://readme.so/editor"
  
}

    ```
  - **Description:**This endpoint allows a user to submit their entry for a specific hackathon.


URL Parameters:  
  hackathon_id: The unique ID of the hackathon to submit an entry for (e.g., 8e840240-6bb7-4379-a482-629db506d82f).
Response:
  Returns confirmation of the submission.


```


### List Submissions
#### Method: GET
#### Endpoint: http://127.0.0.1:8000/app/hackathons/submissions/
#### Header: Authorization: Bearer {token}
#### Body:

```bash
#### List submissions

- **GET Method:**
  - **Endpoint:** http://127.0.0.1:8000/app/hackathons/submissions/`
  - **Header:** Authorization: Bearer {token}
  - **Description:** This endpoint returns a list of submissions for hackathons.
  Response:
     Returns a list of all submissions made by the user..
```





### Testing Tips

#### @ Ensure that you have replaced {token} with the actual token received after logging in.
#### @ Check the response status and data for each request to understand the API behavior.

For further details or issues, please consult the API documentation linked here or contact our support team.

```bash

This section will make your README comprehensive and very helpful for users who wish to interact with your API effectively.


```
