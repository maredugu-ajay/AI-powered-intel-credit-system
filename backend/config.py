"""
IntelCredit - AI-Powered Credit Decisioning Engine
Configuration Module
"""
import os
# Application Settings
APP_NAME = "IntelCredit"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-Powered Corporate Credit Appraisal Engine"
# Server Settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
# File Upload Settings
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {".pdf", ".xlsx", ".xls", ".csv", ".json", ".txt", ".docx"}
# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./intelcredit.db")
# ML Model Settings
MODEL_DIR = os.path.join(os.path.dirname(__file__), "ml_models")
CREDIT_SCORE_WEIGHTS = {
    "character": 0.20,      # Promoter background, litigation, compliance
    "capacity": 0.25,       # Revenue, cash flow, debt service coverage
    "capital": 0.20,         
    "collateral": 0.15,     # Asset coverage, security value
    "conditions": 0.20,     # Industry outlook, regulatory environment
}
# Risk Thresholds
RISK_THRESHOLDS = {
    "low": (75, 100),
    "moderate": (50, 74),
    "high": (25, 49),
    "very_high": (0, 24),
}
# Interest Rate Bands (basis points above base rate)
RATE_BANDS = {
    "low": 150,        # 1.5% spread
    "moderate": 300,   # 3.0% spread
    "high": 500,       # 5.0% spread
    "very_high": None, # Reject
}
BASE_RATE = 8.50  # RBI repo rate + spread
# Research Agent Settings
NEWS_SEARCH_LIMIT = 20
RESEARCH_TIMEOUT = 30  # seconds
# Indian Context Constants
GST_RATE_SLABS = [0, 5, 12, 18, 28]
CIBIL_SCORE_RANGE = (300, 900)
MIN_ACCEPTABLE_CIBIL = 650
# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)