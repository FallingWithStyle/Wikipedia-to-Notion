"""
Wikipedia to Notion Importer - Auto-Combine Version
==================================================

This script imports Wikipedia articles and automatically combines all pages into a single page.

HOW IT WORKS:
=============

This script uses a two-phase approach to handle Notion's limitations:

1. IMPORT PHASE:
   - Fetches Wikipedia article content
   - Extracts infobox data (Born, Awards, etc.) for database properties
   - Parses HTML into organized Notion blocks (headings, paragraphs, lists, tables)
   - Splits content into multiple pages (90 blocks each) to respect Notion's 100 children limit
   - Creates a main page with infobox data + first content chunk
   - Creates additional "Part 2", "Part 3", etc. pages with remaining content

2. COMBINE PHASE:
   - Finds all pages for the article in the database
   - Collects all blocks from all pages
   - Adds all blocks to the main page in small batches (50 blocks at a time)
   - Archives (hides) the part pages to clean up the database
   - Results in one single, complete page with all content

WHY THIS APPROACH:
==================

Notion has strict limits:
- 100 children blocks per page
- 2000 characters per rich text block
- Payload size limits for API requests

This script works around these limits by temporarily creating multiple pages during import, then combining them into a single organized page. The result is a clean, readable article with proper formatting, callouts, and dividers.

SETUP INSTRUCTIONS:
==================

1. INSTALL DEPENDENCIES:
   pip install requests beautifulsoup4 notion-client

2. CREATE NOTION INTEGRATION:
   - Go to https://www.notion.so/my-integrations
   - Click "New integration"
   - Choose "Internal integration"
   - Name it (e.g., "Wikipedia Importer")
   - Select your workspace
   - Enable capabilities: Read content, Update content, Insert content
   - Click "Submit"
   - Copy the "Internal Integration Token" (starts with 'secret_')

3. GET PARENT PAGE ID:
   - Go to the Notion page where you want the database created
   - Copy the page ID from the URL (long string after the last '/')
   - Example: https://notion.so/My-Page-1234567890abcdef
   - Page ID: 1234567890abcdef

4. GRANT INTEGRATION ACCESS:
   - Go to your parent page in Notion
   - Click "Share" (top right)
   - Click "Add people, emails, groups, or integrations"
   - Search for your integration name
   - Add it with "Can edit" permissions

5. UPDATE CONFIG:
   - Replace NOTION_TOKEN with your integration token
   - Replace NOTION_PARENT_PAGE with your page ID

USAGE:
======
python WTNI.py -u https://en.wikipedia.org/wiki/Article_Name
python WTNI.py  # Interactive mode

FEATURES:
=========
- Imports Wikipedia articles with organized content
- Automatically combines all pages into a single page
- Extracts infobox data into database properties
- Better text formatting with proper spacing
- Handles large articles by organizing content sections
- Uses callouts and dividers for better readability
- Respects all Notion API limits and constraints
"""

import re
import requests
import argparse
from bs4 import BeautifulSoup
from notion_client import Client

# --- CONFIG ---
# Replace these with your actual values:
NOTION_TOKEN = "your-secret-api-token"  # Your integration token
NOTION_PARENT_PAGE = "your-parent-page-id"  # Your parent page ID

notion = Client(auth=NOTION_TOKEN)

NOTION_DATABASE_ID = None  # will be created on first run


# ------------------------- Helper Functions -------------------------
def create_database(name: str, columns: list[str]):
    """
    Creates a new Notion database with columns derived from infobox keys.
    """
    properties = {"Name": {"title": {}}}  # every DB needs a title
    for col in columns:
        properties[col] = {"rich_text": {}}

    db = notion.databases.create(
        parent={"page_id": NOTION_PARENT_PAGE},
        title=[{"type": "text", "text": {"content": name}}],
        properties=properties,
    )
    return db["id"]


def fetch_wikipedia_html(url: str) -> tuple[str, str]:
    """
    Fetch Wikipedia page HTML using REST API with a proper User-Agent.
    """
    if "wikipedia.org/wiki/" not in url:
        raise ValueError("Not a valid Wikipedia URL")
    title = url.split("/wiki/")[-1]

    endpoint = f"https://en.wikipedia.org/api/rest_v1/page/html/{title}"
    headers = {
        "User-Agent": "Wiki-Notion-Importer/1.0 (your_email@example.com)"
    }
    r = requests.get(endpoint, headers=headers)
    r.raise_for_status()
    return title.replace("_", " "), r.text


def make_block(text: str, block_type: str = "paragraph"):
    return {
        "object": "block",
        "type": block_type,
        block_type: {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def make_callout(text: str, icon: str = "💡"):
    """Create a callout block for better content organization."""
    # Ensure callout text doesn't exceed Notion's limit
    if len(text) > 2000:
        text = text[:1997] + "..."
    
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"emoji": icon}
        }
    }


def make_divider():
    """Create a divider block to separate content sections."""
    return {
        "object": "block",
        "type": "divider",
        "divider": {}
    }


def parse_html_to_blocks(html: str, max_blocks_per_page: int = 90):
    """
    Convert HTML into Notion blocks with better organization.
    Returns a list of page chunks, each with max_blocks_per_page blocks.
    """
    all_blocks = []
    soup = BeautifulSoup(html, "html.parser")
    MAX_LENGTH = 2000

    def safe_chunk_text(text: str, block_type: str = "paragraph"):
        """Safely chunk text to respect Notion's character limits."""
        if len(text) <= MAX_LENGTH:
            return [make_block(text, block_type)]
        
        chunks = []
        for i in range(0, len(text), 1800):  # Smaller chunks for better readability
            chunk = text[i:i + 1800]
            if len(chunk) > MAX_LENGTH:
                chunk = chunk[:MAX_LENGTH]
            chunks.append(make_block(chunk, block_type))
        return chunks

    # Add a callout with article summary (only to first page)
    all_blocks.append(make_callout("📖 This is a comprehensive Wikipedia article imported into Notion. Content is split across multiple pages for better organization.", "📚"))
    all_blocks.append(make_divider())

    # Process main content elements
    for element in soup.find_all(["h2", "h3", "p", "ul", "ol", "table"]):
        if element.name == "h2":
            text = element.get_text(separator=" ", strip=True).replace("[edit]", "")
            if text and len(text) <= MAX_LENGTH:
                all_blocks.append(make_divider())
                all_blocks.append(make_block(text, "heading_2"))
        elif element.name == "h3":
            text = element.get_text(separator=" ", strip=True).replace("[edit]", "")
            if text and len(text) <= MAX_LENGTH:
                all_blocks.append(make_block(text, "heading_3"))
        elif element.name == "p":
            text = element.get_text(separator=" ", strip=True)
            if text and len(text) > 50:  # Skip very short paragraphs
                all_blocks.extend(safe_chunk_text(text, "paragraph"))
        elif element.name == "ul":
            for li in element.find_all("li"):
                text = li.get_text(separator=" ", strip=True)
                if text and len(text) > 10:  # Skip very short list items
                    if len(text) <= MAX_LENGTH:
                        all_blocks.append(make_block(text, "bulleted_list_item"))
                    else:
                        all_blocks.extend(safe_chunk_text(text, "bulleted_list_item"))
        elif element.name == "ol":
            for li in element.find_all("li"):
                text = li.get_text(separator=" ", strip=True)
                if text and len(text) > 10:  # Skip very short list items
                    if len(text) <= MAX_LENGTH:
                        all_blocks.append(make_block(text, "numbered_list_item"))
                    else:
                        all_blocks.extend(safe_chunk_text(text, "numbered_list_item"))
        elif element.name == "table":
            # Convert tables to organized text blocks
            rows = element.find_all("tr")
            table_text = ""
            for row in rows:
                cols = [col.get_text(" ", strip=True) for col in row.find_all(["th", "td"])]
                table_text += " | ".join(cols) + "\n"
            if table_text.strip():
                table_text = table_text.strip()
                # Truncate table text if too long for callout
                if len(table_text) > 1900:  # Leave room for "📊 Table Data:\n\n" prefix
                    table_text = table_text[:1900] + "\n\n[Table truncated...]"
                all_blocks.append(make_callout(f"📊 Table Data:\n\n{table_text}", "📊"))

    # Split blocks into pages
    page_chunks = []
    for i in range(0, len(all_blocks), max_blocks_per_page):
        chunk = all_blocks[i:i + max_blocks_per_page]
        page_chunks.append(chunk)

    return page_chunks


def extract_infobox(html: str) -> dict[str, str]:
    """
    Extract infobox key/value pairs from Wikipedia page HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    infobox = soup.find("table", class_="infobox")
    data = {}
    if infobox:
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td:
                key = th.get_text(" ", strip=True)
                value = td.get_text(" ", strip=True)
                if key and value:
                    data[key] = value
    return data


def validate_blocks(blocks: list) -> list:
    """
    Validate that all blocks respect Notion's character limits.
    """
    MAX_LENGTH = 2000
    validated_blocks = []
    
    for block in blocks:
        block_type = block.get("type", "paragraph")
        
        if block_type == "callout":
            content_key = "callout"
        else:
            content_key = block_type
            
        if content_key in block and "rich_text" in block[content_key]:
            text_content = block[content_key]["rich_text"][0]["text"]["content"]
            if len(text_content) > MAX_LENGTH:
                print(f"Warning: Truncating {block_type} block from {len(text_content)} to {MAX_LENGTH} characters")
                block[content_key]["rich_text"][0]["text"]["content"] = text_content[:MAX_LENGTH]
        
        validated_blocks.append(block)
    
    return validated_blocks


def get_database_pages(database_id: str, title: str):
    """
    Get all pages from the database that match the article title.
    """
    try:
        # Query the database for pages matching the title
        response = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "Name",
                "title": {
                    "contains": title
                }
            }
        )
        return response["results"]
    except Exception as e:
        print(f"Error querying database: {e}")
        return []


def get_page_blocks(page_id: str):
    """
    Get all blocks from a specific page.
    """
    try:
        response = notion.blocks.children.list(block_id=page_id)
        return response["results"]
    except Exception as e:
        print(f"Error getting blocks from page {page_id}: {e}")
        return []


def combine_pages_into_single(database_id: str, title: str, infobox_data: dict):
    """
    Combine all pages for an article into a single page.
    """
    print(f"🔗 Combining all pages for '{title}' into a single page...")
    
    # Get all pages for this article
    pages = get_database_pages(database_id, title)
    if not pages:
        print("No pages found to combine.")
        return None
    
    print(f"Found {len(pages)} pages to combine")
    
    # Sort pages: main page first, then parts in order
    main_page = None
    part_pages = []
    
    for page in pages:
        page_title = page["properties"]["Name"]["title"][0]["text"]["content"]
        if page_title == title:
            main_page = page
        elif f"{title} (Part" in page_title:
            part_pages.append(page)
    
    # Sort part pages by part number
    part_pages.sort(key=lambda x: int(x["properties"]["Name"]["title"][0]["text"]["content"].split("(Part ")[1].split(")")[0]))
    
    if not main_page:
        print("Main page not found!")
        return None
    
    # Collect all blocks from all pages
    all_blocks = []
    
    # Get blocks from main page
    main_blocks = get_page_blocks(main_page["id"])
    all_blocks.extend(main_blocks)
    print(f"Added {len(main_blocks)} blocks from main page")
    
    # Get blocks from part pages
    for part_page in part_pages:
        part_blocks = get_page_blocks(part_page["id"])
        all_blocks.extend(part_blocks)
        print(f"Added {len(part_blocks)} blocks from {part_page['properties']['Name']['title'][0]['text']['content']}")
    
    # Update the main page with all blocks in batches
    try:
        # Add blocks in batches to avoid payload size limits
        batch_size = 50  # Smaller batches to avoid 413 errors
        total_blocks = len(all_blocks)
        
        for i in range(0, total_blocks, batch_size):
            batch = all_blocks[i:i + batch_size]
            notion.blocks.children.append(
                block_id=main_page["id"],
                children=batch
            )
            print(f"Added batch {i//batch_size + 1}/{(total_blocks + batch_size - 1)//batch_size} ({len(batch)} blocks)")
        
        print(f"✅ Successfully combined all {total_blocks} blocks into main page")
        
        # Delete the part pages
        for part_page in part_pages:
            try:
                notion.pages.update(
                    page_id=part_page["id"],
                    archived=True
                )
                print(f"🗑️ Archived {part_page['properties']['Name']['title'][0]['text']['content']}")
            except Exception as e:
                print(f"Warning: Could not archive {part_page['properties']['Name']['title'][0]['text']['content']}: {e}")
        
        return main_page["id"]
        
    except Exception as e:
        print(f"❌ Error combining pages: {e}")
        return None


# ------------------------- Main Function -------------------------
def add_article_to_database(url: str):
    global NOTION_DATABASE_ID

    # Fetch article
    title, html = fetch_wikipedia_html(url)
    print(f"Fetched article: {title}")

    # Extract infobox data
    infobox_data = extract_infobox(html)
    print(f"Infobox fields: {list(infobox_data.keys())}")

    # Create database if not exists
    if NOTION_DATABASE_ID is None:
        db_name = f"Wikipedia: {title}"
        columns = list(infobox_data.keys())
        try:
            NOTION_DATABASE_ID = create_database(db_name, columns)
            print(f"✅ Created database: {db_name} (ID: {NOTION_DATABASE_ID})")
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            print("This usually means the integration doesn't have access to the parent page.")
            print("Please check that your integration has 'Can edit' permissions on the parent page.")
            return

    # Create organized article pages with better content structure
    page_chunks = parse_html_to_blocks(html)
    print(f"Total blocks to create: {sum(len(chunk) for chunk in page_chunks)}")
    print(f"Split into {len(page_chunks)} pages for better organization")
    
    # Create the main page with infobox data
    page_properties = {"Name": {"title": [{"text": {"content": title}}]}}
    for k, v in infobox_data.items():
        page_properties[k] = {"rich_text": [{"text": {"content": v}}]}

    try:
        # Create the first page with the first chunk of content
        first_page_blocks = validate_blocks(page_chunks[0]) if page_chunks else []
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties=page_properties,
            children=first_page_blocks
        )
        print(f"✅ Created main page: {title}")
        
        # Create additional pages for remaining chunks
        for i, chunk in enumerate(page_chunks[1:], 2):
            additional_page_properties = {
                "Name": {"title": [{"text": {"content": f"{title} (Part {i})"}}]}
            }
            # Don't copy infobox data to additional pages - only main page has it
            
            chunk_blocks = validate_blocks(chunk)
            notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties=additional_page_properties,
                children=chunk_blocks
            )
            print(f"✅ Created additional page: {title} (Part {i})")
        
        print(f"✅ Article added to Notion database with {len(page_chunks)} organized pages total.")
        
        # Now combine all pages into a single page
        combined_page_id = combine_pages_into_single(NOTION_DATABASE_ID, title, infobox_data)
        if combined_page_id:
            print(f"🎉 Successfully created single combined page: {title}")
        else:
            print("⚠️ Pages were created but could not be combined automatically")
        
    except Exception as e:
        print(f"❌ Error creating pages: {e}")
        return


# ------------------------- Run -------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import Wikipedia articles to Notion (Auto-Combine Version)")
    parser.add_argument("-u", "--url", help="Wikipedia URL to import")
    args = parser.parse_args()
    
    if args.url:
        url = args.url.strip()
    else:
        url = input("Enter Wikipedia URL: ").strip()
    
    add_article_to_database(url)
