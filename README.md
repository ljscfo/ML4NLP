# ML4NLP - Group Beta
Material for the Practical Seminar "Machine Learning for Natural Language Processing" (Institute of Cognitive Science, Osnabrück University, Winter Term 2018/2019).

This is the branch of group Beta.

## Documentation Part 1: 

### Introduction
Today’s world changes at a rapid rate and we are flooded by news constantly. News apps update the user’s feed every minute and keeping up-to-date by oneself is a time-consuming challenge. To reduce the amount of information to the news the user is interested in, a News Recommendation System is required. Such a system is aimed to filter the articles to display solely the relevant reports. The News Recommendation System that will be implemented here, is going to filter news articles from the website wikinews.org. 

### Approaches
Building a News Recommendation System, there are two common approaches: collaborative and content-based approaches [1]. Collaborative or popularity-based approaches use the preferences of many users and similarity measures to predict whether or not a user will like a news article. Problems with this method arise mainly due to a lack of adequate data of user-preferences. Furthermore, it is hard to make predictions for new users, because of the lack of information concerning the user’s interests. For this approach it is therefore very helpful to have user feedback or ratings on articles to collect information about collective preferences, which wikinews.org does not provide. 

Content-based approaches take into account the similarity of the content of the news article and the content of the news articles the user previously liked. The content can be either represented by keywords or the categories an article is assigned to. In wikinews.org, every article belongs to one or more categories (which often also seem to be keywords).

A hybrid approach of a collaborative and a content-based approach could use existing user profiles that are based on collective user action. The user profile built by interpreting explicitly (questionnaire) or implicitly (tracing user activities) collected data can then be compared with the different user profiles from the collaborative approach and the user preferences of the (collective) profile closest to the user’s profile can additionally be taken into account to achieve better performance. If we can manage to obtain such collective user profiles on news, we will try to include it.

Because of the problems that come with the collaborative approach, we decided to implement a content-based news recommender system or a hybrid approach.

### Structure of our Approach [cf.1]: 
#### 1) Categories: 

Wikinews.org provides the following categories: 

Region: Africa • Asia • South / Central / North America • Europe • Middle East • Oceania • Antarctica

Topic: Crime and law • Culture and entertainment • Disasters and accidents • Economy and business • Education • Environment • Health • Obituaries • Politics and conflicts • Science and technology • Sports • Wackynews • Weather

We still need to decide on the scope of our recommender system and whether or not we want to include all categories, only the main categories, or only the subcategories of one main category, e.g. sports or economy

#### 2) Profile Building:

We decided to collect data explicitly by collecting user feedback of every new user. There are different possibilities to collect the data. One way is to show the user several articles from different categories, which are either randomly selected or explicitly chosen to be representative for a certain category, and let the user vote on them without showing the associated categories. Another possibility is to let the user directly vote on the categories in question. 

It may be possible to let the user choose which regional scope he/she is interested in regarding the different topics, e.g. Sports - worldwide, Crime and Law - Europe and Middle-East, Economy - Asia, Europe and North America, Weather - Berlin, etc. 
Also, when the user expresses an interest in Sports, it may be useful to further ask in what kind of sports (wikinews.org provides 59 subcategories), whereas for other categories the subcategories are less explicitly stated and should therefore not be queried.

#### 3) News Recommendation:

In the final step, we will give the recommender the user’s profile and the categorized articles as an input and receive recommendations based on their similarity as an output.


## Documentation Part 2 - Dataset: 

### News Articles and Categories

We are going to use the pre-existing dataset of news articles from Wikinews (https://www.wikinews.org). Every article possesses crowd-sourced labels of associated categories. The dataset is constantly manually updated with new articles and category labels. The dataset contains more than 21.000 articles in English, annotated with 22 main- and/or numerous sub-categories. The representativeness and quality depends on the authors of the articles and the collective reviews and changes. We are going to access the articles through the online-platform 'KnowledgeStore'(https://knowledgestore.fbk.eu).

### The User Profile

For the user profiles, we considered two different approaches. The first approach is to build new user profiles in comparison to other user profiles and the second one is to build every new user profile from scratch, merely depending on the own preferences and behaviour. In order to base user profiles on other profiles, we first need to produce the basis of user profiles. To generate such, we have talked about two possibilities with the other groups. Either every group member manually develops a certain number of user profiles by manually liking or disliking random articles or we automatically generate different profiles by automatically liking or disliking random articles. Liking or disliking articles means that the we save the article with its associated categories and annotate it either with a 1 for liking or a 0 for disliking. The resulting array would look somewhat like this: user_X: [[Article_1, 0], [Article_2, 1], … , [Article_15, 1]]. We can then determine articles a user with the produced profile is likely to like, when recommending articles associated with categories of articles that have previously been liked. The problem with manually producing user profiles is that every member must have a certain person in mind and rank the articles as the person would, or we would end up with user profiles only based on our personal interests and therefore with a possibility of meaningless user profiles. Either way, the profiles are probably not going to cover every new user’s interest pattern. The latter possibility of automatically liking or disliking articles is very likely going to end up with meaningless user profiles as well.   

Based on this consideration, we decided that if we cannot get a very good existing dataset of user profiles for news articles, it is not going to help to use other user profiles to compare new users with. Accordingly, we will build a user profile for new users from scratch and can consider using the so produced profiles at a much later stage, when sufficient data is available, to compare new users with. In order to build a user profiles from scratch, we considered the possibility of starting off with a questionnaire. Of course, it would be great if the user did not have to go through such a process, but it seems to be the most straightforward way to get information about the user’s interests. If we manage to build a questionnaire that is flexible enough, we will be able to only ask relevant questions without boring the user and still give good recommendations right from the beginning. As an alternative or an addition, we will consider explicit user feedback, asking the user whether he/she liked or disliked the article he/she just read. A more elegant way of tracking the user’s behaviour would be to measure how long the user spend reading the article, because if it was only a few seconds, the article was probably not very interesting for the user, but this would be out of the scope of this course.

The approach of developing a new user profile we aim for will look as follows: The new user fills out a questionnaire and based on this, an initial user profile is created. From the questionnaire, our algorithm assumes certain weights for the different categories covered. The categories are ordered in descending order of their weights. Articles with at least one of the categories with the highest weights (and none of the categories with the lowest weights) will be considered as a recommendation. Of these, more recent articles are preferred over older articles and articles that have been seen before are not going to be recommended again. The weights of the categories and the categories considered are adapted after every user feedback. How the weights are adapted is going to depend on the breadth of the category. If an article from a category that only includes 3 articles, like Figure Skating, is liked, it is likely that the other two articles are also interesting to the reader. But if an article is liked which is associated with a very large category like North America, the probability of the user to be interested in every other article in that category is very low.


##Documentation Part 3 -  Data Generation

In order to generate an appropriate sized set of training and test data for our classifier, we decided to generate 100 userprofiles, each user of which randomly either likes or dislikes one of the main categories. Four articles of each category are extracted from the dataset of news articles on wikinews.org and automatically annotated according to the category preferences(liked or disliked). Our classifier will then be trained on half of the extracted articles and tested on the other half of the articles. Accordingly the classifier will train on an tuple of the form (user, article, like/dislike) and will be tested on a tuple of the form (user, article, ?). After training, the classifier will be able to score the given articles and recommend articles accordingly.

The user profiles will look as follows: 

|                          |user 1|user 2|user 3|user 4|
|--------------------------|------|------|------|------|
|Crime and law             |1     |1     |0     |0     |
|Culture and entertainment |0     |1     |1     |0     |
|Disasters and accidents   |0     |0     |0     |1     | 
|Economy and business      |1     |1     |1     |1     |
|Education                 |0     |1     |0     |0     |
|Environment               |1     |0     |1     |0     |
|Health                    |0     |0     |0     |1     |
|Obituaries                |1     |0     |0     |1     |
|Politics and conflicts    |1     |1     |0     |1     |
|Science and technology    |0     |0     |1     |0     |
|Sports                    |0     |1     |0     |0     |
|Wackynews                 |0     |0     |1     |1     |
|Weather                   |1     |1     |0     |0     |

                
An article that user 1 would like would hence include one or more of the categories Crime and law, Culture and entertainment, Disasters and accidents, Health, Politics and conflicts, Science and technology, Weather. We would therefore pick four articles out of each category, so that we end up with 52 articles that are either associated with one or more of  the liked categories and are not associated with any of the disliked categories or that are associated with the disliked and with none of the liked articles

For the random assignments of likes and dislikes, we use the pandas library[2], which can randomly output a number in a given range, which will in our case be 1 or 0. To extract articles that belong to a certain category but not to certain others, we use the function get_applicable_news_categories() located in the folder knowledgestore and defined in ks.py or directly with create_data_set.py. in the folder topic_classification.


## Sources: 
[1] Gopidi, S. T. R. (2015). Automatic User Profile Construction for a Personalized News Recommender System Using Twitter.

[2] https://pandas.pydata.org
