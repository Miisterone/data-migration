create table place(
    idPlace integer not null primary key autoincrement,
    name text(30),
    address text(30),
    city text(30)
);

create table tournament
(
    idTournament integer not null primary key references game,
    idPlace      integer not null constraint FK_a7cdb11d62c6d19742ad1a8657c references place,
    idGame       integer not null constraint FK_a7cdb11d62c6d19742ad1a8657c references game,
    date text(30) not null,
    duration integer
);

create table game
(
    idGame integer not null primary key,
    name   text(30) not null
);

create table staff(
    idStaff integer not null primary key autoincrement,
    idEmployeeData integer not null constraint FK_a7cdb11d62c6d19742ad1a8657c references employee_data
);

create table player(
    idPlayer integer not null primary key autoincrement,
    idGame integer not null constraint FK_a7cdb11d62c6d19742ad1a8657c references game,
    ranking integer,
    idEmployeeData integer not null constraint FK_a7cdb11d62c6d19742ad1a8657c references employee_data
);

create table coach(
    idCoach integer not null primary key autoincrement,
    idGame integer not null constraint FK_a7cdb11d62c6d19742ad1a8657c references game,
    licenseDate text(30),
    idEmployeeData integer not null constraint FK_a7cdb11d62c6d19742ad1a8657c references employee_data
);

create table employee_data
(
    idEmployee integer not null primary key autoincrement,
    lastname text(30),
    firstname text(30),
    gender text(30),
    age integer,
    wage integer
);