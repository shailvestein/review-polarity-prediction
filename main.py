import streamlit as st
import pickle5 as pickle
import re
import contractions
# source: https://discuss.streamlit.io/t/change-backgroud/5653/3

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://www.publicdomainpictures.net/pictures/260000/velka/degrade-texture-1-15294231389TA.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True)

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
header_title = '<p style="color:Black; font-size: 50px;">Review analysis</p>'
st.markdown(header_title, unsafe_allow_html=True)
# header_text_1 = '<p style="color:Black; font-size: 20px;">1.  This is AI based web-app, it uses support-vector-machine algorithm in backend to find polarity score.</p>'
header_text_1 = '<p style="color:Black; font-size: 20px;">1.  This is AI based web-app.</p>'
header_text_2 = '<p style="color:Black; font-size: 20px;">2.  It tells whether or not given product/movie review is good. This app is 86% confident that given review is good/bad.</p>'
st.markdown(header_text_1, unsafe_allow_html=True)
st.markdown(header_text_2, unsafe_allow_html=True)


with st.form("input_form"):
    # Taking input review here
    # source: https://discuss.streamlit.io/t/change-font-size-and-font-color/12377/3
    # enter_review_here = '<p style="color:Black; font-size: 20px;">Your review goes here</p>'
    # st.markdown(enter_review_here, unsafe_allow_html=True)
    review = st.text_input(label='', value='write your review here')
    st.markdown('')
    st.markdown('')
    # Predict polarity button
    submitted = st.form_submit_button("Analyse review")

# preprocessing input review
review = preprocess(review)

# converting preprocessed review in vector
vector = tfidfvectorizer.transform([review])

# predicting polarity score of input review
polarity = classifier.predict(vector)

# Showing output ot user if polarity score is 1, it is positive review else negative review
if submitted:
    # If user dosen't enter any word/sentence and press predict polarity than show this message
    if review == '' or review == 'write your review here':
        review_error = '<p style="color:Orange; text-align:center; background-color:Blue; font-size: 20px;">**Please enter your review!**</p>'
        st.markdown(review_error, unsafe_allow_html=True)
        
    # It will show polarity of review
    else:
        #positive_review = '<p style="color:Green; text-align:center; font-size: 20px;">Positive review</p>'
        #negative_review = '<p style="color:Red; text-align:center; font-size: 20px;">Negative review</p>'
        positive_review = '<p style="color:White; text-align:center; background-color:Green; font-size: 20px;">Good review</p>'
        negative_review = '<p style="color:White; text-align:center; background-color:Red; font-size: 20px;">Bad review</p>'
        
        if polarity == 1:
            st.markdown(positive_review, unsafe_allow_html=True)
        else:
            st.markdown(negative_review, unsafe_allow_html=True)

            
hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden; }    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

created_by = '<p style="text-align:center; color:Black">Created by Shailesh</p>'
st.markdown(created_by, unsafe_allow_html=True)

feedback = '<p style="text-align:center; color:Black">Feel free to write your feedback @ shailvesteinsqrt@gmail.com</p>'
st.markdown(feedback, unsafe_allow_html=True)
