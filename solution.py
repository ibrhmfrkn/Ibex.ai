import pyodbc 
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt 
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st 
import seaborn as sns




st.set_page_config(layout='wide')

st.title(""" Ibex.ai Data Analyst Test Solutions""")

Server='capdstest.database.windows.net'
Database='DSTest'
Username='candidate'
Password='P)pE8J%XYVdv)4k_K%8]v@f)'


server = Server
database = Database 
username = Username 
password = Password 

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+'; DATABASE='+database+';UID='+username+';PWD='+ password)

cursor=conn.cursor()

def age_interval(age_dist):

    age_dist=[]

    for i in age_rev_dist['Age']:
         if i <= 19:
            age_dist.append(10)
         elif 19< i <=29:
            age_dist.append(20)
         elif 29<i <= 39:
            age_dist.append(30)
         elif 39< i <= 49:
            age_dist.append(40)
         elif 49<i <=59:
            age_dist.append(50)
         else:
            age_dist.append(60)
        

    age_rev_dist['Age_Dist']=age_dist

    age_dist_2=[]

    for i in age_rev_dist['Age']:
         if i <= 19:
            age_dist_2.append(15)
         elif 19< i <=24:
            age_dist_2.append(20)
         elif 24<i <= 29:
            age_dist_2.append(25)
         elif 29< i <= 34:
            age_dist_2.append(30)
         elif 34<i <=39:
            age_dist_2.append(35)
         elif 39<i <=44:
            age_dist_2.append(40)
         elif 44<i <=49:
            age_dist_2.append(45)
         elif 49<i <=54:
            age_dist_2.append(50)
         elif 54<i <=59:
            age_dist_2.append(55)
         elif 59<i <=64:
            age_dist_2.append(60)
         else:
            age_dist_2.append(65)
      
    age_rev_dist['Age_Dist_2']=age_dist_2

    return age_rev_dist


def chart_query_1(df,x,y):

    fig = px.bar(df, x=x, y=y, text=y,color=y)
    fig.update_traces( textposition='outside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',
                  title_text='Average Revenue For Users By Day of The Week', title_x=0.5)
    fig.add_hline(y=np.mean(df[y]), line_width=0.4,opacity=0.4,line_dash = 'dash', line_color = 'firebrick')

    return st.plotly_chart(fig, use_container_width=False, sharing="streamlit")


def pie_chart(df):
    values=df['Daily Average']
    labels=df.Day

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig.update_layout(
            title={
            'text' :'Average Revenue Percentages For The Users By Day of The Week',
            'x':0.5,
            'xanchor': 'center',},font=dict(size=12,
    ))

    return st.plotly_chart(fig, use_container_width=True)



def chart_query_2(age_rev_dist,x):
    fig = px.histogram(age_rev_dist, x=x, y='Revenue', histfunc='sum',nbins=10,color=x,
           color_discrete_sequence=['seagreen'])

    fig.update_layout(bargap=0.1,title_text='Distribution of Total Revenue Generated By User Age', title_x=0.5)
    fig.update_xaxes(title='Age Group',type='linear', tickfont=dict(size=14),dtick=5,anchor= 'free')
    fig.update_yaxes(title='Revenue')

    return st.plotly_chart(fig, use_container_width=True)

def chart_query_2_1(age_rev_dist,x):

    fig = px.bar(age_rev_dist, x=x, y='Revenue',color=x,
            color_continuous_scale=px.colors.sequential.Turbo_r,title='Distribution of Total Revenue Generated By User Age')
    fig.update_traces( textposition='outside')
    fig.update_layout(uniformtext_minsize=6, uniformtext_mode='hide',
                 title_text='Distribution of Total Revenue Generated By User Age', title_x=0.5)
    return st.plotly_chart(fig, use_container_width=True)



with st.expander('1-) Plot a suitable graph showing the average revenue for users by day of the week'):

    query='''SELECT Day,CAST(ROUND(AVG(Revenue),2) AS DEC(10,2)) AS 'Daily Average' FROM
    (SELECT DATENAME(WEEKDAY, Date) AS Day,Revenue FROM dbo.Activity) AS agg
        GROUP BY Day ORDER BY 'Daily Average' DESC '''

   
    SQL_Query = pd.read_sql_query(query, conn)

    day_of_week= pd.DataFrame(SQL_Query,columns=['Day','Daily Average'])
    a1,a2 = st.columns([1,1])
    with a1:
        chart_query_1(day_of_week,'Day','Daily Average')
    with a2:
        pie_chart(day_of_week)



    if st.button('*Click Here For The Query*'):
        c1,c2 = st.columns([2,1])

        with c1:
             st.code(query, language='sql')
             
        with c2:
            st.write('DataFrame')
            st.dataframe(day_of_week)


with st.expander('2-) Plot a suitable graph showing the distribution of total revenue generated by user age'):
    with st.spinner('Please wait loading...'):
        query=''' SELECT u.UserId,DATEDIFF(year,u.DOB,GETDATE()) AS Age,
        SUM(a.Revenue) AS Revenue FROM  dbo.Users u LEFT JOIN dbo.Activity a ON  
        u.UserId=a.UserId WHERE a.Revenue IS NOT NULL OR a.Revenue !=0
        GROUP BY DATEDIFF(year,u.DOB,GETDATE()),u.UserId '''

        SQL_Query = pd.read_sql_query(query, conn)
        age_rev_dist = pd.DataFrame(SQL_Query)
        age_rev_dist=age_interval(age_rev_dist)
        selected_int=st.selectbox('Age Interval',['Age_Dist_2','Age_Dist'])
        a1,a2 = st.columns([1,1])
        with a1:
            chart_query_2(age_rev_dist,selected_int)
        with a2:
            chart_query_2_1(age_rev_dist,selected_int)

        if st.button('Click Here For The Query'):
            c1,c2 = st.columns([2,1])

            with c1:
                 st.code(query, language='sql')
             
            with c2:
                st.write('DataFrame Preview')
                st.dataframe(age_rev_dist.head(50))
        if st.button('Click For Scatter Plot'):
            fig = px.scatter(age_rev_dist, x="Age", y="Revenue", color=age_rev_dist['Age_Dist_2'].astype(str))
            fig.update_traces(marker_size=10)
            st.plotly_chart(fig, use_container_width=True)
        #if st.button('Click For Box Plot'):
            # fig = px.box(age_rev_dist, x='Age_Dist', y="Revenue")
            #st.plotly_chart(fig, use_container_width=True)



with st.expander("3-) Plot a suitable graph showing the number of revenue-generating users by year-month (e.g. ‘2019-02’ for Feb 2019)"):

    query=''' SELECT COUNT(DISTINCT(UserId)) AS Count,CONCAT(YEAR([Date]), '-', RIGHT(CONCAT('00', MONTH([Date])), 2)) AS Year_Month
        FROM dbo.Activity WHERE Revenue IS NOT NULL OR Revenue !=0
        GROUP BY (CONCAT(YEAR([Date]), '-', RIGHT(CONCAT('00', MONTH([Date])), 2)))
        ORDER BY Year_Month '''


    SQL_Query = pd.read_sql_query(query, conn)

    date_rev = pd.DataFrame(SQL_Query)
    
    fig = px.bar(date_rev, x='Year_Month', y='Count', text='Count',color='Count',
             color_continuous_scale=px.colors.sequential.Bluered)
    fig.update_traces( textposition='outside')
    fig.update_xaxes(title='Date',type='category',tickangle=45)
    fig.update_layout(uniformtext_minsize=6, uniformtext_mode='hide',
                 title_text='The Number of Revenue-Generating Users By Year-Month', title_x=0.5)
    fig.add_hline(y=np.mean(date_rev['Count']), line_width=0.4,opacity=0.4,line_dash = 'dash', line_color = 'firebrick')

    st.plotly_chart(fig, use_container_width=True)
    if st.button('Click For The Query'):
        c1,c2 = st.columns([2,1])

        with c1:
            st.code(query, language='sql')
             
        with c2:
            st.write('DataFrame Preview')
            st.dataframe(date_rev.head(50))
    

with st.expander("4-) Visualise the response rate of each offer. The response rate is the % of communications which  resulted in positive revenue on the day of, or the day after, the communication"):

    query=''' with total_count as ( Select o.Name as Name,count(o.Name) as Total from dbo.Comms c inner join Activity a on
    c.UserId=a.UserId inner join Offers o on c.OfferId=o.OfferId group by o.Name),

    conversion_count as (select o.Name as offer_name,count(o.Name) as Conversion from dbo.Comms c inner join Activity a on
    c.UserId=a.UserId inner join Offers o on c.OfferId=o.OfferId 
    where c.SendDate=a.Date or (DATEADD(dd, 1, SendDate)=A.Date) group by o.Name )


    select Name,Conversion,Total
    from total_count t join conversion_count c on t.Name=c.offer_name '''
    
    SQL_Query = pd.read_sql_query(query, conn)
    response= pd.DataFrame(SQL_Query)
    response['Response Rate']=(100*response.Conversion/response.Total).round(3)
    response.sort_values(by='Response Rate',ascending=False,inplace=True)

    fig = px.bar(response, x='Name', y='Response Rate',color='Conversion',
             color_continuous_scale=px.colors.sequential.Cividis,text='Response Rate')
    fig.update_traces( textposition='inside')
    fig.update_xaxes(title='Name',type='category',tickangle=45)
    fig.update_yaxes(title='Response Rate',tickprefix='%')
    fig.update_layout(uniformtext_minsize=6, uniformtext_mode='hide',
                 title_text='Response Rate of Each Offer', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    with st.spinner('Please wait loading...'):
        if st.button('Click Here For The Query..'):
            c1,c2 = st.columns([2,1])

            with c1:
                st.code(query, language='sql')
             
            with c2:
                st.write('DataFrame Preview')
                st.dataframe(response.head(50))
        if st.button('Click For The Generated Revenue For Each Offer'):
            query_=''' SELECT o.Name , c.UserId,c.SendDate,c.OfferId,a.Date AS 'Revenue Date',a.Revenue 
                FROM dbo.Comms c LEFT JOIN Activity a ON
                c.UserId=a.UserId INNER JOIN Offers o ON c.OfferId=o.OfferId 
                WHERE c.SendDate=a.Date OR (DATEADD(dd, 1, SendDate)=A.Date)'''
    
            SQL_Query = pd.read_sql_query(query_, conn)
            comm_rev_offer = pd.DataFrame(SQL_Query)

            fig = px.bar(comm_rev_offer, x='Name', y='Revenue',color='Name',color_continuous_scale=px.colors.sequential.Bluered)
            fig.update_traces( textposition='outside')
            fig.update_xaxes(title='Date',type='category',tickangle=45)
            fig.update_layout(uniformtext_minsize=6, uniformtext_mode='hide',title_text='Generated Revenue After Each Offer', title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

            c1,c2 = st.columns([2,1])

            with c1:
                st.code(query_, language='sql')
             
            with c2:
                st.write('DataFrame Preview')
                st.dataframe(comm_rev_offer.head(50))


                
                
                
st.markdown('_Source code: _ **_https://github.com/ibrhmfrkn/Ibex.ai_**.')
 

  
