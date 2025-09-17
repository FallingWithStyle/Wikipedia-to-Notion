"""
Wikipedia to Notion Importer - GUI Version
==========================================

A simple GUI for importing Wikipedia articles into Notion databases.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import sys
import os
import webbrowser

# Import the core functionality from WTNI.py
try:
    from WTNI import add_article_to_database, fetch_wikipedia_html, extract_infobox
except ImportError:
    # Fallback to wtnc3.py if WTNI.py is not available
    from wtnc3 import add_article_to_database, fetch_wikipedia_html, extract_infobox

class WikipediaToNotionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wikipedia to Notion Importer")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.url_var = tk.StringVar()
        self.token_var = tk.StringVar()
        self.page_id_var = tk.StringVar()
        
        # Example URLs
        self.example_urls = [
            "https://en.wikipedia.org/wiki/Quantum_mechanics",
            "https://en.wikipedia.org/wiki/Artificial_intelligence", 
            "https://en.wikipedia.org/wiki/Climate_change",
            "https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
            "https://en.wikipedia.org/wiki/Photosynthesis"
        ]
        
        # Load saved credentials if they exist
        self.load_saved_credentials()
        
        # Check if this is first run
        self.is_first_run = not os.path.exists("config.txt")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main import tab
        self.main_frame = ttk.Frame(notebook, padding="20")
        notebook.add(self.main_frame, text="📖 Import Articles")
        
        # Help tab
        self.help_frame = ttk.Frame(notebook, padding="20")
        notebook.add(self.help_frame, text="❓ Help & Setup")
        
        self.setup_main_tab()
        self.setup_help_tab()
        
    def setup_main_tab(self):
        """Set up the main import interface"""
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Wikipedia to Notion Importer", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input section
        url_frame = ttk.LabelFrame(self.main_frame, text="📄 Wikipedia Article", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="Article URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        
        # Example URLs dropdown
        ttk.Label(url_frame, text="Try these examples:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        self.example_combo = ttk.Combobox(url_frame, values=self.example_urls, width=57, state="readonly")
        self.example_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 5), padx=(10, 5))
        self.example_combo.bind('<<ComboboxSelected>>', self.on_example_selected)
        
        # Notion credentials section
        cred_frame = ttk.LabelFrame(self.main_frame, text="🔑 Notion Credentials", padding="10")
        cred_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        cred_frame.columnconfigure(1, weight=1)
        
        # Token input
        ttk.Label(cred_frame, text="Integration Token:").grid(row=0, column=0, sticky=tk.W, pady=5)
        token_frame = ttk.Frame(cred_frame)
        token_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        token_frame.columnconfigure(0, weight=1)
        
        self.token_entry = ttk.Entry(token_frame, textvariable=self.token_var, width=50, show="*")
        self.token_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.token_entry.insert(0, "secret_...")
        self.token_entry.bind('<FocusIn>', self.clear_placeholder)
        self.token_entry.bind('<FocusOut>', self.restore_placeholder)
        
        ttk.Button(token_frame, text="Get Token", command=self.open_notion_integrations).grid(row=0, column=1)
        
        # Page ID input
        ttk.Label(cred_frame, text="Page ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        page_id_frame = ttk.Frame(cred_frame)
        page_id_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        page_id_frame.columnconfigure(0, weight=1)
        
        self.page_id_entry = ttk.Entry(page_id_frame, textvariable=self.page_id_var, width=50)
        self.page_id_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.page_id_entry.insert(0, "1234567890abcdef...")
        self.page_id_entry.bind('<FocusIn>', self.clear_placeholder)
        self.page_id_entry.bind('<FocusOut>', self.restore_placeholder)
        
        ttk.Button(page_id_frame, text="Test Connection", command=self.test_connection).grid(row=0, column=1)
        
        # Setup guide button
        ttk.Button(cred_frame, text="📖 Open Setup Guide", command=self.open_setup_guide).grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # Action buttons
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        self.import_button = ttk.Button(buttons_frame, text="🚀 Import Article", 
                                       command=self.start_import, style='Accent.TButton')
        self.import_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.preview_button = ttk.Button(buttons_frame, text="👁️ Preview Article", 
                                        command=self.preview_article)
        self.preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(buttons_frame, text="🗑️ Clear All", 
                                      command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT)
        
        # Progress and status
        self.progress = ttk.Progressbar(self.main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.status_label = ttk.Label(self.main_frame, text="Ready to import! 🎉", 
                                     foreground='green', font=('Arial', 10, 'bold'))
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Log output
        log_frame = ttk.LabelFrame(self.main_frame, text="📋 Import Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80, font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame grid weights
        self.main_frame.rowconfigure(6, weight=1)
        
        # Show welcome message for first-time users
        if self.is_first_run:
            self.show_welcome_message()
        
    def setup_help_tab(self):
        """Set up the help and setup guide tab"""
        # Create scrollable frame for help content
        canvas = tk.Canvas(self.help_frame)
        scrollbar = ttk.Scrollbar(self.help_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Help content
        title = ttk.Label(scrollable_frame, text="❓ Help & Setup Guide", 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 20))
        
        # Quick start section
        quick_start = ttk.LabelFrame(scrollable_frame, text="🚀 Quick Start", padding="15")
        quick_start.pack(fill=tk.X, pady=(0, 15))
        
        quick_text = """1. Get your Notion integration token (click "Get Token" button)
2. Get your Notion page ID (copy from any Notion page URL)
3. Paste a Wikipedia URL and click "Import Article"
4. Watch the magic happen! ✨"""
        
        ttk.Label(quick_start, text=quick_text, font=('Arial', 10)).pack(anchor=tk.W)
        
        # Notion setup section
        notion_setup = ttk.LabelFrame(scrollable_frame, text="🔑 Setting Up Notion", padding="15")
        notion_setup.pack(fill=tk.X, pady=(0, 15))
        
        notion_text = """To use this tool, you need to create a Notion integration:

1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name it "Wikipedia Importer" (or anything you like)
4. Select your workspace
5. Enable: Read content, Update content, Insert content
6. Click "Submit"
7. Copy the token (starts with 'secret_')

Then share a Notion page with your integration:
1. Go to any Notion page
2. Click "Share" (top right)
3. Click "Add people, emails, groups, or integrations"
4. Search for your integration name
5. Add it with "Can edit" permissions"""
        
        ttk.Label(notion_setup, text=notion_text, font=('Arial', 10)).pack(anchor=tk.W)
        
        # Example URLs section
        examples = ttk.LabelFrame(scrollable_frame, text="📚 Example Articles to Try", padding="15")
        examples.pack(fill=tk.X, pady=(0, 15))
        
        example_text = """Try importing these interesting Wikipedia articles:
• Quantum mechanics - Physics and quantum theory
• Artificial intelligence - AI and machine learning
• Climate change - Environmental science
• Leonardo da Vinci - Renaissance artist and inventor
• Photosynthesis - Plant biology and chemistry"""
        
        ttk.Label(examples, text=example_text, font=('Arial', 10)).pack(anchor=tk.W)
        
        # Troubleshooting section
        troubleshooting = ttk.LabelFrame(scrollable_frame, text="🆘 Troubleshooting", padding="15")
        troubleshooting.pack(fill=tk.X, pady=(0, 15))
        
        trouble_text = """Common issues and solutions:

❌ "Integration doesn't have access"
→ Make sure you shared your Notion page with the integration

❌ "Invalid URL" 
→ Use Wikipedia URLs that start with https://en.wikipedia.org/wiki/

❌ "Python not found"
→ Make sure Python is installed on your computer

❌ App won't start
→ Try running the setup script first, or run 'python3 gui.py' in terminal"""
        
        ttk.Label(troubleshooting, text=trouble_text, font=('Arial', 10)).pack(anchor=tk.W)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def load_saved_credentials(self):
        """Load saved credentials from a simple config file"""
        config_file = "config.txt"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith('token='):
                            self.token_var.set(line[6:].strip())
                        elif line.startswith('page_id='):
                            self.page_id_var.set(line[8:].strip())
            except Exception as e:
                self.log(f"Could not load saved credentials: {e}")
    
    def save_credentials(self):
        """Save credentials to config file"""
        try:
            with open("config.txt", 'w') as f:
                f.write(f"token={self.token_var.get()}\n")
                f.write(f"page_id={self.page_id_var.get()}\n")
        except Exception as e:
            self.log(f"Could not save credentials: {e}")
    
    def log(self, message):
        """Add message to log output"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log output"""
        self.log_text.delete(1.0, tk.END)
    
    def validate_inputs(self):
        """Validate user inputs"""
        url = self.url_var.get().strip()
        token = self.token_var.get().strip()
        page_id = self.page_id_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a Wikipedia URL")
            return False
        
        if not url.startswith("https://en.wikipedia.org/wiki/"):
            messagebox.showerror("Error", "Please enter a valid Wikipedia URL (https://en.wikipedia.org/wiki/...)")
            return False
        
        if not token:
            messagebox.showerror("Error", "Please enter your Notion integration token")
            return False
        
        if not page_id:
            messagebox.showerror("Error", "Please enter your Notion parent page ID")
            return False
        
        return True
    
    def preview_article(self):
        """Preview article information before importing"""
        if not self.validate_inputs():
            return
        
        self.clear_log()
        self.log("🔍 Previewing article...")
        
        try:
            # Fetch and analyze article
            url = self.url_var.get().strip()
            title, html = fetch_wikipedia_html(url)
            infobox_data = extract_infobox(html)
            
            self.log(f"✅ Article: {title}")
            self.log(f"📊 Infobox fields found: {len(infobox_data)}")
            
            if infobox_data:
                self.log("📋 Infobox data:")
                for key, value in list(infobox_data.items())[:5]:  # Show first 5
                    self.log(f"   • {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
                if len(infobox_data) > 5:
                    self.log(f"   ... and {len(infobox_data) - 5} more fields")
            else:
                self.log("ℹ️ No infobox data found")
            
            self.status_label.config(text="Preview complete - ready to import! 🎉", foreground='green')
            
        except Exception as e:
            self.log(f"❌ Error previewing article: {e}")
            self.status_label.config(text="Preview failed", foreground='red')
    
    def start_import(self):
        """Start the import process in a separate thread"""
        if not self.validate_inputs():
            return
        
        # Save credentials
        self.save_credentials()
        
        # Start import in separate thread
        self.import_button.config(state='disabled')
        self.preview_button.config(state='disabled')
        self.progress.start()
        self.clear_log()
        self.status_label.config(text="Importing...", foreground='blue')
        
        import_thread = threading.Thread(target=self.import_article)
        import_thread.daemon = True
        import_thread.start()
    
    def import_article(self):
        """Import article to Notion (runs in separate thread)"""
        try:
            # Update global variables in WTNI module
            import WTNI
            WTNI.NOTION_TOKEN = self.token_var.get().strip()
            WTNI.NOTION_PARENT_PAGE = self.page_id_var.get().strip()
            
            # Redirect stdout to capture print statements
            from io import StringIO
            import sys
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            
            # Run the import
            url = self.url_var.get().strip()
            add_article_to_database(url)
            
            # Restore stdout and get output
            sys.stdout = old_stdout
            output = mystdout.getvalue()
            
            # Update UI in main thread
            self.root.after(0, self.import_complete, output, None)
            
        except Exception as e:
            # Update UI in main thread
            self.root.after(0, self.import_complete, None, str(e))
    
    def import_complete(self, output, error):
        """Handle import completion (runs in main thread)"""
        self.progress.stop()
        self.import_button.config(state='normal')
        self.preview_button.config(state='normal')
        
        if error:
            self.log(f"❌ Import failed: {error}")
            self.status_label.config(text="Import failed", foreground='red')
            messagebox.showerror("Import Failed", f"Error: {error}")
        else:
            # Log the output
            if output:
                for line in output.split('\n'):
                    if line.strip():
                        self.log(line.strip())
            
            self.status_label.config(text="Import completed successfully!", foreground='green')
            messagebox.showinfo("Success", "Article imported successfully to Notion!")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.url_var.set("")
        self.clear_log()
        self.status_label.config(text="Ready to import! 🎉", foreground='green')
        
    def on_example_selected(self, event):
        """Handle example URL selection"""
        selected_url = self.example_combo.get()
        self.url_var.set(selected_url)
        
    def clear_placeholder(self, event):
        """Clear placeholder text when user clicks in field"""
        widget = event.widget
        if widget.get() in ["secret_...", "1234567890abcdef..."]:
            widget.delete(0, tk.END)
            widget.config(foreground='black')
            
    def restore_placeholder(self, event):
        """Restore placeholder text if field is empty"""
        widget = event.widget
        if not widget.get():
            if widget == self.token_entry:
                widget.insert(0, "secret_...")
            elif widget == self.page_id_entry:
                widget.insert(0, "1234567890abcdef...")
            widget.config(foreground='gray')
            
    def open_notion_integrations(self):
        """Open Notion integrations page in browser"""
        webbrowser.open("https://www.notion.so/my-integrations")
        self.log("🌐 Opened Notion integrations page in your browser")
        
    def open_setup_guide(self):
        """Open the setup guide in browser"""
        setup_guide_path = os.path.join(os.path.dirname(__file__), "SETUP_GUIDE.html")
        if os.path.exists(setup_guide_path):
            webbrowser.open(f"file://{setup_guide_path}")
            self.log("📖 Opened setup guide in your browser")
        else:
            # Fallback to GitHub repository
            webbrowser.open("https://github.com/FallingWithStyle/Wikipedia-to-Notion")
            self.log("🌐 Opened project page in your browser (setup guide not found locally)")
        
    def test_connection(self):
        """Test Notion connection with current credentials"""
        if not self.validate_inputs():
            return
            
        self.log("🔍 Testing Notion connection...")
        self.status_label.config(text="Testing connection...", foreground='blue')
        
        try:
            # Test the connection by trying to access the parent page
            from notion_client import Client
            client = Client(auth=self.token_var.get().strip())
            
            # Try to get the parent page
            page = client.pages.retrieve(self.page_id_var.get().strip())
            page_title = page.get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'Unknown')
            
            self.log(f"✅ Connection successful! Found page: {page_title}")
            self.status_label.config(text="Connection successful! 🎉", foreground='green')
            
        except Exception as e:
            error_msg = str(e)
            if "unauthorized" in error_msg.lower():
                self.log("❌ Connection failed: Invalid token or token doesn't have access")
                self.status_label.config(text="Connection failed: Check your token", foreground='red')
            elif "not_found" in error_msg.lower():
                self.log("❌ Connection failed: Page ID not found or integration doesn't have access")
                self.status_label.config(text="Connection failed: Check your page ID and permissions", foreground='red')
            else:
                self.log(f"❌ Connection failed: {error_msg}")
                self.status_label.config(text="Connection failed: Check your credentials", foreground='red')
    
    def show_welcome_message(self):
        """Show welcome message for first-time users"""
        welcome_text = """🎉 Welcome to Wikipedia to Notion Importer!

This tool will help you import Wikipedia articles into your Notion workspace with beautiful formatting.

To get started:
1. Click "Get Token" to open Notion integrations
2. Create a new integration and copy the token
3. Get your Notion page ID from any Notion page URL
4. Paste a Wikipedia URL and click "Import Article"

Need help? Check the Help tab or click "Open Setup Guide" for detailed instructions.

Let's get started! 🚀"""
        
        self.log(welcome_text)
        self.status_label.config(text="Welcome! Follow the steps above to get started", foreground='blue')

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = WikipediaToNotionGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
