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

with open('./svm_classifier.pkl', 'rb') as model:
    classifier = pickle.load(model)
    
with open('./vectorizer.pkl', 'rb') as vectorizer:
    tfidfvectorizer = pickle.load(vectorizer)
    
    
st.header("Review polarity prediction")
#st.text("This is Deep-Learning based model,\nwhich translates english language input sentence to hindi language sentence.")
#st.text("This translator has its limitations:\n1.   Number of words in input sentence should not be greater than 20 words.")


with st.form("input_form"):
    # st.write("Enter your english sentence below")
    review = st.text_input(label='Your review here')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Predict Polarity")

review = preprocess(review)
st.text(review)
vector = tfidfvectorizer.transform([review])

polarity = classifier.predict(vector)

if submitted:
    if review == '' or review == None:
        st.text(f"Please enter your review!")
    else:
        if polarity > 0.5:
            st.text(f"Positive review")
        else:
            st.text(f"Negative review")

            
hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

st.markdown("Created by Shailesh", unsafe_allow_html=False)
