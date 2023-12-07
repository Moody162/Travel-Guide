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
    average_cost DECIMAL(10, 2), -- average cost per day
    best_travel_time VARCHAR(255), -- Stores lists like "January,February,March"
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
