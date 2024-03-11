import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st


st.set_page_config(layout='wide',page_title='Insurance Claim Analysis', page_icon=':chart_with_upwards_trend:')
st.markdown(""" <style>
             div.block-container{
             padding-top:1rem;
             }
             </style>""",unsafe_allow_html= True)

st.title('Health Insurance Claim Analysis')
st.header('About this dataset')
st.write("""This dataset contains insightful information related to insurance claims, giving us an in-depth look into the demographic patterns of those receiving them. 
The dataset contains information on patient age, gender, BMI (Body Mass Index), blood pressure levels, diabetic status, number of children, smoking status and region. 
By analyzing these key factors across geographical areas and across different demographics such as age or gender we can gain a greater understanding of who is most 
likely to receive an insurance claim. This understanding gives us valuable insight that can be used to inform our decision making when considering potential customers 
for our services. On a broader scale it can inform public policy by allowing for more targeted support for those who are most in need and vulnerable. 
These kinds of insights are extremely valuable and this dataset provides us with the tools we need to uncover them.""")

df = pd.read_csv('insurance.csv')
df.drop(columns='index',inplace= True)
st.dataframe(df)
st.download_button('Get Data',data =df.to_csv(),file_name='insurance.csv')
st.divider()

st.header('Basic Feature Engineering')
st.code("""
def categorize_age(age):

  try:
    if 18<= age and age <=29:
      return "young"

    elif 30<= age and age <=35:
      return "30's-35's"

    elif 36 <= age and age <=40:
      return "36's-40's"

    elif 41 <=age and age <= 45:
      return "41's-45's"

    elif 46 <=age and age <= 50:
      return "46's-50's"

    elif 51 <= age and age<= 55:
      return "51's-55's"

    elif 56 <=age and age<=60:
      return "56's-60's"

  except Exception as e:
     return "not defined"

categorize_age = df['age'].apply(categorize_age)
df.insert(2,'categorize_age',categorize_age)""")

st.code("""
def categorize_bmi(bmi):

    if bmi < 18.5:
        return "under-weight"
    elif 18.5 <= bmi < 25:
        return "normal-weight"
    elif 25 <= bmi < 30:
        return "overweight"
    else:
        return "obesity"

categorize_bmi = df['bmi'].apply(categorize_bmi)
df.insert(5,'categorize_bmi',categorize_bmi)
""")

st.code("""
def categorize_bp(value):

    if 80 <= value and value <120:
        return 'Normal'
    elif 120 <= value <= 129:
        return 'Elevated'
    else:
        return 'Hypertension'

categorize_bp = df['bloodpressure'].apply(categorize_bp)
df.insert(7,'categorize_bp',categorize_bp)
""")

st.code("""
lower_q = df['claim'].quantile(0.25)
upper_q = df['claim'].quantile(0.75)

def categorize_claim(claim_amount):
    if claim_amount < lower_q:
        return 'lower'
    elif lower_q <= claim_amount <= upper_q:
        return 'mid'
    else:
        return 'higher'

df['categorize_claim'] = df['claim'].apply(categorize_claim)
""")

# Basic Feature Engineering
def categorize_age(age):

  try:
    if 18<= age and age <=29:
      return "young"

    elif 30<= age and age <=35:
      return "30's-35's"

    elif 36 <= age and age <=40:
      return "36's-40's"

    elif 41 <=age and age <= 45:
      return "41's-45's"

    elif 46 <=age and age <= 50:
      return "46's-50's"

    elif 51 <= age and age<= 55:
      return "51's-55's"

    elif 56 <=age and age<=60:
      return "56's-60's"

  except Exception as e:
     return "not defined"

categorize_age = df['age'].apply(categorize_age)
df.insert(2,'categorize_age',categorize_age)

def categorize_bmi(bmi):

    if bmi < 18.5:
        return "under-weight"
    elif 18.5 <= bmi < 25:
        return "normal-weight"
    elif 25 <= bmi < 30:
        return "overweight"
    else:
        return "obesity"

categorize_bmi = df['bmi'].apply(categorize_bmi)
df.insert(5,'categorize_bmi',categorize_bmi)

def categorize_bp(value):

    if 80 <= value and value <120:
        return 'Normal'
    elif 120 <= value <= 129:
        return 'Elevated'
    else:
        return 'Hypertension'

categorize_bp = df['bloodpressure'].apply(categorize_bp)
df.insert(7,'categorize_bp',categorize_bp)

lower_q = df['claim'].quantile(0.25)
upper_q = df['claim'].quantile(0.75)


def categorize_claim(claim_amount):
    if claim_amount < lower_q:
        return 'lower'
    elif lower_q <= claim_amount <= upper_q:
        return 'mid'
    else:
        return 'higher'

df['categorize_claim'] = df['claim'].apply(categorize_claim)

st.download_button(' Get Updated dataset',data=df.to_csv(),file_name='insurance.csv')
st.divider()

st.header('Insights from the data')

def go_analysis_1():

  temp = df.groupby('region')['claim'].sum().sort_values(ascending=False).reset_index().rename(columns={'claim':'claim_amount'})
  fig = px.bar(temp, x='region', y='claim_amount', text_auto=True, color='region', title='Claim Amount vs Region')
  fig.update_layout(yaxis = dict(title = 'claim amount'))

  st.plotly_chart(fig)
  st.text("""- Typically, individuals from the south-east region make the highest number of insurance claims(total 5.78 M USD), and they also tend to claim larger
  amounts as comparsion to the others.""")
  st.text("""- After south-east, individuals from the north-west region make the highest number of claims(total 4.06 M USD) from insurance companies.""")


  fig = px.pie(temp, values='claim_amount', names='region', hover_name='region', hole=0.5,title=' Region Contribution in Total Claim Amount')
  st.plotly_chart(fig)
  st.text("""- Out of the total claim amount 32.6% amount only goes to south-east region.""")


  temp2 = df[df['categorize_claim'] == 'higher']['region'].value_counts().reset_index()
  fig = px.pie(temp2, values='count',names='region',hover_name = 'region',hole = 0.5,title ='Region contribution in Higher Claim Amounts ')
  st.plotly_chart(fig)
  st.text("""- Out of the total higher claim amounts 33.4% amount only goes to south-east region.""")

  fig = px.scatter(df, y='region', x='claim', color='region', hover_name='claim',title='Number of Claims Over Different Regions')
  st.plotly_chart(fig)
  st.text("""- The density of scatter bubbles is higher in the Southeast region.""")

  temp = df.groupby('region')['claim'].count().reset_index().rename(columns={'claim': 'count'})
  fig = px.pie(temp, values='count', names='region', hover_name='region', hole=0.5, title='Region Contribution in Total Number of Claims')
  st.plotly_chart(fig)
  st.text("""- Out of the total number of claims 33.1% claims only goes to people of south-east region """)

  st.subheader("Why are the majority of claims from the 'South-East' region of the USA?")

  st.text("(By Google)")
  st.markdown("""
  <strong>1. Healthcare Access and Quality:</strong> The Southeast region, particularly in rural areas, faces challenges 
  such as physician shortages and limited access to healthcare facilities. This can result in lower 
  quality care and higher rates of illness, leading to increased health insurance claims.

  <strong>2. Prevalence of Chronic Diseases:</strong> Chronic diseases like obesity, diabetes, heart disease, and hypertension 
  are more common in the Southeast. These conditions necessitate frequent medical visits, hospitalizations, 
  and prescription medication usage, contributing to higher insurance claims.

  <strong>3. Health Behaviors and Lifestyle:</strong> Variations in health behaviors such as smoking, diet, and physical 
  activity affect the prevalence of chronic diseases. Additionally, lower adherence to preventive healthcare 
  practices in the Southeast leads to increased healthcare utilization and insurance claims.""", unsafe_allow_html=True)


def go_analysis_2():
    temp = (pd.crosstab(df['gender'], df['region'], normalize='columns') * 100).round(2)
    st.dataframe(temp)

    st.text("""
1. These regions also have the highest number of insurance claims, often for significant amounts as from previous analysis.
2. Maybe there is a possibility that female population claims the most. Is it ?
3. The answer is No""")

def go_analysis_3():
    st.text("""1. Males apply for insurance amounts more frequently compared to females.
2. Of the total claims, 50.6% were made by males, while 49.4% were made by females.
3. Not a huge difference.""")

    temp = df.groupby('gender')['claim'].count().reset_index().rename(columns={'claim':'claim_count'})
    st.dataframe(temp)
    fig = px.pie(temp, values='claim_count',names='gender',hover_name = 'gender',hole = 0.5,title='Claim Distribution over Gender')
    st.plotly_chart(fig)

    st.subheader("Why majority of claims are done by males than rather females?")

    st.text("(By Google)")
    st.markdown("""
    <strong>1. Occupational Hazards:</strong> Males may be overrepresented in certain occupations that carry higher risks of injury or illness, 
    such as construction, mining, or firefighting. This can lead to a higher frequency of health insurance claims for work-related injuries or 
    occupational diseases

    <strong>2. Healthcare Utilization Patterns:</strong> Research suggests that men, on average, may be less likely to seek preventive care and medical 
    attention for minor health issues compared to women. As a result, when men do seek medical care, their conditions may be more advanced or 
    require more extensive treatment, leading to higher claim rates.

    <strong>3. Health Risk Factors:</strong> Men tend to have higher rates of certain health risk factors, <strong>such as smoking</strong>, alcohol 
    consumption which can increase their likelihood of developing chronic diseases and requiring medical treatment.

    <strong>4. Biological Factors:</strong> Some health conditions, such as cardiovascular disease, may manifest differently in men compared to women, 
    potentially leading to different healthcare utilization patterns and claim rates.""",unsafe_allow_html=True)

def go_analysis_4():
    temp = df.groupby('categorize_age')['claim'].sum().sort_values(ascending=False).reset_index()
    st.dataframe(temp)

    fig = px.bar(temp, x='categorize_age', y='claim', text_auto=True, title='Claim Distribution over Age',color='categorize_age')
    st.plotly_chart(fig)
    st.text("""- Young people that aged between 18 and 29 years claim the most(4.91 Million USD ), while those aged between 51-60 years claim the least(2.44 Million USD)""")

    fig = px.scatter(df,x='age',y='claim',title=' Claim Density over Age',color = 'categorize_age')
    st.plotly_chart(fig)
    st.text("""- The scatter plot reveals that bubbles corresponding to younger age categories exhibit the highest density""")

    st.subheader("""Why do young people takes most number of claims ?""")
    st.text("""By Analysing Data""")
    st.text("""- The significant portion of the young population resides in the south-east region, which is renowned for its elevated total claim amounts.""")

    st.text("(By Google)")
    st.markdown("""
    <strong>1. Healthcare Needs:</strong> Young people may have specific healthcare needs such as accidents, injuries, or illnesses that prompt them to 
    make insurance claims.
    
    <strong>2. Risk-Taking Behavior:</strong> Young individuals might engage in riskier behaviors such as driving fast, participating in extreme sports, 
    or other activities that increase the likelihood of accidents, leading to insurance claims.

    <strong>3. Health Awareness:</strong> Younger generations might be more health-conscious and proactive in seeking medical attention when needed, 
    resulting in more insurance claims for preventive care or early intervention.

    <strong>4. Access to Insurance:</strong> With the Affordable Care Act (ACA), more young adults gained access to health insurance through provisions 
    allowing them to stay on their parents' insurance plans until the age of 26. This expanded coverage could contribute to higher claim rates among young people.

    <strong>5. Occupational Hazards:</strong> Some young adults may work in industries or occupations with higher risks of injury, such as construction or 
    hospitality, leading to more insurance claims.

    <strong>6. Mental Health Concerns:</strong> Young people may also experience mental health issues such as anxiety and depression, leading to therapy 
    or counseling sessions covered by insurance.""",unsafe_allow_html=True)


def  go_analysis_5():
    st.text(""" 
    1. More Females have diabetes than Males
    2. 50.31 % of females are diabetic while 49.69 % of male are diabetic""")

    temp2 = pd.crosstab(df['diabetic'], df['gender'])

    temp = (pd.crosstab(df['diabetic'], df['gender'], normalize='index') * 100).round(2)
    st.dataframe(temp)

    fig = px.bar(temp2, x=temp.index, y=temp.columns, text_auto=True, title='Diabetic population vs gender',barmode='stack')
    fig.update_layout(bargap=0.5)
    st.plotly_chart(fig)

    st.text("""- Individuals without diabetes claim a higher total amount of insurance(9.32 M USD) compared to individuals with diabetes, who claim 8.43 M USD""")
    temp = df.groupby('diabetic')['claim'].sum().reset_index()
    fig = px.bar(temp, y='claim', x='diabetic', text_auto=True, title='Claim Amount Vs Diabetic', color='diabetic')
    fig.update_layout(bargap=0.5)
    st.plotly_chart(fig)

    st.subheader('Why does non-diabetic people claims more than the diabetic ?')
    st.text('(By Analysing Data)')

    st.markdown("""
    1. Given that non-diabetic individuals claim the most compared to others, it's notable that within the non-diabetic category, the highest 
    claim rates are among the <strong>young demographic</strong>. This aligns with our previous findings indicating that <strong>younger individuals tend to make the 
    highest number of insurance claims</strong>. Additionally, it's worth noting that a significant portion of the young population resides in the 
    <strong>Southeast region</strong>, which is renowned for its elevated total claim amounts.""",unsafe_allow_html= True)

    temp = df.groupby(['categorize_age', 'diabetic', 'region'])['claim'].count().sort_values(ascending=False).reset_index().rename(columns={'claim': 'count'})
    st.dataframe(temp)

    fig = px.bar(temp, x='diabetic', y='count', color='categorize_age', facet_col='region',title='Diabetic vs Number of Claims based on age over different region')
    st.plotly_chart(fig)





























st.subheader(""" 1. We can conduct an analysis to determine the geographical region whose residents file the highest volume of insurance claims, and delve into the underlying factors that drive this prevailing trend""")
btn =  st.button('Get Analysis', key='go_button_1')
if btn:
    go_analysis_1()

st.divider()

st.subheader("""2. After Analysing it is found that in south-east and south-west regions, there is a higher proportion of females compared to other regions""")
btn = st.button('Get Analysis', key='go_button_2')
if btn:
    go_analysis_2()

st.divider()

st.subheader("""3. We'll analyze whether males or females file the majority of insurance claims and delve into the reasons behind this phenomenon""")
btn = st.button('Get Analysis', key='go_button_3')
if btn:
    go_analysis_3()

st.divider()

st.subheader("""4. We will explore the relationship between the number of insurance claims and age, identifying the age groups that most frequently submit claims and examining the corresponding claim amounts""")
btn = st.button('Get Analysis', key = 'go_button_4')
if btn:
    go_analysis_4()

st.divider()

st.subheader("""5. We will investigate whether individuals with diabetes or without diabetes file the highest number of insurance claims, and delve into the underlying factors contributing to this trend""")
btn = st.button('Get Analysis', key = 'go_button_5')
if btn:
    go_analysis_5()