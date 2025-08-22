# 🔍 WordPress AI Search Terminal

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free%20AI%20Models-orange.svg)](https://openrouter.ai)

A powerful command-line tool for searching WordPress content using AI-powered natural language queries. Built with Python, OpenRouter AI models, and the WordPress REST API.

**✨ Perfect for:** Content managers, developers, researchers, and anyone who needs to quickly find relevant information across WordPress sites using natural language.

## Features

- 🔍 **Natural Language Search** - Ask questions in plain English
- 🤖 **AI-Powered Analysis** - Get intelligent answers with proper citations
- 🧠 **Semantic Understanding** - AI analyzes content relevance, not just keyword matching
- 📱 **Beautiful Terminal UI** - Rich formatting with colors and panels
- 🔄 **Model Fallback** - Multiple free AI models for reliability
- ⚡ **Fast & Responsive** - Real-time search with loading indicators
- 🔗 **Source Attribution** - All results include proper citations and links
- 🎯 **Flexible Search** - Finds relevant content even without exact keyword matches

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- WordPress site with REST API access
- OpenRouter API key ([free tier available](https://openrouter.ai/keys))

### ⚡ 30-Second Setup

```bash
# Clone the repository
git clone https://github.com/GroundCtrlHQ/wordpress-ai-searcher.git
cd wordpress-ai-searcher

# Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure your credentials
cp .env.example .env
# Edit .env with your API keys

# Start searching!
python -m src.main
```

### Installation

1. **Clone or download the project:**
   ```bash
   git clone https://github.com/GroundCtrlHQ/wordpress-ai-searcher.git
   cd wordpress-ai-searcher
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your actual credentials
   # Required variables:
   # - OPENROUTER_API_KEY: Your OpenRouter API key
   # - WORDPRESS_API_URL: Your WordPress API endpoint
   # - WORDPRESS_USERNAME: WordPress username
   # - WORDPRESS_PASSWORD: WordPress password
   ```

5. **Run the application:**
   ```bash
   python -m src.main
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# AI Model Configuration
OPENROUTER_API_KEY=your_openrouter_api_key
AI_MODEL=z-ai/glm-4.5-air:free

# WordPress API Configuration
WORDPRESS_API_URL=https://your-site.com/wp-json/wp-ai-content/v1/content
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_password

# Application Configuration
MAX_RESULTS=5
REQUEST_TIMEOUT=30
VERBOSE_LOGGING=false
```

### Available AI Models (Free Tier)

The application supports multiple free OpenRouter models:

1. **z-ai/glm-4.5-air:free** - Recommended primary model
2. **qwen/qwen3-coder:free** - Good for technical queries
3. **moonshotai/kimi-k2:free** - Alternative option

The application will automatically fall back to alternative models if the primary model is unavailable.

## Usage

### Interactive Mode

Start the application without arguments for interactive mode:

```bash
python -m src.main
```

Example interaction:
```
🔍 WordPress AI Search Terminal v1.0
Powered by OpenRouter AI Models
Type 'exit' to quit, 'help' for commands

Search> What are the latest gambling regulations in the UK?
```

### Command Line Options

```bash
# Direct search query
python -m src.main --query "gambling regulations"

# Limit results
python -m src.main --max-results 10

# Verbose output
python -m src.main --verbose

# Show version
python -m src.main --version
```

### Available Commands

- **Natural language queries** - Ask questions in plain English
- **`help`** - Show help information
- **`exit`** or **`quit`** - Exit the application
- **`clear`** - Clear the terminal screen

## Examples

### Search Queries

```
Search> What are the latest gambling regulations in the UK?
Search> Tell me about advertising compliance
Search> Show me content about HFSS regulations
Search> Find information about regulatory updates
Search> What are the requirements for Think 25?
```

### Sample Output

```
Query: What are the latest gambling regulations in the UK?
Model: z-ai/glm-4.5-air:free | Results: 3

🤖 AI Analysis
Based on the search results, here are the latest gambling regulations in the UK:

**Think 25 Requirement**: The government has moved from 'Think 21' to 'Think 25' for land-based licensees. The amended LCCP Ordinary codes took effect on 30 August 2024.

**Key Changes**: This represents a significant shift in age verification requirements for gambling establishments.

Found 3 relevant results:

Result 1
Title: Gambling White Paper - Key Proposals: Children & Young adults
Excerpt: Move from 'Think 21' to 'Think 25' for land-based licensees... Amended LCCP Ordinary codes took effect on 30 August 2024.
👤 Jose Garcia | 📅 July 25, 2025
🔗 https://example.com/insight/gambling-regulations/
```

## Recent Improvements

### Enhanced Search Intelligence (Latest Update)

The search system has been significantly improved to provide more flexible and intelligent results:

- **🧠 Semantic Analysis**: AI now analyzes content relevance using semantic understanding, not just keyword matching
- **🎯 Flexible Matching**: Finds relevant content even when exact keywords aren't present
- **📈 Better Results**: More comprehensive and helpful search results
- **🔧 Simplified Code**: Removed complex filtering logic in favor of AI-powered analysis

### How It Works

1. **Content Retrieval**: WordPress API returns all available content
2. **AI Analysis**: AI models analyze content for semantic relevance
3. **Intelligent Filtering**: AI determines what's actually useful to the user
4. **Contextual Results**: Results include related content and broader context

## Architecture

### Core Components

1. **Configuration Management** (`src/config.py`)
   - Environment variable loading
   - Configuration validation
   - API credentials management

2. **WordPress Client** (`src/wordpress_client.py`)
   - REST API integration
   - Authentication handling
   - Content search and filtering

3. **AI Search Engine** (`src/ai_search.py`)
   - OpenRouter integration
   - Tool calling implementation
   - Model fallback logic

4. **Result Formatter** (`src/formatters.py`)
   - Rich terminal formatting
   - Citation formatting
   - User interface components

5. **CLI Interface** (`src/main.py`)
   - Interactive mode
   - Command-line options
   - Error handling

### Data Flow

```
User Query → AI Processing → Tool Call → WordPress API → Results Processing → Formatted Output
```

## Development

### Project Structure

```
wordpress-ai-searcher/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration management
│   ├── wordpress_client.py  # WordPress API client
│   ├── ai_search.py         # AI search engine
│   └── formatters.py        # Result formatting
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── IMPLEMENTATION_CHECKLIST.md  # Development checklist
└── .env                    # Environment variables (create this)
```

### Adding New Features

1. **New AI Models**: Add to `config.fallback_models` list
2. **Additional Tools**: Extend the tool calling system in `ai_search.py`
3. **Custom Formatting**: Modify `formatters.py` for new output styles
4. **API Endpoints**: Extend `wordpress_client.py` for new WordPress endpoints

### Testing

```bash
# Test configuration
python -c "from src.config import config; print('Config valid:', config.validate())"

# Test WordPress connection
python -c "from src.wordpress_client import WordPressClient; client = WordPressClient(); print('WordPress connected:', client.test_connection())"

# Test AI connection
python -c "from src.ai_search import AISearchEngine; engine = AISearchEngine(); print('AI connected:', engine.test_ai_connection())"
```

## Troubleshooting

### Common Issues

1. **Configuration Errors**
   - Ensure all required environment variables are set
   - Check API credentials are correct
   - Verify WordPress API endpoint is accessible

2. **Connection Failures**
   - Check internet connectivity
   - Verify OpenRouter API key is valid
   - Ensure WordPress site is accessible

3. **No Results**
   - Try different search terms
   - Check if WordPress content matches your query
   - Verify API endpoint returns expected data

4. **AI Model Issues**
   - Application will automatically fall back to alternative models
   - Check OpenRouter service status
   - Verify API key has sufficient credits

### Debug Mode

Enable verbose logging for detailed error information:

```bash
python -m src.main --verbose
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Bug Reports
Found a bug? Please [open an issue](https://github.com/GroundCtrlHQ/wordpress-ai-searcher/issues) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior

### 💡 Feature Requests
Have an idea for improvement? [Create an issue](https://github.com/GroundCtrlHQ/wordpress-ai-searcher/issues) with:
- Description of the feature
- Use case and benefits
- Implementation suggestions (if any)

### 🔧 Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### 🎯 Areas for Contribution
- **New AI Models**: Add support for additional OpenRouter models
- **WordPress Integration**: Extend API endpoints and features
- **UI Improvements**: Enhance terminal interface and formatting
- **Documentation**: Improve guides, examples, and tutorials
- **Testing**: Add unit tests and integration tests
- **Performance**: Optimize search speed and efficiency

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Support & Community

### 📚 Documentation
- **Implementation Guide**: Check [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) for detailed development notes
- **Troubleshooting**: See the troubleshooting section above for common issues
- **Examples**: Review the examples section for usage patterns

### 🆘 Getting Help
- **GitHub Issues**: [Open an issue](https://github.com/GroundCtrlHQ/wordpress-ai-searcher/issues) for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions and ideas
- **Documentation**: Check the README and implementation checklist first

### 🌟 Show Your Support
If this project helps you, please:
- ⭐ **Star the repository** to show your appreciation
- 🔄 **Share with others** who might find it useful
- 💬 **Leave feedback** on what you'd like to see next
- 🤝 **Contribute** to make it even better

## Acknowledgments

- **OpenRouter** - Free AI model access
- **WordPress REST API** - Content retrieval
- **Rich** - Beautiful terminal formatting
- **Click** - CLI framework

---

## Made with ❤️ by [GroundCtrlHQ](https://github.com/GroundCtrlHQ)

This project is proudly created and maintained by the [GroundCtrlHQ](https://github.com/GroundCtrlHQ) team. We're passionate about building tools that make developers' lives easier and more productive.

**🌐 Visit us:** [groundctrl.space](http://groundctrl.space)  
**📧 Contact:** contact@groundctrl.space  
**💼 Services:** Expert web app support services
