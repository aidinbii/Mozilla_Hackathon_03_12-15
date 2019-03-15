# Mozilla_Hackathon_03_12-15
A repository for scripts and data sets made during the Kyrgyz Voice Technology Hackathon. 
The scripts consist of web scrapers for those media which granted permission to use their data: april.kg, sputnik.kg and govori.tv.
The parsed data was used to create a kyrgyz language corpora. 

# Sentiment analysis 
Two different sentiment analysis were implemented to determine the "mood" of a sentence: positive, negative or neutral. An input sentence is translated to english thus the model works for any language. Tools from Stanford CoreNLP and VADER-Sentiment-Analysis repository were used. The translation was done by using translate services from Google and Yandex.
Stanford CoreNLP is a n-gram based model and VADER-Sentiment-Analysis is a dictionary based model. The former model splits the input sentence to (>1)-gram sequence, while the latter splits it to 1-gram tokens. Due to these properties the perfomance scores differ.    

The team: Feruza Asanova, Daniiar Abdiev, Aliya Ismailova and Aidin Biibosunov.
