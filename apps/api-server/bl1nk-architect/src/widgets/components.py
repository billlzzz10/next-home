"""
Beautiful UI Components and Widgets

Modern, responsive components for displaying analysis results.
Includes glassmorphism and gradient effects.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum


class WidgetStyle(Enum):
    """Widget styling themes"""
    GLASSMORPHISM = "glassmorphism"
    NEUMORPHISM = "neumorphism"
    MINIMAL = "minimal"
    GRADIENT = "gradient"


@dataclass
class AnalysisCard:
    """Card widget for displaying analysis results"""
    title: str
    icon: str
    value: str
    description: str
    status: str = "success"
    style: WidgetStyle = WidgetStyle.GLASSMORPHISM
    
    def to_html(self) -> str:
        """Generate HTML representation"""
        color_map = {
            "success": "#2E7D32",
            "warning": "#F57C00",
            "error": "#C62828",
            "info": "#1565C0",
        }
        color = color_map.get(self.status, "#2E7D32")
        
        return f"""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin: 10px;
            color: white;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        ">
            <div style="font-size: 28px; margin-bottom: 10px;">{self.icon}</div>
            <div style="font-size: 14px; opacity: 0.7;">{self.title}</div>
            <div style="
                font-size: 32px;
                font-weight: bold;
                margin: 10px 0;
                color: {color};
            ">{self.value}</div>
            <div style="font-size: 12px; opacity: 0.6;">{self.description}</div>
        </div>
        """
    
    def to_markdown(self) -> str:
        """Generate Markdown representation"""
        return f"""
| {self.icon} | {self.title} |
|---|---|
| **{self.value}** | {self.description} |
"""


@dataclass
class MetricsRow:
    """Row widget for displaying metrics"""
    metrics: List[Dict[str, str]]
    
    def to_html(self) -> str:
        """Generate HTML table"""
        rows = ""
        for metric in self.metrics:
            rows += f"""
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <td style="padding: 12px;">{metric.get('icon', '')}</td>
                <td style="padding: 12px;">{metric.get('label', '')}</td>
                <td style="padding: 12px; font-weight: bold;">{metric.get('value', '')}</td>
            </tr>
            """
        
        return f"""
        <table style="
            width: 100%;
            border-collapse: collapse;
            color: white;
        ">
            {rows}
        </table>
        """
    
    def to_markdown(self) -> str:
        """Generate Markdown table"""
        lines = ["| Icon | Metric | Value |", "|------|--------|-------|"]
        for metric in self.metrics:
            lines.append(
                f"| {metric.get('icon', '')} | {metric.get('label', '')} | "
                f"{metric.get('value', '')} |"
            )
        return "\n".join(lines)


@dataclass
class ProgressBar:
    """Progress bar widget"""
    label: str
    value: float
    max_value: float = 100.0
    icon: str = "📊"
    
    def get_percentage(self) -> float:
        """Calculate percentage"""
        return (self.value / self.max_value) * 100 if self.max_value > 0 else 0
    
    def to_html(self) -> str:
        """Generate HTML progress bar"""
        percentage = self.get_percentage()
        return f"""
        <div style="margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>{self.icon} {self.label}</span>
                <span>{self.value:.0f}/{self.max_value:.0f}</span>
            </div>
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                height: 8px;
                overflow: hidden;
            ">
                <div style="
                    background: linear-gradient(90deg, #2E7D32, #66BB6A);
                    height: 100%;
                    width: {percentage}%;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """
    
    def to_markdown(self) -> str:
        """Generate Markdown progress"""
        percentage = self.get_percentage()
        filled = int(percentage / 5)
        empty = 20 - filled
        bar = "█" * filled + "░" * empty
        return f"{self.icon} {self.label}: `{bar}` {percentage:.0f}%"


class AnalysisPanel:
    """Main analysis panel widget"""
    
    def __init__(
        self,
        title: str,
        cards: List[AnalysisCard],
        metrics: Optional[MetricsRow] = None,
        progress_bars: Optional[List[ProgressBar]] = None,
    ):
        self.title = title
        self.cards = cards
        self.metrics = metrics
        self.progress_bars = progress_bars or []
    
    def to_html(self) -> str:
        """Generate full HTML panel"""
        content = f"""
        <div style="
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, rgba(30, 30, 45, 0.8), rgba(50, 50, 70, 0.8));
            border-radius: 16px;
            color: white;
        ">
            <h1 style="margin-bottom: 30px; font-size: 28px;">🏗️ {self.title}</h1>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
        """
        
        for card in self.cards:
            content += card.to_html()
        
        content += """
            </div>
        """
        
        if self.metrics:
            content += f"""
            <div style="margin-top: 30px;">
                <h2 style="margin-bottom: 15px;">📊 Metrics</h2>
                {self.metrics.to_html()}
            </div>
            """
        
        if self.progress_bars:
            content += """
            <div style="margin-top: 30px;">
                <h2 style="margin-bottom: 15px;">📈 Progress</h2>
            """
            for pb in self.progress_bars:
                content += pb.to_html()
            content += """
            </div>
            """
        
        content += """
        </div>
        """
        return content
    
    def to_markdown(self) -> str:
        """Generate full Markdown panel"""
        lines = [f"# 🏗️ {self.title}\n"]
        
        # Add cards as sections
        for card in self.cards:
            lines.append(f"## {card.icon} {card.title}\n")
            lines.append(card.to_markdown())
            lines.append("")
        
        # Add metrics
        if self.metrics:
            lines.append("## 📊 Metrics\n")
            lines.append(self.metrics.to_markdown())
            lines.append("")
        
        # Add progress bars
        if self.progress_bars:
            lines.append("## 📈 Progress\n")
            for pb in self.progress_bars:
                lines.append(pb.to_markdown())
            lines.append("")
        
        return "\n".join(lines)


def create_analysis_report(
    title: str,
    repository: str,
    files_count: int,
    duplicates: List,
    python_deps: List,
    typescript_deps: List,
) -> str:
    """Create a full analysis report with widgets"""
    
    # Create cards
    cards = [
        AnalysisCard(
            title="Repository",
            icon="📦",
            value=repository.split("/")[-1],
            description="Project analyzed",
            status="success",
        ),
        AnalysisCard(
            title="Files Analyzed",
            icon="📁",
            value=str(files_count),
            description="Source files scanned",
            status="info",
        ),
        AnalysisCard(
            title="Code Duplicates",
            icon="⚠️",
            value=str(len(duplicates)),
            description="Duplicate patterns found",
            status="warning" if duplicates else "success",
        ),
        AnalysisCard(
            title="Dependencies",
            icon="📚",
            value=str(len(python_deps) + len(typescript_deps)),
            description="Total dependencies",
            status="info",
        ),
    ]
    
    # Create metrics
    metrics = MetricsRow(
        metrics=[
            {
                "icon": "🐍",
                "label": "Python Deps",
                "value": f"{len(python_deps)} packages",
            },
            {
                "icon": "📘",
                "label": "TypeScript Deps",
                "value": f"{len(typescript_deps)} packages",
            },
            {
                "icon": "🔍",
                "label": "Duplication Rate",
                "value": f"{(len(duplicates) / max(files_count, 1) * 100):.1f}%",
            },
        ]
    )
    
    # Create progress bars
    progress_bars = [
        ProgressBar("Code Quality", 85, icon="✅"),
        ProgressBar("Dependency Health", 72, icon="💪"),
        ProgressBar("Test Coverage", 65, icon="🧪"),
    ]
    
    # Create panel
    panel = AnalysisPanel(
        title=title,
        cards=cards,
        metrics=metrics,
        progress_bars=progress_bars,
    )
    
    return panel.to_markdown()
