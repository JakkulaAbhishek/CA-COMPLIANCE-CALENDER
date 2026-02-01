from datetime import date

COMPLIANCES = [

    # ---------- MONTHLY ----------
    {"name": "PF Payment", "due_day": 15, "frequency": "monthly"},
    {"name": "ESI Payment", "due_day": 15, "frequency": "monthly"},
    {"name": "GST GSTR-3B", "due_day": 20, "frequency": "monthly"},
    {"name": "TDS Payment", "due_day": 7, "frequency": "monthly"},

    # ---------- QUARTERLY ----------
    {"name": "TDS Return (24Q/26Q/27Q)", "due_day": 31, "frequency": "quarterly"},
    {"name": "GSTR-1 (Quarterly)", "due_day": 13, "frequency": "quarterly"},

    # ---------- ANNUAL ----------
    {"name": "GSTR-9", "due_date": (12, 31)},
    {"name": "GSTR-9C", "due_date": (12, 31)},
    {"name": "Income Tax Return (Non-Audit)", "due_date": (7, 31)},
    {"name": "Income Tax Return (Audit)", "due_date": (10, 31)},
    {"name": "Tax Audit Report", "due_date": (9, 30)},
    {"name": "Transfer Pricing Return (3CEB)", "due_date": (11, 30)},

    # ---------- ROC ----------
    {"name": "AOC-4", "due_date": (10, 30)},
    {"name": "MGT-7", "due_date": (11, 30)},

    # ---------- ADVANCE TAX ----------
    {"name": "Advance Tax Installment 1", "due_date": (6, 15)},
    {"name": "Advance Tax Installment 2", "due_date": (9, 15)},
    {"name": "Advance Tax Installment 3", "due_date": (12, 15)},
    {"name": "Advance Tax Installment 4", "due_date": (3, 15)},
]
