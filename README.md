# Flask API for an E-commerce App

## Overview
This Flask API serves as the backend foundation for an e-commerce application, enabling functionalities such as user authentication, product search, cart management, and order processing. Designed with RESTful principles, it ensures smooth communication between the client-side application and the server for a comprehensive e-commerce experience.

## Data Source
The product information is seeded from the Flipkart Fashion Products Dataset available on Kaggle at [this link](https://www.kaggle.com/datasets/aaditshukla/flipkart-fasion-products-dataset). This dataset provides a rich collection of product details that are integrated into the API's database to have some data to work with, this data was initially cleaned before it was ingested into the database, Attached in the file is a cleaning.ipynb file for the  cleaning and ingestion process.

## Data Schema
![Artwork_schema (1)](https://github.com/LogicAL007/Flask_assessment/assets/122959675/ba22f494-5046-4dcd-9354-a1f5345ac718)

- **User**: Holds user details like ID, username, email, and password_hash. Links to orders and cart items.
- **Product**: Details product ID, name, description, price, and image URLs from the Kaggle dataset.
- **Cart**: Tracks items a user plans to purchase, noting product IDs and quantities.
- **Order**: Documents completed purchases, listing products, quantities, and overall status.

## API Components
### 1. Auth
Manages user sign-ups, logins, logouts, and password updates for secure access control.
#### Routes

##### `/sign-up` (GET, POST)

- **Purpose**: Registers a new user by collecting user information such as email, username, and password.
##### `/login` (GET, POST)

- **Purpose**: Authenticates a user based on email and password.
##### `/logout` (GET, POST)

- **Purpose**: Logs out the currently logged-in user, ending their session.
##### `/change-password/<int:customer_id>` (GET, POST)

- **Purpose**: Allows a logged-in user to change their password.

### 2. Views
Facilitates browsing of products, handling of shopping cart operations, and order placements.
#### `/` (GET)
- **Purpose**: Displays a welcome message from Team B in Data Epic.

#### `/add-to-cart/<item_id>` (GET)
- **Purpose**: Adds a specific item to the user's cart or updates its quantity if it already exists.

#### `/cart` (GET, POST)
- **Purpose**: Retrieves the current user's cart, showing product names, quantities, and prices.

#### `/pluscart` (GET)
- **Purpose**: Increases the quantity of a specific cart item by one.

#### `/minuscart` (GET)
- **Purpose**: Decreases the quantity of a specific cart item by one, ensuring it doesn't go below zero.

#### `/removecart` (GET)
- **Purpose**: Removes a specific item from the user's cart entirely.
  
### 3. Search
Allows users to search for products based on various criteria, enhancing product discoverability.
#### `/productsearch` (GET, POST)
- **Purpose**: Facilitates the search for products by name and optionally filters by price range. Provides a list of products matching the search criteria or all products if no criteria are specified.
- 
## Testing
### Postman
- **Setup**: API endpoints were imported into Postman with configurations for different test scenarios. A Postman collection file is included for reference.
- **Execution**: Created test suites in Postman to assess functionalities such as user registration, product browsing, and shopping cart management.

### Pytest
- **Setup**: Utilized fixtures for configuring a test context and a temporary database.
- **Cases**: Developed tests to simulate API calls, verifying response accuracy and status codes.

## Tools Used
- **Flask**: The primary web framework.
- **SQLAlchemy**: For ORM-based database interactions.
- **Flask-Login**: Manages user sessions.
- **Werkzeug**: Offers secure password hashing.
- **Pytest & Pytest-Flask**: For unit and integration testing.
- **Postman**: Assists in API testing and documentation.
- **SQLite**: Serves as the database engine, ideal for development and testing phases.

Integrating authentic dataset sources, providing full-spectrum API capabilities, and applying thorough testing methodologies with Postman and Pytest, this Flask API lays a solid foundation for building secure, efficient, and user-friendly e-commerce platforms.
