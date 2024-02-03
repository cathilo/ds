import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()

    query1 = """
        SELECT  distinct name FROM `Facilities` where membercost >0.0
        """

    query2 = """
           SELECT  count(distinct name) FROM `Facilities` where membercost =0.0      
     """
    query3 = """
    SELECT  distinct facid, name, membercost, monthlymaintenance
FROM `Facilities` 
where membercost< (0.2 * monthlymaintenance)
    """
    query4 = """
    SELECT  *
FROM `Facilities` 
where facid in (1,5)
"""
    query5 = """
    SELECT name, monthlymaintenance, CASE WHEN monthlymaintenance>100 then 'expensive' else 'cheap' end as level
FROM `Facilities`"""

    query6 = """
    select firstname, surname 
from (SELECT max(starttime) , memid
from `Bookings`
where memid >0) a
join  `Members` b 
on a.memid = b.memid
 """

    query7 = """
    SELECT distinct c.name, firstname ||' '|| surname
from `Bookings` a
join  `Members` b 
on a.memid = b.memid
join `Facilities` c 
on a.facid = c.facid
order by firstname, surname """

    query8 = """
    SELECT c.name, firstname, case when a.memid>0 then membercost else guestcost end as cost
from `Bookings` a
join  `Members` b 
on a.memid = b.memid
join `Facilities` c 
on a.facid = c.facid
where date(starttime) = '2012-09-14'
and ((b.memid > 0 and membercost >30)
or (b.memid = 0 and guestcost >30))"""

    query9 = """
    SELECT c.name, firstname, case when a.memid>0 then membercost else guestcost end as cost
from 
(select *
 from`Bookings`
 where date(starttime) = '2012-09-14') a
join  `Members` b 
on a.memid = b.memid
join `Facilities` c 
on a.facid = c.facid
where ((b.memid > 0 and c.membercost >30)
or (b.memid = 0 and c.guestcost >30))"""

    query10 = """
    select facid, name, sum(cost) as revenue
    from (SELECT a.facid, b.name, a.starttime, a.slots, case when a.memid>0 then membercost else guestcost end as cost
    from`Bookings` a 
    JOIN `Facilities` b
    on a.facid = b.facid
    JOIN `Members` c
    on a.memid = c.memid ) t1
    group by facid, name
    having sum(cost) < 1000
    """
    query11 = """
    select surname, firstname, recommendedby
    from `Members` 
    order by surname, firstname 
    """

    query12 = """
    select b.facid,name, sum(memid)
    from `Bookings` a
    JOIN `Facilities` b
    on a.facid = b.facid
    where memid > 0
    group by b.facid, name
    """
    query13 = """
    select b.facid, name, strftime('%m',starttime), sum(memid)
    from `Bookings` a
    JOIN `Facilities` b
    on a.facid = b.facid
    where memid>0
    group by 1,2,3
    order by 1,2,3
    """

    cur.execute(query1)
    rows = cur.fetchall()
    print(
        "Q1: Some of the facilities charge a fee to members, but some do not. Write a SQL query to produce a list of the names of the facilities that do. ")

    for row in rows:
        print(row)
    cur.execute(query2)
    rows = cur.fetchall()
    print(
        "Q2: How many facilities do not charge a fee to members?")

    for row in rows:
        print(row)

    cur.execute(query3)
    rows = cur.fetchall()
    print(
        "Q3: Write an SQL query to show a list of facilities that charge a fee to members, where the fee is less than 20% of the facility's monthly maintenance cost.Return the facid, facility name, member cost, and monthly maintenance of the facilities in question.")

    for row in rows:
        print(row)

    cur.execute(query4)
    rows = cur.fetchall()
    print(
        "Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.Try writing the query without using the OR operator. ")
    for row in rows:
        print(row)

    cur.execute(query5)
    rows = cur.fetchall()
    print(
        "Q5: Produce a list of facilities, with each labelled as 'cheap' or 'expensive', depending on if their monthly maintenance cost is more than $100. Return the name and monthly maintenance of the facilities  in question.")
    for row in rows:
        print(row)

    cur.execute(query6)
    rows = cur.fetchall()
    print(
        "Q6: You'd like to get the first and last name of the last member(s) who signed up. Try not to use the LIMIT clause for your solution.")
    for row in rows:
        print(row)

    cur.execute(query7)
    rows = cur.fetchall()
    print(
        "Q7: Produce a list of all members who have used a tennis court. Include in your output the name of the court, and the name of the member formatted as a single column. Ensure no duplicate data, and order by the member name. ")
    for row in rows:
        print(row)

    cur.execute(query8)
    rows = cur.fetchall()
    print(
        "Q8: Produce a list of bookings on the day of 2012-09-14 which will cost the member (or guest) more than $30. Remember that guests have different costs to members (the listed costs are per half-hour 'slot'), and the guest user's ID is always 0. Include in your output the name of the facility, the name of the member formatted as a single column, and the cost. Order by descending cost, and do not use any subqueries.")
    for row in rows:
        print(row)

    cur.execute(query9)
    rows = cur.fetchall()
    print(
        "Q9: This time, produce the same result as in Q8, but using a subquery.")
    for row in rows:
        print(row)

    cur.execute(query10)
    rows = cur.fetchall()
    print(
        "Q10: Produce a list of facilities with a total revenue less than 1000. The output of facility name and total revenue, sorted by revenue. Remember that there's a different cost for guests and members!")
    for row in rows:
        print(row)

    cur.execute(query11)
    rows = cur.fetchall()
    print(
        "Q11: Produce a report of members and who recommended them in alphabetic surname,firstname order ")
    for row in rows:
        print(row)

    cur.execute(query12)
    rows = cur.fetchall()
    print(
        "Q12: Find the facilities with their usage by member, but not guests")
    for row in rows:
        print(row)

    cur.execute(query13)
    rows = cur.fetchall()
    print(
        "Q13: Find the facilities usage by month, but not guests")
    for row in rows:
        print(row)


def main():
    database = "sqlite_db_pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)


if __name__ == '__main__':
    main()
