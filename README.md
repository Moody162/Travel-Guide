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
