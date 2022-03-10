# SQL EXAM

## Addario Clément, Pader Joris

<img align="right" height="100" src="https://brand.ynov.com/img/logos/projet_etudiant/ynov/prj_ynov.svg" alt="logo projet">




### Usage :
`python migrations.py old_db_esport.sql`

You need to install [Faker](https://faker.readthedocs.io/en/master/) with : `pip install faker`
<br>You need also install [Numpy](https://numpy.org) with : `pip install numpy`

## Instruction :

(Groups of 2 people) Team Solid, a young e-sports team, wants you to migrate its data to a new database, for which they have created the diagram.

 - 1: Write the .sql file to create an SQLite database respecting the new database schema (Cf db_diagramms.png: top == old schema / bottom == new schema)

 
 - 2: Write a script, in the language of your choice, to migrate data from the old database to the new one
the script will have to take as first parameter the path of the old SQLite database (the name of this file will not be provided)
You will need to migrate the data in the dest.sqlite file
ex (script js:)node migration.js origin.sqlite