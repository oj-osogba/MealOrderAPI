"# MealOrderAPI" 
MEAL PREP ORDER APP

For my week 2 Portfolio Project, I designed parts of the backend api endpoints for an app for users/guest to order food from a meal agent. The current functionalities are:
•	Creating user
•	Creating order
•	Adding an item (by site owner)
•	Adding an address
•	Adding payment details

 
Figure: ERD Diagram for Meal Prep App (Modifications have been made but this highlights the framework)

API DOCUMENTATION
GET
	/users: Get all users 
	/users/id: Get details with given user id
	/users/id/orders: get all order id for given user id
	/orders: get all orders
	/address: get all addresses
	/items: get all items
POST
	/users: Create user account
	/orders: Create order
	/address: create address
	/payments: create payment method
PUT/PATCH
	/users/id/update_address: Update address of given user

DELETE
	/users/id: Delete user with given id

The current iteration is just a framework to build upon there are still a lot of logic and understanding of REST API to implement here:
1.	Building the logic of updating an items number in db if it already exists has not been implemented
2.	Add ability to update the user profile completely and so much more




# FoodOrderAPI
# MealOrderAPI
