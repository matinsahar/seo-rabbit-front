"""
Database utilities for SEO frontend
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG


def get_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)


def get_all_sites():
    """Fetch all active sites from database"""
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT site_key, site_name, schema_name,
                   blog_endpoint, keyword_endpoint, campaign_endpoint,
                   domain, homepage_url, contact_url, shop_url,
                   language, language_code, company_name
            FROM util.site_configs
            WHERE active = true
            ORDER BY site_name
        """)
        sites = cur.fetchall()
        cur.close()
        conn.close()
        return sites
    except Exception as e:
        print(f"Database error: {e}")
        return []


def get_site_by_key(site_key):
    """Fetch specific site configuration"""
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT site_key, site_name, schema_name,
                   blog_endpoint, keyword_endpoint, campaign_endpoint,
                   domain, homepage_url, contact_url, shop_url,
                   language, language_code, company_name
            FROM util.site_configs
            WHERE site_key = %s AND active = true
        """, (site_key,))
        site = cur.fetchone()
        cur.close()
        conn.close()
        return site
    except Exception as e:
        print(f"Database error: {e}")
        return None
