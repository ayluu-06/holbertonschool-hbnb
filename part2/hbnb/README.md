# 📚 HBnB - README 📚
#
## `Project description`
The project consist in developing a program  where an user can  list and 
book places, leave and read reviews, and interact with amenities.  
#
## `Project structure and description`

- `𝑎𝑝𝑖/` : Contains the API endpoints for the application, API routes like users, places, reviews, and amenities are handled here
- `𝘷１/` : Contains version 1 of the API endpoints
- `𝑢𝑠𝑒𝑟𝑠.𝑝𝑦` : Contains the API routes for managing user-related actions like registration, authentication, and profile updates.
- `𝑝𝑙𝑎𝑐𝑒𝑠.𝑝𝑦` : Handles API endpoints related to places, such as creating, updating, and fetching place information.
- `𝑟𝑒𝑣𝑖𝑒𝑤𝑠.𝑝𝑦` : Contains API routes for managing reviews of places, such as creating, deleting, and viewing reviews.
- `𝑎𝑚𝑒𝑛𝑖𝑡𝑖𝑒𝑠.𝑝𝑦` : Handles API endpoints for managing amenities associated with places, like adding and fetching amenities.
#
- `𝑚𝑜𝑑𝑒𝑙𝑠/` : Contains the application's business logic and object models
- `𝑏𝑎𝑠𝑒_𝑚𝑜𝑑𝑒𝑙.𝑝𝑦` : Defines a base class with common attributes (id, created_at, updated_at)
- `𝑢𝑠𝑒𝑟.𝑝𝑦` : Handles the user model
- `𝑝𝑙𝑎𝑐𝑒.𝑝𝑦` : Handles the place model (properties, locations)
- `𝑟𝑒𝑣𝑖𝑒𝑤.𝑝𝑦` : Handles user reviews for places
#
- `𝑝𝑒𝑟𝑠𝑖𝑠𝑡𝑒𝑛𝑐𝑒/` : Manages data storage and database interactions
- `𝑟𝑒𝑝𝑜𝑠𝑖𝑡𝑜𝑟𝑦.𝑝𝑦` : Defines the repository pattern for managing and storing data, like users, places, reviews, etc
#
- `𝑠𝑒𝑟𝑣𝑖𝑐𝑒𝑠/` : Implements the Facade pattern, simplifying interaction between different layers of the application
- `𝑓𝑎𝑐𝑎𝑑𝑒.𝑝𝑦` : Implements the Facade pattern, simplifying interaction between different layers of the application
#
- `𝑟𝑢𝑛.𝑝𝑦` : entry point for running the Flask application
- `𝑐𝑜𝑛𝑓𝑖𝑔.𝑝𝑦` : will be used for configuring environment variables and application settings
- `𝑟𝑒𝑞𝑢𝑖𝑟𝑒𝑚𝑒𝑛𝑡𝑠.𝑡𝑥𝑡` : lists all the Python packages needed for the project
- `𝑅𝐸𝐴𝐷𝑀𝐸.𝑚𝑑` : contains a brief overview of the project
#
#
## `Business Logic Layer`

- **User**: Represents a user in the system.
- **Place**: Represents a place that can be booked by users.
- **Review**: Represents a review written by a user for a specific place.
- **Amenity**: Represents amenities associated with a place (e.g., Wi-Fi, Parking).
#
## Entities and Relationships

### `User Class`
#### Attributes:
 - `id`: Unique identifier (UUID)
 - `first_name`: First name of the user (max length 50 characters)
 - `last_name`: Last name of the user (max length 50 characters)
 - `email`: Email address (must be unique and follow valid email format)
 - `is_admin`: Boolean indicating if the user has admin privileges
 - `created_at`: Timestamp when the user is created
 - `updated_at`: Timestamp when the user is last updated

#### Responsibilities:
 - Manages user information
 - Allows for the creation of users and validation of unique emails
#
### `Place Class`
#### Attributes:
 - `id`: Unique identifier (UUID)
 - `title`: Title of the place (max length 100 characters)
 - `description`: Detailed description of the place (optional)
 - `price`: Price per night for the place
 - `latitude`: Latitude of the place (-90 to 90)
 - `longitude`: Longitude of the place (-180 to 180)
 - `owner`: Reference to the User who owns the place
 - `created_at`: Timestamp when the place is created
 - `updated_at`: Timestamp when the place is last updated

#### Relationships:
 - A **User** can own multiple **Place** instances (one-to-many relationship)
 - A **Place** can have multiple **Review** instances (one-to-many relationship)
 - A **Place** can have multiple **Amenity** instances (many-to-many relationship)
#
### `Review Class`
#### Attributes:
 - `id`: Unique identifier (UUID)
 - `text`: Content of the review (required)
 - `rating`: Rating of the place (integer between 1 and 5)
 - `place`: Reference to the **Place** being reviewed
 - `user`: Reference to the **User** who wrote the review
 - `created_at`: Timestamp when the review is created
 - `updated_at`: Timestamp when the review is last updated

#### Relationships:
 - A **Review** is tied to a specific **Place** and written by a specific **User**
#
### `Amenity Class`
#### Attributes:
 - `id`: Unique identifier (UUID)
 - `name`: Name of the amenity (e.g., "Wi-Fi", "Parking")
 - `created_at`: Timestamp when the amenity is created
 - `updated_at`: Timestamp when the amenity is last updated

#### Relationships:
 - A **Place** can have multiple **Amenity** instances, creating a many-to-many relationship
#
## `Installation`
#
#### Install the dependencies using:
*pip install -r requirements.txt*
#
#### Run the application to ensure everything is set up correctly:
*python run.py*
#