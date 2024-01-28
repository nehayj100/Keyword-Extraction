from flask import Flask, request, render_template
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pickle
import sklearn

#flask app
app = Flask(__name__)
# loading files and pickled data
cv = pickle.load(open('count_vector.pkl', 'rb'))
feature_names = pickle.load(open('feature_names.pkl', 'rb'))
TF_IDF_transformer = pickle.load(open('TF_IDF_transformer.pkl', 'rb'))

stop_word = set(stopwords.words('English'))
custom_stop_words = set(["fig","figure","image","sample","using", \
             "show", "result", "large", \
             "also", "one", "two", "three", \
             "four", "five", "seven","eight","nine"])

stop_words = list(stop_word.union(custom_stop_words))
len(stop_words)

# custom functions
def data_processing(text):
    # convert everything to lower case
    text = text.lower()
    # remove all html
    text = re.sub(r"<.*?>", ' ', text)
    # remove special chars
    text = re.sub(r"[^a-zA-Z]", ' ', text)
    # tokenization
    text = nltk.word_tokenize(text)
    # remove stop words
    text = [word for word in text if word not in stop_words]
    # remove keywords that are less than 3 letter
    text = [word for word in text if len(word)>3]
    # limitization
    stm = PorterStemmer()
    text = [stm.stem(word) for word in text]
    return " ".join(text)


def get_keywords(docs, n=10):
    # getting count of words and their respective importance
    docs_cnt = TF_IDF_transformer.transform(cv.transform([docs]))

    # sorting the sparse matrix

    docs_coo = docs_cnt.tocoo()

    tuples = zip(docs_coo.col, docs_coo.data)
    sorted_tuples = sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    # now get top 10 or n keywords
    sorted_tuples = sorted_tuples[:n]

    score_vals = []
    feature_vals = []
    for idx, score in sorted_tuples:
        fname = feature_names[idx]
        score_vals.append(round(score,3))
        feature_vals.append(feature_names[idx])

    #create a tuples of features,score
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]  # Fix: Changed '==' to '='
    return results



# routers
@app.route('/')
# extract keywords
@app.route('/extract_keywords', methods = ['POST', 'GET'])
def extract_keywords():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error = 'File not selectd!')
    if file:
        file = file.read().decode('utf-8', errors= 'ignore')
        clean_file = data_processing(file)
        keywords = get_keywords(clean_file)
        return render_template('keywords.html', keywords= keywords)
    return render_template('index.html')
# search keywords
@app.route('/search_keywords', methods = ['POST', 'GET'])
def search_keywords():
    search_query = request.form['search']
    if search_query:
        keywords = []
        for keyword in feature_names:
            if search_query.lower() in keyword.lower():
                keywords.append(keyword)
                if len(keywords) == 20:  # Limit to 20 keywords
                    break
        return render_template('keywords_list.html', keywords=keywords)
    return render_template('index.html')


def index():
    return render_template('index.html')

# pyhton main

if __name__ == "__main__":
    app.run(debug=True)
