# Stack-exchange-question-recommendation-
This project contains stack exchange data processing to aggregate data for following task - 

Get suggested questions for each user based on previously answered questions.



To run the code - 
  
  
  
  Download Stack Exchange dataset -  https://archive.org/details/stackexchange
  
  Use python 2.7 
  
  Install and Run Cassandra-3 on the system 
  
  run python driver.py


After executing this command, Cassandra on the system will have column family recommended questions containing user ID and questions suggested to user. 
