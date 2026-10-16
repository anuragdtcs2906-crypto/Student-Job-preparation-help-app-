from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import random


@dataclass
class RecommendationItem:
    content_id: str
    content_type: str
    reason: str  # new_level, difficult_item, spaced_revision, target_fulfillment
    reason_label: str
    priority: int  # 1 (low) to 5 (high)
    data: Optional[Dict[str, Any]] = None


class RecommendationStrategy:
    """
    Allocates practice item quotas based on target count and user history.
    """

    @staticmethod
    def calculate_distribution(target_count: int, has_revision: bool, has_difficult: bool) -> Dict[str, int]:
        """
        Calculate ideal distribution for practice items.
        Example for 10 items: 5 new, 3 difficult, 2 revision.
        """
        if target_count <= 2:
            return {"new": target_count, "difficult": 0, "revision": 0}

        if has_revision and has_difficult:
            new_count = max(1, int(target_count * 0.5))
            diff_count = max(1, int(target_count * 0.3))
            rev_count = max(0, target_count - new_count - diff_count)
            return {"new": new_count, "difficult": diff_count, "revision": rev_count}
        elif has_revision:
            new_count = max(1, int(target_count * 0.7))
            rev_count = target_count - new_count
            return {"new": new_count, "difficult": 0, "revision": rev_count}
        elif has_difficult:
            new_count = max(1, int(target_count * 0.7))
            diff_count = target_count - new_count
            return {"new": new_count, "difficult": diff_count, "revision": 0}
        else:
            return {"new": target_count, "difficult": 0, "revision": 0}
