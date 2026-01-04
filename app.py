"""
SEO Content Generator - Dash Frontend
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import requests
import base64
import io
from datetime import datetime, timedelta
from db import get_all_sites, get_site_by_key

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)
app.title = "SEO Content Generator"

# App Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🦩 SEO سیستم تولید محتوای 🦩", className="text-white mb-2"),
                html.P("ایجاد محتوای هوشمند و بهینه‌شده", className="text-white-50")
            ], className="text-center py-4", style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'borderRadius': '10px',
                'marginBottom': '20px'
            })
        ])
    ]),
    
    # Site Selector
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("انتخاب سایت:", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id='site-selector',
                        placeholder="در حال بارگذاری...",
                        style={'direction': 'rtl'}
                    ),
                ])
            ], className="mb-3")
        ])
    ]),
    
    # Tabs
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="ساخت تک پست وبلاگ", tab_id="blog", label_style={'fontSize': '16px'}),
                dbc.Tab(label="تحقیق و افزودن کلیدواژه", tab_id="keyword", label_style={'fontSize': '16px'}),
                dbc.Tab(label="کمپین هوشمند", tab_id="campaign", label_style={'fontSize': '16px'}),
            ], id="tabs", active_tab="blog", className="mb-3"),
            
            html.Div(id="tab-content")
        ])
    ]),
    
    # Hidden div to store site data
    dcc.Store(id='site-data')
    
], fluid=True, className="py-4", style={'maxWidth': '1200px'})


# Blog Post Tab Content
def create_blog_tab():
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("موضوع پست:"),
                    dbc.Input(id="blog-topic", placeholder="مثال: مدیریت بک‌لاگ محصول", style={'direction': 'rtl'})
                ], md=12, className="mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("کلیدواژه اصلی:"),
                    dbc.Input(id="blog-primary-kw", placeholder="مثال: مدیریت بک‌لاگ", style={'direction': 'rtl'})
                ], md=6, className="mb-3"),
                dbc.Col([
                    dbc.Label("سبک نوشتاری:"),
                    dbc.Input(id="blog-style", value="مقاله تخصصی و راهنمای جامع", style={'direction': 'rtl'})
                ], md=6, className="mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("کلیدواژه‌های ثانویه (هر کدام در یک خط):"),
                    dbc.Textarea(id="blog-secondary-kw", placeholder="Product Manager\nاولویت‌بندی تسک\nاسکرام", 
                                style={'direction': 'rtl', 'minHeight': '100px'})
                ], md=8, className="mb-3"),
                dbc.Col([
                    dbc.Label("تعداد کلمات:"),
                    dbc.Input(id="blog-word-count", type="number", value=1500, min=500, max=5000)
                ], md=4, className="mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("ایجاد پست وبلاگ", id="blog-submit", color="primary", 
                              className="w-100", size="lg"),
                    dbc.Spinner([html.Div(id="blog-status", className="mt-3")], color="primary")
                ])
            ])
        ])
    ])


# Keyword Research Tab Content
def create_keyword_tab():
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("آپلود فایل کلیدواژه‌ها (CSV یا Excel):"),
                    html.P("فایل باید دو ستون داشته باشد: keyword و score", className="text-muted small"),
                    dcc.Upload(
                        id='keyword-upload',
                        children=html.Div([
                            html.I(className="fas fa-cloud-upload-alt fa-2x mb-2"),
                            html.Br(),
                            'فایل را اینجا بکشید یا کلیک کنید'
                        ], style={'textAlign': 'center', 'padding': '40px', 'border': '2px dashed #ccc', 
                                 'borderRadius': '10px', 'cursor': 'pointer'}),
                        multiple=False
                    ),
                    html.Div(id='upload-feedback', className="mt-2")
                ], md=12, className="mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Checklist(
                        options=[{"label": " توسعه با LLM", "value": 1}],
                        value=[],
                        id="keyword-llm-expand",
                        inline=True,
                        style={'direction': 'rtl'}
                    )
                ], className="mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("شروع تحقیق کلیدواژه", id="keyword-submit", color="success", 
                              className="w-100", size="lg", disabled=True),
                    dbc.Spinner([html.Div(id="keyword-status", className="mt-3")], color="success")
                ])
            ])
        ])
    ])


# Campaign Tab Content
def create_campaign_tab():
    today = datetime.now().date()
    future = today + timedelta(days=210)
    
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("تعداد پست مورد نیاز:"),
                    dbc.Input(id="campaign-posts", type="number", value=99, min=1, max=999)
                ], md=12, className="mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("تاریخ شروع:"),
                    dbc.Input(id="campaign-start", type="date", value=today.isoformat())
                ], md=6, className="mb-3"),
                dbc.Col([
                    dbc.Label("تاریخ پایان:"),
                    dbc.Input(id="campaign-end", type="date", value=future.isoformat())
                ], md=6, className="mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("ایجاد کمپین هوشمند", id="campaign-submit", color="info", 
                              className="w-100", size="lg"),
                    dbc.Spinner([html.Div(id="campaign-status", className="mt-3")], color="info")
                ])
            ])
        ])
    ])


# Callbacks

@app.callback(
    Output('site-selector', 'options'),
    Output('site-selector', 'value'),
    Input('site-selector', 'id')
)
def load_sites(_):
    """Load sites from database"""
    sites = get_all_sites()
    if not sites:
        return [], None
    
    options = [{'label': site['site_name'], 'value': site['site_key']} for site in sites]
    return options, sites[0]['site_key'] if sites else None


@app.callback(
    Output('site-data', 'data'),
    Input('site-selector', 'value')
)
def store_site_data(site_key):
    """Store selected site configuration"""
    if not site_key:
        return None
    site = get_site_by_key(site_key)
    return dict(site) if site else None


@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'active_tab')
)
def render_tab_content(active_tab):
    """Render content based on active tab"""
    if active_tab == "blog":
        return create_blog_tab()
    elif active_tab == "keyword":
        return create_keyword_tab()
    elif active_tab == "campaign":
        return create_campaign_tab()
    return html.Div()


@app.callback(
    Output('upload-feedback', 'children'),
    Output('keyword-submit', 'disabled'),
    Output('keyword-upload', 'contents'),
    Input('keyword-upload', 'contents'),
    State('keyword-upload', 'filename')
)
def process_upload(contents, filename):
    """Process uploaded keyword file"""
    if contents is None:
        return "", True, None
    
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Read file based on extension
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return dbc.Alert("فرمت فایل پشتیبانی نمی‌شود. لطفا CSV یا Excel آپلود کنید.", color="danger"), True, None
        
        # Validate columns
        if 'keyword' not in df.columns or 'score' not in df.columns:
            return dbc.Alert("فایل باید دو ستون 'keyword' و 'score' داشته باشد.", color="danger"), True, None
        
        # Validate data
        df = df.dropna(subset=['keyword', 'score'])
        if len(df) == 0:
            return dbc.Alert("فایل خالی است یا داده‌های معتبر ندارد.", color="danger"), True, None
        
        return dbc.Alert(f"✓ {len(df)} کلیدواژه بارگذاری شد: {filename}", color="success"), False, contents
        
    except Exception as e:
        return dbc.Alert(f"خطا در خواندن فایل: {str(e)}", color="danger"), True, None


@app.callback(
    Output('blog-status', 'children'),
    Input('blog-submit', 'n_clicks'),
    State('blog-topic', 'value'),
    State('blog-primary-kw', 'value'),
    State('blog-secondary-kw', 'value'),
    State('blog-style', 'value'),
    State('blog-word-count', 'value'),
    State('site-data', 'data'),
    prevent_initial_call=True
)
def submit_blog_post(n_clicks, topic, primary_kw, secondary_kw, style, word_count, site_data):
    """Submit blog post request"""
    if not all([topic, primary_kw, site_data]):
        return dbc.Alert("لطفا موضوع و کلیدواژه اصلی را وارد کنید.", color="warning")
    
    try:
        secondary = [kw.strip() for kw in (secondary_kw or "").split('\n') if kw.strip()]
        
        payload = {
            "topic": topic,
            "primary_keyword": primary_kw,
            "secondary_keywords": secondary,
            "style": style or "مقاله تخصصی و راهنمای جامع",
            "word_count": int(word_count or 1500),
            "client_config": {
                "domain": site_data['domain'],
                "homepage_url": site_data['homepage_url'],
                "contact_url": site_data['contact_url'],
                "shop_url": site_data['shop_url'],
                "language": site_data['language'],
                "language_code": site_data['language_code'],
                "company_name": site_data['company_name']
            }
        }
        
        response = requests.post(
            site_data['blog_endpoint'],
            json=payload,
            timeout=300
        )
        
        if response.status_code == 200:
            return dbc.Alert("✓ پست وبلاگ با موفقیت ایجاد شد!", color="success")
        else:
            return dbc.Alert(f"خطا: {response.status_code} - {response.text}", color="danger")
            
    except Exception as e:
        return dbc.Alert(f"خطا: {str(e)}", color="danger")


@app.callback(
    Output('keyword-status', 'children'),
    Input('keyword-submit', 'n_clicks'),
    State('keyword-upload', 'contents'),
    State('keyword-upload', 'filename'),
    State('keyword-llm-expand', 'value'),
    State('site-data', 'data'),
    prevent_initial_call=True
)
def submit_keyword_research(n_clicks, contents, filename, llm_expand, site_data):
    """Submit keyword research request"""
    if not contents or not site_data:
        return dbc.Alert("لطفا فایل کلیدواژه را آپلود کنید.", color="warning")
    
    try:
        # Parse uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            df = pd.read_excel(io.BytesIO(decoded))
        
        df = df.dropna(subset=['keyword', 'score'])
        
        # Convert to API format
        keywords = [
            {"keyword": row['keyword'], "score": int(row['score'])}
            for _, row in df.iterrows()
        ]
        
        payload = {
            "schema": site_data['schema_name'],
            "keywords": keywords,
            "expand_with_llm": len(llm_expand) > 0
        }
        
        response = requests.post(
            site_data['keyword_endpoint'],
            json=payload,
            timeout=600
        )
        
        if response.status_code == 200:
            return dbc.Alert(f"✓ تحقیق کلیدواژه با موفقیت انجام شد! ({len(keywords)} کلیدواژه)", color="success")
        else:
            return dbc.Alert(f"خطا: {response.status_code} - {response.text}", color="danger")
            
    except Exception as e:
        return dbc.Alert(f"خطا: {str(e)}", color="danger")


@app.callback(
    Output('campaign-status', 'children'),
    Input('campaign-submit', 'n_clicks'),
    State('campaign-posts', 'value'),
    State('campaign-start', 'value'),
    State('campaign-end', 'value'),
    State('site-data', 'data'),
    prevent_initial_call=True
)
def submit_campaign(n_clicks, posts_needed, start_date, end_date, site_data):
    """Submit smart campaign request"""
    if not all([posts_needed, start_date, end_date, site_data]):
        return dbc.Alert("لطفا تمام فیلدها را پر کنید.", color="warning")
    
    try:
        payload = {
            "schema": site_data['schema_name'],
            "posts_needed": int(posts_needed),
            "start_date": start_date,
            "end_date": end_date
        }
        
        response = requests.post(
            site_data['campaign_endpoint'],
            json=payload,
            timeout=600
        )
        
        if response.status_code == 200:
            return dbc.Alert(f"✓ کمپین هوشمند با موفقیت ایجاد شد! ({posts_needed} پست)", color="success")
        else:
            return dbc.Alert(f"خطا: {response.status_code} - {response.text}", color="danger")
            
    except Exception as e:
        return dbc.Alert(f"خطا: {str(e)}", color="danger")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
