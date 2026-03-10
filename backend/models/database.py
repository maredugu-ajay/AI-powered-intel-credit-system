"""
IntelCredit - In-memory Database Module
Simple in-memory storage for the hackathon prototype.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid


class InMemoryDB:
    """Simple in-memory database for prototype."""
    
    def __init__(self):
        self.companies: Dict[str, Dict] = {}
        self.documents: Dict[str, Dict] = {}
        self.analyses: Dict[str, Dict] = {}
        self.cam_reports: Dict[str, Dict] = {}
        self.primary_insights: Dict[str, List[Dict]] = {}
    
    def store_company(self, company_data: dict) -> str:
        company_id = str(uuid.uuid4())[:8]
        self.companies[company_id] = {
            **company_data,
            "id": company_id,
            "created_at": datetime.now().isoformat()
        }
        return company_id
    
    def store_document(self, filename: str, doc_type: str, extracted_data: dict) -> str:
        doc_id = str(uuid.uuid4())[:8]
        self.documents[doc_id] = {
            "id": doc_id,
            "filename": filename,
            "type": doc_type,
            "extracted_data": extracted_data,
            "uploaded_at": datetime.now().isoformat()
        }
        return doc_id
    
    def store_analysis(self, company_id: str, analysis_data: dict) -> str:
        analysis_id = str(uuid.uuid4())[:8]
        self.analyses[analysis_id] = {
            "id": analysis_id,
            "company_id": company_id,
            **analysis_data,
            "created_at": datetime.now().isoformat()
        }
        return analysis_id
    
    def store_cam_report(self, report_data: dict) -> str:
        report_id = str(uuid.uuid4())[:8]
        self.cam_reports[report_id] = {
            "id": report_id,
            **report_data,
            "generated_at": datetime.now().isoformat()
        }
        return report_id
    
    def add_primary_insight(self, company_id: str, insight: dict) -> None:
        if company_id not in self.primary_insights:
            self.primary_insights[company_id] = []
        self.primary_insights[company_id].append({
            **insight,
            "recorded_at": datetime.now().isoformat()
        })
    
    def get_company(self, company_id: str) -> Optional[Dict]:
        return self.companies.get(company_id)
    
    def get_all_companies(self) -> List[Dict]:
        return list(self.companies.values())
    
    def get_cam_report(self, report_id: str) -> Optional[Dict]:
        return self.cam_reports.get(report_id)
    
    def get_insights(self, company_id: str) -> List[Dict]:
        return self.primary_insights.get(company_id, [])


# Global database instance
db = InMemoryDB()
