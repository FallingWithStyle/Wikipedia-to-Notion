# Wikipedia to Notion Importer

A simple tool that imports Wikipedia articles into your Notion workspace with beautiful formatting and automatic organization.

## ✨ What This Does

- 📖 **Imports Wikipedia articles** directly into your Notion workspace
- 🎨 **Beautiful formatting** with organized sections, callouts, and dividers
- 🗃️ **Smart data extraction** - pulls out important info like birth dates, awards, etc.
- 🔄 **Auto-combines** everything into one clean, readable page
- ⚡ **Handles large articles** by working around Notion's limits automatically

## 🚀 Quick Start (Recommended)

### What You Need
- A computer with Python installed ([Download Python](https://www.python.org/downloads/))
- A Notion account
- About 5 minutes to set up

### Step 1: Download and Setup
1. **Download this project** (click the green "Code" button → "Download ZIP")
2. **Extract the ZIP file** to a folder on your computer
3. **Open Terminal/Command Prompt** in that folder
4. **Run the setup**:
   - **Mac/Linux**: Double-click `setup.sh` or run `./setup.sh` in terminal
   - **Windows**: Double-click `setup.bat`

### Step 2: Set Up Notion (One-time setup)
1. **Go to [Notion Integrations](https://www.notion.so/my-integrations)**
2. **Click "New integration"**
3. **Fill out the form**:
   - Name: "Wikipedia Importer" (or whatever you like)
   - Workspace: Select your workspace
   - Capabilities: Check "Read content", "Update content", "Insert content"
4. **Click "Submit"**
5. **Copy the token** (starts with `secret_`) - you'll need this!

### Step 3: Get Your Notion Page ID
1. **Go to any Notion page** where you want the articles to appear
2. **Copy the long string** from the URL after the last `/`
   - Example: `https://notion.so/My-Page-1234567890abcdef`
   - Page ID: `1234567890abcdef`

### Step 4: Grant Access
1. **On your Notion page**, click "Share" (top right)
2. **Click "Add people, emails, groups, or integrations"**
3. **Search for "Wikipedia Importer"** (or whatever you named it)
4. **Add it with "Can edit" permissions**

### Step 5: Launch the App
- **Mac/Linux**: Double-click `run_gui.py` or run `python3 run_gui.py`
- **Windows**: Double-click `run_gui.bat`

### Step 6: Import Your First Article
1. **Paste a Wikipedia URL** (like `https://en.wikipedia.org/wiki/Quantum_mechanics`)
2. **Enter your Notion token** (the `secret_...` from step 2)
3. **Enter your page ID** (from step 3)
4. **Click "Import Article"** and watch the magic happen! ✨

## 🎯 How to Use

### Using the GUI (Recommended)
The GUI makes everything super easy:
- **Paste any Wikipedia URL** and click import
- **Preview articles** before importing
- **Save your credentials** so you don't have to re-enter them
- **Watch real-time progress** as articles are imported

### Example Wikipedia URLs to Try
- https://en.wikipedia.org/wiki/Quantum_mechanics
- https://en.wikipedia.org/wiki/Artificial_intelligence
- https://en.wikipedia.org/wiki/Climate_change
- https://en.wikipedia.org/wiki/Leonardo_da_Vinci

## 🔧 Advanced Usage (Command Line)

If you prefer command line or want to automate imports:

1. **Follow the setup steps above** (steps 1-4)
2. **Open `WTNI.py`** in a text editor
3. **Replace the placeholder values**:
   - `your-secret-api-token` → your actual token
   - `your-parent-page-id` → your actual page ID
4. **Run the script**:
   ```bash
   python WTNI.py -u https://en.wikipedia.org/wiki/Article_Name
   ```

## 🆘 Troubleshooting

### "Integration doesn't have access"
- Make sure you shared your Notion page with the integration (Step 4 above)
- Check that the integration has "Can edit" permissions

### "Python not found" or setup errors
- Make sure Python is installed: [Download Python](https://www.python.org/downloads/)
- On Mac/Linux, you might need to use `python3` instead of `python`

### "Invalid URL" errors
- Make sure you're using a Wikipedia URL that starts with `https://en.wikipedia.org/wiki/`
- Try a different article if one doesn't work

### App won't start
- Make sure you ran the setup script first
- Try running `python3 gui.py` directly in the terminal to see error messages

## 📁 What You Get

After importing, you'll have:
- **One beautiful page** with all the article content
- **Organized sections** with proper headings and formatting
- **Smart data extraction** - important info like birth dates, awards, etc.
- **Clean layout** with callouts, dividers, and easy-to-read text
- **No clutter** - everything is automatically organized

## 🔧 Technical Details

### Requirements
- Python 3.7 or newer
- A Notion account
- Internet connection

### How It Works
This tool is smart about Notion's limits:
1. **Imports the article** and splits it into manageable chunks
2. **Creates temporary pages** to work around Notion's 100-block limit
3. **Combines everything** into one beautiful, organized page
4. **Cleans up** by removing the temporary pages

### File Structure
```
Wikipedia-to-Notion/
├── gui.py               # Easy-to-use graphical interface
├── run_gui.py           # Simple launcher script
├── WTNI.py              # Command-line version
├── requirements.txt     # What the app needs to run
├── setup.sh/setup.bat   # One-click setup
└── README.md            # This guide
```

## 🤝 Contributing

Found a bug or want to add a feature? Great!
1. Fork this repository
2. Make your changes
3. Test them thoroughly
4. Submit a pull request

## 📄 License

This project is open source and free to use, modify, and share.

## 🙏 Acknowledgments

- **Wikipedia** for providing amazing content
- **Notion** for their excellent API
- **The Python community** for the fantastic libraries
