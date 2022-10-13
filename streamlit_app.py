import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image

st.set_page_config(layout="wide")

image = Image.open('listrik.jpg')
st.image(image, caption='Saluran Transmisi Tegangan Tinggi 500KV')

st.title('Ketimpangan Listrik, Ketimpangan Kesejahteraan?')

string1 = '''
         Dalam kehidupan modern, energi listrik merupakan bentuk energi yang paling mudah dibangkitkan, 
         didistribusikan, dan digunakan, baik oleh sektor rumah tangga, komersial maupun industri. Karena energi 
         listrik telah menjadi bagian tidak terpisahkan dari kehidupan manusia masa kini dan dimanfaatkan pada setiap
         lini kehidupan, energi listrik digunakan menjadi penanda tingkat kesejahteraan atau kemakmuran suatu 
         masyarakat. 
         
         Artikel ini mencoba melihat bagaimana perbandingan pemakaian listrik di Indonesia dan di 
         negara-negara ASEAN lain dan melihat sejauh apa korelasinya dengan kesejahteraan masyarakat di 
         masing-masing negara.
         '''
st.write(string1)

ASEANElecGen_df = pd.read_csv('ASEANElecGen.csv',sep=';')
ASEANElecGen_df = ASEANElecGen_df[ASEANElecGen_df['Year']>=2000]
ASEANElecGen_df = ASEANElecGen_df[ASEANElecGen_df['Year']<=2020].reset_index()

ASEANElecGenPerCapita_df = pd.read_csv('ASEANElecGenPerCapita.csv',sep=';')
ASEANElecGenPerCapita_df = ASEANElecGenPerCapita_df[ASEANElecGenPerCapita_df['Year']>=2000]
ASEANElecGenPerCapita_df = ASEANElecGenPerCapita_df[ASEANElecGenPerCapita_df['Year']<=2020].reset_index()

ASEANElecGen_df['Population'] = ASEANElecGen_df['Electricity generation (TWh)']*1000000000 / ASEANElecGenPerCapita_df['Per capita electricity (kWh)']
ASEANElecGen_df['Per capita electricity (kWh)'] = ASEANElecGenPerCapita_df['Per capita electricity (kWh)']
ASEANElecGen_df = ASEANElecGen_df.astype({'Population':'int64','Per capita electricity (kWh)':'int64'})

st.subheader('Perbandingan Pemakaian Listrik Indonesia dengan Negara ASEAN lain')

col1, col2 = st.columns([2,1])

with col1:
    st.subheader('')
    st.subheader('')
    c = alt.Chart(ASEANElecGen_df).mark_line().encode(
        x='Year', y='Electricity generation (TWh)', color='Country')
    st.altair_chart(c, use_container_width=True)

with col2:
    tahun = st.slider('Tahun', 2000, 2020, 2020)
    c = alt.Chart(ASEANElecGen_df[ASEANElecGen_df['Year']==tahun]).mark_bar().encode(
       alt.X('Country', sort='-y'), 
       alt.Y('Electricity generation (TWh)'),color='Country')
    st.altair_chart(c, use_container_width=True)

c = alt.Chart(ASEANElecGen_df).mark_line(color='blue').encode(
    x='Year', y='Electricity generation (TWh)', color='Country')
st.altair_chart(c, use_container_width=True)

string2 = '''
        Dari data pemakaian listrik di tingkat agregat / negara, dapat dilihat bahwa Indonesia adalah pengguna 
        listrik terbesar di wilayah Asia Tenggara (ASEAN) dari tahun ke tahun, terutama sejak tahun 2008. 
        
        Namun, tidaklah tepat jika kita hanya melihat dari besarnya pemakaian agregat satu negara, karena besarnya 
        populasi di tiap negara yang berbeda.
        '''
st.write(string2)

st.subheader('Populasi Penduduk Negara ASEAN')

col1, col2, col3 = st.columns([1,3,1])

with col2:
    c = alt.Chart(ASEANElecGen_df).mark_line().encode(
        x='Year', y='Population', color='Country')
    st.altair_chart(c, use_container_width=True)



string3 = '''
         Pada tampilan chart di atas, terlihat jelas bahwa jumlah penduduk masing-masing negara berbeda dan terdapat 
         perbedaan yang cukup besar antara Indonesia dan negara ASEAN lainnya. 
         
         Untuk itu, akan lebih tepat jika yang diperbandingkan adalah pemakaian listrik per kapita di masing-masing
         negara ASEAN. 
         '''
st.write(string3)

st.subheader('Perbandingan Pemakaian Listrik Per Kapita Indonesia dengan Negara ASEAN lain')

c = alt.Chart(ASEANElecGen_df).mark_line().encode(
    x='Year', y='Per capita electricity (kWh)', color='Country')

st.altair_chart(c, use_container_width=True)

string3 = '''
         Jika pada chart pertama terlihat bahwa pemakaian listrik Indonesia adalah yang terbesar, di chart ini 
         terlihat bahwa secara per kapita, penggunaan listrik terbesar adalah oleh masyarakat Brunei dan Singapura.
         Kedua negara kecil yang dari perspektif agregat pemakaian listrik tidak begitu signifikan, ternyata dari
         sisi per kapita merupakan konsumen listrik yang masif.
         
         Untuk membantu memperjelas grafik di atas, disajikan pemakaian listrik per kapita pada tahun 
         2020 di negara-negara ASEAN dalam bentuk Bar Chart di bawah ini:
         
         '''
st.write(string3)

tahun1 = st.slider('Tahun', 2000, 2020, 2020, key='123')
ASEAN2000_df = pd.DataFrame()
## ASEAN2000_df = ASEANElecGen_df[ASEANElecGen_df['Year']==2020].sort_values(by='Per capita electricity (kWh)',ascending=False)[['Entity','Per capita electricity (kWh)']].reset_index()
#ASEAN2000_df['Country'] = ASEANElecGen_df[ASEANElecGen_df['Year']==2020].sort_values(by='Per capita electricity (kWh)',ascending=False)['Country']
ASEAN2000_df[['Country','Per capita electricity (kWh)']] = ASEANElecGen_df[ASEANElecGen_df['Year']==tahun1].sort_values(by='Per capita electricity (kWh)',ascending=False)[['Country','Per capita electricity (kWh)']]

#c = alt.Chart(ASEAN2000_df).mark_Sbar().encode(
#       alt.X('Country', sort='-y'), 
#       alt.Y('Per capita electricity (kWh)'),
#       color='Country')
#st.altair_chart(c, use_container_width=True)

domain = ['Indonesia','Malaysia','Singapore','Laos','Thailand','Vietnam','Philippines', 'Cambodia','Myanmar','Brunei']
range_ = ['#1CD9EF','#969696','#969696','#969696','#969696','#969696','#969696','#969696','#969696','#969696']
#range_ = ['#F44336', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray']

c = alt.Chart(ASEAN2000_df).mark_bar().encode(
        alt.X('Country', sort='-y'), 
        alt.Y('Per capita electricity (kWh)'),
        color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
st.altair_chart(c, use_container_width=True)

string4 = '''
         Dari tahun ke tahun, terlihat jelas bahwa Brunei dan Singapura meninggalkan mayoritas negara ASEAN dalam 
         hal pemakaian listrik per kapita, dengan pemakaian berkisar 9,000 - 10.000 kWh per kapita per tahun.
         
         Kemudian Malaysia dan Laos menyusul dengan pemakaian berkisar 4.000 - 5.000 kWh per kapita per tahun. 
         Selanjutnya adalah Thailand dan Vietnam dengan pemakaian listrik per kapita per tahun berkisar 2.000 kWH. 
         
         Vietnam dan Laos awalnya memiliki pemakaian listrik per kapita per tahun yang setara dengan Indonesia.
         Tetapi di mulai tahun 2007, Vietnam meninggalkan Indonesia. Di tahun 2010, Laos meninggalkan Indonesia
         dan bahkan meninggalkan Vietnam. 
         
         Sangat nampak bahwa Indonesia jauh tertinggal dibanding tetangga-tetangga yang lebih makmur. Nampak bahwa
         Pemakaian listrik per kapita di Singapura dan di Brunei sekitar sembilan kali lipat pemakaian per kapita 
         di Indonesia, yang hanya sekitar 1000 kWH. 
         
         Indonesia hanya lebih tinggi dibandingkan Myanmar, Kamboja dan Philipina. 
         '''
st.write(string4)
