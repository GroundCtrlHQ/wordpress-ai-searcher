# Product Requirements Document: WordPress AI Search Terminal Demo

## Project Overview

**Product Name:** WP-AI Search Terminal  
**Version:** 1.0 MVP  
**Type:** Command-line demonstration tool  
**Target Users:** Developers, content managers, WordPress site administrators

## Problem Statement

Users need an efficient way to search and retrieve specific information from WordPress content with AI-powered natural language queries. Current WordPress search functionality is limited to basic keyword matching and doesn't provide contextual understanding or proper source attribution.

## Solution

A terminal-based AI search tool that allows users to query WordPress content using natural language, returning relevant results with proper citations and source links from the WordPress REST API.

## Core Goals

### Primary Goals
1. **Natural Language Search** - Enable users to search WordPress content using conversational queries
2. **Accurate Citations** - Provide source attribution with direct links to original WordPress posts/pages
3. **Terminal Interface** - Create a simple, developer-friendly command-line experience
4. **AI-Powered Relevance** - Use AI to understand context and return semantically relevant results

### Secondary Goals
1. **Fast Response Times** - Deliver search results quickly (< 3 seconds)
2. **Structured Output** - Present results in a clean, readable terminal format
3. **Error Handling** - Gracefully handle API failures and invalid queries

## Technical Architecture

### Core Components

1. **AI SDK Integration**
   - Use `streamText` for processing natural language queries
   - Implement tool calling for WordPress API interactions
   - Handle response streaming for real-time feedback

2. **WordPress Search Tool**
   ```typescript
   searchWordPress: {
     description: 'Search WordPress content for relevant information',
     inputSchema: z.object({
       query: z.string().describe('Search query to find relevant content'),
       maxResults: z.number().optional().default(5)
     }),
     execute: async ({ query, maxResults }) => {
       // WordPress REST API search implementation
     }
   }
   ```

3. **Citation System**
   - Extract and format WordPress post/page metadata
   - Generate proper attribution with title, author, date, URL
   - Ensure all information includes source links

### Data Flow

```
User Query → AI Processing → Tool Call → WordPress API → Results Processing → Formatted Output with Citations
```

## Functional Requirements

### Core Features

1. **Natural Language Query Processing**
   - Accept conversational search queries
   - Parse user intent and generate appropriate WordPress API calls
   - Handle follow-up questions and clarifications

2. **WordPress Content Search**
   - Search across posts, pages, and custom content types
   - Filter by content type, date, author if specified
   - Return relevant excerpts with full context

3. **Citation Generation**
   - Format: `[Title] by [Author] ([Date]) - [URL]`
   - Include post excerpt or relevant section
   - Maintain source integrity and accuracy

4. **Terminal Interface**
   - Interactive command-line interface
   - Real-time response streaming
   - Clear formatting with colors/emphasis
   - Exit commands and help documentation

### API Integration

**WordPress REST API Endpoints:**
- `/wp-json/wp/v2/search` - Primary search endpoint
- `/wp-json/wp/v2/posts` - Post-specific queries
- `/wp-json/wp/v2/pages` - Page-specific queries

**Required API Fields:**
```json
{
  "id": "number",
  "title": "object",
  "url": "string", 
  "excerpt": "object",
  "author": "object",
  "date": "string",
  "type": "string",
  "content": "object"
}
```

## User Experience

### Example Interaction

```bash
$ wp-ai-search

WP-AI Search Terminal v1.0
Connected to: dev.wiggin.co.uk
Type 'exit' to quit, 'help' for commands

> What are the latest gambling regulations in the UK?

Searching WordPress content...

Found 3 relevant results:

1. **Gambling White Paper - Key Proposals: Children & Young adults**
   "Move from 'Think 21' to 'Think 25' for land-based licensees... 
   Amended LCCP Ordinary codes took effect on 30 August 2024."
   
   Source: https://dev.wiggin.co.uk/insight/custom-content-popup-development-page/
   Author: Jose Garcia | Date: July 25, 2025

2. **HFSS Compliance Checker**
   Information about advertising compliance and regulatory updates...
   
   Source: https://dev.wiggin.co.uk/expertise/hfss-advertising/
   Author: Sam Pearson | Date: January 20, 2025

> Tell me more about the Think 25 requirement

Searching for more details...
```

### Error Handling

```bash
> invalid query with special chars @#$%

Error: Unable to process query. Please use natural language.

> search for content on a site that's down

Error: WordPress API connection failed. Please try again later.
```

## Technical Specifications

### Dependencies
- **AI SDK Core** - `generateText`, `streamText`, tool calling
- **WordPress REST API** - Content search and retrieval
- **Node.js** - Runtime environment
- **TypeScript** - Type safety and development experience
- **Zod** - Schema validation for tool inputs

### Configuration
```typescript
interface Config {
  wordpressApiUrl: string;
  maxResults: number;
  timeout: number;
  aiModel: string; // e.g., 'gpt-4o'
}
```

### Performance Requirements
- Response time: < 3 seconds for typical queries
- Support for concurrent users: 10+
- API rate limiting: Respect WordPress API limits
- Memory usage: < 100MB for terminal session

## Success Metrics

### Quantitative
- **Response Accuracy:** >85% of queries return relevant results
- **Response Time:** <3 seconds average
- **Citation Accuracy:** 100% of results include valid source links
- **Error Rate:** <5% of queries result in errors

### Qualitative
- Users can find information faster than manual WordPress search
- Citations are clear and verifiable
- Terminal interface is intuitive for developers
- Results are contextually relevant to queries

## Development Phases

### Phase 1: Core MVP (2-3 weeks)
- Basic terminal interface
- WordPress API integration
- Simple AI-powered search
- Citation formatting

### Phase 2: Enhanced Features (1-2 weeks)
- Improved query processing
- Better error handling
- Performance optimizations
- Enhanced formatting

### Phase 3: Polish & Testing (1 week)
- User testing and feedback
- Bug fixes and improvements
- Documentation and examples

## Out of Scope (Future Considerations)

- Web-based interface
- Authentication for private WordPress sites
- Multi-site search across different WordPress instances
- Advanced filtering and sorting options
- Search result caching
- Integration with other CMS platforms

## Risk Assessment

### Technical Risks
- **WordPress API Changes** - Monitor for breaking changes
- **AI Model Limitations** - Handle cases where AI misunderstands queries
- **Rate Limiting** - Implement proper throttling and retry logic

### Mitigation Strategies
- Comprehensive error handling and fallback mechanisms
- Flexible configuration for different WordPress setups
- Clear documentation for troubleshooting common issues

## Implementation Details

### Tool Configuration Example

```typescript
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const tools = {
  searchWordPress: {
    description: 'Search WordPress content and return relevant results with citations',
    inputSchema: z.object({
      query: z.string().describe('The search query to find relevant WordPress content'),
      contentType: z.enum(['posts', 'pages', 'all']).optional().default('all'),
      maxResults: z.number().min(1).max(10).optional().default(5)
    }),
    execute: async ({ query, contentType, maxResults }) => {
      const baseUrl = 'https://dev.wiggin.co.uk/wp-json/wp/v2';
      const searchUrl = `${baseUrl}/search?search=${encodeURIComponent(query)}&per_page=${maxResults}`;
      
      try {
        const response = await fetch(searchUrl);
        const results = await response.json();
        
        return results.map(item => ({
          title: item.title?.rendered || 'Untitled',
          excerpt: item.excerpt?.rendered || '',
          url: item.url,
          date: item.date,
          type: item.type,
          author: item.author || 'Unknown'
        }));
      } catch (error) {
        throw new Error(`WordPress API error: ${error.message}`);
      }
    }
  }
};
```

### CLI Interface Structure

```typescript
interface CLIOptions {
  wordpressUrl: string;
  model: string;
  maxResults: number;
  verbose: boolean;
}

class WPAISearch {
  constructor(options: CLIOptions) {
    // Initialize with options
  }
  
  async start() {
    // Start interactive session
  }
  
  async processQuery(query: string) {
    // Process user query with AI and tools
  }
  
  formatResults(results: SearchResult[]) {
    // Format and display results with citations
  }
}
```