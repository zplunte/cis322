/* Creates the necessary database tables for LOST legacy data.
   Written by Z.P.L. for LOST legacy data migration demo. */
 
CREATE TABLE products (
    product_pk serial primary key,
    vendor varchar(256),
    description varchar(256),
    alt_description varchar(256)
);

CREATE TABLE assets(
    asset_pk serial primary key,
    product_fk int REFERENCES products (product_pk),
    asset_tag varchar(256),
    description varchar(256),
    alt_description varchar(256)
);

CREATE TABLE vehicles(
    vehicle_pk serial primary key,
    asset_fk int REFERENCES assets (asset_pk)
);

CREATE TABLE facilities(
    facility_pk serial primary key,
    fcode varchar(256),
    common_name varchar(256),
    location varchar(256)
);

CREATE TABLE asset_at(
    asset_fk int REFERENCES assets (asset_pk),
    facility_fk int REFERENCES facilities (facility_pk),
    arrive_dt date,
    depart_dt date
);

CREATE TABLE convoys(
    convoy_pk serial primary key,
    request varchar(256),
    source_fk int REFERENCES facilities (facility_pk),
    dest_fk int REFERENCES facilities (facility_pk),
    depart_dt date,
    arrive_dt date
);

CREATE TABLE used_by(
    vehicle_fk int REFERENCES vehicles (vehicle_pk),
    convoy_fk int REFERENCES convoys (convoy_pk)
);

CREATE TABLE asset_on(
    asset_fk int REFERENCES assets (asset_pk),
    convoy_fk int REFERENCES convoys (convoy_pk),
    load_dt date,
    unloaded_dt date
);

CREATE TABLE users(
    user_pk serial primary key,
    username varchar(256),
    active boolean
);

CREATE TABLE roles(
    role_pk serial primary key,
    title varchar(256)
);

CREATE TABLE user_is(
    user_fk int REFERENCES users (user_pk),
    role_fk int REFERENCES roles (role_pk)
);

CREATE TABLE user_supports(
    user_fk int REFERENCES users (user_pk),
    facility_fk int REFERENCES facilities (facility_pk)
);

CREATE TABLE levels(
    level_pk serial primary key,
    abbrv varchar(256),
    comment varchar(256)
);

CREATE TABLE compartments(
    compartment_pk serial primary key,
    abbrv varchar(256),
    comment varchar(256)
);

CREATE TABLE security_tags(
    tag_pk serial primary key,
    level_fk int REFERENCES levels (level_pk),
    compartment_fk int REFERENCES compartments (compartment_pk),
    user_fk int REFERENCES users (user_pk),
    product_fk int REFERENCES products (product_pk),
    asset_fk int REFERENCES assets (asset_pk)
);
