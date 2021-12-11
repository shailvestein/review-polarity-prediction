import streamlit as st
import pickle5 as pickle
import re
import contractions


##############################################################################################
##################                      Preprocessing               ##########################
##############################################################################################

punctuation = """
!"#$%&'()*+, -/:;<=>?@[\]^_`{|}~—“”
"""

def remove_text_with_brackets(row):
    row=re.sub("\(.*?\)","",row)
    row=re.sub("\{.*?\}","",row)
    row=re.sub("\[.*?\]","",row)
    row=re.sub("\<.*?\>","",row)
    return row

def remove_stopwords(row):
    doc = ' '.join([word for word in row.split() if word not in stopword])
    return doc

def remove_punctuations(row):
    for punc in punctuation:
        row = row.replace(punc, ' ')
    return row

def remove_digits(row):
    doc = ' '.join([word for word in row.split() if word.isalpha()])
    return doc

def remove_urls(row):
    doc = []
    for word in row.split():
        if not word.startswith('http') and not word.startswith('www'):
            if not len(word)<=2 and not len(word)>12:
                doc.append(word)
    return ' '.join(doc)


def preprocess(row):
    row = str(row)
    row = remove_digits(row)
    row = row.lower()
    decontracted_word_sentences = ' '.join([contractions.fix(word) for word in row.split(' ')])
    row = decontracted_word_sentences.strip()
    row = remove_text_with_brackets(row)
    # row = remove_stopwords(row)
    row = remove_urls(row)
    row = remove_punctuations(row)
    doc = ' '.join([word for word in row.split()])
    
    return doc


##############################################################################################
##################                      Prediction                  ##########################
##############################################################################################


# Below we are defining a streamlit webpage which will take user input and predict polarity of taken review

# Loading SVM classifier model
with open('./svm_classifier.pkl', 'rb') as model:
    classifier = pickle.load(model)
 
# Loading TF-IDF vectorizer, which converts text into vector
with open('./vectorizer.pkl', 'rb') as vectorizer:
    tfidfvectorizer = pickle.load(vectorizer)
    
# Header of streamlit webpage   
st.header("Review polarity prediction")
st.text("1.\tThis is Machine-Learning based model,\n\tuses support vector machine algorithm in backend to find polarity score.\n2.\tIt tells whether or not given product review is positive.")


with st.form("input_form"):
    # Taking input review here
    review = st.text_input(label='Enter your review here')

    # Predict polarity button
    submitted = st.form_submit_button("Predict Polarity")

# preprocessing input review
review = preprocess(review)

# converting preprocessed review in vector
vector = tfidfvectorizer.transform([review])

# predicting polarity score of input review
polarity = classifier.predict(vector)

# Showing output ot user if polarity score is 1, it is positive review else negative review
if submitted:
    # If user dosen't enter any word/sentence and press predict polarity than show this message
    if review == '' or review == None:
        st.text(f"Please enter your review!")
        
    # It will show polarity of review
    else:
        if polarity == 1:
            st.text(<p style="color:green">Positive review</p>)
        else:
            st.text(<p style="color:red">Negative review</p>)

            
hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

st.markdown("Created by Shailesh", unsafe_allow_html=False)
