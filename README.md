# Travel Guide Application

## Entity Relationship Description and Application Basic Structure

### Entity Relationship Description
- **Client**: Represents each user who registers on the application.
  - Attributes:
    - `client_id`: Primary Key
    - `first_name`
    - `last_name`
    - `email`
    - `password`

- **Destination**: Represents each travel destination.
  - Attributes:
    - `destination_id`: Primary Key
    - `name`
    - `average_cost`: Average cost per day
    - `best_travel_time`: Best months for travel
    - `average_weather`: Typical weather condition

- **Questionnaire**: Represents each set of answers provided by the user.
  - Attributes:
    - `questionnaire_id`: Primary Key
    - `client_id`: Foreign Key referencing Client
    - `budget`
    - `weather_preference`
    - `travel_start_date`
    - `travel_end_date`

- **Suggestion**: Represents travel destination suggestions for each user.
  - Attributes:
    - `suggestion_id`: Primary Key
    - `questionnaire_id`: Foreign Key referencing Questionnaire
    - `destination_id`: Foreign Key referencing Destination
    - `match_score`: Score indicating the suitability of the suggestion

### Application Basic Structure
- The application follows a straightforward structure, connecting users with personalized travel suggestions based on their preferences.

## Entity Relationship Diagram

Below is the Entity Relationship Diagram for the Travel Guide Application:

![Entity Relationship Diagram](docs/TravelGuideERModel.jpg)

## Source Code: Relational Schema
```sql
CREATE TABLE client (
    client_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TYPE temperature_preference AS ENUM ('Freezing', 'Cold', 'Cool', 'Mild', 'Warm', 'Hot', 'Very Hot');

CREATE TABLE questionnaire (
    questionnaire_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    budget DECIMAL(10, 2),
    weather_preference temperature_preference,
    travel_start_date DATE,
    travel_end_date DATE,
    FOREIGN KEY (client_id) REFERENCES client(client_id),
    CHECK (travel_end_date > travel_start_date)
);

CREATE TABLE destination (
    destination_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    average_cost DECIMAL(10, 2),
    best_travel_time VARCHAR(255),
    average_weather temperature_preference
);

CREATE TABLE suggestion (
    suggestion_id SERIAL PRIMARY KEY,
    questionnaire_id INT NOT NULL,
    destination_id INT NOT NULL,
    match_score DECIMAL(5, 2),
    FOREIGN KEY (questionnaire_id) REFERENCES questionnaire(questionnaire_id),
    FOREIGN KEY (destination_id) REFERENCES destination(destination_id)
);
