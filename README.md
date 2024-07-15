# ActiveTrack

This is my third milestone project for the Code Institute Level 5 Diploma in Web Application Development. It was designed to implement CRUD functionality while ensuring responsiveness and accessibility across all devices. The project utilizes HTML, CSS, JavaScript, and Python, along with Bootstrap and Jinja. It is a full-stack application built on a PostgreSQL relational database, utilizing technologies such as Flask and SQLAlchemy with Psycopg2.

![Site Image](activetrack/static/documents/site-preview.png)

[View live webpage](https://activetrack-milestone-3-d2dff2fa8baa.herokuapp.com/)

## Project Goal

This project aims to develop a user-friendly, reliable, and secure exercise tracking website to help users monitor and enhance their fitness journey. The site will allow users to track their progress in various exercises, such as logging weights and reps for strength training or recording distance and time for endurance activities. Users will have access to detailed records of their achievements and personal bests to help set future goals. Additionally, the website will feature a community page where users can view and comment on each other's achievements, fostering a supportive and interactive environment.

### CRUD

This project meets CRUD functionality by:

#### Create

- Users can sign up and create an account.
- Users can log new activities.
- Users can add comments.

#### Read

- Users can view their own activity logs.
- Users can view activity logs of other users.
- Users can view their own comments.
- Users can view comments made by others.

#### Update

- Users can update their activity logs.

#### Delete

- Users can delete their activity logs.
- Users can delete their own comments.
- Users can delete comments from others on their own activity logs.

## User Experience (UX)

### Site Contents

- A home page with a welcome to the site.
- A login page for the user to log in.
- A sign up page for the user to sign up for an account.
- A diary page where the user can add, edit, delete or view their own activity logs.
- An add activity page where the user can add an activity log.
- An edit activity page where the user can edit an existing activity log.
- An activity feed page that shows other users activity logs.
- An error page.

### Target Audience

Fitness Enthusiasts
- Individuals who are passionate about fitness and consistently engage in various forms of exercise, such as weightlifting, running, cycling, and swimming and are wanting to track their progress to achieve personal goals.

Beginners in Fitness
- People who are new to fitness and who will benefit from a structured and easy-to-use platform to track their progress and stay motivated.

Competitive Athletes
- Athletes who participate in sports or competitive events and need a reliable way to monitor their training progress.

People with Specific Fitness Goals
- Individuals targeting specific fitness objectives, such as weight loss, muscle gain, or preparing for a marathon.

### User Stories

#### First time visitor
1. As a first-time visitor, I want to create an account quickly using my email so that I can start using the site immediately.
2. As a first-time visitor, I want to log my first activity easily so that I can start tracking my fitness activities right away.
3. As a first-time visitor, I want to be able to easily navigate the site.
4. As a first-time visitor, I want to know immediately what the site is for.

#### Registered visitor
5. As a registered visitor, I want to log in quickly using my credentials so that I can access my saved data.
6. As a registered visitor, I want to log different types of activities so that I can accurately track my exercise.
7. As a registered visitor, I want to see other users activities.
8. As a registered visitor, I want to be able to comment on other users activity logs.
9. As a registered visitor, I want to be able to delete my comments and other users comments on my own activity logs.
10. As a registered visitor, I want to be able to update my current activity logs and delete them.

#### Site owner
11. As a site owner, I want to provide a seamless onboarding experience for new users so that they can quickly and easily start using the app.
12. As a site owner, I want to create a community space within the app where users can interact and support each other.
13. As a site owner, I want to ensure there is sufficient defensive programming to prevent the user deleting data by mistake.
14. As a site owner, I want to ensure there is sufficient defensive programming to prevent a logged-out user from accessing areas of the site only accessible by being logged into an account.
15. As a site owner, I want to ensure there is sufficient defensive programming to guarantee that usernames and emails are unique during signup.

## Accessibility

The site has been built with accessibility in mind to ensure that it is always a positive experience.

This has been achieved by:
- Semantic HTML.
- Choosing fonts and colours with high contrast.
- Adequate aria-labels for interactive features.

## Design

### Imagery

Attribution for the background image used for the site:
[Image by freepik](https://www.freepik.com/free-photo/top-view-perfectly-ordered-fitness-items_40483721.htm#fromView=search&page=5&position=12&uuid=5b9bb55e-33a3-4753-9d3f-3c1ce3062493)

### Wireframes

<details>
<summary>Home Page</summary>
<img src="activetrack/static/documents/wireframes/home-page.png">
</details>
<details>
<summary>Login Page</summary>
<img src="activetrack/static/documents/wireframes/login-page.png">
</details>
<details>
<summary>Sign Up Page</summary>
<img src="activetrack/static/documents/wireframes/sign-up-page.png">
</details>
<details>
<summary>Diary Page</summary>
<img src="activetrack/static/documents/wireframes/diary-page.png">
</details>
<details>
<summary>Activity Feed Page</summary>
<img src="activetrack/static/documents/wireframes/activity-feed-page.png">
</details>
<details>
<summary>Add/Edit Activity Page</summary>
<img src="activetrack/static/documents/wireframes/activity-form-page.png">
</details>
<details>
<summary>Activity Card</summary>
<img src="activetrack/static/documents/wireframes/activity-card.png">
</details>
<details>
<summary>Comments Modal</summary>
<img src="activetrack/static/documents/wireframes/comments-modal.png">
</details>
<details>
<summary>Delete Modal</summary>
<img src="activetrack/static/documents/wireframes/delete-modal.png">
</details>
<details>
<summary>Error Page</summary>
<img src="activetrack/static/documents/wireframes/error-page.png">
</details>

### Database

A relational database was implemented for this site, consisting of three tables: user, activity, and comment. PostgreSQL is the relational database used, employing one-to-many relationships with primary and foreign keys, and db.relationship to effectively manage the connections between the tables.

#### User Journey

<details>
<summary>Flowchart</summary>
<img src="activetrack/static/documents/database/user-journey-chart.png">
</details>

#### Schema

<details>
<summary>Table Schema</summary>
<img src="activetrack/static/documents/database/table-schema.png">
</details>

#### User Table

Represents a user in the database.

User passwords are stored in a hashed format using the werkzeug security library in Python.

- id: Unique identifier for each user, serves as the primary key.
- username: Unique string that identifies the user, used for login purposes.
- email: Unique email address for the user, used for signup.
- password: Encrypted password for user authentication.
- activities (relationship): Establishes a one-to-many relationship with the Activity model. A user can have multiple activities. The cascade="all, delete" ensures that when a user is deleted, all associated activities are also deleted.
- __repr__: Provides a human-readable representation of the user instance.

#### Activity Table

Represents an activity logged by a user.

- id: Unique identifier for each activity, serves as the primary key.
- user_id: Foreign key linking to the User table, indicates which user the activity belongs to. The ondelete="CASCADE" ensures that when a user is deleted, all their activities are also deleted.
- workout_type: Describes the type of workout (endurance or strength).
- exercise_name: Name of the exercise performed (e.g., running, bench press).
- reps: Number of repetitions performed (if applicable).
- distance: Distance covered during the activity (if applicable).
- sets: Number of sets performed (if applicable).
- weight: Weight used during the exercise (if applicable).
- duration: Duration of the activity (if applicable).
- created_at: Timestamp of when the activity was created, defaulting to the current time.
- comments (relationship): Establishes a one-to-many relationship with the Comment model. An activity can have multiple comments. The cascade="all, delete" ensures that when an activity is deleted, all associated comments are also deleted.
- __repr__: Provides a human-readable representation of the activity instance.

#### Comment Table

Represents a comment made by a user on a specific activity.

- id: Unique identifier for each comment, serves as the primary key.
- user_id: Foreign key linking to the User table, indicates which user made the comment. The ondelete="CASCADE" ensures that when a user is deleted, all their comments are also deleted.
- activity_id: Foreign key linking to the Activity table, indicates which activity the comment is related to. The ondelete="CASCADE" ensures that when an activity is deleted, all associated comments are also deleted.
- comment_text: The actual text of the comment.
- created_at: Timestamp of when the comment was created, defaulting to the current time.
- user (relationship): Establishes a many-to-one relationship with the User model, allowing access to the user who made the comment.
- __repr__: Provides a human-readable representation of the comment instance.

### Typography

The following Google Fonts were used on this site:

- Bebas Neue is used for the headings on the site.

![Bebas Neue](activetrack/static/documents/fonts/heading-font.png)

- Oswald is used for the main text of the site.

![Oswald](activetrack/static/documents/fonts/regular-font.png)

Both of these fonts look professional and are easy to read.

### Colour Scheme

The site utilizes a black and white colour scheme for a clean, clear, and visually appealing design.

## Features

### Features On Each Page

#### Navbar

Each page features a navbar containing the site heading and links to various pages. The links displayed vary based on the user's login status. The navbar adjusts based on the device the user is using.

<details>
<summary>Desktop Logged In</summary>
<img src="activetrack/static/documents/page-features/navbar-logged-in.png">
</details>

<details>
<summary>Desktop Logged Out</summary>
<img src="activetrack/static/documents/page-features/navbar-logged-out.png">
</details>

<details>
<summary>Mobile Logged In</summary>
<img src="activetrack/static/documents/page-features/mobile-navbar-logged-in.png">
</details>

<details>
<summary>Mobile Logged Out</summary>
<img src="activetrack/static/documents/page-features/mobile-navbar-logged-out.png">
</details>

User Stories: 3

#### Home Page

The home page greets the user with a personalized welcome message that includes their username. It also provides an introduction to the site and links to other pages, which vary based on the user's login status.

<details>
<summary>Logged In</summary>
<img src="activetrack/static/documents/page-features/home-page-logged-in.png">
</details>

<details>
<summary>Logged Out</summary>
<img src="activetrack/static/documents/page-features/home-page-logged-out.png">
</details>

User Stories: 3, 4

#### Sign Up Page

The sign-up page includes a form for users to create an account. It employs defensive programming to ensure usernames and emails are unique and not already in the database. Additionally, the password fields have character length limitations.

<details>
<summary>Preview</summary>
<img src="activetrack/static/documents/page-features/sign-up-page.png">
</details>

User Stories: 1, 11, 15

#### Login Page

The login page includes a form for users to enter their existing credentials to access their account.

<details>
<summary>Preview</summary>
<img src="activetrack/static/documents/page-features/login-page.png">
</details>

User Stories: 5, 14

#### Diary Page

The diary page greets the user by displaying their username and includes a button to add an activity log. Once a log is added, it appears below the welcome message. The layout of the activity log cards is responsive, switching from rows to columns based on screen size. Each activity log card displays all the logged information and the time it was created. Additionally, each card features three buttons: Comments, Edit, and Delete. The Comments button shows any comments made on the activity, the Edit button allows the user to modify the log, and the Delete button removes it.

<details>
<summary>Preview</summary>
<img src="activetrack/static/documents/page-features/diary-page.png">
</details>

User Stories: 2, 6, 10

#### Add/Edit Activity Page

The add activity page includes a form for users to log an activity. Users can select the type of exercise, either endurance or strength, which populates the exercise dropdown with relevant options. This functionality is implemented using JavaScript, with exercise data provided via a JSON file. The edit page uses the same form structure, but the workout type and exercise fields are fixed and cannot be modified.

<details>
<summary>Add Activity</summary>
<img src="activetrack/static/documents/page-features/add-activity-page.png">
</details>

<details>
<summary>Edit Activity</summary>
<img src="activetrack/static/documents/page-features/edit-activity-page.png">
</details>

User Stories: 2, 6, 10

#### Activity Feed Page

The activity feed page displays all users' activity logs. Each card shows the details of an activity and includes a Comments button, allowing users to view, add, and delete comments. Similar to the diary page, the layout is responsive, adjusting to show in rows or columns based on the device.

<details>
<summary>Preview</summary>
<img src="activetrack/static/documents/page-features/activity-feed-page.png">
</details>

User Stories: 7, 8, 12

#### Comments Modal

The comments modal appears when a user clicks the Comments button on an activity log card, whether on their own logs in the diary page or others' logs in the activity feed page. The modal displays all comments made on that particular activity log. Users can delete their own comments, and the owner of the activity log can delete comments made by others. The modal also includes a text area form for users to write and submit new comments.

<details>
<summary>Preview</summary>
<img src="activetrack/static/documents/page-features/comments-modal.png">
</details>

User Stories: 8, 9, 12

#### Delete Modal

The delete modal appears when a user attempts to delete an activity or a comment. This serves as a defensive programming measure to prevent accidental deletions.

<details>
<summary>Preview</summary>
<img src="activetrack/static/documents/page-features/delete-modal.png">
</details>

User Stories: 9, 10, 13

#### Error Pages

The content of the error pages varies based on the specific error encountered. This is achieved by using a variable declared within the route, which holds the appropriate message for each error.

<details>
<summary>Preview</summary>
<img src="activetrack/static/documents/page-features/error-page.png">
</details>

User Stories: 14

## Future Implementations

- Profile Creation: Implement user profiles that can be customised with photos, bios, and personal information.
- Profile Editing: Allow users to update their details, such as username, email, and password.
- Account Deletion: Enable users to delete their accounts if they choose to do so.
- Liking Activities: Allow users to like activities shared by others.
- Following Users: Implement a feature for users to follow other users to stay updated on their activities.
- Search Capabilities: Add a search feature that allows users to find specific posts based on workout types, exercises, or other users.

## Technologies Used

### Languages

#### HTML

- Used to create the structure of the site.

#### CSS

- Used for the styling of the site.

#### JavaScript

- Used to dynamically populate the exercises within the add activity form based on the selected workout type, ensuring the exercises select menu updates with appropriate values.

#### Python

- Used for developing the backend of the application.

#### Jinja Templating Language

- Used alongside Python and Flask to dynamically display content.

### Frameworks

#### Bootstrap 5

- Used to easily build pages with a responsive and stylish design.

#### Flask

- Used for backend development of the application, including user session management with Flask-Login.

### Libraries

#### SQLAlchemy

- ORM used with Python to work with postgreSQL.

#### Werkzeug

- Used to provide security features for the app, including functionality for password hashing.

### Database

#### PostgeSQL

- Used as the relational database for the app.

## Deployment

## Testing

## Credits

## Acknowledgements