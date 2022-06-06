from flask import render_template, Flask, flash, request, redirect
from Model_imdb import Model_imdb
import psycopg2

# def create_app():

imdb = Model_imdb()

app = Flask(__name__)
app.secret_key = "nlaksckl"

def get_db_connection():
    conn = psycopg2.connect(host='database-2.cxv32gki8sxt.us-east-1.rds.amazonaws.com',
                            database='imdb',
                            user='postgres',
                            password='adminYasser')
    return conn

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the review
        if 'review' not in request.form or request.form['review'] == '':
            flash('No review part')
            return redirect(request.url)
        review = request.form['review']

        return render_template('index.html', result=imdb.get_result(review))
        #Response(json.dumps(imdb.get_result(review)),  mimetype='application/json')
        
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        if 'word' not in request.form or request.form['word'] == '':
            flash('No word part')
            return redirect(request.url)

        word = request.form['word']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT sum(CASE WHEN sentiment = 'pos' then 1 ELSE 0 END) as positive, sum(CASE WHEN sentiment = 'neg' then 1 ELSE 0 END) as negative FROM public.reviews WHERE review LIKE '%"+word+"%';")
        row = cur.fetchall()
        if row[0][1] and row[0][1]:
            neg = str(round(row[0][1]*100/(row[0][0]+row[0][1])))+"%"
            cur.execute("SELECT reviews.review, movies.title FROM reviews join movies on movies.id = reviews.movie_id where sentiment = 'neg' AND review LIKE '%"+word+"%' LIMIT 1;")
            neg_review = cur.fetchall()

            pos = str(round(row[0][0]*100/(row[0][0]+row[0][1])))+"%"
            cur.execute("SELECT reviews.review, movies.title FROM reviews join movies on movies.id = reviews.movie_id where sentiment = 'pos' AND review LIKE '%"+word+"%' LIMIT 1;")
            pos_review = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('query.html', 
            neg=neg, 
            neg_review=neg_review,
            pos=pos,
            pos_review=pos_review,
            flag='flex')
        else:
            flash('No reviews for this term')
            return redirect(request.url)
        
    return render_template('query.html',flag='none', neg_review=[0,1],pos_review=[0,1])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # return app