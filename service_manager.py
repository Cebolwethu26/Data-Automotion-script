import json
import os
from typing import List, Optional
from models import Business, Review


class MarketplaceManager:
    def __init__(self, storage_file: str = "data.json"):
        self.storage_file = storage_file
        self.businesses: List[Business] = []
        self.load_data()

    def load_data(self):
        """Loads business database from local JSON file."""
        if not os.path.exists(self.storage_file):
            self.seed_initial_data()
            return

        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
                self.businesses = [Business.from_dict(b) for b in data]
        except (json.JSONDecodeError, KeyError):
            self.businesses = []

    def save_data(self):
        """Persists current state to JSON disk storage."""
        with open(self.storage_file, "w") as f:
            json.dump([b.to_dict() for b in self.businesses], f, indent=4)

    def register_business(self, name: str, category: str, location: str, contact: str, reg_num: str = "") -> Business:
        biz_id = f"BIZ-{len(self.businesses) + 101}"
        new_biz = Business(biz_id, name, category, location, contact)
        
        if reg_num:
            new_biz.verify_business(reg_num)
            
        self.businesses.append(new_biz)
        self.save_data()
        return new_biz

    def search_services(self, location: str, category: Optional[str] = None, verified_only: bool = False) -> List[Business]:
        """Filters listings by location, optional service category, and verification status."""
        loc = location.lower().strip()
        results = []

        for biz in self.businesses:
            match_loc = loc in biz.location
            match_cat = (category.lower() in biz.category.lower()) if category else True
            match_ver = biz.is_verified if verified_only else True

            if match_loc and match_cat and match_ver:
                results.append(biz)

        return results

    def add_review_to_business(self, biz_id: str, reviewer: str, rating: float, comment: str) -> bool:
        for biz in self.businesses:
            if biz.biz_id.upper() == biz_id.upper():
                biz.add_review(Review(reviewer, rating, comment))
                self.save_data()
                return True
        return False

    def seed_initial_data(self):
        """Seeds initial sample data for demonstration/testing."""
        b1 = Business("BIZ-101", "Glow Nails & Beauty", "Nail Tech", "Boksburg", "0712345678", "REG-882190", True)
        b1.add_review(Review("Sipho", 5.0, "Excellent house call service! Very professional."))
        b1.add_review(Review("Lindiwe", 4.5, "On time and great quality nails."))

        b2 = Business("BIZ-102", "Boksburg Auto Repair", "Mechanic", "Boksburg", "0829876543", "REG-334112", True)
        b2.add_review(Review("Kagiso", 5.0, "Fixed my car fast, trusted mechanic."))

        b3 = Business("BIZ-103", "Trendy Hair Studio", "Hairdresser", "Johannesburg", "0631112223", "", False)

        self.businesses = [b1, b2, b3]
        self.save_data()
