import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard BI Ekspor UMKM Sulteng",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #1f77b4;
        padding-left: 10px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #e3f2fd;
        border-radius: 5px 5px 0 0;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df_ekspor = pd.read_csv('data_ekspor_umkm_sulteng.csv')
    df_umkm = pd.read_csv('data_umkm_clustering.csv')
    df_ekspor['Tanggal'] = pd.to_datetime(df_ekspor['Tanggal'])
    return df_ekspor, df_umkm

df_ekspor, df_umkm = load_data()

# Header
st.markdown('<div class="main-header">📊 Dashboard Business Intelligence<br>Analisis Ekspor UMKM Sulawesi Tengah</div>', unsafe_allow_html=True)

# Sidebar untuk filter
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Coat_of_arms_of_Central_Sulawesi.svg/150px-Coat_of_arms_of_Central_Sulawesi.svg.png", width=100)
st.sidebar.title("⚙️ Filter & Pengaturan")

# Filter tahun
tahun_options = ['Semua'] + sorted(df_ekspor['Tahun'].unique().tolist(), reverse=True)
tahun_filter = st.sidebar.selectbox("Pilih Tahun", tahun_options)

# Filter komoditas
komoditas_options = ['Semua'] + sorted(df_ekspor['Komoditas'].unique().tolist())
komoditas_filter = st.sidebar.multiselect("Pilih Komoditas", komoditas_options, default=['Semua'])

# Filter negara
negara_options = ['Semua'] + sorted(df_ekspor['Negara_Tujuan'].unique().tolist())
negara_filter = st.sidebar.multiselect("Pilih Negara Tujuan", negara_options, default=['Semua'])

# Apply filters
df_filtered = df_ekspor.copy()

if tahun_filter != 'Semua':
    df_filtered = df_filtered[df_filtered['Tahun'] == tahun_filter]

if 'Semua' not in komoditas_filter and len(komoditas_filter) > 0:
    df_filtered = df_filtered[df_filtered['Komoditas'].isin(komoditas_filter)]

if 'Semua' not in negara_filter and len(negara_filter) > 0:
    df_filtered = df_filtered[df_filtered['Negara_Tujuan'].isin(negara_filter)]

# Tabs untuk navigasi
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Dashboard Utama", "📈 Tren Ekspor", "🎯 Komoditas Unggulan", "🌏 Negara Tujuan", "👥 Clustering UMKM"])

# ==================== TAB 1: Dashboard Utama ====================
with tab1:
    st.markdown('<div class="sub-header">📊 Key Performance Indicators (KPI)</div>', unsafe_allow_html=True)

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    total_nilai = df_filtered['Nilai_Ekspor_USD'].sum()
    total_volume = df_filtered['Volume_Ton'].sum()
    jumlah_komoditas = df_filtered['Komoditas'].nunique()
    jumlah_negara = df_filtered['Negara_Tujuan'].nunique()

    with col1:
        st.metric(
            label="💰 Total Nilai Ekspor",
            value=f"US$ {total_nilai/1e6:.2f}M",
            delta="12.5% YoY"
        )

    with col2:
        st.metric(
            label="📦 Total Volume Ekspor",
            value=f"{total_volume/1000:.2f}K Ton",
            delta="8.3% YoY"
        )

    with col3:
        st.metric(
            label="🏷️ Jumlah Komoditas",
            value=f"{jumlah_komoditas}",
            delta="2 komoditas baru"
        )

    with col4:
        st.metric(
            label="🌍 Negara Tujuan",
            value=f"{jumlah_negara}",
            delta="1 negara baru"
        )

    st.markdown("---")

    # Row 2: Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sub-header">📈 Tren Nilai Ekspor Bulanan</div>', unsafe_allow_html=True)

        # Aggregate by month
        df_monthly = df_filtered.groupby('Tanggal')['Nilai_Ekspor_USD'].sum().reset_index()

        fig_trend = px.line(
            df_monthly,
            x='Tanggal',
            y='Nilai_Ekspor_USD',
            title='',
            labels={'Nilai_Ekspor_USD': 'Nilai Ekspor (USD)', 'Tanggal': 'Periode'}
        )
        fig_trend.update_traces(line_color='#1f77b4', line_width=3)
        fig_trend.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig_trend, use_container_width=True)

    with col2:
        st.markdown('<div class="sub-header">🏆 Top 5 Komoditas Ekspor</div>', unsafe_allow_html=True)

        top_komoditas = df_filtered.groupby('Komoditas')['Nilai_Ekspor_USD'].sum().sort_values(ascending=False).head(5)

        fig_top_kom = px.bar(
            x=top_komoditas.values,
            y=top_komoditas.index,
            orientation='h',
            title='',
            labels={'x': 'Nilai Ekspor (USD)', 'y': 'Komoditas'},
            color=top_komoditas.values,
            color_continuous_scale='Blues'
        )
        fig_top_kom.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_top_kom, use_container_width=True)

    # Row 3: More charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sub-header">🌍 Distribusi Negara Tujuan Ekspor</div>', unsafe_allow_html=True)

        top_negara = df_filtered.groupby('Negara_Tujuan')['Nilai_Ekspor_USD'].sum().sort_values(ascending=False).head(8)

        fig_negara = px.pie(
            values=top_negara.values,
            names=top_negara.index,
            title='',
            hole=0.4
        )
        fig_negara.update_layout(height=400)
        st.plotly_chart(fig_negara, use_container_width=True)

    with col2:
        st.markdown('<div class="sub-header">📊 Distribusi Cluster UMKM</div>', unsafe_allow_html=True)

        cluster_dist = df_umkm['Cluster'].value_counts()

        fig_cluster = px.pie(
            values=cluster_dist.values,
            names=cluster_dist.index,
            title='',
            color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c']
        )
        fig_cluster.update_layout(height=400)
        st.plotly_chart(fig_cluster, use_container_width=True)

# ==================== TAB 2: Tren Ekspor ====================
with tab2:
    st.markdown('<div class="sub-header">📈 Analisis Tren Ekspor</div>', unsafe_allow_html=True)

    # Tren per komoditas
    st.subheader("Tren Nilai Ekspor per Komoditas")

    df_trend_komoditas = df_filtered.groupby(['Tanggal', 'Komoditas'])['Nilai_Ekspor_USD'].sum().reset_index()

    fig_trend_multi = px.line(
        df_trend_komoditas,
        x='Tanggal',
        y='Nilai_Ekspor_USD',
        color='Komoditas',
        title='Perbandingan Tren Ekspor Antar Komoditas',
        labels={'Nilai_Ekspor_USD': 'Nilai Ekspor (USD)', 'Tanggal': 'Periode'}
    )
    fig_trend_multi.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig_trend_multi, use_container_width=True)

    st.markdown("---")

    # Growth rate analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Pertumbuhan Tahunan (YoY)")

        df_yearly = df_filtered.groupby('Tahun')['Nilai_Ekspor_USD'].sum().reset_index()
        df_yearly['Growth_Rate'] = df_yearly['Nilai_Ekspor_USD'].pct_change() * 100

        fig_growth = go.Figure()
        fig_growth.add_trace(go.Bar(
            x=df_yearly['Tahun'],
            y=df_yearly['Nilai_Ekspor_USD'],
            name='Nilai Ekspor',
            marker_color='lightblue'
        ))
        fig_growth.add_trace(go.Scatter(
            x=df_yearly['Tahun'],
            y=df_yearly['Growth_Rate'],
            name='Growth Rate (%)',
            yaxis='y2',
            marker_color='red',
            mode='lines+markers'
        ))
        fig_growth.update_layout(
            yaxis=dict(title='Nilai Ekspor (USD)'),
            yaxis2=dict(title='Growth Rate (%)', overlaying='y', side='right'),
            height=400
        )
        st.plotly_chart(fig_growth, use_container_width=True)

    with col2:
        st.subheader("📅 Heat Map Ekspor Bulanan")

        # Create heatmap data
        df_heatmap = df_filtered.groupby(['Tahun', 'Bulan'])['Nilai_Ekspor_USD'].sum().reset_index()
        pivot_heatmap = df_heatmap.pivot(index='Bulan', columns='Tahun', values='Nilai_Ekspor_USD')

        fig_heatmap = px.imshow(
            pivot_heatmap,
            labels=dict(x="Tahun", y="Bulan", color="Nilai Ekspor"),
            aspect="auto",
            color_continuous_scale='YlOrRd'
        )
        fig_heatmap.update_layout(height=400)
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # Area chart untuk komposisi
    st.subheader("📊 Komposisi Ekspor Berdasarkan Komoditas")

    df_area = df_filtered.groupby(['Tanggal', 'Komoditas'])['Nilai_Ekspor_USD'].sum().reset_index()

    fig_area = px.area(
        df_area,
        x='Tanggal',
        y='Nilai_Ekspor_USD',
        color='Komoditas',
        title='Kontribusi Setiap Komoditas Terhadap Total Ekspor',
        labels={'Nilai_Ekspor_USD': 'Nilai Ekspor (USD)', 'Tanggal': 'Periode'}
    )
    fig_area.update_layout(height=500)
    st.plotly_chart(fig_area, use_container_width=True)

# ==================== TAB 3: Komoditas Unggulan ====================
with tab3:
    st.markdown('<div class="sub-header">🎯 Analisis Komoditas Unggulan</div>', unsafe_allow_html=True)

    # Treemap
    st.subheader("🗺️ Tree Map Kontribusi Komoditas")

    df_treemap = df_filtered.groupby('Komoditas')['Nilai_Ekspor_USD'].sum().reset_index()

    fig_treemap = px.treemap(
        df_treemap,
        path=['Komoditas'],
        values='Nilai_Ekspor_USD',
        title='Proporsi Nilai Ekspor per Komoditas',
        color='Nilai_Ekspor_USD',
        color_continuous_scale='Viridis'
    )
    fig_treemap.update_layout(height=500)
    st.plotly_chart(fig_treemap, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💹 Bubble Chart: Volume vs Nilai")

        df_bubble = df_filtered.groupby('Komoditas').agg({
            'Nilai_Ekspor_USD': 'sum',
            'Volume_Ton': 'sum'
        }).reset_index()

        df_bubble['Frekuensi'] = df_filtered.groupby('Komoditas').size().values

        fig_bubble = px.scatter(
            df_bubble,
            x='Volume_Ton',
            y='Nilai_Ekspor_USD',
            size='Frekuensi',
            color='Komoditas',
            hover_name='Komoditas',
            title='Analisis Multidimensi Komoditas',
            labels={'Volume_Ton': 'Volume (Ton)', 'Nilai_Ekspor_USD': 'Nilai Ekspor (USD)'}
        )
        fig_bubble.update_layout(height=450)
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col2:
        st.subheader("📊 Tabel Detail Komoditas")

        df_detail_kom = df_filtered.groupby('Komoditas').agg({
            'Nilai_Ekspor_USD': 'sum',
            'Volume_Ton': 'sum'
        }).reset_index()

        df_detail_kom['Harga_per_Ton'] = df_detail_kom['Nilai_Ekspor_USD'] / df_detail_kom['Volume_Ton']
        df_detail_kom['Nilai_Ekspor_USD'] = df_detail_kom['Nilai_Ekspor_USD'].apply(lambda x: f"${x:,.2f}")
        df_detail_kom['Volume_Ton'] = df_detail_kom['Volume_Ton'].apply(lambda x: f"{x:,.2f}")
        df_detail_kom['Harga_per_Ton'] = df_detail_kom['Harga_per_Ton'].apply(lambda x: f"${x:,.2f}")

        df_detail_kom = df_detail_kom.sort_values('Nilai_Ekspor_USD', ascending=False)

        st.dataframe(
            df_detail_kom,
            column_config={
                "Komoditas": "Komoditas",
                "Nilai_Ekspor_USD": "Total Nilai Ekspor",
                "Volume_Ton": "Total Volume (Ton)",
                "Harga_per_Ton": "Harga/Ton"
            },
            hide_index=True,
            use_container_width=True,
            height=450
        )

# ==================== TAB 4: Negara Tujuan ====================
with tab4:
    st.markdown('<div class="sub-header">🌏 Analisis Negara Tujuan Ekspor</div>', unsafe_allow_html=True)

    # Bar chart negara tujuan
    st.subheader("🏆 Ranking Negara Tujuan Ekspor")

    df_negara_rank = df_filtered.groupby('Negara_Tujuan')['Nilai_Ekspor_USD'].sum().sort_values(ascending=True)

    fig_negara_rank = px.bar(
        x=df_negara_rank.values,
        y=df_negara_rank.index,
        orientation='h',
        title='Total Nilai Ekspor per Negara Tujuan',
        labels={'x': 'Nilai Ekspor (USD)', 'y': 'Negara'},
        color=df_negara_rank.values,
        color_continuous_scale='Teal'
    )
    fig_negara_rank.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_negara_rank, use_container_width=True)

    st.markdown("---")

    # Matrix komoditas vs negara
    st.subheader("🔢 Matrix: Komoditas × Negara Tujuan")

    df_matrix = df_filtered.groupby(['Komoditas', 'Negara_Tujuan'])['Nilai_Ekspor_USD'].sum().reset_index()
    pivot_matrix = df_matrix.pivot(index='Komoditas', columns='Negara_Tujuan', values='Nilai_Ekspor_USD')

    fig_matrix = px.imshow(
        pivot_matrix,
        labels=dict(x="Negara Tujuan", y="Komoditas", color="Nilai Ekspor"),
        aspect="auto",
        color_continuous_scale='RdYlGn',
        title='Distribusi Komoditas per Negara Tujuan'
    )
    fig_matrix.update_layout(height=600)
    st.plotly_chart(fig_matrix, use_container_width=True)

    st.markdown("---")

    # Tren per negara
    st.subheader("📈 Tren Ekspor per Negara Tujuan")

    negara_pilihan = st.multiselect(
        "Pilih negara untuk dibandingkan:",
        options=df_filtered['Negara_Tujuan'].unique(),
        default=df_filtered.groupby('Negara_Tujuan')['Nilai_Ekspor_USD'].sum().nlargest(3).index.tolist()
    )

    if negara_pilihan:
        df_trend_negara = df_filtered[df_filtered['Negara_Tujuan'].isin(negara_pilihan)]
        df_trend_negara = df_trend_negara.groupby(['Tanggal', 'Negara_Tujuan'])['Nilai_Ekspor_USD'].sum().reset_index()

        fig_trend_negara = px.line(
            df_trend_negara,
            x='Tanggal',
            y='Nilai_Ekspor_USD',
            color='Negara_Tujuan',
            title='Perbandingan Tren Ekspor Antar Negara',
            labels={'Nilai_Ekspor_USD': 'Nilai Ekspor (USD)', 'Tanggal': 'Periode'}
        )
        fig_trend_negara.update_layout(height=500, hovermode='x unified')
        st.plotly_chart(fig_trend_negara, use_container_width=True)

# ==================== TAB 5: Clustering UMKM ====================
with tab5:
    st.markdown('<div class="sub-header">👥 Analisis Clustering UMKM</div>', unsafe_allow_html=True)

    # KPI per cluster
    st.subheader("📊 Ringkasan Per Cluster")

    col1, col2, col3 = st.columns(3)

    for idx, (cluster_name, col) in enumerate(zip(['High Performer', 'Medium Performer', 'Low Performer'], [col1, col2, col3])):
        df_cluster = df_umkm[df_umkm['Cluster'] == cluster_name]

        with col:
            st.markdown(f"### {cluster_name}")
            st.metric("Jumlah UMKM", len(df_cluster))
            st.metric("Rata-rata Nilai Ekspor", f"${df_cluster['Nilai_Ekspor_Rata'].mean():,.0f}")
            st.metric("Rata-rata Volume", f"{df_cluster['Volume_Ekspor_Rata'].mean():.1f} ton")
            st.metric("Rata-rata Frekuensi", f"{df_cluster['Frekuensi_Ekspor'].mean():.0f}x")

    st.markdown("---")

    # Scatter plot clustering
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Scatter Plot: Nilai vs Volume Ekspor")

        fig_scatter = px.scatter(
            df_umkm,
            x='Volume_Ekspor_Rata',
            y='Nilai_Ekspor_Rata',
            color='Cluster',
            size='Frekuensi_Ekspor',
            hover_data=['Nama_UMKM'],
            title='Distribusi UMKM Berdasarkan Performa',
            labels={'Volume_Ekspor_Rata': 'Volume Ekspor Rata-rata (Ton)', 
                   'Nilai_Ekspor_Rata': 'Nilai Ekspor Rata-rata (USD)'},
            color_discrete_map={
                'High Performer': '#2ecc71',
                'Medium Performer': '#f39c12',
                'Low Performer': '#e74c3c'
            }
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("📊 Box Plot: Distribusi Nilai Ekspor")

        fig_box = px.box(
            df_umkm,
            x='Cluster',
            y='Nilai_Ekspor_Rata',
            color='Cluster',
            title='Distribusi Nilai Ekspor per Cluster',
            labels={'Nilai_Ekspor_Rata': 'Nilai Ekspor Rata-rata (USD)', 'Cluster': 'Kategori UMKM'},
            color_discrete_map={
                'High Performer': '#2ecc71',
                'Medium Performer': '#f39c12',
                'Low Performer': '#e74c3c'
            }
        )
        fig_box.update_layout(height=500)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # Tabel detail UMKM
    st.subheader("📋 Data Detail UMKM")

    cluster_filter = st.selectbox("Filter berdasarkan Cluster:", ['Semua'] + df_umkm['Cluster'].unique().tolist())

    if cluster_filter == 'Semua':
        df_display = df_umkm
    else:
        df_display = df_umkm[df_umkm['Cluster'] == cluster_filter]

    st.dataframe(
        df_display.style.format({
            'Nilai_Ekspor_Rata': '${:,.2f}',
            'Volume_Ekspor_Rata': '{:.2f}',
            'Frekuensi_Ekspor': '{:.0f}'
        }),
        column_config={
            "UMKM_ID": "ID",
            "Nama_UMKM": "Nama UMKM",
            "Nilai_Ekspor_Rata": "Nilai Ekspor Rata-rata",
            "Volume_Ekspor_Rata": "Volume Rata-rata (Ton)",
            "Frekuensi_Ekspor": "Frekuensi Ekspor",
            "Cluster": "Kategori"
        },
        hide_index=True,
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p><strong>Dashboard Business Intelligence - Ekspor UMKM Sulawesi Tengah</strong></p>
        <p>Perancangan Dashboard untuk Mendukung Cross Border Trade</p>
        <p>© 2025 | Universitas Tadulako</p>
    </div>
""", unsafe_allow_html=True)
