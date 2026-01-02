from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List

from storage import load_subscriptions, save_subscriptions
from intelligence import (
    generate_monthly_summary,
    analyze_category_spend,
    analyze_duplicates,
    calculate_annual_savings
)
from calendar_export import export_calendar
from llm_explainer import explain_alert
from agent_state import get_state

from validators import (
    validate_name,
    validate_monthly_cost,
    validate_category,
    validate_date,
    ValidationError
)

mcp = FastMCP("Subscription Intelligence MCP")

# -----------------------
# STATUS TOOL
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
    try:
        return load_subscriptions()
    except Exception as e:
        return [{"error": str(e)}]


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
    try:
        name = validate_name(name)
        monthly_cost = validate_monthly_cost(monthly_cost)
        category = validate_category(category)

        billing_start_date = validate_date(billing_start_date)
        trial_end_date = validate_date(trial_end_date)
        renewal_date = validate_date(renewal_date)

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

        return {
            "status": "success",
            "message": f"{name} added successfully"
        }

    except ValidationError as e:
        return {"status": "error", "message": str(e)}

    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {e}"}

# -----------------------
# ANALYSIS
# -----------------------

@mcp.tool()
def analyze_spend() -> Dict:
    try:
        subs = load_subscriptions()
        cat = analyze_category_spend(subs)
        return {
            "total_monthly_spend": sum(cat.values()),
            "category_breakdown": cat
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_monthly_summary() -> str:
    try:
        return generate_monthly_summary(load_subscriptions())
    except Exception as e:
        return f"Error generating summary: {e}"

# -----------------------
# SMART SAVINGS
# -----------------------

@mcp.tool()
def recommend_savings() -> str:
    try:
        subs = load_subscriptions()
        overlaps = analyze_duplicates(subs)

        if not overlaps:
            return "✅ No overlapping subscriptions found."

        facts = []
        for tag, _, _ in overlaps:
            category = tag.replace("duplicate_", "")
            matches = [s for s in subs if s.get("category") == category]

            if len(matches) >= 2:
                cheapest = min(matches, key=lambda x: x["monthly_cost"])
                annual = calculate_annual_savings(cheapest["monthly_cost"])
                facts.append(
                    f"Canceling one {category} subscription saves about ₹{annual} per year."
                )

        prompt = (
            "Here are the savings opportunities:\n"
            + "\n".join(facts)
            + "\n\nExplain this gently to the user."
        )

        return explain_alert({"name": "Savings Advisor"}, prompt)

    except Exception as e:
        return f"Error analyzing savings: {e}"

# -----------------------
# CALENDAR EXPORT
# -----------------------

@mcp.tool()
def export_calendar_file() -> Dict:
    try:
        subs = load_subscriptions()
        file = export_calendar(subs)
        return {
            "status": "success",
            "file": file,
            "message": "Calendar file generated successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def start_mcp_server():
    mcp.run()


if __name__ == "__main__":
    start_mcp_server()
