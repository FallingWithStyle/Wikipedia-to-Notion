#!/usr/bin/env python3
"""
Demo script showing how to use the Wikipedia to Notion GUI programmatically
"""

import tkinter as tk
from gui import WikipediaToNotionGUI

def demo():
    """Run a demo of the GUI with sample data"""
    root = tk.Tk()
    app = WikipediaToNotionGUI(root)
    
    # Pre-fill with sample data for demo
    app.url_var.set("https://en.wikipedia.org/wiki/Artificial_intelligence")
    app.token_var.set("your-notion-token-here")
    app.page_id_var.set("your-page-id-here")
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    print("Demo GUI launched with sample data")
    print("Try the 'Preview Article' button to see how it works!")
    
    root.mainloop()

if __name__ == "__main__":
    demo()
