# SEO Content Generator - Dash Frontend

Professional frontend for your SEO automation workflows with database-driven site management.

## Features

- 🎯 **Database-driven site selector** - All site configs stored in PostgreSQL
- 📝 **Single Blog Post** - Simple form with full customization
- 📊 **Keyword Research** - CSV/Excel upload support (keyword, score columns)
- 🚀 **Smart Campaign** - Date range and bulk post generation
- ⚡ **Persian RTL Support** - Proper right-to-left layout
- 🔄 **Real-time API Integration** - Direct connection to your n8n workflows

## Setup

### 1. Database Setup

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE seo_automation;

# Run schema
\c seo_automation
\i schema.sql
```

### 2. Configure Database Connection

Edit `config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',  # Your DB host
    'port': '5432',
    'database': 'seo_automation',
    'user': 'postgres',
    'password': 'your_password'  # Update this!
}
```

Or use environment variables:
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=seo_automation
export DB_USER=postgres
export DB_PASSWORD=your_password
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python app.py
```

Access at: `http://localhost:8050`

## File Upload Format

For Keyword Research, upload CSV or Excel with exactly 2 columns:

| keyword | score |
|---------|-------|
| مدیریت پروژه | 5 |
| اسکرام | 4 |
| گردش کار | 5 |

## API Endpoints

The app reads endpoints from database. Current structure:

- **Blog Post**: `/webhook/blog_{site_key}`
- **Keyword Research**: `/webhook-test/keyword-research`
- **Campaign**: `/webhook-test/smart-campaign`

## Adding New Sites

```sql
INSERT INTO site_configs (
    site_key, site_name, schema_name,
    blog_endpoint, keyword_endpoint, campaign_endpoint,
    domain, homepage_url, contact_url, shop_url,
    language, language_code, company_name
) VALUES (
    'newsite',
    'NewSite.com (Description)',
    'newsite_schema',
    'https://flowmingo.oxalisys.com/webhook/blog_newsite',
    'https://flowmingo.oxalisys.com/webhook-test/keyword-research',
    'https://flowmingo.oxalisys.com/webhook-test/smart-campaign',
    'newsite.com',
    'https://newsite.com/',
    'https://newsite.com/contact',
    'https://newsite.com/',
    'Persian',
    'fa',
    'Company Name'
);
```

## Troubleshooting

**Database connection fails:**
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in `config.py`
- Check firewall settings

**File upload fails:**
- Ensure columns are named exactly 'keyword' and 'score'
- Check file encoding (UTF-8 recommended for Persian)
- Maximum file size ~10MB

**API timeout:**
- Keyword research can take 5-10 minutes
- Campaign creation can take 10+ minutes
- Increase timeout in `app.py` if needed (currently 300-600s)

## Production Deployment

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn app:server -b 0.0.0.0:8050 --workers 4 --timeout 600
```

Or use systemd service for auto-restart.
