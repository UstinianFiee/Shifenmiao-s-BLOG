from flask import Blueprint, jsonify, current_app
from datetime import datetime

site_bp = Blueprint("site", __name__)

@site_bp.get("/info")
def site_info():
    start_str = current_app.config.get("BLOG_START_DATE", "2025-01-01")
    return jsonify({"blog_start_date": start_str})
