from cassandra.cluster import Cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.set_keyspace('stackexchageanalysis')


def create_recommended_posts_column_family():
    session.execute("""
        CREATE COLUMNFAMILY IF NOT EXISTS RecommendedPosts
            (
                UserID TEXT
                ,Questions LIST<TEXT>
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


def drop_table():
    session.execute("""
    DROP COLUMNFAMILY "mykeyspace"."recommendedposts"
    """, )


