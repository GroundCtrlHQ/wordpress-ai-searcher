"""
Main CLI interface for WordPress AI Search Terminal.
"""

import sys
import signal
from typing import Optional
import click
from rich.console import Console
from rich.prompt import Prompt

from src.config import config
from src.wordpress_client import WordPressClient
from src.ai_search import AISearchEngine
from src.formatters import ResultFormatter


class WPAISearchTerminal:
    """Main terminal application for WordPress AI Search."""
    
    def __init__(self):
        self.console = Console()
        self.formatter = ResultFormatter()
        self.wordpress_client = WordPressClient()
        self.ai_engine = AISearchEngine()
        self.running = True
        
        # Set up signal handlers for graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals for graceful exit."""
        self.console.print("\n[yellow]Shutting down gracefully...[/yellow]")
        self.running = False
        sys.exit(0)
    
    def start(self, query: Optional[str] = None, max_results: Optional[int] = None, verbose: bool = False):
        """Start the terminal application."""
        try:
            # Validate configuration
            if not config.validate():
                self.console.print("[red]Configuration validation failed. Please check your .env file.[/red]")
                sys.exit(1)
            
            # Test connections
            wordpress_status = self.wordpress_client.test_connection()
            ai_status = self.ai_engine.test_ai_connection()
            
            # Display welcome and status
            self.formatter.display_welcome()
            self.formatter.display_connection_status(wordpress_status, ai_status)
            
            if not wordpress_status:
                self.console.print("[red]WordPress API connection failed. Please check your credentials.[/red]")
                sys.exit(1)
            
            if not ai_status:
                self.console.print("[yellow]AI model connection failed. Will use fallback search.[/yellow]")
            
            # Display current model info
            self.formatter.display_model_info(config.ai_model)
            
            # Handle direct query if provided
            if query:
                self._process_query(query, max_results or config.max_results)
                return
            
            # Start interactive mode
            self._interactive_mode()
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Goodbye![/yellow]")
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {e}[/red]")
            if verbose:
                import traceback
                traceback.print_exc()
    
    def _interactive_mode(self):
        """Run interactive mode."""
        while self.running:
            try:
                # Get user input
                user_input = self.formatter.get_user_input()
                
                # Handle commands
                if user_input.lower() in ['exit', 'quit']:
                    self.console.print("[yellow]Goodbye![/yellow]")
                    break
                elif user_input.lower() == 'help':
                    self.formatter.display_help()
                    continue
                elif user_input.lower() == 'clear':
                    self.formatter.clear_screen()
                    self.formatter.display_welcome()
                    continue
                elif not user_input.strip():
                    continue
                
                # Process search query
                self._process_query(user_input, config.max_results)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Use 'exit' to quit or continue searching...[/yellow]")
            except Exception as e:
                self.formatter.display_error(f"Error processing query: {e}")
    
    def _process_query(self, query: str, max_results: int):
        """Process a search query."""
        try:
            # Show loading indicator
            progress = self.formatter.display_loading("Searching WordPress content...")
            
            # Perform search
            search_data = self.ai_engine.search(query, max_results)
            
            # Stop loading indicator
            progress.stop()
            
            # Display results
            self.formatter.display_search_results(search_data)
            
        except Exception as e:
            self.formatter.display_error(f"Search failed: {e}")


@click.command()
@click.option('--query', '-q', help='Direct search query')
@click.option('--max-results', '-m', type=int, help='Maximum number of results')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--version', is_flag=True, help='Show version and exit')
def main(query: Optional[str], max_results: Optional[int], verbose: bool, version: bool):
    """
    WordPress AI Search Terminal
    
    A command-line tool for searching WordPress content using AI-powered natural language queries.
    
    Examples:
        wp-ai-search
        wp-ai-search --query "gambling regulations"
        wp-ai-search --max-results 10
    """
    if version:
        from src import __version__
        click.echo(f"WordPress AI Search Terminal v{__version__}")
        return
    
    # Create and start terminal
    terminal = WPAISearchTerminal()
    terminal.start(query, max_results, verbose)


if __name__ == '__main__':
    main()
