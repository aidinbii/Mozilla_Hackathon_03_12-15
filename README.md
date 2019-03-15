# Mozilla_Hackathon_03_12-15
A repository for scripts and data sets made during the Kyrgyz Voice Technology Hackathon. 
The scripts consist of web scrapers for those media which granted permission to use their data: april.kg, sputnik.kg and govori.tv.
The parsed data was used to create a kyrgyz language corpora. 

# Sentiment analysis 
Two different sentiment analysis were implemented to determine the "mood" of a sentence: positive, negative or neutral. An input sentence is translated to english thus the model works for any language (Universal Sentiment Analysis). Tools from Stanford CoreNLP and VADER-Sentiment-Analysis repository were used. The translation was done by using translate services from Google and Yandex.
Stanford CoreNLP is a deep learning model and VADER-Sentiment-Analysis is a dictionary based model. The latter splits the input sentence to tokens and applies grammatical and syntactical rules to compare it with the dictionary. The former model predominantly uses probabilistic machine learning and deep learning components and does not use any rules.

# Audio data
Link to audio files parsed from govori.tv  
https://drive.google.com/open?id=183s3HO1UyNas4BqS0i8D6-ZwDR8ket6-
# The team 
Feruza Asanova, Daniiar Abdiev, Aliya Ismailova and Aidin Biibosunov
