create table app(
    app_id int primary key,
    name varchar(65532) not null
    header_url varchar(65532),
    release_date date,
    type varchar(50),
    basegame_id int,
    constraint fk_basegame_id
        foreign key(basegame_id)
            references app(app_id)
            on delete cascade
);

create table store(
    store_id serial primary key,
    store varchar(50) not null
);

create table price(
    date date,
    store_id int,
    app_id int,
    price int not null,
    init_price int not null,
    discount int,
    constraint fk_store_id
        foreign key(store_id)
            references store(store_id)
            on delete cascade,
    constraint fk_app_id
        foreign key(app_id)
            references app(app_id)
            on delete cascade,
    primary key(date, store_id, app_id)
);

create table developer(
    developer_id serial primary key,
    name varchar(200) not null
);

create table app_dev(
    developer_id int,
    app_id int,
    constraint fk_developer_id
        foreign key(developer_id)
            references developer(developer_id)
            on delete cascade,
    constraint fk_app_id
        foreign key(app_id)
            references app(app_id)
            on delete cascade,
    primary key(developer_id, app_id)
);

create table genre(
    genre_id int primary key,
    genre varchar(50) not null
);

create table app_genre(
    genre_id int,
    app_id int,
    constraint fk_genre_id
        foreign key(genre_id)
            references genre(genre_id)
            on delete cascade,
    constraint fk_app_id
        foreign key(app_id)
            references app(app_id)
            on delete cascade,
    primary key(genre_id, app_id)
);

create table recommendation(
    app_id int,
    count int,
    constraint fk_app_id
        foreign key(app_id)
            references app(app_id)
            on delete cascade
);

create table Publisher(
    publisher_id serial primary key,
    name varchar(200)
);

create table app_pub(
    publisher_id int,
    app_id int,
    constraint fk_publisher_id
        foreign key(publisher_id)
            references publisher(publisher_id)
            on delete cascade,
    constraint fk_app_id
        foreign key(app_id)
            references app(app_id)
            on delete cascade,
    primary key(publisher_id, app_id)
);

create table description(
    app_id int primary key,
    short_description text,
    min_requirement text,
    rec_requirement text,
    constraint fk_app_id
        foreign key(app_id)
            references app(app_id)
            on delete cascade
);