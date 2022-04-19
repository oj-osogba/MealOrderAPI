"# MealOrderAPI" 
MEAL PREP ORDER APP

For my week 2/3 Portfolio Project, I designed parts of the backend api endpoints for an app for users/guest to order food from a meal agent and deployed on google cloud. The current functionalities are:
•	Creating user
•	Creating order
•	Adding an item (by site owner)
•	Adding/Updating an address
•	Adding payment details

 
Figure: ERD Diagram for Meal Prep App (Modifications have been made but this highlights the framework)

API DOCUMENTATION
GET
/users: Get all users 
/users/id: Get details with given user id
/users/id/orders: get all order id for given user id
/orders: get all orders
/items: get all items
POST
/users: Create user account
/orders: Create order
/address: create address
/payments: create payment method

PUT/PATCH
/address: Update address of given user

DELETE
/users/id: Delete user with given id

The current iteration is just a framework to build upon there are still a lot of logic and understanding of REST API to implement here


