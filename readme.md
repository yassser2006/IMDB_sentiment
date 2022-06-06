**Outlines:**

-   **Data Preparation**

-   **Database Architecture**

-   **Data Preprocessing**

-   **Model training**

-   **Model Evaluation**

-   **Web view**

-   **Deploying**

**Data preparation:**

Large Movie Review Dataset: This is a dataset for binary sentiment
classification containing substantially more data than previous
benchmark datasets. We provide a set of 25,000 highly polar movie
reviews for training, and 25,000 for testing.

Now we have the dataset splatted into two directories (train, test) and
each directory has two folders for negative and positive reviews each
review is a text file labeled with the rate. So we can use
keras.utils.text_dataset_from_directory from Tensorflow to make a
generator to feed the model with it but as we need to store the data
into database.

First we have DB_filling_reviews_movies notebook to loop over the files
to fill and prepare the data for the database and link each review with
its movie’s title. Again we have to loop over the movies to link the
reviews with corresponding ids.

So second we have link_reviews_with_review_ID notebook to link the
reviews with review ids from the website

<img src="media/image1.png" style="width:4.25891in;height:2.59351in"
alt="C:\Users\Yasser\AppData\Local\Microsoft\Windows\INetCache\Content.Word\prepare.png" />

**Database architecture:**

The dataset structure shows that we have a relation between the movie
and the review as we can see in the database architecture we can have
many reviews for one movie so I preferred to use a relation database as
PostgreSQL to store our data. And the architecture is quiet simple as
linked both tables with the movie id. So RDS on AWS is the convenient
service we can hold our database there as it support PostgreSQL.

<img src="media/image2.png" style="width:4.90625in;height:3.25in"
alt="C:\Users\Yasser\Downloads\s.drawio (1).png" />

**Data Preprocessing:**

Before we can feed the data to our model there are many cleaning and
preprocessing should be done to prepare our data for this model as:

-   Clean HTML tags from the data

-   Removing the square brackets

-   Removing URLs

-   Removing the stopwords from text

After that we need to tokenize reviews so we can encode them and feed
them to our model. Then a train test split is done to validate and test
our model after that.

For the target we can use label encoder or we can just replace the text
with a class number.

**Model training:**

**Transformers**

> As I used the BERT transformer to train it on the data we don’t need
> the previous preprocessing part as we can use the tokenizer of BERT to
> do all the preprocessing on the data.
>
> BERT makes use of Transformer, an attention mechanism that learns
> contextual relations between words (or sub-words) in a text. In its
> vanilla form, Transformer includes two separate mechanisms — an
> encoder that reads the text input and a decoder that produces a
> prediction for the task. Since BERT’s goal is to generate a language
> model, only the encoder mechanism is necessary.
>
> <img src="media/image3.png" style="width:4.09306in;height:2.77543in"
> alt="https://miro.medium.com/max/1400/0*ViwaI3Vvbnd-CJSQ.png" />
>
> As opposed to directional models, which read the text input
> sequentially (left-to-right or right-to-left), the Transformer encoder
> reads the entire sequence of words at once. Therefore it is considered
> bidirectional, though it would be more accurate to say that it’s
> non-directional. This characteristic allows the model to learn the
> context of a word based on all of its surroundings (left and right of
> the word).
>
> Model hyper parameter:

-   Adam optimizer with learning_rate: 2e-5

-   Loss function: binary_crossentropy

-   Metric: Accuracy

-   Batch size: 32

-   Epochs: 1

-   Maximum length for the tokens: 400

> **Bert transformer is too large** for this problem as we can get a
> good results with only one epoch and the model size is big as we have
> millions of parameters. This won’t be cost effective as we need more
> resources to run this model.

**I also used LSTM and CNN but the most suitable classifier for this
problem would some classic ML classifiers as Naïve bayes with tf-idf or
BOW.**

**Model Evaluation (Transformer BERT):**

Bert model got accuracy of 92% on the test data with the following
confusion matrix:

<img src="media/image4.png" style="width:4.96875in;height:3.44792in"
alt="C:\Users\Yasser\Desktop\conf.png" />

And for other metrics we can see the classification report as follows:

<img src="media/image5.png" style="width:4.56314in;height:1.6669in" />

**Web view:**

The web view consist of two simple parts (Sentimental analysis, Search
DB) as in the following photo you can find the two parts by clicking on
the navigation bar.

Pure HTML and CSS used to develop the frontend and Flask with PostgreSQL
were used to develop the backend.

**Sentimental analysis:** you can add the review in the text box and
click check to get the results from the model in the same web view

<img src="media/image6.png" style="width:6in;height:2.27569in" />

**Search DB:** we can see in this part that we are searching our
database to get percent of time the word or term appears in positive vs
negative reviews along with a review as example.

<img src="media/image7.png" style="width:6in;height:2.23333in" />

**Deploying:**

On AWS there are many service that can deploy this project but as we
have a simple project with only two functions. **EC2 with t3.medium
instance** is very convenient in this case as we need at least 2 GB for
the project only to run the Bert model on it. And the project has a
Dockerfile if we need to deploy it as an image or to deploy it to
Elastic bean stalk or Elastic Container services. So EC2 was used to run
our application on it. I used Windows Subsystem for Linux WSL to
communicate and to deploy the project file from my file system to the
storage on AWS.
