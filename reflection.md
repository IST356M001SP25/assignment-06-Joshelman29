# Reflection

Student Name:  josh elman
Sudent Email:  Jdelman@syr.edu

## Instructions

Reflection is a key activity of learning. It helps you build a strong metacognition, or "understanding of your own learning." A good learner not only "knows what they know", but they "know what they don't know", too. Learning to reflect takes practice, but if your goal is to become a self-directed learner where you can teach yourself things, reflection is imperative.

- Now that you've completed the assignment, share your throughts. What did you learn? What confuses you? Where did you struggle? Where might you need more practice?
- A good reflection is: **specific as possible**,  **uses the terminology of the problem domain** (what was learned in class / through readings), and **is actionable** (you can pursue next steps, or be aided in the pursuit). That last part is what will make you a self-directed learner.
- Flex your recall muscles. You might have to review class notes / assigned readings to write your reflection and get the terminology correct.
- Your reflection is for **you**. Yes I make you write them and I read them, but you are merely practicing to become a better self-directed learner. If you read your reflection 1 week later, does what you wrote advance your learning?

Examples:

- **Poor Reflection:**  "I don't understand loops."   
**Better Reflection:** "I don't undersand how the while loop exits."   
**Best Reflection:** "I struggle writing the proper exit conditions on a while loop." It's actionable: You can practice this, google it, ask Chat GPT to explain it, etc. 
-  **Poor Reflection** "I learned loops."   
**Better Reflection** "I learned how to write while loops and their difference from for loops."   
**Best Reflection** "I learned when to use while vs for loops. While loops are for sentiel-controlled values (waiting for a condition to occur), vs for loops are for iterating over collections of fixed values."

`--- Reflection Below This Line ---`


In apicalls.py, we implemented four helper functions that handle external API requests: get_google_place_details() to retrieve place details and reviews using the Google Places API, and three Azure-based functions including get_azure_sentiment(), get_azure_key_phrase_extraction(), and get_azure_named_entity_recognition(). These functions are used to analyze the sentiment, extract key phrases, and detect named entities in the review text. In assignment_etl.py, we first created reviews_step() function which takes a list of Google Place IDs, calls the Google API to fetch reviews, and flattens them into a structured DataFrame, saving it as reviews.csv. The second function, sentiment_step(), processes these reviews by calling the Azure sentiment API for each review, normalizing the results at the sentence level, and writing them to reviews_sentiment_by_sentence.csv. The final function, entity_extraction_step(), uses the Azure entity recognition API to extract named entities from each sentence and stores the output in reviews_sentiment_by_sentence_with_entities.csv. The code difficulty level is hard and one test failed. 



