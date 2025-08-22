"""
Result formatting for terminal output using Rich library.
"""

from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.markdown import Markdown
from datetime import datetime


class ResultFormatter:
    """Format search results for terminal display."""
    
    def __init__(self):
        self.console = Console()
    
    def display_welcome(self):
        """Display welcome message."""
        welcome_text = Text()
        welcome_text.append("🔍 WordPress AI Search Terminal v1.0\n", style="bold blue")
        welcome_text.append("Powered by OpenRouter AI Models\n", style="italic")
        welcome_text.append("Type 'exit' to quit, 'help' for commands", style="dim")
        
        panel = Panel(welcome_text, border_style="blue")
        self.console.print(panel)
    
    def display_connection_status(self, wordpress_status: bool, ai_status: bool):
        """Display connection status."""
        status_table = Table(title="Connection Status", show_header=False, box=None)
        status_table.add_column("Service", style="cyan")
        status_table.add_column("Status", style="bold")
        
        wordpress_icon = "✅" if wordpress_status else "❌"
        ai_icon = "✅" if ai_status else "❌"
        
        status_table.add_row("WordPress API", f"{wordpress_icon} {'Connected' if wordpress_status else 'Failed'}")
        status_table.add_row("AI Model", f"{ai_icon} {'Connected' if ai_status else 'Failed'}")
        
        self.console.print(status_table)
        self.console.print()
    
    def display_search_results(self, search_data: Dict[str, Any]):
        """Display formatted search results."""
        query = search_data.get('query', '')
        results = search_data.get('results', [])
        analysis = search_data.get('analysis', '')
        model_used = search_data.get('model_used', 'unknown')
        total_results = search_data.get('total_results', 0)
        
        # Display query
        self.console.print(f"\n[bold cyan]Query:[/bold cyan] {query}")
        self.console.print(f"[dim]Model: {model_used} | Results: {total_results}[/dim]\n")
        
        # Display AI analysis
        if analysis:
            analysis_panel = Panel(
                Markdown(analysis),
                title="🤖 AI Analysis",
                border_style="green"
            )
            self.console.print(analysis_panel)
            self.console.print()
        
        # Display individual results
        if results:
            self.console.print(f"[bold]Found {len(results)} relevant results:[/bold]\n")
            
            for i, result in enumerate(results, 1):
                self._display_result_item(i, result)
        else:
            self.console.print("[yellow]No relevant results found.[/yellow]\n")
    
    def _display_result_item(self, index: int, result: Dict[str, Any]):
        """Display a single result item."""
        title = result.get('title', 'Untitled')
        excerpt = result.get('excerpt', '')
        url = result.get('url', '')
        author = result.get('author', 'Unknown')
        date = result.get('date', '')
        
        # Format date
        if date:
            try:
                parsed_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
                formatted_date = parsed_date.strftime('%B %d, %Y')
            except:
                formatted_date = date
        else:
            formatted_date = 'Unknown date'
        
        # Create result panel
        content = Text()
        content.append(f"[bold]{title}[/bold]\n", style="white")
        
        if excerpt:
            # Clean HTML tags from excerpt
            clean_excerpt = self._clean_html(excerpt)
            content.append(f"{clean_excerpt[:300]}...\n\n", style="dim")
        
        content.append(f"👤 {author} | 📅 {formatted_date}\n", style="cyan")
        content.append(f"🔗 {url}", style="blue")
        
        panel = Panel(
            content,
            title=f"Result {index}",
            border_style="blue"
        )
        
        self.console.print(panel)
        self.console.print()
    
    def _clean_html(self, html_text: str) -> str:
        """Remove HTML tags from text."""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html_text)
    
    def display_error(self, error_message: str):
        """Display error message."""
        error_panel = Panel(
            f"❌ {error_message}",
            title="Error",
            border_style="red"
        )
        self.console.print(error_panel)
    
    def display_help(self):
        """Display help information."""
        help_text = """
# WordPress AI Search Terminal - Help

## Commands:
- Type your question naturally (e.g., "What are the latest gambling regulations?")
- `help` - Show this help message
- `exit` or `quit` - Exit the application
- `clear` - Clear the screen

## Examples:
- "Tell me about advertising compliance"
- "What are the HFSS regulations?"
- "Show me content about gambling laws"
- "Find information about regulatory updates"

## Tips:
- Use natural language - no need for special syntax
- Be specific for better results
- The AI will search and analyze WordPress content for you
- All results include proper citations and source links
        """
        
        help_panel = Panel(
            Markdown(help_text),
            title="Help",
            border_style="yellow"
        )
        self.console.print(help_panel)
    
    def display_loading(self, message: str = "Searching..."):
        """Display loading spinner."""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        )
        task = progress.add_task(message, total=None)
        progress.start()
        return progress
    
    def get_user_input(self) -> str:
        """Get user input with styled prompt."""
        return Prompt.ask("\n[bold green]Search[/bold green]")
    
    def display_model_info(self, model: str):
        """Display current AI model information."""
        model_info = f"🤖 Using AI Model: [bold]{model}[/bold]"
        self.console.print(model_info, style="dim")
    
    def display_fallback_notice(self, original_model: str, fallback_model: str):
        """Display notice when falling back to alternative model."""
        notice = f"⚠️  Primary model {original_model} unavailable, using {fallback_model}"
        self.console.print(notice, style="yellow")
    
    def clear_screen(self):
        """Clear the terminal screen."""
        self.console.clear()
    
    def display_stats(self, stats: Dict[str, Any]):
        """Display search statistics."""
        if not stats:
            return
        
        stats_table = Table(title="Search Statistics", show_header=False, box=None)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="bold")
        
        for key, value in stats.items():
            stats_table.add_row(key.replace('_', ' ').title(), str(value))
        
        self.console.print(stats_table)
        self.console.print()
