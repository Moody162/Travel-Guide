# Travel-Guide
Travel Guide Application that will help users decide vacation travel destinations.

# 1.	Entity Relationship Description and Application Basic Structure
## 1.1.	Entities
### •	User
Represents each user who registers on the application. <br>
Attributes: userID (PK), name, email. <br>

### •	Destination
Represents each travel destination. <br>
Attributes: destinationID (PK), name, averageCost, bestTravelTime, averageWeather <br>

### •	Questionnaire
Represents each set of answers provided by the user. <br>
Attributes: questionnaireID (PK), userID (FK), budget, weatherPreference, travelStartDate, travelEndDate <br>

### •	Suggestion
Represents travel destination suggestions for each user. <br>
Attributes: suggestionID (PK), questionnaireID (FK), destinationID (FK), matchScore <br>

## 1.2.	Relationships
### •	User – Questionnaire (Fills Out)
One-to-Many from User to Questionnaire: one user can fill out multiple questionnaires over time. Each Questionnaire entry corresponds to exactly one user. <br>

### •	Questionnaire – Suggestion (Generates)
One-to-Many from Questionnaire to Suggestion: based on a single questionnaire, multiple travel suggestions can be generated. Each suggestion corresponds to exactly one questionnaire. <br>

### •	Destination – Suggestion (Is Suggested As)
One-to-Many from Destination to Suggestion: one destination can be suggested in multiple suggestions, but each suggestion points to exactly one destination. <br>

## 1.3.	Working Mechanism
Users register and login. <br>
Users fill out a questionnaire detailing their travel preferences. <br>
Our application will process this data and compare it with the attributes of various travel destinations. Based on matching criteria (like budget, preferred weather, and travel dates), the application generates a score for each destination for the specific user. The destinations with the highest scores will be suggested to the user, which will be saved as Suggestion entities linked to the specific Questionnaire entity. <br>

# 2.	Entity Relationship Diagram
![TravelGuideERModel](https://github.com/Moody162/Travel-Guide/assets/16467758/11e5a582-a7d3-462c-a021-fe398fbece68)

# 3.	Source Code

 
# 4.	Project Members
•	Mohamad Dib Fares (A20482852) <br>
•	HAMZA Taheir BU OBIAD (A20500711) <br>
•	Mehal Gosalia (A20484633) <br>
•	Rajdeep Singh Konthoujam (A20493036) <br>
