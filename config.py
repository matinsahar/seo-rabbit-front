"""
Database configuration
Update these values with your PostgreSQL credentials
"""

import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '103.75.199.47'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'n8n'),
    'user': os.getenv('DB_USER', 'n8n'),
    'password': os.getenv('DB_PASSWORD', 'n8n_password')
}
