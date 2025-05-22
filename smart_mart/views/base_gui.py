import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

class BaseGUI:
    def __init__(self, title: str):
        self.root = tk.Tk()
        self.root.title(f"Smart Mart - {title}")
        self.root.geometry("1200x800")  # Larger default window
        self.root.resizable(True, True)  # Allow resizing
        
        # Set theme and configure styles
        self.setup_styles()
        
        # Create main container with padding
        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)

    def setup_styles(self):
        """Configure modern styles for the application."""
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color palette
        self.colors = {
            'primary': '#2196F3',      # Material Blue
            'primary_dark': '#1976D2',
            'secondary': '#FF4081',     # Pink Accent
            'success': '#4CAF50',       # Material Green
            'warning': '#FFC107',       # Material Amber
            'danger': '#F44336',        # Material Red
            'light': '#FAFAFA',         # Almost White
            'dark': '#212121',          # Almost Black
            'gray': '#9E9E9E',          # Material Gray
            'white': '#FFFFFF'
        }
        
        # Configure common styles
        style.configure('TFrame', background=self.colors['light'])
        style.configure('TLabel', 
                       background=self.colors['light'],
                       font=('Segoe UI', 10))
        style.configure('Header.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.colors['primary_dark'])
        
        # Button styles
        self._configure_button_style(style, 'Primary.TButton', self.colors['primary'])
        self._configure_button_style(style, 'Success.TButton', self.colors['success'])
        self._configure_button_style(style, 'Danger.TButton', self.colors['danger'])
        
        # Entry style
        style.configure('TEntry',
                       fieldbackground=self.colors['white'],
                       padding=5)
        
        # Treeview style
        style.configure('Treeview',
                       background=self.colors['white'],
                       fieldbackground=self.colors['white'],
                       rowheight=30)
        style.configure('Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       padding=5)
        
        # Notebook style
        style.configure('TNotebook',
                       background=self.colors['light'])
        style.configure('TNotebook.Tab',
                       padding=[10, 5],
                       font=('Segoe UI', 10))

    def _configure_button_style(self, style, name, color):
        """Configure button style with hover effects."""
        style.configure(name,
                       background=color,
                       foreground=self.colors['white'],
                       font=('Segoe UI', 10),
                       padding=[10, 5])
        
        # Hover effect (darker)
        darker_color = self._adjust_color_brightness(color, -20)
        style.map(name,
                 background=[('active', darker_color)],
                 foreground=[('active', self.colors['white'])])

    def _adjust_color_brightness(self, color: str, factor: int) -> str:
        """Adjust color brightness by a factor (-255 to 255)."""
        # Convert hex to RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Adjust brightness
        new_rgb = tuple(max(0, min(255, c + factor)) for c in rgb)
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def create_entry_field(self, container, label: str, show: str = None) -> ttk.Entry:
        """Create a styled entry field with label."""
        frame = ttk.Frame(container)
        frame.pack(fill=tk.X, pady=10)
        
        label = ttk.Label(frame, text=label)
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        entry = ttk.Entry(frame, show=show)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        return entry

    def create_button(self, container, text: str, command, style: str = 'Primary.TButton') -> ttk.Button:
        """Create a styled button."""
        button = ttk.Button(container, text=text, command=command, style=style)
        button.pack(pady=5, padx=5, fill=tk.X)
        return button

    def create_section(self, container, title: str) -> ttk.Frame:
        """Create a section with a header."""
        frame = ttk.Frame(container, padding="10")
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(frame, text=title, style='Header.TLabel').pack(pady=(0, 10))
        
        return frame

    def show_error(self, message: str):
        """Show styled error message."""
        messagebox.showerror("Error", message)

    def show_success(self, message: str):
        """Show styled success message."""
        messagebox.showinfo("Success", message)

    def show_warning(self, message: str):
        """Show styled warning message."""
        messagebox.showwarning("Warning", message)

    def run(self):
        """Start the GUI main loop."""
        # Center the window on screen
        self.center_window()
        self.root.mainloop()

    def close(self):
        """Close the window."""
        self.root.destroy()

    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def set_background(self):
        """Set the background image for the window."""
        try:
            # Get the path to the images directory
            current_dir = os.path.dirname(os.path.dirname(__file__))
            image_path = os.path.join(current_dir, 'assets', 'background.png')
            
            # Create assets directory if it doesn't exist
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # If background image doesn't exist, create a default one
            if not os.path.exists(image_path):
                self.create_default_background(image_path)
            
            # Load and set the background
            image = Image.open(image_path)
            image = image.resize((1024, 768), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        except Exception as e:
            print(f"Error setting background: {e}")
            self.root.configure(bg=self.colors['light'])

    def create_default_background(self, image_path: str):
        """Create a default gradient background image."""
        try:
            from PIL import Image, ImageDraw
            
            # Create a gradient background
            image = Image.new('RGB', (1024, 768))
            draw = ImageDraw.Draw(image)
            
            for y in range(768):
                r = int(44 + (y / 768) * 0)
                g = int(62 + (y / 768) * 0)
                b = int(80 + (y / 768) * 0)
                draw.line([(0, y), (1024, y)], fill=(r, g, b))
                
            image.save(image_path)
            
        except Exception as e:
            print(f"Error creating default background: {e}") 