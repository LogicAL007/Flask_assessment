# Flask API for an E-commerce App

## Overview
This Flask API underpins an e-commerce application, supporting user authentication, product exploration, shopping cart management, and order processes. Leveraging RESTful design, it facilitates robust client-server interactions.

## Data Source
Product data originates from the [Flipkart Fashion Products Dataset](https://www.kaggle.com/datasets/aaditshukla/flipkart-fasion-products-dataset) on Kaggle, offering a diverse array of fashion items. The dataset underwent initial cleaning to align with the API's database schema.

## Data Schema
![Artwork_schema (1)](https://github.com/LogicAL007/Flask_assessment/assets/122959675/ba22f494-5046-4dcd-9354-a1f5345ac718)

- **User**: Holds user details like ID, username, email, and password_hash. Links to orders and cart items.
- **Product**: Details product ID, name, description, price, and image URLs from the Kaggle dataset.
- **Cart**: Tracks items a user plans to purchase, noting product IDs and quantities.
- **Order**: Documents completed purchases, listing products, quantities, and overall status.

## API Components
### 1. Auth
Manages user sign-ups, logins, logouts, and password updates for secure access control.

### 2. Views
Facilitates browsing of products, handling of shopping cart operations, and order placements.

### 3. Search
Allows users to search for products based on various criteria, enhancing product discoverability.

## Testing
### Postman
- **Setup**: API endpoints were imported into Postman with configurations for different test scenarios. A Postman collection file is included for reference.
- **Execution**: Created test suites in Postman to assess functionalities such as user registration, product browsing, and shopping cart management.

### Pytest
- **Setup**: Utilized fixtures for configuring a test context and an ephemeral database.
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
