import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")

image = Image.open('listrik.jpg')

st.image(image, caption='Saluran Transmisi Tegangan Tinggi 500KV')



st.title('Ketimpangan Listrik, Ketimpangan Kesejahteraan?')

string1 = '''
         Dalam kehidupan modern, energi listrik merupakan bentuk energi yang paling mudah dibangkitkan, 
         didistribusikan, dan digunakan, baik oleh sektor rumah tangga, komersial maupun industri. Karena energi 
         listrik telah menjadi bagian tidak terpisahkan dari kehidupan manusia masa kini dan dimanfaatkan pada setiap, 
         energi listrik dapat lini kehidupan, energi listrik digunakan menjadi penanda tingkat kemakmuran suatu 
         masyarakat. 
         
         Bagian awal artikel ini mencoba melihat bagaimana perbandingan pemakaian listrik di Indonesia dan di 
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

import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

st.subheader('Perbandingan Pemakaian Listrik Indonesia dengan Negara ASEAN lain')

col1, col2 = st.columns([3,1])

with col1:
    c = alt.Chart(ASEANElecGen_df).mark_line().encode(
        x='Year', y='Electricity generation (TWh)', color='Entity')
    st.altair_chart(c, use_container_width=True)

with col2:
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
        x='Year', y='Population', color='Entity')
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
    x='Year', y='Per capita electricity (kWh)', color='Entity')

st.altair_chart(c, use_container_width=True)

string3 = '''
         Jika pada chart pertama terlihat bahwa pemakaian listrik Indonesia adalah yang terbesar, di chart ini 
         terlihat bahwa secara per kapita, penggunaan listrik terbesar adalah oleh masyarakat Brunei dan Singapura.
         Kedua negara kecil yang dari perspektif agregat pemakain listrik tidak begitu signifikan, ternyata dari
         sisi per kapita merupakan konsumen listrik yang masif.
         
         Untuk membantu memperjelas grafik di atas, disajikan pemakaian listrik per kapita pada tahun 
         2020 di negara-negara ASEAN dalam bentuk Bar Chart di bawah ini:
         
         '''
st.write(string3)

ASEAN2000_df = pd.DataFrame()
## ASEAN2000_df = ASEANElecGen_df[ASEANElecGen_df['Year']==2020].sort_values(by='Per capita electricity (kWh)',ascending=False)[['Entity','Per capita electricity (kWh)']].reset_index()
ASEAN2000_df['Entity'] = ASEANElecGen_df[ASEANElecGen_df['Year']==2020].sort_values(by='Per capita electricity (kWh)',ascending=False)['Entity']
ASEAN2000_df[['Entity','Per capita electricity (kWh)']] = ASEANElecGen_df[ASEANElecGen_df['Year']==2020].sort_values(by='Per capita electricity (kWh)',ascending=False)[['Entity','Per capita electricity (kWh)']]

## st.bar_chart(data=ASEAN2000_df, x='Per capita electricity (kWh)', y='Entity')

c = alt.Chart(ASEAN2000_df).mark_bar().encode(
       alt.X('Entity', sort='-y'), 
       alt.Y('Per capita electricity (kWh)'),color='Entity')

st.altair_chart(c, use_container_width=True)

string4 = '''
         Terlihat jelas bahwa Brunei dan Singapura meninggalkan mayoritas negara ASEAN dalam hal pemakaian listrik
         per kapita, dengan pemakaian berkisar 9,000 - 10.000 kWh per kapita per tahun.
         
         Kemudian Malaysia dan Laos menyusul dengan pemakaian berkisar 4.000 - 5.000 kWh per kapita per tahun. 
         Selanjutnya adalah Thailan dan Vietnam yang pemakaian listrik per kapita per tahun adalah sekitar 2.000 kWH. 
         
         Sangat nampak bahwa Indonesia jauh tertinggal dibanding tetangga-tetangga yang lebih makmur. Nampak bahwa
         Pemakaian listrik per kapita di Singapura dan di Brunei sekitar sembilan kali lipat pemakaian per kapita 
         di Indonesia. Indonesia hanya lebih tinggi dibandingkan Myanmar, Kamboja dan Philipina. 
         '''
st.write(string4)



