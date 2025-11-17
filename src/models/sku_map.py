SKU_MAP = {
    "salad green": 1101,
    "salad purple": 1110,
    "salad orange": 1115,
    "yogurt blue": 2606,
    "yogurt yellow": 2604,
    "oats purple": 2401,
    "wrap blue": 1601,
    "wrap brown": 1602,
    "wrap yellow": 1603,
    "wrap green": 1604,
    "pudding": 2706,
}

def normalize_label(label: str) -> str:
    """
    Normalize class label from YOLO into a consistent format.
    Example: "Salad Green" → "salad green"
    """
    return label.strip().lower()
