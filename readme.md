### Introduction
- This project is built using Python/ Django Framework
- This project is developed for the task that has been assigned to me by MDBee team
- The project has some Test Cases for auth endpoints

### CRUD Operations for Borrowing Books By Amr Elsayed

- This project is developed by Amr Elsayed for MDBee
- This project is developed using Django & Rest API
- This project is using Docker & Postgresql

### Project Features and assumptions
- There are 2 roles in the system, Admin and Visitor
- Admin can add, view, edit and remove Books
- Visitors can only view books
- The list of books is different from Admin to Visitor (Some fields added to Admin)
- There is a field indicates whether the book can be borrowed or not based on some conditions
- If a book can be borrowed the Admin add a borrow record and fill the necessarily data
- Admin and Visitor can view borrowed books and filter based on (overdue) or not
- When book is retruned the Admin sumbit it and the books available amount is raised

### How to run?
- Make sure you have Docker and Docker Compose intsalled in your system
- In app directory where docker files are, Run (docker-compose up --build)
- In your browser navigate to (http://localhost:8000) to access the application
- In order to try it with Postman, You can find a collection in the app folder in order to load it in Postman

### Postman Collection
- You can find a Postman collection in the main dir of the project
- Load it into Postman and you can see Endpoints and their response as well
- Postman collection is organized and endpoints are separated into Folders and requests

### Running the Test Cases
- The application has a customized test cases on all Endpoints
- To run test cases make sure to run the containers with (docker-compose up --build)
- Get inside the container by (docker exec -it <ContainerID> sh)
- Run the following command (python manage.py test)
- The test cases will run and you can see the result at the end
