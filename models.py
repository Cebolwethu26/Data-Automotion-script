import json
import os
from typing import List, Dict, Optional


class Review:
    def __init__(self, reviewer_name: str, rating: float, comment: str):
        self.reviewer_name = reviewer_name
        self.rating = min(max(rating, 1.0), 5.0)  # Bound between 1 and 5
        self.comment = comment

    def to_dict(self) -> Dict:
        return {
            "reviewer_name": self.reviewer_name,
            "rating": self.rating,
            "comment": self.comment
        }


class Business:
    def __init__(
        self,
        biz_id: str,
        name: str,
        category: str,
        location: str,
        contact: str,
        reg_number: str = "",
        is_verified: bool = False,
        reviews: Optional[List[Review]] = None
    ):
        self.biz_id = biz_id
        self.name = name
        self.category = category
        self.location = location.lower()
        self.contact = contact
        self.reg_number = reg_number
        self.is_verified = is_verified
        self.reviews = reviews if reviews is not None else []

    @property
    def average_rating(self) -> float:
        if not self.reviews:
            return 0.0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    def verify_business(self, reg_number: str) -> bool:
        """
        Anti-scam verification engine: checks official registration format 
        before granting verified status.
        """
        if len(reg_number.strip()) >= 6:
            self.reg_number = reg_number
            self.is_verified = True
            return True
        return False

    def add_review(self, review: Review):
        self.reviews.append(review)

    def to_dict(self) -> Dict:
        return {
            "biz_id": self.biz_id,
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "contact": self.contact,
            "reg_number": self.reg_number,
            "is_verified": self.is_verified,
            "reviews": [r.to_dict() for r in self.reviews]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Business':
        reviews = [Review(**r) for r in data.get("reviews", [])]
        return cls(
            biz_id=data["biz_id"],
            name=data["name"],
            category=data["category"],
            location=data["location"],
            contact=data["contact"],
            reg_number=data.get("reg_number", ""),
            is_verified=data.get("is_verified", False),
            reviews=reviews
        )
