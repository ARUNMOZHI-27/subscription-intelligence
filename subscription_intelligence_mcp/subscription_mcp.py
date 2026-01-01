from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List
from agent_state import get_state
from storage import load_subscriptions, save_subscriptions
from intelligence import (
    generate_monthly_summary,
    analyze_category_spend,
    analyze_duplicates,
    calculate_annual_savings
)
from llm_explainer import explain_alert
from calendar_export import export_calendar
from storage import load_subscriptions



mcp = FastMCP("Subscription Intelligence MCP")

# -----------------------
# STATUS TOOL (ONLY ONCE)
# -----------------------

@mcp.tool()
def status() -> Dict:
    """Show agent runtime status"""
    return get_state()

# -----------------------
# CORE TOOLS
# -----------------------

@mcp.tool()
def list_subscriptions() -> List[Dict]:
    return load_subscriptions()

@mcp.tool()
def add_subscription(
    name: str,
    monthly_cost: int,
    category: str,
    billing_start_date: Optional[str] = None,
    trial_end_date: Optional[str] = None,
    renewal_date: Optional[str] = None,
    auto_pay: bool = True,
    notes: Optional[str] = None
) -> Dict:
    subs = load_subscriptions()
    subs.append({
        "name": name,
        "monthly_cost": monthly_cost,
        "category": category,
        "billing_start_date": billing_start_date,
        "trial_end_date": trial_end_date,
        "renewal_date": renewal_date,
        "auto_pay": auto_pay,
        "notes": notes or "",
        "last_billed_amount": monthly_cost,
        "notified": []
    })
    save_subscriptions(subs)
    return {"status": "success", "message": f"{name} added"}

# -----------------------
# ANALYSIS
# -----------------------

@mcp.tool()
def analyze_spend() -> Dict:
    subs = load_subscriptions()
    cat = analyze_category_spend(subs)
    return {
        "total_monthly_spend": sum(cat.values()),
        "category_breakdown": cat
    }

@mcp.tool()
def get_monthly_summary() -> str:
    return generate_monthly_summary(load_subscriptions())

# -----------------------
# SMART SAVINGS (PHASE 2)
# -----------------------

@mcp.tool()
def recommend_savings() -> str:
    subs = load_subscriptions()
    overlaps = analyze_duplicates(subs)

    if not overlaps:
        return "✅ No overlapping subscriptions found."

    savings_facts = []

    for tag, _, msg in overlaps:
        category = tag.replace("duplicate_", "")
        matching = [s for s in subs if s.get("category") == category]

        if len(matching) >= 2:
            cheapest = min(matching, key=lambda x: x["monthly_cost"])
            annual = calculate_annual_savings(cheapest["monthly_cost"])

            savings_facts.append(
                f"Canceling one {category} service saves approximately ₹{annual}/year."
            )

    prompt = (
        "Here are concrete savings opportunities:\n" +
        "\n".join(savings_facts) +
        "\n\nExplain this gently to the user and suggest what to cancel."
    )

    return explain_alert(
        {"name": "Savings Advisor"},
        prompt
    )
@mcp.tool()
def export_calendar_file() -> dict:
    """
    Export subscriptions to a calendar (.ics) file
    """
    subs = load_subscriptions()
    file = export_calendar(subs)
    return {
        "status": "success",
        "file": file,
        "message": "Calendar file generated. Import subscriptions.ics into your calendar."
    }



def start_mcp_server():
    mcp.run()

if __name__=="__main__":
  start_mcp_server()
