/* Creates the necessary database tables for LOST web application. */

/* A user can have a username, a password, and an associated role */
CREATE TABLE users (
    username varchar(16),
    password varchar(16),
    role varchar(256),
    active boolean default true
);

/* Assets table with primary key, tag, description, disposed flag, and in transit flag */
CREATE TABLE assets (
    asset_tag varchar(16),
    description varchar(256),
    facility varchar(6),
    acquired date,
    disposed date,
    is_disposed boolean default false,
    in_transit boolean default false
);

/* Facilities table with primary key, common name, and facility code */
CREATE TABLE facilities (
    fcode varchar(6),
    common_name varchar(32)
);

/* Decided to create an extra table for asset/facility relationship data */
CREATE TABLE asset_position (
    arrival_time date,
    departure_time date,
    a_tag varchar(16),
    f_code varchar(6) 
);

/* Decided to just have one transfer request table, load/unload date are specified in request form */
CREATE TABLE transfers (
    request_pk serial primary key,
    request_by varchar(16),
    request_dt date,
    approve_by varchar(16),
    approve_dt date,
    asset_tag varchar(16), 
    source varchar(6),
    destination varchar(6),
    load_dt date,
    unload_dt date
);
