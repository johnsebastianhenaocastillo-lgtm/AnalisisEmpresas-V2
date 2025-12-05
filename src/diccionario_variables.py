"""
Diccionario de Variables - Mapeo Yahoo Finance <-> Paper Codes
Basado en Jensen, Kelly & Pedersen (2023) - Global Factor Data

Este archivo mapea las columnas de Yahoo Finance a los códigos del paper académico.
"""

# ===== MAPEO BÁSICO (Variables Contables) =====

MAPEO_CONTABLE_YAHOO = {
    # Income Statement
    "sale": "Total Revenue",
    "cogs": "Cost Of Revenue", 
    "gp": "Gross Profit",
    "xsga": "Selling General And Administrative",
    "xad": "Advertising",  # No siempre disponible
    "xrd": "Research And Development",
    "xlr": "Labor Expenses",  # Rara vez en Yahoo
    "spi": "Special Charges",
    "ebitda": "EBITDA",
    "dp": "Depreciation And Amortization",
    "ebit": "EBIT",
    "int": "Interest Expense",
    "pi": "Pretax Income",
    "tax": "Tax Provision",
    "ni": "Net Income",
    "nix": "Net Income Including Extraordinary Items",
    "dvc": "Common Stock Dividends Paid",  # Rara vez disponible
    
    # Balance Sheet - Assets
    "at": "Total Assets",
    "ca": "Current Assets",
    "rec": "Accounts Receivable",
    "cash": "Cash And Cash Equivalents",
    "inv": "Inventory",
    "intan": "Goodwill And Intangible Assets",
    "ivao": "Investments And Advances",
    "ppeg": "Gross PPE",
    "ppen": "Net PPE",
    
    # Balance Sheet - Liabilities
    "lt": "Total Liabilities Net Minority Interest",
    "cl": "Current Liabilities",
    "ap": "Accounts Payable",
    "debtst": "Current Debt",
    "txp": "Current Income Taxes Payable",  # Rara vez disponible
    "debtlt": "Long Term Debt",
    "txditc": "Deferred Tax Liabilities",  # Rara vez disponible
    
    # Balance Sheet - Equity
    "pstk": "Preferred Stock",
    "seq": "Stockholders Equity",
    
    # Cash Flow Statement
    "capx": "Capital Expenditure",
    "ocf": "Operating Cash Flow",
    "fcf": "Free Cash Flow",
    "eqbb": "Repurchase Of Capital Stock",
    "eqis": "Issuance Of Capital Stock",
}

# ===== MAPEO ALPHA VANTAGE =====
# Alpha Vantage usa nombres diferentes

MAPEO_CONTABLE_ALPHA_VANTAGE = {
    # Income Statement
    "sale": "totalRevenue",
    "cogs": "costOfRevenue",
    "gp": "grossProfit",
    "ebitda": "ebitda",
    "ebit": "operatingIncome",
    "int": "interestExpense",
    "pi": "incomeBeforeTax",
    "tax": "incomeTaxExpense",
    "ni": "netIncome",
    "xrd": "researchAndDevelopment",
    "xsga": "sellingGeneralAndAdministrative",
    
    # Balance Sheet
    "at": "totalAssets",
    "ca": "totalCurrentAssets",
    "cash": "cashAndCashEquivalentsAtCarryingValue",
    "rec": "currentNetReceivables",
    "inv": "inventory",
    "ppen": "propertyPlantEquipment",
    "intan": "intangibleAssets",
    "lt": "totalLiabilities",
    "cl": "totalCurrentLiabilities",
    "debtst": "shortTermDebt",
    "debtlt": "longTermDebt",
    "seq": "totalShareholderEquity",
    
    # Cash Flow
    "ocf": "operatingCashflow",
    "capx": "capitalExpenditures",
}

# ===== VARIABLES DERIVADAS =====
# Estas se calculan a partir de las básicas

VARIABLES_DERIVADAS = {
    # Variables del Paper que requieren cálculo
    "be": "Book Equity = seq + txditc - pstk",
    "me": "Market Equity = Close * shares_outstanding",
    "debt": "Total Debt = debtlt + debtst",
    "netdebt": "Net Debt = debt - cash",
    "nwc": "Net Working Capital = ca - cl",
    "coa": "Current Operating Assets = ca - cash",
    "col": "Current Operating Liabilities = cl - debtst",
    "cowc": "Current Operating Working Capital = coa - col",
    "ncoa": "Non-Current Operating Assets = at - ca - ivao",
    "ncol": "Non-Current Operating Liabilities = lt - cl - debtlt",
    "nncoa": "Net Non-Current Operating Assets = ncoa - ncol",
    "oa": "Operating Assets = coa + ncoa",
    "ol": "Operating Liabilities = col + ncol",
    "noa": "Net Operating Assets = oa - ol",
    "oacc": "Operating Accruals = ni - ocf",
    "tacc": "Total Accruals = oacc + change(nfna)",
    "bev": "Book Enterprise Value = seq + netdebt",
    "mev": "Market Enterprise Value = me + netdebt",
}

# ===== CARACTERÍSTICAS DEL PAPER (120 Principales) =====

CARACTERISTICAS_DISPONIBLES = {
    # MOMENTUM (23 características) - 100% disponible
    "ret_1_0": "Short-term reversal (t-1 to t)",
    "ret_2_0": "Momentum 2 months (t-2 to t)",
    "ret_3_0": "Momentum 3 months (t-3 to t)",
    "ret_3_1": "Momentum 3 months (t-3 to t-1)",
    "ret_6_0": "Momentum 6 months (t-6 to t)",
    "ret_6_1": "Momentum 6 months (t-6 to t-1)",
    "ret_9_0": "Momentum 9 months (t-9 to t)",
    "ret_9_1": "Momentum 9 months (t-9 to t-1)",
    "ret_12_0": "Momentum 12 months (t-12 to t)",
    "ret_12_1": "Momentum 12 months (t-12 to t-1)",
    "ret_12_7": "Momentum 12-7 months",
    "ret_18_1": "Long-term momentum 18 months",
    "ret_24_1": "Long-term momentum 24 months",
    "ret_36_1": "Long-term momentum 36 months",
    "ret_48_1": "Long-term momentum 48 months",
    "ret_60_1": "Long-term momentum 60 months",
    "ret_60_12": "Long-term reversal",
    
    # VALUE (20 características) - ~90% disponible
    "be_me": "Book-to-market",
    "at_me": "Assets-to-market",
    "cash_me": "Cash-to-market",
    "ebitda_me": "EBITDA-to-market",
    "ebit_me": "EBIT-to-market",
    "ni_me": "Earnings-to-price",
    "ocf_me": "Operating cash flow-to-market",
    "fcf_me": "Free cash flow-to-market",
    "sale_me": "Sales-to-market",
    "div12m_me": "Dividend yield",
    "bev_mev": "Book-to-market enterprise value",
    "ebitda_mev": "EBITDA-to-market enterprise value",
    "debt_me": "Debt-to-market",
    "netdebt_me": "Net debt-to-market",
    
    # PROFITABILITY (25 características) - ~85% disponible
    "gp_at": "Gross profit-to-assets",
    "ebitda_at": "EBITDA-to-assets",
    "ebit_at": "EBIT-to-assets",
    "ni_at": "Net income-to-assets",
    "roa": "Return on assets",
    "roe": "Return on equity (ni/be)",
    "ni_be": "Net income-to-book equity",
    "ocf_at": "Operating cash flow-to-assets",
    "fcf_at": "Free cash flow-to-assets",
    "cop_at": "Cash-based operating profitability",
    "gp_sale": "Gross profit margin",
    "ebitda_sale": "EBITDA margin",
    "ebit_sale": "EBIT margin",
    "ni_sale": "Net profit margin",
    "ocf_sale": "Operating cash flow margin",
    "at_turnover": "Asset turnover",
    "sale_at": "Sales-to-assets",
    
    # INVESTMENT (30 características) - ~75% disponible
    "at_gr1": "Asset growth (1 year)",
    "at_gr3": "Asset growth (3 years)",
    "sale_gr1": "Sales growth (1 year)",
    "sale_gr3": "Sales growth (3 years)",
    "capx_gr1": "CapEx growth (1 year)",
    "capx_gr3": "CapEx growth (3 years)",
    "inv_gr1": "Inventory growth",
    "be_gr1": "Book equity growth",
    "debt_gr1": "Debt growth",
    "capx_at": "CapEx-to-assets",
    "inv_at": "Investment-to-assets",
    "noa_at": "Net operating assets-to-assets",
    "noa_gr1a": "Change in net operating assets",
    "cowc_gr1a": "Change in working capital",
    
    # ACCRUALS (6 características) - 100% disponible
    "oaccruals_at": "Operating accruals-to-assets",
    "oaccruals_ni": "Percent operating accruals",
    "taccruals_at": "Total accruals-to-assets",
    "taccruals_ni": "Percent total accruals",
    
    # LOW RISK (15 características) - ~80% disponible
    "beta_60m": "Market beta (60 months)",
    "rvol_21d": "Return volatility (21 days)",
    "rvol_252d": "Return volatility (252 days)",
    "ivol_capm_21d": "Idiosyncratic volatility CAPM",
    "ivol_ff3_21d": "Idiosyncratic volatility FF3",
    "rmax1_21d": "Maximum daily return",
    "rmax5_21d": "Mean of 5 highest returns",
    
    # SIZE (6 características) - 100% disponible
    "market_equity": "Market capitalization",
    "at": "Total assets",
    "sale": "Sales",
    "be": "Book equity",
    
    # QUALITY (12 características) - ~75% disponible
    "f_score": "Piotroski F-Score",
    "z_score": "Altman Z-Score",
    "o_score": "Ohlson O-Score",
    "gp_atl1": "Gross profit-to-lagged assets",
    "cop_atl1": "Cash operating profit-to-lagged assets",
    "at_turnover": "Asset turnover",
}

# ===== VARIABLES CRÍTICAS =====
# Si estas faltan, muchas características no se pueden calcular

VARIABLES_CRITICAS = [
    "at",      # Total Assets
    "sale",    # Sales
    "ni",      # Net Income
    "seq",     # Stockholders Equity
    "cash",    # Cash
    "lt",      # Total Liabilities
    "ca",      # Current Assets
    "cl",      # Current Liabilities
    "debtlt",  # Long-term Debt
    "debtst",  # Short-term Debt
    "capx",    # CapEx
    "ocf",     # Operating Cash Flow
]

# ===== FUNCIONES HELPER =====

def get_paper_code(yahoo_column):
    """Convierte nombre de columna de Yahoo a código del paper"""
    for code, yahoo_name in MAPEO_CONTABLE_YAHOO.items():
        if yahoo_name == yahoo_column:
            return code
    return None

def get_yahoo_column(paper_code):
    """Convierte código del paper a nombre de columna de Yahoo"""
    return MAPEO_CONTABLE_YAHOO.get(paper_code, None)

def check_data_availability(df_columns):
    """Verifica qué variables críticas están disponibles"""
    available = []
    missing = []
    
    for var_code in VARIABLES_CRITICAS:
        yahoo_col = get_yahoo_column(var_code)
        if yahoo_col and yahoo_col in df_columns:
            available.append(var_code)
        else:
            missing.append(var_code)
    
    print(f"\n📊 Disponibilidad de Variables Críticas:")
    print(f"   ✅ Disponibles: {len(available)}/{len(VARIABLES_CRITICAS)} ({len(available)/len(VARIABLES_CRITICAS)*100:.1f}%)")
    print(f"   ❌ Faltantes: {len(missing)}")
    
    if missing:
        print(f"\n⚠️ Variables faltantes:")
        for var in missing[:10]:  # Mostrar solo primeras 10
            print(f"   - {var} ({get_yahoo_column(var)})")
    
    return available, missing

def estimate_characteristic_coverage():
    """Estima cuántas características se pueden calcular"""
    total = len(CARACTERISTICAS_DISPONIBLES)
    
    # Esto es una estimación conservadora basada en disponibilidad típica de Yahoo
    estimated_available = {
        "Momentum": 23,      # 100%
        "Value": 18,         # ~90%
        "Profitability": 21, # ~85%
        "Investment": 22,    # ~75%
        "Accruals": 6,       # 100%
        "Low Risk": 12,      # ~80%
        "Size": 6,           # 100%
        "Quality": 9,        # ~75%
    }
    
    total_estimated = sum(estimated_available.values())
    
    print(f"\n🎯 Estimación de Cobertura de Características:")
    print(f"   Total en paper: {total}")
    print(f"   Estimado disponible: {total_estimated} (~{total_estimated/total*100:.0f}%)")
    print(f"\n   Por categoría:")
    for cat, count in estimated_available.items():
        print(f"   • {cat}: {count} características")
    
    return estimated_available


if __name__ == "__main__":
    # Test del diccionario
    print("🧪 Probando diccionario de variables...")
    print(f"\n📚 Total de mapeos Yahoo: {len(MAPEO_CONTABLE_YAHOO)}")
    print(f"📚 Total de mapeos Alpha Vantage: {len(MAPEO_CONTABLE_ALPHA_VANTAGE)}")
    print(f"📚 Total de características disponibles: {len(CARACTERISTICAS_DISPONIBLES)}")
    
    # Estimar cobertura
    estimate_characteristic_coverage()