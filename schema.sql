-- Database schema for SEO frontend site configurations

-- Create util schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS util;

-- Create the site_configs table in util schema
CREATE TABLE IF NOT EXISTS util.site_configs (
    id SERIAL PRIMARY KEY,
    site_key VARCHAR(50) UNIQUE NOT NULL,
    site_name VARCHAR(100) NOT NULL,
    schema_name VARCHAR(50) NOT NULL,
    blog_endpoint VARCHAR(255) NOT NULL,
    keyword_endpoint VARCHAR(255) NOT NULL,
    campaign_endpoint VARCHAR(255) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    homepage_url VARCHAR(255) NOT NULL,
    contact_url VARCHAR(255) NOT NULL,
    shop_url VARCHAR(255) NOT NULL,
    language VARCHAR(50) NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert seed data for the 4 sites
INSERT INTO util.site_configs (
    site_key, site_name, schema_name, 
    blog_endpoint, keyword_endpoint, campaign_endpoint,
    domain, homepage_url, contact_url, shop_url,
    language, language_code, company_name
) VALUES 
(
    'worket',
    'Worket.pro (مدیریت پروژه)',
    'worket',
    'https://flowmingo.oxalisys.com/webhook/blog_workett',
    'https://flowmingo.oxalisys.com/webhook-test/keyword-research',
    'https://flowmingo.oxalisys.com/webhook-test/smart-campaign',
    'blog.worket.pro',
    'https://worket.pro/',
    'https://worket.pro/contact-us',
    'https://worket.pro/',
    'Persian',
    'fa',
    'شرکت نرم افزاری وورکت'
),
(
    'abzar',
    'AbzarDaghighAria.com (ابزار صنعتی)',
    'abzar',
    'https://flowmingo.oxalisys.com/webhook/blog_abzar',
    'https://flowmingo.oxalisys.com/webhook-test/keyword-research',
    'https://flowmingo.oxalisys.com/webhook-test/smart-campaign',
    'abzardaghigharia.com',
    'https://abzardaghigharia.com/',
    'https://abzardaghigharia.com/contact',
    'https://abzardaghigharia.com/shop',
    'Persian',
    'fa',
    'ابزار دقیق آریا'
),
(
    'finoxsys',
    'Finoxsys.com (نرم‌افزار مالی)',
    'finoxsys',
    'https://flowmingo.oxalisys.com/webhook/blog_finoxsys',
    'https://flowmingo.oxalisys.com/webhook-test/keyword-research',
    'https://flowmingo.oxalisys.com/webhook-test/smart-campaign',
    'finoxsys.com',
    'https://finoxsys.com/',
    'https://finoxsys.com/contact',
    'https://finoxsys.com/',
    'Persian',
    'fa',
    'فینوکسیس'
),
(
    'oxalisys',
    'Oxalisys.com (هوش تجاری)',
    'oxalisys',
    'https://flowmingo.oxalisys.com/webhook/blog_oxalisys',
    'https://flowmingo.oxalisys.com/webhook-test/keyword-research',
    'https://flowmingo.oxalisys.com/webhook-test/smart-campaign',
    'oxalisys.com',
    'https://oxalisys.com/',
    'https://oxalisys.com/contact',
    'https://oxalisys.com/',
    'Persian',
    'fa',
    'اکسالیسیس'
);
