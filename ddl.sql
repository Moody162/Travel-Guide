CREATE TABLE AppUser (
    userID INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE Questionnaire (
    questionnaireID INT PRIMARY KEY,
    userID INT,
    budget DECIMAL(10, 2),
    weatherPreference VARCHAR(50),
    travelStartDate DATE,
    travelEndDate DATE,
    FOREIGN KEY (userID) REFERENCES User1(userID)
);

CREATE TABLE Destination (
    destinationID INT PRIMARY KEY,
    name VARCHAR(50),
    averageCost DECIMAL(10, 2),
    bestTravelTime VARCHAR(50),
    averageWeather VARCHAR(50)
);

CREATE TABLE Suggestion (
    suggestionID INT PRIMARY KEY,
    questionnaireID INT,
    destinationID INT,
    matchScore DECIMAL(5, 2),
    FOREIGN KEY (questionnaireID) REFERENCES Questionnaire(questionnaireID),
    FOREIGN KEY (destinationID) REFERENCES Destination(destinationID)
);