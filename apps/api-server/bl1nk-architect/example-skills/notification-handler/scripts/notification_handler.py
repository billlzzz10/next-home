"""
Example Notification Handler Skill Script

This script shows how to implement skill logic
that can be loaded and executed by Bl1nk Architect.
"""

def handle_slack_notification(message: str) -> dict:
    """Handle Slack notification"""
    return {
        "status": "success",
        "platform": "slack",
        "message": message,
        "action": "notification sent"
    }

def handle_linear_issue(title: str, description: str) -> dict:
    """Handle Linear issue creation"""
    return {
        "status": "success",
        "platform": "linear",
        "title": title,
        "action": "issue created",
        "issue_id": "LIN-123"
    }

def handle_clickup_task(name: str, description: str) -> dict:
    """Handle ClickUp task creation"""
    return {
        "status": "success",
        "platform": "clickup",
        "name": name,
        "action": "task created",
        "task_id": "clk_12345"
    }

def parse_query(query: str) -> dict:
    """Parse incoming query to determine action"""
    query_lower = query.lower()
    
    if "slack" in query_lower:
        return {"action": "slack", "query": query}
    elif "linear" in query_lower:
        return {"action": "linear", "query": query}
    elif "clickup" in query_lower:
        return {"action": "clickup", "query": query}
    else:
        return {"action": "unknown", "query": query}

def execute(query: str) -> dict:
    """Main execution function"""
    parsed = parse_query(query)
    action = parsed["action"]
    
    if action == "slack":
        return handle_slack_notification(query)
    elif action == "linear":
        return handle_linear_issue("Analysis Results", query)
    elif action == "clickup":
        return handle_clickup_task("Analysis Task", query)
    else:
        return {"status": "error", "message": "Unknown action"}
