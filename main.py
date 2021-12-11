import streamlit as st

#############################################################################################
#############################################################################################


##############################################################################################
##############################################################################################

# Below we are defining a streamlit webpage which will take user input and predict polarity of taken review

st.header("English-Hindi translator")
st.text("This is Deep-Learning based model,\nwhich translates english language input sentence to hindi language sentence.")
st.text("This translator has its limitations:\n1.   Number of words in input sentence should not be greater than 20 words.")


with st.form("input_form"):
    # st.write("Enter your english sentence below")
    review = st.text_input(label='Please enter your english sentence below')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Translate")

if len(review.split(' ')) > 20:
    st.text('Your input sentence has more than 20 words, please see its limitations')
    # translated_sentence = predict(review)

else:
    if submitted:
        if review == '' or review == None:
            st.text(f"Please enter your english sentence below and press translate!")
        else:
            st.text(f"Your translated sentece will be shown here")

            
hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

copyright = """
<style>
.reportview-container .main footer {visibility: show;}    
"""

st.markdown("Created by Shailesh", unsafe_allow_html=False)
