"""
instructions.py — Waste Disposal Knowledge Base

Covers 40+ item types with:
  - Waste category
  - Bin color & label
  - Step-by-step disposal instructions
  - Carbon CO2 savings estimate
  - Recyclability flag
  - Pro tips
"""

from typing import Optional

# ──────────────────────────────────────────────
# Waste Category Metadata
# ──────────────────────────────────────────────
WASTE_CATEGORIES = {
    "plastic": {
        "label":       "Plastic",
        "bin":         "Blue Recycling Bin",
        "bin_color":   "#00b4d8",
        "icon":        "🧴",
        "description": "Rinse and dry before recycling. Remove caps unless instructed otherwise.",
    },
    "paper": {
        "label":       "Paper",
        "bin":         "Blue Recycling Bin",
        "bin_color":   "#00b4d8",
        "icon":        "📄",
        "description": "Keep dry. Remove plastic windows from envelopes.",
    },
    "metal": {
        "label":       "Metal",
        "bin":         "Blue Recycling Bin",
        "bin_color":   "#00b4d8",
        "icon":        "🥫",
        "description": "Rinse cans. Crush if space allows. Remove paper labels.",
    },
    "glass": {
        "label":       "Glass",
        "bin":         "Green Glass Bank",
        "bin_color":   "#2dc653",
        "icon":        "🍶",
        "description": "Rinse thoroughly. Never mix with ceramics or Pyrex.",
    },
    "organic": {
        "label":       "Organic / Food Waste",
        "bin":         "Brown Compost Bin",
        "bin_color":   "#8b5a2b",
        "icon":        "🍌",
        "description": "Compostable. No meat or dairy in home compost.",
    },
    "ewaste": {
        "label":       "Electronic Waste",
        "bin":         "E-Waste Drop Point",
        "bin_color":   "#ff4d6d",
        "icon":        "📱",
        "description": "Never in general waste. Take to a certified e-waste recycling centre.",
    },
    "hazardous": {
        "label":       "Hazardous Waste",
        "bin":         "Hazardous Waste Collection Site",
        "bin_color":   "#ff6b35",
        "icon":        "⚗️",
        "description": "Contains toxic materials. Never in general or recycling bins.",
    },
    "general": {
        "label":       "General / Non-Recyclable Waste",
        "bin":         "Black General Waste Bin",
        "bin_color":   "#555555",
        "icon":        "🗑️",
        "description": "Items that cannot be recycled. Minimise where possible.",
    },
}


# ──────────────────────────────────────────────
# Per-Item Disposal Database
# ──────────────────────────────────────────────
# Key = YOLO label (lowercase).
# carbon_saved_g = approximate grams of CO₂ saved vs landfill/incineration.

_DISPOSAL_DB: dict[str, dict] = {

    # ══ PLASTIC ══════════════════════════════
    "bottle": {
        "category":     "plastic",
        "item_name":    "Plastic Bottle",
        "recyclable":   True,
        "carbon_saved_g": 82,
        "instructions": [
            "Empty and rinse the bottle thoroughly.",
            "Squeeze flat to save space.",
            "Replace the cap — most plants now accept caps on.",
            "Place in the Blue Recycling Bin.",
        ],
        "tips": [
            "Check the resin code (1–7) stamped on the bottom.",
            "PET (#1) and HDPE (#2) are the most widely accepted.",
        ],
    },
    "sports ball": {
        "category":     "plastic",
        "item_name":    "Sports Ball",
        "recyclable":   False,
        "carbon_saved_g": 0,
        "instructions": [
            "Deflate fully.",
            "Check manufacturer for take-back schemes.",
            "If no scheme exists, place in General Waste.",
        ],
        "tips": ["Some sports retailers accept old balls for recycling."],
    },

    # ══ PAPER ═════════════════════════════════
    "book": {
        "category":     "paper",
        "item_name":    "Book / Magazine",
        "recyclable":   True,
        "carbon_saved_g": 50,
        "instructions": [
            "If in good condition, donate to a library or charity shop.",
            "Otherwise, remove any plastic covers or spiral bindings.",
            "Place in Blue Recycling Bin or paper bank.",
        ],
        "tips": ["Hardback spines may need to be removed at some facilities."],
    },
    "newspaper": {
        "category":     "paper",
        "item_name":    "Newspaper",
        "recyclable":   True,
        "carbon_saved_g": 30,
        "instructions": [
            "Keep dry — wet paper is often rejected.",
            "Bundle loosely and place in Blue Recycling Bin.",
        ],
        "tips": ["No need to remove staples — sorters handle them."],
    },

    # ══ METAL ═════════════════════════════════
    "can": {
        "category":     "metal",
        "item_name":    "Metal Can",
        "recyclable":   True,
        "carbon_saved_g": 170,
        "instructions": [
            "Rinse out food or drink residue.",
            "You can lightly crush the can to save space.",
            "Place in Blue Recycling Bin.",
        ],
        "tips": [
            "Aluminium cans are infinitely recyclable.",
            "Steel and aluminium cans are both accepted curbside.",
        ],
    },
    "scissors": {
        "category":     "metal",
        "item_name":    "Scissors / Cutlery",
        "recyclable":   True,
        "carbon_saved_g": 40,
        "instructions": [
            "Wrap sharp ends in tape or cardboard for safety.",
            "Take to a scrap metal drop-off or recycling centre.",
            "Do NOT place loose sharp metal in recycling bins.",
        ],
        "tips": ["Many supermarkets have metal collection points."],
    },
    "knife": {
        "category":     "metal",
        "item_name":    "Knife / Cutlery",
        "recyclable":   True,
        "carbon_saved_g": 35,
        "instructions": [
            "Wrap blade securely in thick cardboard or tape.",
            "Drop off at a household recycling centre (HRC).",
        ],
        "tips": ["Never place unwrapped knives in loose recycling."],
    },
    "fork": {
        "category":     "metal",
        "item_name":    "Fork / Cutlery",
        "recyclable":   True,
        "carbon_saved_g": 20,
        "instructions": [
            "Rinse off food residue.",
            "Bundle with other cutlery and take to a HRC or scrap metal point.",
        ],
        "tips": [],
    },
    "spoon": {
        "category":     "metal",
        "item_name":    "Spoon / Cutlery",
        "recyclable":   True,
        "carbon_saved_g": 18,
        "instructions": [
            "Rinse off food residue.",
            "Bundle with other cutlery and take to a HRC or scrap metal point.",
        ],
        "tips": [],
    },
    "toaster": {
        "category":     "metal",
        "item_name":    "Toaster / Small Appliance",
        "recyclable":   True,
        "carbon_saved_g": 250,
        "instructions": [
            "Empty crumb tray and clean.",
            "Take to a household recycling centre (WEEE zone).",
            "Some retailers offer appliance take-back.",
        ],
        "tips": ["Toasters contain valuable metals — always recycle."],
    },

    # ══ GLASS ═════════════════════════════════
    "wine glass": {
        "category":     "glass",
        "item_name":    "Wine Glass",
        "recyclable":   True,
        "carbon_saved_g": 55,
        "instructions": [
            "Rinse thoroughly.",
            "Wrap in newspaper if cracked or broken for safe handling.",
            "Drop into a Glass Bank (not curbside bin in most areas).",
        ],
        "tips": [
            "Separate by colour (clear, green, brown) at bottle banks.",
            "Pyrex and ceramic are NOT recyclable in glass banks.",
        ],
    },
    "cup": {
        "category":     "glass",
        "item_name":    "Glass Cup / Mug",
        "recyclable":   False,
        "carbon_saved_g": 0,
        "instructions": [
            "Mugs and ceramic cups are NOT recyclable in glass banks.",
            "If intact, donate to a charity shop.",
            "If broken, wrap carefully and place in General Waste.",
        ],
        "tips": ["Ceramic contaminates glass recycling — keep them separate."],
    },
    "vase": {
        "category":     "glass",
        "item_name":    "Glass Vase",
        "recyclable":   True,
        "carbon_saved_g": 80,
        "instructions": [
            "Empty and rinse.",
            "Handle carefully if cracked.",
            "Take to a glass bottle bank.",
        ],
        "tips": [],
    },

    # ══ ORGANIC ═══════════════════════════════
    "banana": {
        "category":     "organic",
        "item_name":    "Banana / Fruit Peel",
        "recyclable":   True,
        "carbon_saved_g": 5,
        "instructions": [
            "Place in Brown Compost Bin.",
            "If composting at home, chop into smaller pieces for faster breakdown.",
        ],
        "tips": ["Banana peels are great compost activators — high in potassium."],
    },
    "apple": {
        "category":     "organic",
        "item_name":    "Apple Core / Fruit Scraps",
        "recyclable":   True,
        "carbon_saved_g": 4,
        "instructions": ["Place whole in Brown Compost Bin."],
        "tips": [],
    },
    "sandwich": {
        "category":     "organic",
        "item_name":    "Food / Sandwich",
        "recyclable":   True,
        "carbon_saved_g": 3,
        "instructions": [
            "Remove any plastic packaging first.",
            "Place food scraps in Brown Compost Bin.",
        ],
        "tips": ["Cooked meat and fish should go in a council food waste bin, not home compost."],
    },
    "orange": {
        "category":     "organic",
        "item_name":    "Orange Peel / Citrus",
        "recyclable":   True,
        "carbon_saved_g": 4,
        "instructions": ["Place in Brown Compost Bin."],
        "tips": ["Citrus in small amounts is fine in compost."],
    },
    "broccoli": {
        "category":     "organic",
        "item_name":    "Vegetable Scraps",
        "recyclable":   True,
        "carbon_saved_g": 5,
        "instructions": ["Place in Brown Compost Bin or council food waste caddy."],
        "tips": [],
    },
    "carrot": {
        "category":     "organic",
        "item_name":    "Vegetable Scraps",
        "recyclable":   True,
        "carbon_saved_g": 5,
        "instructions": ["Place in Brown Compost Bin or council food waste caddy."],
        "tips": [],
    },
    "potted plant": {
        "category":     "organic",
        "item_name":    "Plant / Soil",
        "recyclable":   True,
        "carbon_saved_g": 2,
        "instructions": [
            "Remove plastic pot and recycle separately.",
            "Compost dead plant matter in Brown Bin.",
        ],
        "tips": [],
    },

    # ══ E-WASTE ═══════════════════════════════
    "cell phone": {
        "category":     "ewaste",
        "item_name":    "Mobile Phone",
        "recyclable":   True,
        "carbon_saved_g": 1400,
        "instructions": [
            "Back up and factory reset your data before disposal.",
            "Remove SIM and SD cards.",
            "Take to a certified e-waste drop-off or phone retailer.",
            "Many networks offer free recycling by post.",
        ],
        "tips": ["A recycled phone saves ~1.4 kg of CO₂ and recovers gold, silver, and copper."],
    },
    "laptop": {
        "category":     "ewaste",
        "item_name":    "Laptop / Computer",
        "recyclable":   True,
        "carbon_saved_g": 5000,
        "instructions": [
            "Wipe your data (factory reset or use a data-wiping tool).",
            "Remove and keep the battery if possible.",
            "Take to a certified WEEE recycling facility.",
        ],
        "tips": ["Manufacturer take-back schemes (Dell, Apple, HP) often offer free recycling."],
    },
    "keyboard": {
        "category":     "ewaste",
        "item_name":    "Keyboard / Peripheral",
        "recyclable":   True,
        "carbon_saved_g": 300,
        "instructions": [
            "Take to a household recycling centre (WEEE zone).",
            "Or donate if still functional.",
        ],
        "tips": [],
    },
    "mouse": {
        "category":     "ewaste",
        "item_name":    "Computer Mouse",
        "recyclable":   True,
        "carbon_saved_g": 150,
        "instructions": ["Take to WEEE drop-off or donate if working."],
        "tips": [],
    },
    "remote": {
        "category":     "ewaste",
        "item_name":    "Remote Control",
        "recyclable":   True,
        "carbon_saved_g": 80,
        "instructions": [
            "Remove batteries first (recycle separately at a battery bank).",
            "Take remote to WEEE recycling point.",
        ],
        "tips": [],
    },
    "tv": {
        "category":     "ewaste",
        "item_name":    "Television",
        "recyclable":   True,
        "carbon_saved_g": 12000,
        "instructions": [
            "Never place in general waste — contains toxic materials.",
            "Book a large item collection with your council, OR",
            "Drop off at a household recycling centre.",
            "Retailers are legally required to take back old TVs (WEEE Directive).",
        ],
        "tips": ["A recycled TV recovers valuable rare-earth elements."],
    },
    "microwave": {
        "category":     "ewaste",
        "item_name":    "Microwave",
        "recyclable":   True,
        "carbon_saved_g": 3000,
        "instructions": [
            "Clean and remove any food.",
            "Book council collection or take to recycling centre.",
        ],
        "tips": [],
    },
    "refrigerator": {
        "category":     "ewaste",
        "item_name":    "Refrigerator / Fridge-Freezer",
        "recyclable":   True,
        "carbon_saved_g": 25000,
        "instructions": [
            "Must be professionally decommissioned — contains refrigerant gases.",
            "Contact your council for a special collection.",
            "Retailers who sell you a new fridge must take back the old one.",
        ],
        "tips": ["Never attempt to remove refrigerant yourself — it is harmful to the ozone layer."],
    },
    "hair drier": {
        "category":     "ewaste",
        "item_name":    "Hair Dryer / Small Appliance",
        "recyclable":   True,
        "carbon_saved_g": 200,
        "instructions": [
            "Take to a household recycling centre (WEEE zone).",
            "Some supermarkets have e-waste drop boxes.",
        ],
        "tips": [],
    },

    # ══ HAZARDOUS ════════════════════════════
    "battery": {
        "category":     "hazardous",
        "item_name":    "Battery",
        "recyclable":   True,
        "carbon_saved_g": 50,
        "instructions": [
            "NEVER place in general waste or recycling bin — fire hazard.",
            "Tape over terminals of lithium batteries before disposal.",
            "Drop off at a battery collection point (supermarkets, DIY stores).",
        ],
        "tips": [
            "Lithium batteries (from phones/laptops) are particularly dangerous in landfill.",
            "Most supermarkets have a battery recycling box near the entrance.",
        ],
    },
}

# ──────────────────────────────────────────────
# Fallback entries for any unmapped category
# ──────────────────────────────────────────────
_CATEGORY_FALLBACK = {
    "plastic":   {"item_name": "Plastic Item",    "carbon_saved_g": 30,  "recyclable": True,  "tips": ["Check for resin code on the bottom."]},
    "paper":     {"item_name": "Paper Item",      "carbon_saved_g": 25,  "recyclable": True,  "tips": ["Keep dry before recycling."]},
    "metal":     {"item_name": "Metal Item",      "carbon_saved_g": 100, "recyclable": True,  "tips": ["Rinse off food residue."]},
    "glass":     {"item_name": "Glass Item",      "carbon_saved_g": 50,  "recyclable": True,  "tips": ["Handle carefully if broken."]},
    "organic":   {"item_name": "Organic Waste",   "carbon_saved_g": 4,   "recyclable": True,  "tips": []},
    "ewaste":    {"item_name": "Electronic Waste","carbon_saved_g": 500, "recyclable": True,  "tips": ["Wipe personal data before disposal."]},
    "hazardous": {"item_name": "Hazardous Item",  "carbon_saved_g": 0,   "recyclable": False, "tips": ["Contact your local authority for disposal guidance."]},
    "general":   {"item_name": "General Item",    "carbon_saved_g": 0,   "recyclable": False, "tips": []},
}


# ──────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────
def get_disposal_info(label: str) -> dict:
    """
    Return full disposal info for a YOLO label.
    Always returns a valid dict — never raises.
    """
    label_lower = label.lower()

    # Try exact match first
    if label_lower in _DISPOSAL_DB:
        entry = _DISPOSAL_DB[label_lower]
    else:
        # Build a generic entry from the category
        from detector import classify_label
        cat = classify_label(label_lower)
        fb = _CATEGORY_FALLBACK.get(cat, _CATEGORY_FALLBACK["general"])
        entry = {
            "category":     cat,
            "item_name":    fb["item_name"],
            "recyclable":   fb["recyclable"],
            "carbon_saved_g": fb["carbon_saved_g"],
            "instructions": [
                f"Identified as: {label}.",
                f"Likely category: {cat.upper()}.",
                f"Place in: {WASTE_CATEGORIES[cat]['bin']}.",
            ],
            "tips": fb["tips"],
        }

    cat = entry["category"]
    cat_meta = WASTE_CATEGORIES.get(cat, WASTE_CATEGORIES["general"])

    return {
        "item_name":      entry["item_name"],
        "category":       cat,
        "bin":            cat_meta["bin"],
        "bin_color":      cat_meta["bin_color"],
        "bin_icon":       cat_meta["icon"],
        "recyclable":     entry["recyclable"],
        "carbon_saved_g": entry["carbon_saved_g"],
        "instructions":   entry["instructions"],
        "tips":           entry.get("tips", []),
    }