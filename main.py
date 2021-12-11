import streamlit as st
import pickle5 as pickle

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
