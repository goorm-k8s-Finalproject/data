create table app(
    appid int primary key,
    name varchar(65532) not null
);

create table appdetail(
    appid int primary key,
    header_url varchar(65532),
    release_date date,
    type varchar(50),
    constraint fk_appid
        foreign key(appid)
            references app(appid)
            on delete cascade
);

create table dlc(
    appid int,
    dlcid int,
    primary key(appid, dlcid),
    constraint fk_appid
        foreign key(appid)
            references appdetail(appid)
            on delete cascade,
    constraint fk_dlcid
        foreign key(dlcid)
            references app(appid)
            on delete cascade
);

create table store(
    store_id serial primary key,
    store varchar(50) not null
);

create table price(
    date date,
    store_id int,
    appid int,
    price int not null,
    init_price int not null,
    discount int,
    constraint fk_store_id
        foreign key(store_id)
            references store(store_id)
            on delete cascade,
    constraint fk_appid
        foreign key(appid)
            references appdetail(appid)
            on delete cascade,
    primary key(date, store_id, appid)
);

create table developer(
    devid serial primary key,
    name varchar(200) not null
);

create table app_dev(
    devid int,
    appid int,
    constraint fk_devid
        foreign key(devid)
            references developer(devid)
            on delete cascade,
    constraint fk_appid
        foreign key(appid)
            references appdetail(appid)
            on delete cascade,
    primary key(devid, appid)
);

create table genre(
    genid int primary key,
    genre varchar(50) not null
);

create table app_genre(
    genid int,
    appid int,
    constraint fk_genid
        foreign key(genid)
            references genre(genid)
            on delete cascade,
    constraint fk_appid
        foreign key(appid)
            references appdetail(appid)
            on delete cascade,
    primary key(genid, appid)
);

