# Wikipedia to Notion Importer

A Python script that imports Wikipedia articles into Notion databases with automatic page combination and organized formatting.

## Features

- 📖 **Complete Article Import** - Fetches full Wikipedia articles with all content
- 🗃️ **Structured Data** - Extracts infobox data (Born, Awards, etc.) into database properties
- 🎨 **Organized Formatting** - Uses callouts, dividers, and proper text spacing
- 🔄 **Auto-Combine** - Automatically combines multiple pages into a single organized page
- ⚡ **Smart Batching** - Handles Notion's API limits with intelligent content splitting
- 🛡️ **Error Handling** - Comprehensive validation and error recovery

## How It Works

This script uses a two-phase approach to handle Notion's limitations:

1. **Import Phase**: Creates multiple temporary pages (90 blocks each) to respect Notion's 100 children limit
2. **Combine Phase**: Automatically combines all pages into a single organized page and archives the temporary pages

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Wikipedia-to-Notion.git
   cd Wikipedia-to-Notion
   ```

2. **Install dependencies**
   ```bash
   pip install requests beautifulsoup4 notion-client
   ```

3. **Set up Notion integration**
   - Go to [Notion Integrations](https://www.notion.so/my-integrations)
   - Create a new "Internal integration"
   - Copy your integration token
   - Get your parent page ID from the Notion URL

4. **Configure the script**
   - Open `WTNI.py`
   - Replace `your-secret-api-token` with your integration token
   - Replace `your-parent-page-id` with your page ID
   - Grant your integration access to the parent page

5. **Run the script**
   ```bash
   python WTNI.py -u https://en.wikipedia.org/wiki/Quantum_mechanics
   ```

## Usage

### Command Line
```bash
# With URL argument
python WTNI.py -u https://en.wikipedia.org/wiki/Article_Name

# Interactive mode
python WTNI.py
```

### What You Get
- **Single organized page** with all article content
- **Database properties** with infobox data (Born, Awards, etc.)
- **Clean formatting** with callouts, dividers, and proper spacing
- **No duplicate pages** - temporary pages are automatically archived

## Requirements

- Python 3.7+
- Notion account with integration access
- Internet connection for Wikipedia API

## Dependencies

- `requests` - HTTP requests to Wikipedia API
- `beautifulsoup4` - HTML parsing
- `notion-client` - Notion API integration

## File Structure

```
Wikipedia-to-Notion/
├── WTNI.py              # Main script (clean version)
├── wtnc3.py             # Personal version (gitignored)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Limitations

- Notion's 100 children blocks per page limit
- Notion's 2000 character limit per rich text block
- Wikipedia API rate limits
- Large articles may take time to process

## Troubleshooting

### Common Issues

**"Integration doesn't have access"**
- Make sure you've shared your parent page with the integration
- Check that the integration has "Can edit" permissions

**"Payload too large" errors**
- The script handles this automatically with batching
- If you still get errors, the article might be extremely large

**"No pages found to combine"**
- This usually means the import phase failed
- Check your Notion token and page ID

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute.

## Acknowledgments

- Wikipedia for providing the content
- Notion for the excellent API
- The Python community for the amazing libraries
