CREATE TABLE products (
    product_pk int primary key,
    vendor text,
    description text not null,
    alt_description text
);

CREATE TABLE assets(
    asset_pk int primary key,
    product_fk int REFERENCES products(product_pk) not null,
    asset_tag text,
    description text,
    alt_description text
);

CREATE TABLE vehicles(
    vehicle_pk int primary key,
    asset_fk int REFERENCES assets(asset_pk) not null
);

CREATE TABLE facilities(
    facility_pk int primary key,
    fcode varchar(6) not null,
    common_name text,
    location text
);

CREATE TABLE asset_at(
    asset_fk int REFERENCES assets(asset_pk) not null,
    facility_fk int REFERENCES facilities(facility_pk) not null,
    arrive_dt timestamp,
    depart_dt timestamp
);

CREATE TABLE convoys(
    convoy_pk int primary key,
    request text not null,
    source_fk int REFERENCES facilities(facility_pk) not null,
    dest_fk int REFERENCES facilities(facility_pk) not null,
    depart_dt timestamp not null,
    arrive_dt timestamp not null
);

CREATE TABLE used_by(
    vehicle_fk int REFERENCES vehicles(vehicle_pk) not null,
    convoy_fk int REFERENCES convoys(convoy_pk) not null
);

CREATE TABLE asset_on(
    asset_fk int REFERENCES assets(asset_pk) not null,
    convoy_fk int REFERENCES convoys(convoy_pk) not null,
    load_dt timestamp not null,
    unloaded_dt timestamp not null
);

CREATE TABLE users(
    user_pk int primary key,
    username text not null,
    active boolean not null
);

CREATE TABLE roles(
    role_pk int primary key,
    title text not null
);

CREATE TABLE user_is(
    user_fk int REFERENCES users(user_pk) not null,
    role_fk int REFERENCES roles(role_pk) not null
);

CREATE TABLE user_supports(
    user_fk int REFERENCES users(user_pk) not null,
    facility_fk int REFERENCES facilities(facility_pk) not null
);

CREATE TABLE levels(
    level_pk int primary key,
    abbrv text not null,
    comment text
);

CREATE TABLE compartments(
    compartment_pk int primary key,
    abbrv text not null,
    comment text
);

CREATE TABLE security_tags(
    tag_pk serial primary key,
    level_fk int REFERENCES levels(level_pk) not null,
    compartment_fk int REFERENCES compartments(compartment_pk) not null,
    user_fk int REFERENCES users(user_pk),
    product_fk int REFERENCES products(product_pk),
    asset_fk int REFERENCES assets(asset_pk)
);
