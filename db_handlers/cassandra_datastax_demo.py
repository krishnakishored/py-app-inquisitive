'''
https://docs.datastax.com/en/developer/python-driver/3.15/getting_started/
'''


#
# Connecting to Cassandra
#

from cassandra.cluster import Cluster

cluster = Cluster()

# cluster = Cluster(['192.168.0.1', '192.168.0.2'])  # You can also specify a list of IP addresses for nodes in your cluster:
# The set of IP addresses we pass to the Cluster is simply an initial set of contact points. 
# After the driver connects to one of these nodes it will automatically discover the rest of the nodes in the cluster and connect to them, 
# so you don’t need to list every node in your cluster.

# The connect() method takes an optional keyspace argument which sets the default keyspace for all queries made through that Session:
# session = cluster.connect('worte_liste') 

session = cluster.connect('deutsch_fragen') 

# You can always change a Session’s keyspace using set_keyspace() or by executing a USE query:
# session.execute("CREATE KEYSPACE worte_liste WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' };") 
# session.set_keyspace('worte_liste')
# session.execute('USE users') # or you can do this instead

#
# Executing Queries
# 




# Passing Parameters to CQL Queries

# When executing non-prepared statements, the driver supports two forms of parameter place-holders: positional and named.

# INSERT - Positional parameters are used with a %s placeholder. 
# Note that you should use %s for all types of arguments, not just strings. 
#  you must always use a sequence for the second argument - [], (), even if you are only passing in a single variable 
session.execute(
    """
    INSERT INTO tbl_worte_liste (german, english, partsofspeech)
    VALUES (%s, %s, %s) 
    """,
    ("sein", "to be", "verb")
)

# Named place-holders use the %(name)s form:
session.execute(
    """
    INSERT INTO tbl_worte_liste (german, english, partsofspeech)
    VALUES (%(german)s, %(english)s, %(partsofspeech)s)
    """,
    {'german': "bekommen", 'english': "to receive", 'partsofspeech': "verb"}
)



# SELECT 
rows = session.execute('SELECT german,english FROM tbl_worte_liste')
for row in rows:
    # print(row.german, row.english)
    print(row[0], row[1])


#
# Asynchronous Queries
#






session.execute(
    """
    INSERT INTO tbl_worte_liste (german, english, partsofspeech)
    VALUES (%s, %s, %s)
    """,
    ("arbeiten", 'to work', "verb")
)

