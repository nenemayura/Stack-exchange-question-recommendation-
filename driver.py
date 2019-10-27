import recommendation_helper
if __name__ == '__main__':
    r_helper = recommendation_helper.RecommendationHelper()
    r_helper.find_recommended_questions()
    r_helper.visualize_question()