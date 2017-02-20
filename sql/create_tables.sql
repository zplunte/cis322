/* Creates the necessary database tables for LOST web application. */

/* NOTE: Here I chose to use the username field as the primary key 
directly. I don't have much experience managing primary/foreign keys 
and this seems to make the most sense right now. I chose length 16 
for both the username and password fields because this forces the 
user to choose usernames and passwords that are at most 16 characters 
long. */ 

CREATE TABLE userdata (
    username varchar(16),
    password varchar(16)
);
