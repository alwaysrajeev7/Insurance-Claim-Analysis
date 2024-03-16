import pandas as pd
import plotly.express as px
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
st.download_button(label='Get Data',data =df.to_csv(),file_name='insurance.csv')
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

df.dropna(inplace= True)
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
  st.text("""- Typically, individuals from the south-east region make the highest 
  number of insurance claims(total 5.78 M USD), and they also tend to 
  claim larger amounts as comparsion to the others.
- After south-east, individuals from the north-west region make the 
  highest number of claims(total 4.06 M USD) from insurance companies.""")

  col1 ,col2 = st.columns(2)
  with col1:
    fig = px.pie(temp, values='claim_amount', names='region', hover_name='region', hole=0.5,title=' Region Contribution in Total Claim Amount')
    st.plotly_chart(fig)
    st.text("""- Out of the total claim amount 32.6% amount only goes to south-east region.""")

  with col2:
    temp2 = df[df['categorize_claim'] == 'higher']['region'].value_counts().reset_index()
    fig = px.pie(temp2, values='count',names='region',hover_name = 'region',hole = 0.5,title ='Region contribution in Higher Claim Amounts ')
    st.plotly_chart(fig)
    st.text("""- Out of the total higher claim amount 33.6% amount only goes to south-east 
  region.""")

  col1,col2 = st.columns(2)
  with col1:
    fig = px.scatter(df, y='region', x='claim', color='region', hover_name='claim',title='Number of Claims Over Different Regions')
    st.plotly_chart(fig)
    st.text("""- The density of scatter bubbles is higher in the Southeast region.""")

  with col2:
    temp = df.groupby('region')['claim'].count().reset_index().rename(columns={'claim': 'count'})
    fig = px.pie(temp, values='count', names='region', hover_name='region', hole=0.5, title='Region Contribution in Total Number of Claims')
    st.plotly_chart(fig)
    st.text("""- Out of the total number of claims 33.2% claims only goes to people of south-east 
  region """)

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
1. South-east region have the highest number of insurance claims, often for significant amounts as from previous analysis.
2. Maybe there is a possibility that female population claims the most. Is it ?
3. The answer is No""")

def go_analysis_3():
    st.text("""1. Males apply for insurance amounts more frequently compared to females.
2. Of the total claims, 50.3% were made by males, while 49.7% were made by females.
3. Not a huge difference.""")

    temp = df.groupby('gender')['claim'].count().reset_index().rename(columns={'claim':'claim_count'})
    st.dataframe(temp)
    fig = px.pie(temp, values='claim_count',names='gender',hover_name = 'gender',hole = 0.5,title='Claim Distribution over Gender',color_discrete_map={'male':'red','female':'green'} )
    st.plotly_chart(fig)

    fig  = px.box(df, y='claim', color='gender',title='Claim Distribution over Gender', color_discrete_map={'male':'red','female':'green'} )
    st.plotly_chart(fig)
    st.text("""- A wider box (i.e males) indicate a higher density of data points within that range.""")

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
    fig.update_layout(xaxis = dict(title = 'age category'))
    st.plotly_chart(fig)
    st.text("""- Young people that aged between 18 and 29 years claim the most(4.91 Million USD ), while those aged between 51-60 years claim the least(2.44 Million USD)""")

    fig = px.scatter(df,x='age',y='claim',title=' Claim Density over Age',color = 'categorize_age')
    st.plotly_chart(fig)
    st.text("""- The scatter plot reveals that bubbles corresponding to younger age categories exhibit the highest density""")

    st.subheader("""Why do young people takes most number of claims ?""")
    st.text("""(By Analysing Data)""")
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
    2. 50.71 % of females are diabetic while 49.29 % of male are diabetic""")

    temp2 = pd.crosstab(df['diabetic'], df['gender'])

    temp = (pd.crosstab(df['diabetic'], df['gender'], normalize='index') * 100).round(2)
    st.dataframe(temp)

    fig = px.bar(temp2, x=temp.index, y=temp.columns, text_auto=True, title='Diabetic population vs gender',barmode='stack',color_discrete_map= {'female':'#FD8A8A', 'male':'#F1F7B5'})
    fig.update_layout(bargap=0.5)
    st.plotly_chart(fig)

    st.text("""- Individuals without diabetes claim a higher total amount of insurance(9.31 M USD) compared to individuals with diabetes, who claim 8.43 M USD""")
    temp = df.groupby('diabetic')['claim'].sum().reset_index()
    fig = px.bar(temp, y='claim', x='diabetic', text_auto=True, title='Claim Amount Vs Diabetic', color='diabetic',color_discrete_map= {'No':'#FAEDCB','Yes':'#C6DEF1'})
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

def go_analysis_6():

   st.write("- Let's explore this relationship through exploratory data analysis (EDA)")
   st.text("- There is a no significant realtionship that people who are diabetic also have Elevated or High blood-pressure levels.")
   temp = df.groupby(['diabetic', 'categorize_bp'])['claim'].count().sort_values(ascending=False).reset_index().rename(columns={'claim': 'count'})
   st.dataframe(temp)

   st.text("""- Normal blood pressure + Non-diabetic : claims -> (8.09 M USD)
- Normal blood pressure + Diabetic : claims -> (7.04 M USD) then comes the rest. """)

   temp = df.groupby(['diabetic','categorize_bp'])['claim'].sum().sort_values(ascending = False).reset_index()
   st.dataframe(temp)

def go_analysis_7():

    st.write("- Let's explore this relationship through exploratory data analysis (EDA)")
    st.text(""" - Generally, individuals with no children claim the highest amount (7.09 million USD), then
- 1 child (4.12 M USD)
- 2 children (3.61 M USD)
- 3 children (2.14 M USD)
- 4 children (346.26k USD)
- 5 children (158.14k USD) """)

    temp = df.groupby('children')['claim'].sum().sort_values(ascending=False).reset_index().round(2)
    fig = px.bar(temp, x='children', y='claim', title='Claim Amount vs. Number of Children', text_auto=True, color='children',color_continuous_scale='Viridis')
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig)

    st.markdown("**What factors contribute to this relationship?**")
    st.text("(By Analysing Data)")
    st.text("The majority of individuals having 0, 1, 2, or 3 children are from the Southeast region, where claim rates are known to be highest")

    temp = (pd.crosstab(df['children'], df['region'], normalize='index') * 100).round(2)
    st.dataframe(temp)

    st.text("""
- 32.57% of people that have 0 child belongs to south-east.
- 35.19% of people that have 1 child belongs to south-east.
- 33.33% of people that have 2 child belongs to south-east.
- 31.21% of people that have 3 child belongs to south-east.
    
    """)
    fig = px.imshow(temp, color_continuous_scale='Viridis', text_auto=True)
    fig.update_layout(xaxis=dict(title='region'), yaxis=dict(title='chilren'))
    st.plotly_chart(fig)

    st.text("(By Google)")
    st.markdown("""
    **1. Healthcare Needs and Utilization:** Individuals or couples without children may have higher healthcare needs and utilization due to factors such as 
    aging, pre-existing health conditions, or lifestyle choices. They may be more likely to seek medical care and treatment for themselves, leading to higher health 
    insurance claims.

    **2. Age and Health Status:** As mentioned earlier, individuals without children may be older on average, and older age is associated with higher healthcare
     needs and utilization. Older individuals are more likely to have chronic health conditions and require medical treatment, resulting in higher healthcare costs.
    """)

def go_analysis_8():

    st.write("- Let's explore this relationship through exploratory data analysis (EDA)")
    st.text("""- The total amount claimed by non-smokers(8.96 M USD) is generally greater than that claimed by smokers(8.78 M USD).)
- The amount gap is not of concern as there is no such huge gap.""")

    temp= df.groupby('smoker')['claim'].sum().reset_index().rename(columns={'claim':'claim_amount'})
    fig = px.bar(temp, x ='smoker',y='claim_amount',title ='Claim Amount Vs Smoker' ,text_auto = True,color='smoker',color_discrete_map= {'No':'#FD8A8A','Yes':'#F1F7B5'})
    fig.update_layout(bargap = 0.5)
    st.plotly_chart(fig)

    st.text("- More Male smoker population(58.03%) as comparsion to Female smoker(41.97%).")
    temp = (pd.crosstab(df['smoker'], df['gender'], normalize='index') * 100).round(2)
    st.dataframe(temp)

    st.divider()
    st.markdown("From this we can conclude that **Male non-smoker and Female smoker** claim the lowest.")
    temp = df.groupby(['smoker', 'gender'])['claim'].sum().sort_values(ascending=False).reset_index()
    st.dataframe(temp)
    st.text("""Specifically:
- Male smokers claim the highest amount, totaling 5.25 million USD.
- Female smokers claim the lowest amount, totaling 3.52 million USD.
- Male non-smokers follow, with a total claim amount of 4.17 million USD.
- Female non-smokers come next, with a total claim amount of 4.79 million USD.""")


def go_analysis_9():
    st.text("""- In terms of insurance claims, individuals classified as obese present the highest total, amounting to 10.98M USD.
- Overweight individuals : 4.27M USD.
- Normal-weight individuals : 2.3M USD.
- Underweight individuals : 177k USD.""")

    temp = df.groupby('categorize_bmi')['claim'].sum().sort_values(ascending=False).reset_index().rename(columns={'categorize_bmi': 'category'})
    fig = px.bar(temp,x='category', y='claim',text_auto = True,title ='Claim Amount vs BMI Classification',color='category')
    fig.update_layout(bargap = 0.2)
    st.plotly_chart(fig)

    col1,col2 = st.columns(2)
    with col1:
       fig = px.scatter(df,x='bmi',y='claim',title=' Claim Amount vs BMI', color='categorize_bmi',hover_name ='claim')
       st.plotly_chart(fig)

    with col2:
       fig = px.scatter(df,x='bmi',y='claim',title=' Claim Amount Count vs BMI',facet_col= 'categorize_bmi',hover_name ='claim')
       st.plotly_chart(fig)

    st.markdown(""" - The density of scatter plot bubbles indicates that not only do **obese individuals tend to file more insurance claims in terms of quantity**,
but they also **claim higher amounts compared to others.**""")

def go_analysis_10():

    st.text("""- Generally, individuals with normal blood pressure (less than 120) tend to make more number of insurance claims (21x) as compared to those under 
elevated and hyper-tension blood pressure category.""")
    temp = df.groupby('categorize_bp')['claim'].count().reset_index().rename(columns={'claim': 'count'})
    st.dataframe(temp)

    st.text("- Out of the total number of insurance claims 95.6% goes to people with normal blood pressure.")
    fig = px.pie(temp,values='count',labels ='categorize_bp',hover_name = 'categorize_bp',title = 'Claim amount distribution over Blood pressure category')
    st.plotly_chart(fig)

    st.text("- Insurance claims totaling 15.5 M USD are paid to individuals with normal blood pressure.")
    st.text("- Combined Insurance claims totaling 2.23 M USD are paid to individuals with elevated and high blood pressure.")

    temp = df.groupby('categorize_bp')['claim'].sum().reset_index().rename(columns={'claim': 'claim_amount'})
    fig = px.bar(temp,y = 'claim_amount',x ='categorize_bp',color='categorize_bp',text_auto = True,title = 'Claim amount distribution over Blood Pressure category')
    st.plotly_chart(fig)

    st.text("""- However, despite the higher frequency of claims from individuals with normal blood pressure, the individual insurance amount claimed by a single person in 
the hypertension or elevated blood pressure category is greater than that claimed by a single person in the normal blood pressure category.""")

    fig = px.scatter(df, x='claim',y = 'bloodpressure',color='categorize_bp',hover_name = 'claim',title ='Blood pressure category vs Claim amount')
    fig.update_layout(width=1000, height=500)
    st.plotly_chart(fig)

def go_analysis_11():

    st.text("(It is strange but after Analysing Data)")

    st.markdown("""**1. Normal Blood Pressure** : In cases of obesity and overweight, the majority of individuals fall under the Normal blood pressure category,
which also coincides with our observation that individuals in the **normal blood pressure category tend to make the most claims.**""")
    temp = (pd.crosstab(df['categorize_bmi'],df['categorize_bp'],normalize = 'index')*100).round(2)
    st.dataframe(temp)

    st.markdown("""**2. Non-Diabetic:** In cases of obesity and overweight, the majority of individuals fall under the Non-Diabetic category, which also  coincides 
with our observation that individuals with **no diabetes tend to make the most claims.**""")
    temp = (pd.crosstab(df['categorize_bmi'],df['diabetic'],normalize = 'index')*100).round(2)
    st.dataframe(temp)

    st.markdown("""**3. Young Individuals:** In cases of obesity and overweight, the majority of individuals fall under the Young category, which also coincides 
with our observation that **young individuals tend to make the most claims.**""")
    temp = (pd.crosstab(df['categorize_bmi'],df['categorize_age'],normalize = 'index')*100).round(2)
    st.dataframe(temp)

    st.markdown("""**4. Non-Smoker:** In cases of obesity and overweight, the majority of individuals fall under the Non-Smoking category, which also coincides 
with our observation that **non-smokers tend to make the most claims.**""")
    temp = (pd.crosstab(df['categorize_bmi'], df['smoker'], normalize='index')*100).round(2)
    st.dataframe(temp)

def go_analysis_12():

    st.text("- We have a significantly higher proportion of young males, at a ratio of 2.38 times compared to young females.")
    temp = pd.crosstab(df['gender'], df['categorize_age'])
    st.dataframe(temp)

    st.text("""- Additionally, from previous analysis, we've discovered that young individuals make the most claims, and now among them, males submit the 
highest number of claims.""")
    temp = df[df['categorize_age'] == 'young']
    fig = px.scatter(temp,x='age',y='claim',color='gender',title = 'Claim distribution among Young individuals by gender',color_discrete_map= {'male':'blue','female':'red'})
    st.plotly_chart(fig)

def  go_categorical_univariate_analysis():

     st.subheader("1. gender")
     st.text("""- Male -> 50.3 % and Female -> 49.7%
- Not a huge gap is shown between male/female population.
- No missing values""")
     temp = df['gender'].value_counts().reset_index().rename(columns={'count': 'population'})

     col1,col2 = st.columns(2)
     with col1:
       fig = px.pie(temp,values='population',names='gender',hole = 0.5,title='Gender Contribution in Total Population',hover_name = 'gender',
                    color='gender',color_discrete_map= {'male':'#FAD1FA','female':'#BDB2FF'})
       st.plotly_chart(fig)

     with col2:
       fig = px.bar(temp, x='gender', y='population', title='Population vs Gender Analysis',text_auto=True,color= 'gender',
                    color_discrete_map= {'male':'#FAD1FA','female':'#BDB2FF'} )
       fig.update_layout(xaxis=dict(title='Gender'), yaxis=dict(title='Population'), bargap=0.6)
       st.plotly_chart(fig)

     st.divider()

     st.subheader("2. diabetic")
     st.text("""- Diabetic -> 47.8% 
- Non-Diabetic ->52.2%
- No missig values""")
     temp = df['diabetic'].value_counts().reset_index()

     col1,col2 = st.columns(2)
     with col1:

       fig = px.pie(temp,values='count',names='diabetic',hole = 0.5,title='Diabetic vs Non-diabetic in Total Population',hover_name = 'diabetic',
                    color='diabetic',color_discrete_map= {'No':'#FD8A8A','Yes':'#F1F7B5'})
       st.plotly_chart(fig)

     with col2:
      fig = px.bar(temp, x='diabetic', y='count', color='diabetic', title='Diabetic vs Non-diabetic Population',text_auto=True, color_discrete_map= {'No':'#FD8A8A','Yes':'#F1F7B5'})
      fig.update_layout(xaxis=dict(title='Diabetic'), yaxis=dict(title='Population'), bargap=0.6)
      st.plotly_chart(fig)

     st.divider()

     st.subheader("3. children")
     st.text("""How many chilren
-> 0 -> 42.6%
-> 1 -> 24.3%
-> 2 -> 18.0%
-> 3 -> 11.8%
-> 4 -> 1.88%
-> 5 -> 1.35%
- No missing values""")

     temp = df['children'].value_counts().reset_index()

     col1,col2 = st.columns(2)
     with col1:
       fig = px.pie(temp,values='count',names='children',hole = 0.5,title= 'Distribution of the population based on the number of children they have',
                      color='children', hover_name = 'children')
       st.plotly_chart(fig)

     with col2:
       fig = px.bar(temp, x='children', y='count', color='children',title='Population Distribution by Number of Children', text_auto=True, color_continuous_scale= 'Viridis')
       fig.update_layout(xaxis=dict(title=' No. of Children'), yaxis=dict(title='Count'))
       st.plotly_chart(fig)

     st.divider()

     st.subheader("4. smoker")
     st.text("""- 20.6 % -> Smoker
- 79.4 % -> Non Smoker
- No missing values.""")

     temp = df['smoker'].value_counts().reset_index()
     st.dataframe(temp)

     col1,col2 = st.columns(2)

     with col1:
         fig = px.pie(temp, values='count', names='smoker', hole=0.5, title='Smoker Population Distribution',hover_name='smoker',
                      color='smoker', color_discrete_map={'No':'blue','Yes':'red'})
         st.plotly_chart(fig)

     with col2:
         fig = px.bar(temp, x='smoker', y='count', color='smoker', title='Smoker Population Distribution',text_auto=True,color_discrete_map={'No':'blue','Yes':'red'})
         fig.update_layout(xaxis=dict(title=' smoker'), yaxis=dict(title='Count'), bargap=0.6)
         st.plotly_chart(fig)

     st.divider()

     st.subheader("5. region")
     st.text("""- The majority of population come from the Southeast, followed by the Northwest, Southwest, and then Northeast.
- No missing values.""")

     col1,col2 = st.columns(2)
     with col1:
       temp = df['region'].value_counts().reset_index()
       fig = px.pie(temp,values='count',names='region',hole = 0.5,title='Population Distribution by Region',hover_name = 'region')
       st.plotly_chart(fig)

     with col2:
         fig = px.bar(temp, x='region', y='count', color='region', title='Population Distribution by Region',text_auto=True)
         fig.update_layout(xaxis=dict(title='Region'), yaxis=dict(title='Count'))
         st.plotly_chart(fig)

     st.divider()

     st.subheader("6. categorize_bmi")
     st.text("""- 52.7 % are under obsesity
- 29.1 % are under over-weight
- 16.7 % are under normal-weight
- 1.5 % are under under-weight""")

     temp = df['categorize_bmi'].value_counts().sort_values(ascending=False).reset_index()#.rename(columns={'index': 'category', 'categorize_bmi': 'bmi'})
     st.dataframe(temp)
     fig = px.pie(temp, values='count', names='categorize_bmi', hover_name='categorize_bmi', hole=0.5,title='Population distribution in BMI Categories')
     st.plotly_chart(fig)


def  go_numerical_univariate_analysis():
     st.subheader("1. age")
     st.text("""- min. age -> 18 yr
- mean age -> 38 yr
- max. age -> 60 yr
- No skewness
- Bi-modal Distribution
- No missing values""")
     st.dataframe(df['age'].describe())

     col1,col2 = st.columns(2)
     with col1:
       st.markdown('**- Mostly people are from age 26-49yr**')
       fig = px.histogram(df,x='age',nbins=40,text_auto = True)
       st.plotly_chart(fig)


     with col2:
       st.markdown('**- No outliers**')
       fig = px.box(df, x='age', color_discrete_sequence=['green'])
       st.plotly_chart(fig)


     temp = df['categorize_age'].value_counts().reset_index()
     st.dataframe(temp)
     col1,col2 = st.columns(2)

     with col1:
       fig = px.pie(temp, values='count', names='categorize_age', hover_name='categorize_age', hole=0.5, color = 'categorize_age',
                    color_discrete_map={'young': '#ff0303', "30's-35's": '#8400ff', "46's-50's": '#00fff6',
                                        "41's-45's": '#0028ff', "36's-40's": '#00ff28', "56's-60's": '#f1802d',
                                        "51's-55's": '#549aab'}, title='Population distribution in Age Categories')
       st.plotly_chart(fig)
       st.markdown("**- Majority of population is of Young people**")

     with col2:
         fig = px.histogram(df, x='age', text_auto=True, color='categorize_age', title = 'Age category density',
                            color_discrete_map={'young': '#ff0303', "30's-35's": '#8400ff', "46's-50's": '#00fff6',
                                                "41's-45's": '#0028ff', "36's-40's": '#00ff28', "56's-60's": '#f1802d',
                                                "51's-55's": '#549aab'})
         st.plotly_chart(fig)


     st.divider()


     st.subheader("2. bmi")
     st.text("""- avg. bmi - 30.65
- min. bmi - 16
- Normal Distribution
- No skewness
- No missing values """)
     st.dataframe(df['bmi'].describe())

     st.markdown("**- Mostly people have bmi from 25.5 - 33.5**")
     fig = px.histogram(df, x='bmi', nbins=40, text_auto=True,height=500,width=1000)
     st.plotly_chart(fig)

     st.markdown("**- Outliers**")
     fig = px.box(df,x='bmi',color_discrete_sequence = ['green'])
     st.plotly_chart(fig)

     st.markdown("**- Outliers are there but they are valid**")
     st.dataframe(df[df['bmi']>=47.7])

     temp = df['categorize_bmi'].value_counts().sort_values(ascending=False).reset_index()

     col1,col2 = st.columns(2)

     with col1:
       fig = px.pie(temp, values='count', names='categorize_bmi', hover_name='categorize_bmi', hole=0.5, color = 'categorize_bmi',
                    title='Population distribution in BMI Categories',color_discrete_map={'obesity': '#e9724d', 'normal-weight': '#d6d727', 'overweight': '#92cad1',
                                        'under-weight': '#79ccb3'} )
       st.plotly_chart(fig)

       st.text("""- 52.7 % are under obsesity
- 29.1 % are under over-weight
- 16.7 % are under normal-weight
- 1.5 % are under under-weight""")


     with col2:
         fig = px.histogram(df, x='bmi', text_auto=True, color='categorize_bmi', title = 'BMI category density',
                            color_discrete_map= {'obesity':'#e9724d', 'normal-weight':'#d6d727','overweight':'#92cad1','under-weight':'#79ccb3'})
         st.plotly_chart(fig)

     st.divider()

     st.subheader("3. bloodpressure")
     st.text(""" - postively skewed
- no missing values """)

     st.dataframe(df['bloodpressure'].describe())

     st.markdown('**- mostly people have bloodpressure from 80-101**')
     fig = px.histogram(df,x='bloodpressure',nbins = 40,text_auto = True,height=500,width=1000)
     st.plotly_chart(fig)

     st.markdown('**- Outliers**')
     st.plotly_chart(px.box(df,x='bloodpressure'))

     st.markdown("**- Outliers are there but they are valid**")
     st.dataframe(df[df['bloodpressure']>=119])

     col1,col2 = st.columns(2)
     with col1:
       temp = df['categorize_bp'].value_counts().reset_index()
       fig = px.pie(temp, values='count', names='categorize_bp', hover_name='categorize_bp', hole=0.5,title='Population distribution in Blood Pressure Categories')
       st.plotly_chart(fig)
       st.text("""- 95.6 % of population is in Normal Blood Pressure Category
- 2.25 % of population is in Elevated Blood Pressure Category
- 2.18 % of population is in Hypertension Blood Pressure Category""")

     with col2:
         fig = px.histogram(df, x='bloodpressure', color='categorize_bp', text_auto=True,title = 'Bloodpressure category density')
         st.plotly_chart(fig)

     st.divider()

     st.subheader("4. claim")
     st.text("""- avg. claim : 13325
- No missing values""")

     st.dataframe(df['claim'].describe())

     st.markdown('**- Highest claim is from someone of southeast region**')
     st.markdown('**- We also knew that people from southeast region claims the most times**')
     st.dataframe(df[df['claim'] == df['claim'].max()])

     st.markdown('**- Lowest claim is from someone of southeast region**')
     st.dataframe(df[df['claim'] == df['claim'].min()])

     st.markdown('**- Majority of claims are from 0-14k**')
     st.plotly_chart(px.histogram(df, x='claim',nbins = 50,text_auto = True))

     st.markdown('**Outliers**')
     st.plotly_chart(px.box(df,x='claim'))

     st.markdown('**- Outliers are there but they are valid**')
     st.dataframe(df[df['claim']>=35000])

     temp = df['categorize_claim'].value_counts().reset_index()
     col1,col2 = st.columns(2)

     with col1:
         fig = px.pie(temp, values='count', names='categorize_claim', hole=0.5, title='Claim category distribution',color = 'categorize_claim',
                      color_discrete_map= {'mid':'red','lower':'green','higher':'yellow'})
         st.plotly_chart(fig)

     with col2:
         fig = px.histogram(df, x='claim', color='categorize_claim', text_auto=True,title='Claim category density ',
                            color_discrete_map= {'mid':'red','lower':'green','higher':'yellow'})
         st.plotly_chart(fig)









st.subheader(""" 1. We can conduct an analysis to determine the geographical region whose residents file the highest volume of insurance claims, and delve into the underlying factors that drive this prevailing trend""")
btn =  st.button('Get Analysis', key='go_button_1')
if btn:
    st.balloons()
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
st.divider()


st.subheader("6. Is there a correlation between blood pressure levels, diabetes, and insurance claims?")
btn = st.button('Get Analysis',key = 'go_button_6')
if btn:
    go_analysis_6()
st.divider()


st.subheader("7. Is there a relationship between the number of children individuals have and the amount of insurance claims they file? ")
btn = st.button('Get Analysis',key = 'go_button_7')
if btn:
    go_analysis_7()
st.divider()


st.subheader("8. We can analyze whether smokers or non-smokers make the most insurance claims and investigate the reasons behind it.")
btn = st.button('Get Analysis',key = 'go_button_8')
if btn:
    go_analysis_8()
st.divider()


st.subheader("9. We can analyze is there any relationship b/w individuals with higher BMI and insurance claims.")
btn = st.button('Get Analysis',key = 'go_button_9')
if btn:
    go_analysis_9()
st.divider()


st.subheader("10. Is there a correlation between blood pressure levels and insurance claims?")
btn = st.button('Get Analysis',key = 'go_button_10')
if btn:
    go_analysis_10()
st.divider()


st.subheader("11. What are the reasons that why individuals with higher BMI make the most insurance claims?")
btn = st.button('Get Analysis',key = 'go_button_11')
if btn:
    go_analysis_11()
st.divider()

st.subheader("12. Within the group of young people, how does the number of claims vary between males and females ?")
btn = st.button('Get Analysis',key = 'go_button_12')
if btn:
    go_analysis_12()
st.divider()

st.title('Uni-Variate Analysis')

btn1 = st.button('On Categorical Columns',key = 'go_button_13')
if btn1:
    go_categorical_univariate_analysis()

btn2 = st.button('On Numerical Columns',key = 'go_button_14')
if btn2:
    go_numerical_univariate_analysis()



import streamlit as st

# Custom CSS for footer
footer_style = """
    <style>
        .footer {
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            text-decoration: none;
            color: #000000;
        }
        .footer p {
            margin: 0;
            font-size: 14px;
        }
        .footer a {
            display: flex;
            align-items: center;
            text-decoration: none;
            color: #000000;
            margin-bottom: 5px;
        }
        .footer a img {
            margin-right: 5px;
        }
    </style>
"""

# Footer content
footer_content = """
    <div class="footer">
        <p>Made with ❤️ by Rajeev Nayan Tripathi</p>
        <a href="https://www.linkedin.com/in/rajeev-nayan-tripathi-1499581b7/" target="_blank">
            <img src="https://img.icons8.com/color/48/000000/linkedin.png"/>
        </a>
        <a href="mailto:rajeevnayantripathi36@gmail.com" target="_blank">
            <img src="https://img.icons8.com/color/48/000000/gmail--v1.png"/>
        </a>
    </div>
"""

# Display the footer
st.markdown(footer_style, unsafe_allow_html=True)
st.markdown(footer_content, unsafe_allow_html=True)
