/* Creates the necessary database tables for LOST web application. */

/* A user can have a username, a password, and an associated role */
CREATE TABLE userdata (
    username varchar(16),
    password varchar(16),
    role_fk int REFERENCES roles (role_pk)
);

/* Decided to create a new table specifically for roles */
CREATE TABLE roles (
    role_pk serial primary key,
    role varchar(256)
);

/* Assets table with primary key, tag, description, disposed flag, and in transit flag */
CREATE TABLE assets (
    asset_pk serial primary key,
    asset_tag varchar(16),
    description varchar(256),
    is_disposed boolean default false,
    in_transit boolean default false
);

/* Facilities table with primary key, common name, and facility code */
CREATE TABLE facilities (
    facility_pk serial primary key,
    common_name varchar(32),
    code varchar(6)
);

/* Decided to create an extra table for asset/facility relationship data */
CREATE TABLE asset_position (
    arrival_time date,
    departure_time date,
    asset_fk int REFERENCES assets (asset_pk),
    facility_fk int REFERENCES facilities (facility_pk)
);
