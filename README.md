# truck-app

# Trucking Database Web Application

This is a Flask web application that handles various operations related to a trucking database. This application provides features for managing tractor information, repair information, user authentication, and more.

## Features

1. **User Authentication**: Uses Flask-Login to manage user sessions and protect certain routes.
2. **Tractor Information**:
   - Insert new tractor details.
   - Retrieve tractor information based on asset ID.
   - Delete tractor information.
3. **Repair Information**:
   - Insert new repair details.
   - Retrieve repair information based on asset ID and year.
4. **Excel Data Export**: Allows users to fetch tractor and repair information in Excel format.

## Installation & Setup

### Prerequisites:

- Python
- Flask
- Flask-Login
- PyMySQL
- dotenv
- Pandas

### API Endpoints:

- Home: GET /
- Login: GET, POST /login
- Logout: GET /logout
- Insert Tractor Info: POST /insert_tractor
- Insert Repair Info: POST /insert_repair
- Get Repair Info: POST /get_repair
- Get Tractor Info: POST /get_tractor_info
- Delete Tractor Info: POST /delete_tractor_info
