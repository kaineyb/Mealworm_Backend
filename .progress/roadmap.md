# API

# Endpoints

## /auth

| Endpoint    | Methods   | Description                                | Implemented | Tested |
| ----------- | --------- | ------------------------------------------ | ----------- | ------ |
| /auth/      | GET       | Main Endpoint for the Auth System          | [x]         | [ ]    |
| auth/users/ | GET, POST | List your user info. Or all users if Admin | [x]         | [ ]    |

**Standard Djoser Endpoints:**

| Endpoint                                     | Methods | Description                                                                                                 | Implemented | Tested |
| -------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------- | ----------- | ------ |
| /users/                                      |         |                                                                                                             | [x]         | [ ]    |
| /users/me/                                   |         |                                                                                                             | [x]         | [ ]    |
| /users/confirm/                              |         |                                                                                                             | [x]         | [ ]    |
| /users/resend_activation/                    |         |                                                                                                             | [x]         | [ ]    |
| /users/set_password/                         |         |                                                                                                             | [x]         | [ ]    |
| /users/reset_password/                       |         |                                                                                                             | [x]         | [ ]    |
| /users/reset_password_confirm/               |         |                                                                                                             | [x]         | [ ]    |
| /users/set_username/                         |         |                                                                                                             | [x]         | [ ]    |
| /users/reset_username/                       |         |                                                                                                             | [x]         | [ ]    |
| /users/reset_username_confirm/               |         |                                                                                                             | [x]         | [ ]    |
| /token/login/ (Token Based Authentication)   |         |                                                                                                             | [x]         | [ ]    |
| /token/logout/ (Token Based Authentication)  |         |                                                                                                             | [x]         | [ ]    |
| /jwt/create/ (JSON Web Token Authentication) |         |                                                                                                             | [x]         | [ ]    |
| /jwt/verify/ (JSON Web Token Authentication) |         | (Note Error with this 22/02/2022 see https://github.com/jazzband/djangorestframework-simplejwt/issues/449 ) | [x]         | [ ]    |

### /stores/ Tests

## /stores

| Endpoint   | Methods            | Description                    | Implemented | Tested |
| ---------- | ------------------ | ------------------------------ | ----------- | ------ |
| /stores/   | GET, POST          | Lists all Stores for that user | [x]         | [ ]    |
| stores/:id | GET, PATCH, DELETE | List a specific Store          | [x]         | [ ]    |

### /stores/ Tests

## /sections

| Endpoint     | Methods            | Description                      | Implemented | Tested |
| ------------ | ------------------ | -------------------------------- | ----------- | ------ |
| /sections/   | GET, POST          | Lists all Sections for that user | [x]         | [ ]    |
| sections/:id | GET, PATCH, DELETE | List a specific Section          | [x]         | [ ]    |

### /sections Tests

## /plans

| Endpoint  | Methods            | Description                   | Implemented | Tested |
| --------- | ------------------ | ----------------------------- | ----------- | ------ |
| /plans/   | GET, POST          | Lists all Plans for that user | [x]         | [ ]    |
| plans/:id | GET, PATCH, DELETE | List a specific Plan          | [x]         | [ ]    |

### /plans Tests

## /plans/:id/days/

| Endpoint           | Methods            | Description                                     | Implemented | Tested |
| ------------------ | ------------------ | ----------------------------------------------- | ----------- | ------ |
| /plans/:id/days/   | GET, POST          | Lists all Days for that Plan                    | [x]         | [ ]    |
| plans/:id/days/:id | GET, PATCH, DELETE | List a specific Day thats assigned to that Plan | [x]         | [ ]    |

### /plans/:id/days/ Tests

## /ingredients

| Endpoint        | Methods            | Description                         | Implemented | Tested |
| --------------- | ------------------ | ----------------------------------- | ----------- | ------ |
| /ingredients/   | GET, POST          | Lists all Ingredients for that user | [x]         | [ ]    |
| ingredients/:id | GET, PATCH, DELETE | List a specific Ingredient          | [x]         | [ ]    |

### /ingredients Tests

## /meals

| Endpoint  | Methods            | Description                        | Implemented | Tested |
| --------- | ------------------ | ---------------------------------- | ----------- | ------ |
| /meals/   | GET, POST          | Lists all Meals for that user      | [X]         | [ ]    |
| meals/:id | GET, PATCH, DELETE | List a specific Meal for that User | [X]         | [ ]    |

### /meals Tests
