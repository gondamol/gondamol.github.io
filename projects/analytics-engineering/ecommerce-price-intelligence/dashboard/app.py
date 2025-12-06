"""
E-commerce Price Intelligence Dashboard
Real-time price tracking and comparison for Kenya

Run with: streamlit run dashboard/app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
SCRAPED_DIR = Path(__file__).parent.parent / "data" / "scraped"

# Page config
st.set_page_config(
    page_title="🛒 Price Intelligence Kenya",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B35, #F7C59F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: #666;
        font-size: 1.1rem;
        margin-top: 0;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Deal card */
    .deal-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px 0;
    }
    
    /* Price tag */
    .price-tag {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FF6B35;
    }
    
    .old-price {
        text-decoration: line-through;
        color: #999;
        font-size: 0.9rem;
    }
    
    /* Live banner */
    .live-banner {
        background: linear-gradient(90deg, #FF6B35, #FF8C42);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def load_data():
    """Load all data from JSON files"""
    data = {}
    
    try:
        # Load products
        products_file = DATA_DIR / "products.json"
        if not products_file.exists():
            products_file = SCRAPED_DIR / "products_latest.json"
        
        if products_file.exists():
            with open(products_file) as f:
                data['products'] = json.load(f)
        else:
            data['products'] = []
        
        # Load stats
        stats_file = DATA_DIR / "stats.json"
        if stats_file.exists():
            with open(stats_file) as f:
                data['stats'] = json.load(f)
        else:
            data['stats'] = {}
        
        # Load price history
        history_file = SCRAPED_DIR / "price_history_latest.json"
        if history_file.exists():
            with open(history_file) as f:
                data['history'] = json.load(f)
        else:
            data['history'] = []
        
        return data
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


def format_price(amount: float, currency: str = "KES") -> str:
    """Format price with currency"""
    if not amount:
        return "N/A"
    return f"{currency} {amount:,.0f}"


def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<p class="main-header">🛒 Price Intelligence Kenya</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time E-commerce Price Tracking & Comparison</p>', unsafe_allow_html=True)
    
    # Live banner
    st.markdown("""
    <div class="live-banner">
        📊 <strong>LIVE</strong> - Tracking prices across Jumia, Kilimall & more!
        Last updated: today
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    if not data or not data.get('products'):
        st.warning("⚠️ No product data available. Run the scraper first:")
        st.code("python3 scripts/scrape_prices.py", language="bash")
        return
    
    products = data['products']
    stats = data.get('stats', {})
    history = data.get('history', [])
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/200px-Flag_of_Kenya.svg.png", width=80)
        st.header("🔧 Filters")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Category filter
        categories = ['All'] + sorted(set(p.get('category', 'Other') for p in products))
        selected_category = st.selectbox("📁 Category", categories)
        
        # Source filter
        sources = ['All'] + sorted(set(p.get('source', 'unknown') for p in products))
        selected_source = st.selectbox("🏪 Source", sources)
        
        # Price range
        prices = [p['current_price'] for p in products if p.get('current_price')]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 500000
        
        price_range = st.slider(
            "💰 Price Range (KES)",
            min_value=int(min_price),
            max_value=int(max_price),
            value=(int(min_price), int(max_price)),
            step=1000
        )
        
        # Only deals
        show_deals = st.checkbox("🔥 Show Only Deals", value=False)
        
        st.markdown("---")
        st.markdown("### 📊 About")
        st.info("Track prices across Kenyan e-commerce platforms. Get alerts for price drops!")
    
    # Apply filters
    filtered_products = products
    
    if selected_category != 'All':
        filtered_products = [p for p in filtered_products if p.get('category') == selected_category]
    
    if selected_source != 'All':
        filtered_products = [p for p in filtered_products if p.get('source') == selected_source]
    
    filtered_products = [
        p for p in filtered_products
        if price_range[0] <= (p.get('current_price') or 0) <= price_range[1]
    ]
    
    if show_deals:
        filtered_products = [p for p in filtered_products if p.get('discount_percent')]
    
    # Key Metrics
    st.markdown("## 📈 Market Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Products",
            value=f"{len(products):,}",
            delta=f"Tracking"
        )
    
    with col2:
        num_deals = len([p for p in products if p.get('discount_percent')])
        st.metric(
            label="🔥 Active Deals",
            value=f"{num_deals}",
            delta="With discounts"
        )
    
    with col3:
        avg_price = sum(p['current_price'] for p in products if p.get('current_price')) / max(len(products), 1)
        st.metric(
            label="Avg Price",
            value=format_price(avg_price),
            delta="Across all"
        )
    
    with col4:
        categories_count = len(set(p.get('category', 'Other') for p in products))
        st.metric(
            label="Categories",
            value=categories_count,
            delta="Tracked"
        )
    
    with col5:
        sources_count = len(set(p.get('source', 'unknown') for p in products))
        st.metric(
            label="Sources",
            value=sources_count,
            delta="Platforms"
        )
    
    st.markdown("---")
    
    # Two column layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Products by Category")
        category_data = {}
        for p in products:
            cat = p.get('category', 'Other')
            category_data[cat] = category_data.get(cat, 0) + 1
        
        df_cat = pd.DataFrame([
            {'Category': k, 'Count': v}
            for k, v in sorted(category_data.items(), key=lambda x: -x[1])
        ])
        
        fig = px.bar(
            df_cat,
            x='Count',
            y='Category',
            orientation='h',
            color='Count',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏪 Products by Source")
        source_data = {}
        for p in products:
            src = p.get('source', 'unknown').title()
            source_data[src] = source_data.get(src, 0) + 1
        
        df_src = pd.DataFrame([
            {'Source': k, 'Count': v}
            for k, v in source_data.items()
        ])
        
        fig = px.pie(
            df_src,
            values='Count',
            names='Source',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Average Price by Category
    st.markdown("### 💰 Average Price by Category")
    
    avg_by_cat = {}
    for p in products:
        cat = p.get('category', 'Other')
        if cat not in avg_by_cat:
            avg_by_cat[cat] = []
        if p.get('current_price'):
            avg_by_cat[cat].append(p['current_price'])
    
    avg_prices = [
        {'Category': k, 'Average Price': sum(v)/len(v) if v else 0}
        for k, v in avg_by_cat.items()
    ]
    df_avg = pd.DataFrame(avg_prices)
    df_avg = df_avg.sort_values('Average Price', ascending=True)
    
    fig = px.bar(
        df_avg,
        x='Average Price',
        y='Category',
        orientation='h',
        color='Average Price',
        color_continuous_scale='Viridis',
        text=[format_price(v) for v in df_avg['Average Price']]
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Price History Chart (if available)
    if history:
        st.markdown("---")
        st.markdown("### 📈 Price History Trends")
        
        # Get unique products with history
        product_names = list(set(h.get('name', 'Unknown')[:50] for h in history))[:10]
        
        selected_product = st.selectbox(
            "Select product to view price history:",
            product_names
        )
        
        product_history = [h for h in history if h.get('name', '').startswith(selected_product[:30])]
        
        if product_history:
            df_history = pd.DataFrame(product_history)
            df_history['date'] = pd.to_datetime(df_history['date'])
            df_history = df_history.sort_values('date')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_history['date'],
                y=df_history['price'],
                mode='lines+markers',
                name='Price',
                line=dict(color='#FF6B35', width=3),
                marker=dict(size=8)
            ))
            
            # Add range slider
            fig.update_layout(
                title=f"Price History: {selected_product[:50]}",
                xaxis_title="Date",
                yaxis_title="Price (KES)",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Best Deals Section
    st.markdown("---")
    st.markdown("## 🔥 Best Deals Right Now")
    
    deals = sorted(
        [p for p in products if p.get('discount_percent')],
        key=lambda x: x.get('discount_percent', 0),
        reverse=True
    )[:12]
    
    if deals:
        cols = st.columns(4)
        for i, deal in enumerate(deals):
            with cols[i % 4]:
                with st.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 15px; border-radius: 10px; color: white; margin: 5px 0;">
                        <p style="font-weight: bold; margin-bottom: 5px;">{deal['name'][:40]}...</p>
                        <p style="font-size: 1.3rem; margin: 5px 0;">
                            KES {deal['current_price']:,.0f}
                        </p>
                        <p style="text-decoration: line-through; opacity: 0.7; margin: 0;">
                            KES {deal.get('old_price', 0):,.0f}
                        </p>
                        <p style="background: #38ef7d; color: black; padding: 2px 8px; 
                                  border-radius: 5px; display: inline-block; margin-top: 5px;">
                            -{deal['discount_percent']:.0f}% OFF
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No deals currently available.")
    
    # Product Table
    st.markdown("---")
    st.markdown("## 📋 All Products")
    
    # Search
    search_term = st.text_input("🔍 Search products by name", "")
    
    display_products = filtered_products
    if search_term:
        search_lower = search_term.lower()
        display_products = [
            p for p in filtered_products
            if search_lower in p.get('name', '').lower()
        ]
    
    # Format for display
    df_display = pd.DataFrame([
        {
            'Product': p['name'][:60] + ('...' if len(p['name']) > 60 else ''),
            'Price (KES)': f"{p['current_price']:,.0f}" if p.get('current_price') else 'N/A',
            'Old Price': f"{p['old_price']:,.0f}" if p.get('old_price') else '-',
            'Discount': f"-{p['discount_percent']:.0f}%" if p.get('discount_percent') else '-',
            'Rating': f"⭐ {p['rating']:.1f}" if p.get('rating') else '-',
            'Reviews': p.get('review_count', 0),
            'Category': p.get('category', 'Other'),
            'Source': p.get('source', 'unknown').title(),
        }
        for p in display_products[:100]
    ])
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400
    )
    
    st.markdown(f"**Showing {len(df_display)} of {len(filtered_products)} products**")
    
    # Footer
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔗 Quick Links")
        st.markdown("""
        - [Jumia Kenya](https://www.jumia.co.ke)
        - [Kilimall Kenya](https://www.kilimall.co.ke)
        - [GitHub Repo](https://github.com/gondamol)
        """)
    
    with col2:
        st.markdown("### 📧 Contact")
        st.markdown("""
        **Nicodemus Werre Amollo**  
        Research Data Manager  
        📧 nichodemuswerre@gmail.com
        """)
    
    with col3:
        st.markdown("### 🛠️ Tech Stack")
        st.markdown("""
        - Python + BeautifulSoup
        - Streamlit + Plotly
        - GitHub Actions
        """)
    
    st.markdown(
        "<center>Built with ❤️ by Nicodemus Werre | Kenya 🇰🇪</center>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
