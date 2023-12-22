from flask import Flask, request, render_template
import joblib
from nltk.stem  import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()
wln= WordNetLemmatizer()
app = Flask(__name__)


def clean_text(text):
    words1 = word_tokenize(text)
    words2 = [word.lower() for word in words1 if word.isalpha() or word.isdigit()]  #Removing punctuations
    words3 = [ls.stem(word) for word in words2 if word not in stopwords.words('english')]  #Removing Stopwords
    tags = pos_tag(words3)
    token3 = []
    
    for word in tags:
        if word[1].startswith('N'):
            token3.append(wln.lemmatize(word[0],pos='n'))
        if word[1].startswith('V'):
            token3.append(wln.lemmatize(word[0],pos='v'))
        if word[1].startswith('R'):
            token3.append(wln.lemmatize(word[0],pos='r'))
        if word[1].startswith('J'):
            token3.append(wln.lemmatize(word[0],pos='a'))

    return token3

classifier = joblib.load('model.bin')
tfidf= joblib.load('vectorizer.bin')


@app.route('/')
def student():
   return render_template('spamdetector.html')

@app.route('/spamfinder',methods=['GET','POST'])
def result():
   if request.method == 'POST':
       data = dict(request.form)
       message = tfidf.transform([data['message']])
       data['result']=classifier.predict(message)[0]
       return render_template('spamoutput.html', data=data)


if __name__ == '__main__':
   app.run(debug=True)
