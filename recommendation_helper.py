import os
import xml.etree.ElementTree as xml
from dataset_helper import extract_data
import cassandra_helper


class RecommendationHelper:

    def __init__(self):
        self.users_id_list = []
        self.user_recommended_question = []
        self.user_name_dictionary = {}
        cassandra_helper.create_recommended_posts_column_family()

    def find_recommended_questions(self):

        # get data from zip folder
        users_path, posts_path, postlinks_path = extract_data()

        users_to_process = []

        # XML parsing of users data.
        users_tree = xml.parse(users_path)
        users_root = users_tree.getroot()

        for child in users_root:
            if child.attrib.has_key('Id'):
                if child.attrib['Id'] > '0':
                    users_to_process.append(child.attrib['Id'])
                    if child.attrib.has_key('DisplayName'):
                        name = child.attrib['DisplayName']
                        d = {child.attrib['Id']: name}
                        self.user_name_dictionary.update(d)
        # get all parent ID of posts for which user has answered

        posts_tree = xml.parse(posts_path)
        posts_root = posts_tree.getroot()

        user_wise_answered_questions = []
        post_body_dictionary = {}
        i = 0
        max_user_to_process  = 100
        for userid in users_to_process:
            if i < max_user_to_process:
                per_user_posts_ID = []
                per_user_posts_ID.append(userid)
                for child in posts_root:

                    # generate post ID and title map for future use
                    if child.attrib.has_key('PostTypeId') and child.attrib.has_key(
                            'Id') and child.attrib.has_key('Title'):
                        if child.attrib['PostTypeId'] == '1':
                            d = {child.attrib['Id']: child.attrib['Title']}
                            post_body_dictionary.update(d)

                    # fetch post IDs of questions which user has answered.
                    if child.attrib.has_key('PostTypeId') and child.attrib.has_key(
                            'OwnerUserId') and child.attrib.has_key('ParentId'):

                        if child.attrib['PostTypeId'] == '2' and child.attrib['OwnerUserId'] == userid:
                            per_user_posts_ID.append(child.attrib['ParentId'])
                if len(per_user_posts_ID) > 1:
                    user_wise_answered_questions.append(per_user_posts_ID)
            i = i + 1

        # for a particular user, find recommended posts it
        user_recommended_posts_id = []

        postlinks_tree = xml.parse(postlinks_path)
        postlinks_root = postlinks_tree.getroot()

        related_post_dictionary = {}

        # Aggregate post ID and related post ID from postlinks table to avoid three table join
        # and reduce time complexity

        for child in postlinks_root:
            id_list = []
            if child.attrib.has_key('PostId') and child.attrib.has_key('RelatedPostId') and child.attrib.has_key(
                    'LinkTypeId'):
                if child.attrib['LinkTypeId'] == '1':
                    postId = child.attrib['PostId']
                    related_post_id = child.attrib['RelatedPostId']

                    if related_post_dictionary.has_key(postId):
                        id_list = related_post_dictionary.pop(postId)
                    id_list.append(related_post_id)
                    d = {postId: id_list}
                    related_post_dictionary.update(d)

        recommended_questions_id_dictionary = {}

        # generate dataset containing each User ID and IDs of posts suggested to him
        # based on multiple questions he has answered
        for user in user_wise_answered_questions:
            related_question = []

            for id in range(1, len(user)):

                if related_post_dictionary.has_key(user[id]):
                    related_question.extend(related_post_dictionary.get(user[id]))

            d = {user[0]: related_question}
            recommended_questions_id_dictionary.update(d)

        users_recommended_questions_body = {}

        for user_id in recommended_questions_id_dictionary.iterkeys():
            questions_list = recommended_questions_id_dictionary.get(user_id)
            # print user_id, questions_list
            questions_body_list = []
            if len(questions_list) > 0:
                for question_id in questions_list:
                    if post_body_dictionary.has_key(question_id):
                        question_body = post_body_dictionary.get(question_id)
                        question_body = '\n' + question_body
                        questions_body_list.append(question_body)
                d = {user_id: questions_body_list}

                users_recommended_questions_body.update(d)

        self.user_recommended_question = users_recommended_questions_body
        # print users_recommended_questions_body
        self.insert_into_cassandra()

    def visualize_question(self):
        results = cassandra_helper.get_recommeded_questions_for_user()

        for tuple in results:
            name = self.user_name_dictionary.get(tuple.userid)
            questions = tuple.questions
            print '\n'+name + ''.join(questions)

    def insert_into_cassandra(self):
        for user_id in self.user_recommended_question.iterkeys():
            questions_list = self.user_recommended_question.get(user_id)
            cassandra_helper.insert_values_in_recommended_posts_column_family(user_id, questions_list)

