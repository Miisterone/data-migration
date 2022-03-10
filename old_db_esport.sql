create table game
 (
     idGame integer  not null
         primary key autoincrement,
     name   text(30) not null
 );

 create table coach
 (
     idCoach     integer  not null
         primary key autoincrement,
     lastname    text(30) not null,
     firstname   text(30) not null,
     gender      text(30) not null,
     age         integer  not null,
     wage        integer  not null,
     licenseDate text(30) not null,
     IdGame      integer
         constraint FK_8ce1eeb16389d742df20c458324
             references game
 );

 create table player
 (
     idPLayer  integer  not null
         primary key autoincrement,
     lastname  text(30) not null,
     firstname text(30) not null,
     gender    text(30) not null,
     age       integer  not null,
     wage      integer  not null,
     ranking   integer  not null,
     IdGame    integer
         constraint FK_9d24c46ddfcc57ed29c453c2b50
             references game
 );

 create table staff
 (
     idStaff   integer  not null primary key autoincrement,
     lastname  text(30) not null,
     firstname text(30) not null,
     gender    text(30) not null,
     age       integer  not null,
     wage      integer  not null
 );

 create table tournament
 (
     idTournament integer  not null
         primary key autoincrement,
     date         text(30) not null,
     placeName    text(30) not null,
     address      text(30) not null,
     city         text(30) not null,
     duration     integer  not null,
     IdGame       integer
         constraint FK_a7cdb11d62c6d19742ad1a8657c
             references game
 );
