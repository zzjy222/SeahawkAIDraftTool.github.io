import streamlit as st

page_bg_img = """
<style>
[data-testid= "stAppViewContainer"] {
background-image: url("https://github.com/EloiseYiyunXu/AI-Chatbot.github.io/blob/main/static/bg.png?raw=true");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Add a simple poll to increase user engagement
st.subheader('Fan Poll: Who should be the next Seahawk Draft Pick?')
poll_options = ['Player A', 'Player B', 'Player C', 'Player D']
poll_response = st.radio("Choose your player:", poll_options)
st.write('You selected:', poll_response)


# Include a quiz to test user knowledge and increase engagement
with st.form(key='quiz_form'):
    st.subheader('Seahawk Quiz: Test Your Knowledge!')
    q1 = st.radio("Who won the Super Bowl in 2014?", ['Patriots', 'Seahawks', 'Broncos', 'Packers'], key='q1')
    #q2 = st.text_input("Who is the Seahawks' all-time leading rusher?", key='q2')
    submit_button = st.form_submit_button(label='Submit')
    #if submit_button:
        #correct_answers = 0
    if q1 == 'Seahawks':

        #if q2.lower() == 'marshawn lynch':
            #correct_answers += 1
        st.write(f'You got correct answers')
    else:
        st.write(f'Answer is incorrect!')