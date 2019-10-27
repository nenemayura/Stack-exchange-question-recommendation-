from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

#KEYSPACE = "testkeysppace"
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
session.set_keyspace('mykeyspace')


def create_recommended_posts_column_family():
    session.execute("""
        CREATE COLUMNFAMILY RecommendedPosts
            (
                UserID TEXT
                ,Questions TEXT
                ,  PRIMARY KEY (UserID)
            );
    """)

def insert_values_in_recommended_posts_column_family(userid, questions):
    session.execute("""
        INSERT INTO RecommendedPosts 
        (UserID, Questions)
        VALUES
        (%s, %s);
    """, (userid, questions))


def get_recommeded_questions_for_user():
    result = session.execute("""
        SELECT *
        FROM RecommendedPosts
    """, )

    return result



