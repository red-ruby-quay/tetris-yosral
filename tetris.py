from doctest import DONT_ACCEPT_TRUE_FOR_1
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime
import time
import streamlit.components.v1 as components

#helper to convert times to seconds
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

@st.cache
def load_data(prov_input = 'INDONESIA'):
    df_crime_clock = pd.read_excel("Crime Clock By Polda.xlsx", index_col = 0)
    df_crime_clock = df_crime_clock.astype(str)
    df_crime_clock = df_crime_clock.applymap(get_sec)
    df_murder_year = pd.read_excel("Jumlah Kasus Kejahatan Pembunuhan Pada Satu Tahun Terakhir.xlsx", index_col = 0)
    df_crime_count = pd.read_excel("Jumlah Tindak Pidana Menurut Kepolisian Daerah.xlsx", index_col = 0)
    df_crime_solve = pd.read_excel("Persentase Penyelesaian Tindak Pidana.xlsx", index_col = 0)
    df_crime_risk  = pd.read_excel("Risiko Penduduk Terkena Tindak Pidana (Per 100.000 Penduduk).xlsx", index_col = 0)
    if(prov_input != 'INDONESIA'):
        # df_crime_clock = df_crime_clock.filter(items = [prov_input], axis = 0)
        # df_crime_count = df_crime_count.filter(items = [prov_input], axis = 0)
        # df_crime_solve = df_crime_solve.filter(items = [prov_input], axis = 0)
        # df_crime_risk = df_crime_risk.filter(items = [prov_input], axis = 0)
        df_crime_clock = df_crime_clock.loc[prov_input]
        df_crime_count = df_crime_count.loc[prov_input]
        df_crime_solve = df_crime_solve.loc[prov_input]
        df_crime_risk = df_crime_risk.loc[prov_input]
    return df_crime_clock, df_murder_year, df_crime_count, df_crime_solve, df_crime_risk

st.markdown("<h2 style='text-align: center; '>Percuma Lapor Polisi?</h2>", unsafe_allow_html=True)
st.markdown("![Lambang POLRI](https://static.republika.co.id/uploads/images/inpicture_slide/logo_200625094047-486.jpg)")
st.markdown('<div style="text-align: justify;">Frasa atau tagar <b>#PercumaLaporPolisi</b> saat ini sering muncul dalam berbagai pemberitaan di media massa yang berkaitan dengan kasus yang menyandung internal kepolisian.<br><br> Berdasarkan data pencarian kata yang dihimpun Google Trend, ternyata frasa atau tagar ini sudah sering dipakai dalam 5 tahun terakhir, namun kembali <b>booming</b> akhir-akhir ini, terutama di media sosial.\n\nFenomena <b>booming-phrase</b> tersebut kembali terjadi dikarenakan beberapa kasus internal polisi yang dinilai negatif oleh masyarakat, seperti [Kasus Pembunuhan oleh Ferdy Sambo](https://nasional.kompas.com/read/2022/09/07/11293841/kasus-ferdy-sambo-dan-siasat-kapolri-benahi-polri) dan yang paling terbaru adalah [Kasus Narkoba Teddy Minahasa](https://nasional.kompas.com/read/2022/10/15/15304311/pertaruhan-citra-polri-di-3-kasus-besar-teddy-minahasa-ferdy-sambo-dan)</div>', unsafe_allow_html=True)

if(st.checkbox('Lihat Data Google Trend')):
    components.html('<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3045_RC01/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("TIMESERIES", {"comparisonItem":[{"keyword":"#percumalaporpolisi","geo":"ID","time":"today 5-y"}],"category":0,"property":""}, {"exploreQuery":"date=today%205-y&geo=ID&q=%23percumalaporpolisi","guestPath":"https://trends.google.co.id:443/trends/embed/"}); </script>', width=750, height=400, scrolling=True)
    st.markdown('<p style="text-align: center;">Rate Tren Frasa "#PercumaLaporPolisi" Tahun 2017-2022</p>', unsafe_allow_html=True)
    components.html('<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3045_RC01/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("GEO_MAP", {"comparisonItem":[{"keyword":"#percumalaporpolisi","geo":"ID","time":"today 5-y"}],"category":0,"property":""}, {"exploreQuery":"date=today%205-y&geo=ID&q=%23percumalaporpolisi","guestPath":"https://trends.google.co.id:443/trends/embed/"}); </script>', width=750, height=400, scrolling=True)
    st.markdown('<p style="text-align: center;">Tren Frasa "#PercumaLaporPolisi" Berdasarkan Provinsi Tahun 2017-2022</p>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;">Terlihat bahwa daerah provinsi yang paling aktif dalam menyuarakan frasa tersebut diantaranya <b>Sumatera Utara</b>, <b>Jajaran Seluruh Provinsi di Pulau Jawa</b>, dan <b>Sulawesi Selatan</b>. Terlihat sekali bahwa terdapat kesenjangan pengakses aplikasi media sosial yang hanya berkutat di kota-kota besar. Ini bisa jadi mengindikasikan kurangnya pemerataan perlindungan hukum jika kasus yang bisa di<i>blow-up</i> menggunakan #PercumaLaporPolisi hanya terbatas pada daerah provinsi besar. Ini juga menunjukkan kalau kemungkinan besar provinsi-provinsi lainnya tidak mendapatkan perhatian yang sama dalam proses pelaporan kepada POLRI jika <b>#NoViralNoJustice<b></br></br></div>', unsafe_allow_html=True)

st.markdown('<div style="text-align: justify;">Apakah perspektif dalam bentuk tagar atau frasa yang sedang bergema di masyarakat ini menggambarkan turunnya elektabilitas POLRI dan situasi keamanan di Indonesia? Mari kita sandingkan opini tersebut berdasarkan data yang ada!</br></br></div>', unsafe_allow_html=True)

df_crime_clock, df_murder_year, df_crime_count, df_crime_solve, df_crime_risk = load_data()

with open("provinsi.txt") as f: 
    lines = f.readlines()
    prov_list = [s.rstrip() for s in lines]
    # prov_list = tuple(lines)

prov_input = st.selectbox(
        "PILIH WILAYAH",
        prov_list
    )

def show_desc(prov_input):
    df_crime_clock, df_murder_year, df_crime_count, df_crime_solve, df_crime_risk = load_data(prov_input)
    st.markdown("<h3 style='text-align: center; '>Selang Waktu Kejahatan</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; '>adalah selang waktu atau interval waktu terjadinya satu tindak kejahatan dengan kejahatan yang lain. Selang waktu kejadian kriminal dinyatakan dalam satuan waktu detik</p>", unsafe_allow_html=True)
    st.dataframe(df_crime_clock)
# df_crime_clock

if(prov_input):
    show_desc(prov_input)


