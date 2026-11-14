#!/usr/bin/env python3
"""
Freelance Floor Rate & Fixed-Price Quote Calculator
Part of the Freelance Client Onboarding Toolkit
Repository: https://github.com/AHMEDFOUAAD/freelance-client-onboarding-toolkit
Storefront: https://fouaad.gumroad.com
"""

import sys

def calculate_rates(target_net_income: float, annual_overhead: float, tax_rate_pct: float, weeks_off: int = 6, billable_ratio: float = 0.60):
    working_weeks = 52 - weeks_off
    if working_weeks <= 0:
        raise ValueError("Working weeks must be greater than zero.")
    
    # Gross needed to achieve target net income after taxes and overhead
    # Net = (Gross - Overhead) * (1 - TaxRate)
    # Gross = Overhead + Net / (1 - TaxRate)
    tax_factor = 1.0 - (tax_rate_pct / 100.0)
    if tax_factor <= 0:
        raise ValueError("Tax rate must be under 100%.")
        
    gross_needed = annual_overhead + (target_net_income / tax_factor)
    tax_reserve = gross_needed - annual_overhead - target_net_income
    
    total_hours = working_weeks * 40.0
    billable_hours = total_hours * billable_ratio
    
    if billable_hours <= 0:
        raise ValueError("Billable hours must be greater than zero.")
        
    floor_hourly_rate = gross_needed / billable_hours
    day_rate = floor_hourly_rate * 8.0
    monthly_retainer = gross_needed / 12.0
    
    return {
        "working_weeks": working_weeks,
        "total_hours": total_hours,
        "billable_hours": billable_hours,
        "gross_needed": gross_needed,
        "tax_reserve": tax_reserve,
        "floor_hourly_rate": floor_hourly_rate,
        "day_rate": day_rate,
        "monthly_retainer": monthly_retainer,
    }

def format_currency(val: float) -> str:
    return f"${val:,.2f}"

def interactive_mode():
    print("==========================================================")
    print(" Freelance Floor Rate & Fixed-Price Quote Calculator ")
    print(" From the Freelance Client Onboarding Toolkit — fouaad.gumroad.com ")
    print("==========================================================\n")
    
    try:
        target_net = float(input("1. Desired take-home (net) personal income per year [$]: ") or 75000)
        overhead = float(input("2. Annual business overhead (software, gear, insurance) [$]: ") or 8000)
        tax_rate = float(input("3. Estimated effective tax + self-employment rate [%]: ") or 28)
        weeks_off = int(input("4. Weeks off per year (vacation, holidays, illness) [weeks]: ") or 6)
        billable_pct = float(input("5. Billable time percentage (typical is 50-60%) [%]: ") or 60)
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        sys.exit(1)
        
    res = calculate_rates(target_net, overhead, tax_rate, weeks_off, billable_pct / 100.0)
    
    print("\n------------------- SUMMARY & TARGETS --------------------")
    print(f"Working Weeks / Year:    {res['working_weeks']} weeks")
    print(f"Total Annual Hours:      {res['total_hours']:,.0f} hours")
    print(f"Billable Hours / Year:   {res['billable_hours']:,.0f} hours ({billable_pct:.0f}% of total)")
    print(f"Tax Reserve Needed:      {format_currency(res['tax_reserve'])}")
    print(f"Total Gross Revenue:     {format_currency(res['gross_needed'])}")
    print("------------------- MINIMUM RATES ------------------------")
    print(f"FLOOR HOURLY RATE:       {format_currency(res['floor_hourly_rate'])} / hour")
    print(f"DAY RATE (8 hrs):        {format_currency(res['day_rate'])} / day")
    print(f"TARGET MONTHLY REVENUE:  {format_currency(res['monthly_retainer'])} / month")
    print("----------------------------------------------------------")
    print("\nFixed-Price Project Quoting Calculator:")
    try:
        est_hours = float(input("Enter estimated pure delivery hours for project: ") or 40)
        buffer_pct = float(input("Scope contingency buffer (recommended 20-30%) [%]: ") or 25)
    except ValueError:
        return
        
    buffered_hours = est_hours * (1.0 + buffer_pct / 100.0)
    quote_floor = buffered_hours * res['floor_hourly_rate']
    
    print(f"Estimated delivery:      {est_hours:.1f} hrs + {buffer_pct:.0f}% buffer = {buffered_hours:.1f} billed hrs")
    print(f"Recommended Fixed Quote: {format_currency(quote_floor)}")
    print("\nTip: For complete contract templates, rate calculators with Excel formulas,"
          "and 48 service menu offerings, see: https://fouaad.gumroad.com/l/pmnhvv")

if __name__ == '__main__':
    interactive_mode()
