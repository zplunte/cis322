/* Creates the necessary database tables for LOST web application. */

/* A user can have a username, a password, and an associated role */
CREATE TABLE userdata (
    username varchar(16),
    password varchar(16),
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
    code varchar(6),
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
CREATE TABLE transfer_requests (
    requester varchar(16),
    request_date date,
    approver varchar(16),
    approval_date date,
    a_tag varchar(16), 
    src_f_code varchar(6),
    dest_f_code varchar(6),
    load_date date,
    unload_date date
);
