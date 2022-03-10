import sqlite3
from sqlite3 import OperationalError

import sys

import numpy as np

from faker import Faker

fake = Faker()


def execute_scripts_from_file(filename):
    conn = sqlite3.connect("dest.sqlite")
    c = conn.cursor()

    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            c.execute(command)
        except OperationalError as msg:
            print("Command skipped: ", msg)


def fill_old_database(file):
    execute_scripts_from_file(file)

    np.random.seed(None)
    print("Filling the old database ...")
    old = sqlite3.connect('old_db_esport.sqlite')
    current = old.cursor()

    try:
        current.execute("""DELETE FROM staff""")
        current.execute("""DELETE FROM coach""")
        current.execute("""DELETE FROM player""")
        current.execute("""DELETE FROM game""")
        current.execute("""DELETE FROM tournament""")
    except:
        print("There is nothing in table")

    id_game = 0
    nb_games = fake.pyint(min_value=5, max_value=20)

    for _ in range(fake.pyint(min_value=10, max_value=50)):
        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        staff = ((fake.last_name(), fake.first_name_male() if gender == "M" else fake.first_name_female(), gender,
                  fake.pyint(min_value=18, max_value=65), fake.pyint(min_value=500, max_value=5000)))
        current.execute("""INSERT into staff(lastname, firstname, gender, age, wage) VALUES(?,?,?,?,?)""",
                        staff)

    number_of_players = fake.pyint(min_value=10, max_value=50)

    for _ in range(nb_games):
        city = str(fake.country()) + " - " + str(fake.country())
        games = (
            city
        )
        current.execute("""INSERT into game(name) VALUES(?)""", (games,))
        id_game = current.lastrowid

        gender = np.random.choice(["M", "F", "NB"], p=[0.4999, 0.4999, 0.0002])
        coachs = ((id_game, fake.last_name(), fake.first_name_male() if gender == "M" else fake.first_name_female(),
                   gender,
                   fake.pyint(min_value=18, max_value=65), fake.pyint(min_value=500, max_value=5000), fake.date()
                   ))
        current.execute(
            """INSERT into coach(idGame, lastname, firstname, gender, age, wage, licenseDate) VALUES(?,?,?,?,?,?,?)""",
            coachs)

        tournaments = ((
            fake.date(), fake.country(), fake.address(), fake.city(), fake.pyint(min_value=20, max_value=180),
            id_game
        ))
        current.execute(
            """INSERT into tournament(date, placeName, address, city, duration, idGame) VALUES(?,?,?,?,?,?)""",
            tournaments)

    for _ in range(nb_games):
        gender = np.random.choice(["M", "F", "NB"], p=[0.46, 0.46, 0.08])
        players = ((id_game, fake.last_name(), fake.first_name_male() if gender == "M" else fake.first_name_female(),
                    gender,
                    fake.pyint(min_value=18, max_value=65), fake.pyint(min_value=500, max_value=5000),
                    fake.pyint(min_value=1, max_value=number_of_players)))
        current.execute(
            """INSERT into player(idGame, lastname, firstname, gender, age, wage, ranking) VALUES(?,?,?,?,?,?,?)""",
            players)

    old.commit()
    old.close()


def migration(filename):
    conn = sqlite3.connect("dest.sqlite")
    cursor = conn.cursor()
    old = sqlite3.connect(filename.split(".")[0] + ".sqlite")
    old_cursor = old.cursor()

    # region Staff employee
    old_cursor.execute("SELECT lastname, firstname, gender, age, wage FROM staff")
    staffs = old_cursor.fetchall()

    for employee in staffs:
        cursor.execute("INSERT INTO Employee_Data(lastname, firstname, gender, age, wage) VALUES(?,?,?,?,?)", employee)
        id_employee_data = cursor.lastrowid
        # region Staff staff
        cursor.execute("Insert into staff(idEmployeeData) VALUES (?)", (id_employee_data,))
        # endregion

    old.commit()
    conn.commit()
    # endregion

    # region Player employee
    old_cursor.execute("SELECT lastname, firstname, gender, age, wage FROM player")
    players = old_cursor.fetchall()

    for player in players:
        cursor.execute("INSERT INTO Employee_Data(lastname, firstname, gender, age, wage) VALUES(?,?,?,?,?)", player)

    # endregion

    # region Player player
    old_cursor.execute("SELECT idGame,ranking FROM player")
    playerRanks = old_cursor.fetchall()

    for playerRank in playerRanks:
        cursor.execute("INSERT INTO Employee_Data(lastname, firstname, gender, age, wage) VALUES(?,?,?,?,?)", employee)
        id_employee_data = cursor.lastrowid
        cursor.execute("INSERT INTO player(idEmployeeData,idGame, ranking) VALUES(?,?,?)",
                       (id_employee_data, playerRank[0], playerRank[1]))

    old.commit()
    conn.commit()
    # endregion

    # region Coach employee
    old_cursor.execute("SELECT lastname, firstname, gender, age, wage FROM coach")
    coachs = old_cursor.fetchall()

    for coach in coachs:
        cursor.execute("INSERT INTO Employee_Data(lastname, firstname, gender, age, wage) VALUES(?,?,?,?,?)", coach)
    # endregion

    # region Coach coach
    old_cursor.execute("SELECT idGame,licenseDate FROM coach")
    coachInfos = old_cursor.fetchall()

    for coachInfo in coachInfos:
        cursor.execute("INSERT INTO Employee_Data(lastname, firstname, gender, age, wage) VALUES(?,?,?,?,?)", employee)
        id_employee_data = cursor.lastrowid
        cursor.execute("INSERT INTO coach(idGame, licenseDate,idEmployeeData) VALUES (?,?,?)",
                       (coachInfo[0], coachInfo[1], id_employee_data))

    old.commit()
    conn.commit()
    # endregion

    # region Game
    old_cursor.execute("Select * from game")
    games = old_cursor.fetchall()

    for game in games:
        cursor.execute("INSERT OR IGNORE INTO game(idGame,name) VALUES(?,?)", game)
    # endregion

    # region Place
    old_cursor.execute("Select placeName,address,city from tournament")
    places = old_cursor.fetchall()

    for place in places:
        cursor.execute("INSERT INTO place(name, address, city) VALUES(?,?,?)", place)
    # endregion

    # region Tournament
    old_cursor.execute("Select idTournament,IdGame,date,duration from tournament")
    tournaments = old_cursor.fetchall()

    for tournament in tournaments:
        cursor.execute("INSERT INTO Employee_Data(lastname, firstname, gender, age, wage) VALUES(?,?,?,?,?)", employee)
        id_employee_data = cursor.lastrowid
        cursor.execute("INSERT OR IGNORE INTO tournament(idTournament,idPlace,idGame,date,duration) VALUES(?,?,?,?,?)",
                       (tournament[0], id_employee_data, tournament[1], tournament[2], tournament[3]))
    # endregion

    conn.commit()
    conn.close()


if __name__ == '__main__':
    db_file = sys.argv[1]
    # fill_old_database(db_file) A dé commenter pour remplir l'ancienne DB
    execute_scripts_from_file("new-db.sql")
    migration(db_file)
