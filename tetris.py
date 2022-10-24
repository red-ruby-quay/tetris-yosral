import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime
import time
import streamlit.components.v1 as components
from statsmodels.tsa.seasonal import seasonal_decompose


#helper to convert times to seconds
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# @st.cache
def load_data(prov_input = 'INDONESIA'):
    df_crime_clock = pd.read_excel("Crime Clock By Polda.xlsx", index_col = 0)
    df_crime_clock = df_crime_clock.astype(str)
    df_crime_clock = df_crime_clock.applymap(get_sec)
    df_murder_year = pd.read_excel("Jumlah Kasus Kejahatan Pembunuhan Pada Satu Tahun Terakhir.xlsx", index_col = 0)
    df_crime_count = pd.read_excel("Jumlah Tindak Pidana Menurut Kepolisian Daerah.xlsx", index_col = 0)
    df_crime_solve = pd.read_excel("Persentase Penyelesaian Tindak Pidana.xlsx", index_col = 0)
    df_crime_risk  = pd.read_excel("Risiko Penduduk Terkena Tindak Pidana (Per 100.000 Penduduk).xlsx", index_col = 0)
    df_crime_count = df_crime_count.astype(int)
    df_crime_solve = df_crime_solve.astype(int)
    df_crime_risk = df_crime_risk.astype(int)
    if(prov_input != 'INDONESIA'):
        df_crime_clock = df_crime_clock.loc[prov_input]
        df_crime_count = df_crime_count.loc[prov_input]
        df_crime_solve = df_crime_solve.loc[prov_input]
        df_crime_risk = df_crime_risk.loc[prov_input]
    return df_crime_clock, df_murder_year, df_crime_count, df_crime_solve, df_crime_risk

st.markdown('<h2 style="text-align: center;">Percuma Lapor Polisi?</h2>', unsafe_allow_html=True)
st.markdown('<img src="https://static.republika.co.id/uploads/images/inpicture_slide/logo_200625094047-486.jpg" alt="Lambang POLRI" style="width:700px; height:400px; text-align:center;"><br/><br/>', unsafe_allow_html=True)
st.markdown('<div style="text-align: justify;">Frasa atau tagar <b>#PercumaLaporPolisi</b> saat ini sering muncul dalam berbagai pemberitaan di media massa yang berkaitan dengan kasus yang menyandung internal kepolisian.<br><br>\n\n Berdasarkan data pencarian kata yang dihimpun Google Trend, ternyata frasa atau tagar ini sudah sering dipakai dalam 5 tahun terakhir [\(Keluh Warga Ramai #PercumaLaporPolisi\: Memang Percuma)](https://www.cnnindonesia.com/nasional/20211014165320-12-707927/keluh-warga-ramai-percumalaporpolisi-memang-percuma), namun kembali <b>booming</b> akhir-akhir ini, terutama di media sosial.\n\nFenomena <b>booming-phrase</b> tersebut kembali terjadi dikarenakan beberapa kasus internal polisi yang dinilai negatif oleh masyarakat, seperti [Kasus Pembunuhan oleh Ferdy Sambo](https://nasional.kompas.com/read/2022/09/07/11293841/kasus-ferdy-sambo-dan-siasat-kapolri-benahi-polri) dan yang paling terbaru adalah [Kasus Narkoba Teddy Minahasa](https://nasional.kompas.com/read/2022/10/15/15304311/pertaruhan-citra-polri-di-3-kasus-besar-teddy-minahasa-ferdy-sambo-dan)</div>', unsafe_allow_html=True)

if(st.checkbox('Lihat Data Google Trend')):
    components.html('<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3045_RC01/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("TIMESERIES", {"comparisonItem":[{"keyword":"#percumalaporpolisi","geo":"ID","time":"today 5-y"}],"category":0,"property":""}, {"exploreQuery":"date=today%205-y&geo=ID&q=%23percumalaporpolisi","guestPath":"https://trends.google.co.id:443/trends/embed/"}); </script>', width=750, height=400, scrolling=True)
    st.markdown('<p style="text-align: center;">Rate Tren Frasa "#PercumaLaporPolisi" Tahun 2017-2022</p>', unsafe_allow_html=True)
    components.html('<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3045_RC01/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("GEO_MAP", {"comparisonItem":[{"keyword":"#percumalaporpolisi","geo":"ID","time":"today 5-y"}],"category":0,"property":""}, {"exploreQuery":"date=today%205-y&geo=ID&q=%23percumalaporpolisi","guestPath":"https://trends.google.co.id:443/trends/embed/"}); </script>', width=750, height=400, scrolling=True)
    st.markdown('<p style="text-align: center;">Tren Frasa "#PercumaLaporPolisi" Berdasarkan Provinsi Tahun 2017-2022</p>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;">Terlihat bahwa daerah provinsi yang paling aktif dalam menyuarakan frasa tersebut diantaranya <b>Sumatera Utara</b>, <b>Jajaran Seluruh Provinsi di Pulau Jawa</b>, dan <b>Sulawesi Selatan</b>. Terlihat sekali bahwa terdapat kesenjangan pengakses aplikasi media sosial yang hanya berkutat di kota-kota besar. Ini bisa jadi mengindikasikan kurangnya pemerataan perlindungan hukum jika kasus yang bisa di<i>blow-up</i> menggunakan #PercumaLaporPolisi hanya terbatas pada daerah provinsi besar. Ini juga menunjukkan kalau kemungkinan besar provinsi-provinsi lainnya tidak mendapatkan perhatian yang sama dalam proses pelaporan kepada POLRI jika <b>#NoViralNoJustice<b></br></br></div>', unsafe_allow_html=True)

st.markdown('<div style="text-align: justify;">Apakah perspektif dalam bentuk tagar atau frasa yang sedang bergema di masyarakat ini menggambarkan turunnya elektabilitas POLRI dan situasi keamanan di Indonesia? Mari kita sandingkan opini tersebut berdasarkan data yang ada!</br></br></div>', unsafe_allow_html=True)

with open("provinsi.txt") as f: 
    lines = f.readlines()
    prov_list = [s.rstrip() for s in lines]
    # prov_list = tuple(lines)

prov_input = st.selectbox(
        "PILIH WILAYAH",
        prov_list
    )

def decompose_series(series, title, prov_input):
    if(prov_input == 'INDONESIA' and 'INDONESIA' in series):
        series = series.INDONESIA
        # series.loc[prov_input] = pd.to_numeric(series.loc[prov_input])
    result = seasonal_decompose(series, model='multiplicative', period = 3)
    slope = np.polyfit(series.index, series,2)[0]
    down_or_up = "penurunan" if slope < 0 else "penaikan"
    if(st.checkbox(f'Lihat hasil dekomposisi multiplikatif {title}')):
        trend_plot = px.line(result.trend)
        st.plotly_chart(trend_plot)
        st.markdown(f'<div style="text-align: justify;">Menggunakan proses uji dekomposisi deret waktu, dapat dilihat bahwa {title} mengalami {down_or_up} (<i>Slope regresi polinomial<i> = {slope})</br></br></div>', unsafe_allow_html=True)
    return result

def show_desc(prov_input):
    df_crime_clock, df_murder_year, df_crime_count, df_crime_solve, df_crime_risk = load_data(prov_input)
    st.markdown("```*Catatan: khusus provinsi Sulawesi Barat, Kalimantan Utara dan Papua Barat, data tahun 2005 sampai tahun pemekaran provinsi baru diisi menggunakan data provinsi induk asal pemekaran```")
    if(prov_input == 'INDONESIA'):
        #MURDER YEAR
        st.markdown(f"<h3 style='text-align: center; '>Jumlah Kasus Pembunuhan Per Satu Tahun Terakhir Se-Indonesia Pada 2011-2020</h3>", unsafe_allow_html=True)
        fig1 = px.line(df_murder_year, markers=True, labels={"index": "Tahun", "value": "Jumlah (Orang)"})
        fig1.update_traces(textposition="bottom right")
        st.plotly_chart(fig1, use_container_width=True)
        decompose_series(df_murder_year, 'trend jumlah kasus pembunuhan per satu tahun terakhir', prov_input)

    # CRIME CLOCK
    st.markdown(f"<h3 style='text-align: center; '>Selang Waktu Kejahatan di {prov_input.lower().capitalize()} Tahun 2005-2020</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; '>adalah selang waktu atau interval waktu terjadinya satu tindak kejahatan dengan kejahatan yang lain. Selang waktu kejadian kriminal dinyatakan dalam satuan waktu detik</p>", unsafe_allow_html=True)
    df_crime_clock = df_crime_clock.T
    fig2 = px.line(df_crime_clock, markers=True, labels={"index": "Tahun", "value": "Selang Waktu (Detik)"})
    fig2.update_traces(textposition="bottom right")
    st.plotly_chart(fig2, use_container_width=True)
    decompose_series(df_crime_clock, 'trend selang waktu kejahatan', prov_input)

    # CRIME COUNT
    st.markdown(f"<h3 style='text-align: center; '>Jumlah Tindak Pidana di {prov_input.lower().capitalize()} Tahun 2005-2020</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; '>aadalah peristiwa yang dilaporkan yaitu setiap peristiwa yang diterima kepolisian dari laporan masyarakat, atau peristiwa yang pelakunya tertangkap tangan oleh polisi.</p>", unsafe_allow_html=True)
    df_crime_count = df_crime_count.T
    fig3 = px.line(df_crime_count, markers=True, labels={"index": "Tahun", "value": "Jumlah Tindak Pidana"})
    fig3.update_traces(textposition="bottom right")
    st.plotly_chart(fig3, use_container_width=True)
    # decompose_series(df_crime_count, 'jumlah tindak pidana', prov_input)

    # CRIME RISK
    st.markdown(f"<h3 style='text-align: center; '>Risiko Penduduk {prov_input.lower().capitalize()} Terkena Tindak Pidana Tahun 2005-2020</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; '>adalah jumlah kejahatan setahun dibagi dengan jumlah penduduk {prov_input.lower().capitalize()} di tahun tertentu dikalikan 100.000.</p>", unsafe_allow_html=True)
    fig4 = px.line(df_crime_risk, markers=True, labels={"index": "Tahun", "value": "Penduduk Per 100.000"})
    fig4.update_traces(textposition="bottom right")
    st.plotly_chart(fig4, use_container_width=True)
    st.dataframe(df_crime_risk)
    # decompose_series(df_crime_risk, 'risiko penduduk terkena tindak pidana (per 100.000 orang)', prov_input)

    #CRIME SOLVE
    st.markdown(f"<h3 style='text-align: center; '>Persentase Penyelesaian Tindak Pidana di {prov_input.lower().capitalize()} Tahun 2005-2020</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; '>merupakan perbandingan jumlah tindak kejahatan yang dapat diselesaikan oleh pihak kepolisian dengan tindak kejahatan yang dilaporkan pada kurun waktu tertentu di wilayah {prov_input.lower().capitalize()} dikalikan 100 persen.</p>", unsafe_allow_html=True)
    fig5 = px.line(df_crime_solve, markers=True, labels={"index": "Tahun", "value": "Persentase"})
    fig5.update_traces(textposition="bottom right")
    st.plotly_chart(fig5, use_container_width=True)
    # decompose_series(df_crime_solve, 'persentase penyelesaian tindak pidana', prov_input)

if(prov_input):
    show_desc(prov_input)

st.markdown(f"<p style='text-align: justify; '>Berdasarkan jumlah, rate, ataupun proporsi dari setiap statistik yang ada, seperti jumlah kasus pembunuhan, jumlah tindak pidana, dan risiko pidana semakin meningkat. Ini menandakan bahwa perkembangan kinerja polisi dari tahun ke tahun justru cenderung menurun. Ditambah lagi selang waktu tindak kejahatan dan penyelesaian yang semakin turun, menandakan bahwa semakin cepat selang kejahatan berlangsung sedangkan penyelesaian yang dilakukan oleh POLRI justru secara mayoritas di setiap daerah malah cenderung semakin lama. </p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: justify; '>Jadi, wajar saja jika tagar <b>#percumalaporpolisi</b> kini semakin menggema, ditambah lagi pemberitaan kasus besar yang penyelesaiannya lama meskipun alur kronologinya sudah jelas bagi masyarakat awam sekalipun. Dari kesimpulan hasil data yang dipaparkan, kita hanya bisa berharap semoga POLRI bisa segera membenahi diri agar rakyat Indonesia tidak perlu menggemakan tagar <b>#percumalaporpolisi</b> lagi di media sosial. Bagaimana?.</p>", unsafe_allow_html=True)
st.markdown('</br><footer><p>Sumber Data/Berita: </p><ol><li><a href="https://www.bps.go.id">Badan Pusat Statistik (Statistik Politik dan Keamanan Tahun 2005-2020)</a></li><li><a href="https://www.kompas.com">Kompas</a></li><li><a href="https://www.cnnindonesia.com">CNN Indonesia</a></li><li><a href="https://www.twitter.com">Twitter</a></li></ol></footer>', unsafe_allow_html=True)


# tweets_df = pd.read_json('hasil_scrapping.json', lines=True)
# st.dataframe(tweets_df)
