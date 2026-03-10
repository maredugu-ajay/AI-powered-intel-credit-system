"""
IntelCredit - Document Parser Service
Handles extraction of data from PDFs, Excel files, and other documents.
Supports Annual Reports, GST Returns, Bank Statements, ITRs, etc.
"""
import os
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class DocumentParser:
    """
    Multi-format document parser for Indian corporate credit documents.
    Extracts structured data from PDFs, Excel files, and other formats.
    """
    
    def __init__(self):
        self.extraction_patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict[str, List[Dict]]:
        """Load regex patterns for Indian financial document extraction."""
        return {
            "revenue": [
                r"(?:total\s+)?(?:revenue|income|turnover|sales)[\s:]*(?:from\s+operations)?[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)\s*(?:cr|crore|lakh|lakhs|million)?",
                r"(?:net\s+)?sales[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            ],
            "ebitda": [
                r"EBITDA[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
                r"(?:operating\s+)?profit\s+before\s+(?:interest|depreciation)[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            ],
            "pat": [
                r"(?:profit|loss)\s+after\s+tax[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
                r"PAT[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
                r"net\s+(?:profit|income)[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            ],
            "total_assets": [
                r"total\s+assets[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            ],
            "net_worth": [
                r"(?:net\s+worth|shareholders?\s*(?:equity|funds?))[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            ],
            "total_debt": [
                r"total\s+(?:debt|borrowings?)[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
                r"(?:long\s+term|short\s+term)\s+borrowings?[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            ],
            "cin": [
                r"CIN[\s:]*([A-Z]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6})",
            ],
            "gstin": [
                r"GSTIN[\s:]*(\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d{1}[A-Z]{1}\d{1})",
            ],
            "pan": [
                r"PAN[\s:]*([A-Z]{5}\d{4}[A-Z]{1})",
            ],
        }
    
    async def parse_document(self, file_path: str, doc_type: str) -> Dict[str, Any]:
        """
        Parse a document based on its type and extract relevant data.
        """
        extension = os.path.splitext(file_path)[1].lower()
        
        if extension == ".pdf":
            return await self._parse_pdf(file_path, doc_type)
        elif extension in (".xlsx", ".xls"):
            return await self._parse_excel(file_path, doc_type)
        elif extension == ".csv":
            return await self._parse_csv(file_path, doc_type)
        elif extension == ".json":
            return await self._parse_json(file_path, doc_type)
        else:
            return {"error": f"Unsupported file format: {extension}"}
    
    async def _parse_pdf(self, file_path: str, doc_type: str) -> Dict[str, Any]:
        """Extract data from PDF documents using PyMuPDF."""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(file_path)
            full_text = ""
            pages_data = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                full_text += text + "\n"
                pages_data.append({
                    "page": page_num + 1,
                    "text_length": len(text),
                    "has_tables": bool(page.find_tables()),
                })
            
            doc.close()
            
            # Route to specific parser based on document type
            extracted = {
                "raw_text_length": len(full_text),
                "total_pages": len(pages_data),
                "pages_info": pages_data[:5],  # First 5 pages info
            }
            
            if doc_type == "annual_report":
                extracted.update(self._extract_annual_report_data(full_text))
            elif doc_type == "financial_statement":
                extracted.update(self._extract_financial_data(full_text))
            elif doc_type == "gst_return":
                extracted.update(self._extract_gst_data(full_text))
            elif doc_type == "bank_statement":
                extracted.update(self._extract_bank_statement_data(full_text))
            elif doc_type == "itr":
                extracted.update(self._extract_itr_data(full_text))
            elif doc_type == "legal_notice":
                extracted.update(self._extract_legal_data(full_text))
            elif doc_type == "sanction_letter":
                extracted.update(self._extract_sanction_data(full_text))
            elif doc_type == "rating_report":
                extracted.update(self._extract_rating_data(full_text))
            else:
                extracted.update(self._extract_general_data(full_text))
            
            return extracted
            
        except ImportError:
            return {"error": "PDF parsing library (PyMuPDF) not available. Please install it with: pip install pymupdf"}
        except Exception as e:
            return {"error": str(e)}
    
    async def _parse_excel(self, file_path: str, doc_type: str) -> Dict[str, Any]:
        """Parse Excel files for financial data."""
        try:
            import pandas as pd
            
            xls = pd.ExcelFile(file_path)
            sheets_data = {}
            
            for sheet in xls.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet)
                sheets_data[sheet] = {
                    "rows": len(df),
                    "columns": list(df.columns),
                    "sample": df.head(5).to_dict(orient="records"),
                }
            
            return {
                "sheets": list(xls.sheet_names),
                "data": sheets_data,
                "document_type": doc_type,
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _parse_csv(self, file_path: str, doc_type: str) -> Dict[str, Any]:
        """Parse CSV files."""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            return {
                "rows": len(df),
                "columns": list(df.columns),
                "sample": df.head(10).to_dict(orient="records"),
                "document_type": doc_type,
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _parse_json(self, file_path: str, doc_type: str) -> Dict[str, Any]:
        """Parse JSON files."""
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return {"data": data, "document_type": doc_type}
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_value(self, text: str, patterns: List[str]) -> Optional[float]:
        """Extract numeric value using regex patterns."""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value_str = match.group(1).replace(",", "")
                try:
                    return float(value_str)
                except ValueError:
                    continue
        return None
    
    def _extract_annual_report_data(self, text: str) -> Dict[str, Any]:
        """Extract key data from annual reports."""
        data = {
            "type": "annual_report",
            "company_identifiers": {},
            "financial_highlights": {},
            "key_risks": [],
            "commitments": [],
        }
        
        # Extract identifiers
        for key in ["cin", "gstin", "pan"]:
            patterns = self.extraction_patterns.get(key, [])
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    data["company_identifiers"][key] = match.group(1)
                    break
        
        # Extract financial highlights
        for key in ["revenue", "ebitda", "pat", "total_assets", "net_worth", "total_debt"]:
            value = self._extract_value(text, self.extraction_patterns.get(key, []))
            if value:
                data["financial_highlights"][key] = value
        
        # Extract risk mentions
        risk_keywords = [
            "risk factor", "contingent liabilit", "pending litigation",
            "regulatory action", "going concern", "material uncertainty",
            "default", "NPA", "overdue", "stress"
        ]
        for keyword in risk_keywords:
            if keyword.lower() in text.lower():
                # Extract surrounding context
                idx = text.lower().find(keyword.lower())
                context = text[max(0, idx-100):idx+200].strip()
                data["key_risks"].append({
                    "keyword": keyword,
                    "context": context[:300],
                })
        
        # Extract commitments
        commitment_patterns = [
            r"(?:capital\s+)?commitment[s]?\s+(?:of|worth|amounting)\s+[₹Rs.\s]*([\d,]+\.?\d*)\s*(?:cr|crore|lakh)",
            r"guarantee[s]?\s+(?:of|worth|given)\s+[₹Rs.\s]*([\d,]+\.?\d*)",
        ]
        for pattern in commitment_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                data["commitments"].append({
                    "amount": match.group(1),
                    "context": match.group(0)[:200],
                })
        
        return data
    
    def _extract_financial_data(self, text: str) -> Dict[str, Any]:
        """Extract data from financial statements."""
        data = {
            "type": "financial_statement",
            "profit_loss": {},
            "balance_sheet": {},
            "ratios": {},
        }
        
        # P&L items
        for key in ["revenue", "ebitda", "pat"]:
            value = self._extract_value(text, self.extraction_patterns.get(key, []))
            if value:
                data["profit_loss"][key] = value
        
        # Balance sheet items
        for key in ["total_assets", "net_worth", "total_debt"]:
            value = self._extract_value(text, self.extraction_patterns.get(key, []))
            if value:
                data["balance_sheet"][key] = value
        
        return data
    
    def _extract_gst_data(self, text: str) -> Dict[str, Any]:
        """Extract GST return data."""
        data = {
            "type": "gst_return",
            "gstr1_data": [],
            "gstr3b_data": [],
            "mismatches": [],
        }
        
        # GST-specific patterns
        gstr_patterns = {
            "taxable_value": r"(?:taxable\s+value|total\s+taxable)[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            "igst": r"IGST[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            "cgst": r"CGST[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            "sgst": r"SGST[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
            "itc": r"(?:ITC|input\s+tax\s+credit)[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)",
        }
        
        for key, pattern in gstr_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["gstr3b_data"].append({key: float(match.group(1).replace(",", ""))})
        
        return data
    
    def _extract_bank_statement_data(self, text: str) -> Dict[str, Any]:
        """Extract bank statement data."""
        data = {
            "type": "bank_statement",
            "transactions": [],
            "summary": {},
            "cheque_bounces": 0,
            "emi_payments": [],
        }
        
        # Look for bounce indicators
        bounce_count = len(re.findall(r"(?:bounce|return|dishono)", text, re.IGNORECASE))
        data["cheque_bounces"] = bounce_count
        
        # Extract balances
        balance_pattern = r"(?:closing|opening)\s+balance[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)"
        balances = re.findall(balance_pattern, text, re.IGNORECASE)
        if balances:
            data["summary"]["balances_found"] = [float(b.replace(",", "")) for b in balances[:10]]
        
        return data
    
    def _extract_itr_data(self, text: str) -> Dict[str, Any]:
        """Extract ITR data."""
        return {
            "type": "itr",
            "gross_income": self._extract_value(text, [r"gross\s+(?:total\s+)?income[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)"]),
            "total_income": self._extract_value(text, [r"total\s+income[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)"]),
            "tax_paid": self._extract_value(text, [r"(?:tax\s+paid|total\s+tax)[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)"]),
        }
    
    def _extract_legal_data(self, text: str) -> Dict[str, Any]:
        """Extract data from legal notices."""
        return {
            "type": "legal_notice",
            "parties_mentioned": re.findall(r"(?:M/s|Shri|Smt|Mr\.|Mrs\.|Ms\.)\s+([A-Z][a-zA-Z\s]+)", text)[:10],
            "amounts_mentioned": [float(a.replace(",", "")) for a in re.findall(r"[₹Rs.\s]*([\d,]+\.?\d*)\s*(?:cr|crore|lakh)", text, re.IGNORECASE)][:10],
            "case_numbers": re.findall(r"(?:case|suit|wp|oa|ma)[\s.]*(?:no|number)?[\s.:]*(\d+[/\-]\d+)", text, re.IGNORECASE)[:10],
            "courts": re.findall(r"(?:high\s+court|supreme\s+court|tribunal|NCLT|DRT|district\s+court)[^.]*", text, re.IGNORECASE)[:5],
        }
    
    def _extract_sanction_data(self, text: str) -> Dict[str, Any]:
        """Extract data from bank sanction letters."""
        return {
            "type": "sanction_letter",
            "sanctioned_amount": self._extract_value(text, [r"(?:sanctioned?|approved?|limit)\s+(?:amount|of)[\s:]*[₹Rs.\s]*([\d,]+\.?\d*)"]),
            "interest_rate": self._extract_value(text, [r"(?:interest|rate)[\s:]*(\d+\.?\d*)\s*%"]),
            "tenure": self._extract_value(text, [r"(?:tenure|period|term)[\s:]*(\d+)\s*(?:months?|years?)"]),
            "security": re.findall(r"(?:security|collateral|hypothecation|mortgage)[^.]*\.", text, re.IGNORECASE)[:5],
        }
    
    def _extract_rating_data(self, text: str) -> Dict[str, Any]:
        """Extract credit rating data."""
        rating_patterns = [
            r"((?:CRISIL|ICRA|CARE|FITCH|IND-RA|BWR|ACUITE)\s*[A-D]+[+-]?\d*)",
            r"rating[s]?\s*(?:of|:)\s*([A-D]+[+-]?\d*)",
        ]
        ratings = []
        for pattern in rating_patterns:
            ratings.extend(re.findall(pattern, text, re.IGNORECASE))
        
        return {
            "type": "rating_report",
            "ratings_found": ratings[:10],
            "outlook": "stable" if "stable" in text.lower() else ("positive" if "positive" in text.lower() else "negative"),
            "rating_agency": re.findall(r"(CRISIL|ICRA|CARE|FITCH|India Ratings|BWR|Acuite)", text, re.IGNORECASE)[:3],
        }
    
    def _extract_general_data(self, text: str) -> Dict[str, Any]:
        """General extraction for unclassified documents."""
        data = {"type": "general", "identifiers": {}, "financial_values": {}}
        for key in ["cin", "gstin", "pan"]:
            for pattern in self.extraction_patterns.get(key, []):
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    data["identifiers"][key] = match.group(1)
                    break
        for key in ["revenue", "pat", "net_worth"]:
            value = self._extract_value(text, self.extraction_patterns.get(key, []))
            if value:
                data["financial_values"][key] = value
        return data

# Global parser instance
document_parser = DocumentParser()
