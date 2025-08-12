import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from typing import List, Optional, Dict, Any

class ModernTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Notes")
        self.root.geometry("999x898")
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.colors = {
            'bg': "#000000",           # Dark blue background
            'card_bg': '#16213e',       # Card background
            'accent': '#0f4c75',        # Accent color
            'primary': '#3282b8',       # Primary buttons
            'success': '#27ae60',       # Success/add buttons
            'warning': '#f39c12',       # Edit buttons
            'danger': '#e74c3c',        # Delete buttons
            'text': '#ecf0f1',          # Main text
            'text_muted': '#95a5a6',    # Muted text
            'border': '#34495e',        # Borders
            'hover': '#2c3e50'          # Hover states
        }
        
        # Configure root
        self.root.configure(bg=self.colors['bg'])
        
        # Data file
        self.data_file = "tasks_nested.json"
        self.tasks_tree = []
        
        # Setup modern styling
        self.setup_styles()
        
        # Load data
        self.load_tasks()
        
        # Setup UI
        self.setup_ui()
        
        # Initial display
        self.refresh_display()
        
        # Auto-save on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Modern.TFrame', background=self.colors['bg'])
        style.configure('Card.TFrame', background=self.colors['card_bg'], 
                       relief='flat', borderwidth=1)
        style.configure('Modern.TLabel', background=self.colors['bg'], 
                       foreground=self.colors['text'], font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=self.colors['bg'], 
                       foreground=self.colors['text'], font=('Segoe UI', 20, 'bold'))
        style.configure('Modern.TEntry', fieldbackground=self.colors['card_bg'],
                       foreground=self.colors['text'], borderwidth=0, relief='flat')
        
        # Button styles
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton', font=('Segoe UI', 9))
        style.configure('Warning.TButton', font=('Segoe UI', 9))
        style.configure('Danger.TButton', font=('Segoe UI', 9))
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    if os.path.getsize(self.data_file) > 0:
                        self.tasks_tree = json.load(f)
                    else:
                        self.tasks_tree = []
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks_tree = []
        else:
            self.tasks_tree = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks_tree, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def create_modern_button(self, parent, text, command, bg_color, width=80, height=35):
        """Create a modern flat button"""
        btn_frame = tk.Frame(parent, bg=bg_color, height=height, width=width)
        btn_frame.pack_propagate(False)
        
        btn = tk.Button(btn_frame, text=text, command=command,
                       bg=bg_color, fg='white', relief='flat', bd=0,
                       font=('Segoe UI', 9, 'bold'), cursor='hand2')
        btn.pack(fill='both', expand=True)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self.lighten_color(bg_color))
        def on_leave(e):
            btn.configure(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn_frame
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        color_map = {
            self.colors['primary']: '#4a9fd1',
            self.colors['success']: '#2ecc71',
            self.colors['warning']: '#f5a623',
            self.colors['danger']: '#ec5555'
        }
        return color_map.get(color, color)
    
    def setup_ui(self):
        """Setup the modern user interface"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header with gradient effect
        header_frame = tk.Frame(main_container, bg=self.colors['bg'], height=80)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_container = tk.Frame(header_frame, bg=self.colors['bg'])
        title_container.pack(expand=True)
        
        title_label = tk.Label(title_container, text="✨ To-Do Notes", 
                              font=('Segoe UI', 24, 'bold'), 
                              bg=self.colors['bg'], fg="#FFFFFF")
        title_label.pack(pady=20)
        
        # Input section with modern styling
        input_container = tk.Frame(main_container, bg=self.colors['card_bg'], 
                                  relief='flat', bd=0, height=70)
        input_container.pack(fill='x', pady=(0, 25))
        input_container.pack_propagate(False)
        
        input_inner = tk.Frame(input_container, bg=self.colors['card_bg'])
        input_inner.pack(fill='both', expand=True, padx=25, pady=15)
        
        # Modern entry field
        entry_frame = tk.Frame(input_inner, bg=self.colors['bg'], relief='flat', bd=2)
        entry_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        self.task_entry = tk.Entry(entry_frame, font=('Segoe UI', 12), 
                                  bg=self.colors['bg'], fg=self.colors['text'],
                                  relief='flat', bd=10, insertbackground=self.colors['text'])
        self.task_entry.pack(fill='both', expand=True)
        self.task_entry.bind('<Return>', self.add_main_task)
        
        # Add button
        add_btn_frame = self.create_modern_button(input_inner, "Add Task", 
                                                 self.add_main_task, 
                                                 self.colors['success'], 120, 45)
        add_btn_frame.pack(side='right')
        
        # Main content area with custom scrollbar
        content_container = tk.Frame(main_container, bg=self.colors['bg'])
        content_container.pack(fill='both', expand=True)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(content_container, bg=self.colors['bg'], 
                               highlightthickness=0, bd=0)
        
        # Custom scrollbar
        scrollbar_frame = tk.Frame(content_container, bg=self.colors['border'], width=8)
        scrollbar_frame.pack(side="right", fill="y")
        
        self.scrollbar = tk.Frame(scrollbar_frame, bg=self.colors['primary'], width=6)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Mousewheel binding
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.root.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Focus on entry
        self.task_entry.focus()
    
    def get_task_from_path(self, path: List[int]) -> Optional[Dict[Any, Any]]:
        """Navigate to a task using path indices"""
        if not path:
            return None
        
        current = self.tasks_tree
        for i, index in enumerate(path):
            try:
                if i == len(path) - 1:
                    return current[index]
                else:
                    current = current[index].get('subtasks', [])
            except (IndexError, KeyError, AttributeError):
                return None
        return None
    
    def get_parent_list_from_path(self, path: List[int]) -> Optional[List]:
        """Get the list containing the target task"""
        if not path:
            return None
        if len(path) == 1:
            return self.tasks_tree
        
        parent_path = path[:-1]
        current = self.tasks_tree
        for index in parent_path:
            try:
                current = current[index]['subtasks']
            except (IndexError, KeyError):
                return None
        return current
    
    def add_main_task(self, event=None):
        """Add a main task from the entry field"""
        text = self.task_entry.get().strip()
        if text:
            self.add_task_to_path(text, None)
            self.task_entry.delete(0, tk.END)
            self.task_entry.focus()
    
    def add_task_to_path(self, text: str, path: Optional[List[int]]):
        """Add a task at the specified path"""
        if not text.strip():
            return
        
        new_task = {
            "text": text.strip(),
            "done": False,
            "subtasks": []
        }
        
        if path is None:
            self.tasks_tree.append(new_task)
        else:
            parent_task = self.get_task_from_path(path)
            if parent_task is not None:
                if 'subtasks' not in parent_task:
                    parent_task['subtasks'] = []
                parent_task['subtasks'].append(new_task)
        
        self.save_tasks()
        self.refresh_display()
    
    def toggle_task(self, path: List[int]):
        """Toggle task completion status"""
        task = self.get_task_from_path(path)
        if task is not None:
            task['done'] = not task.get('done', False)
            self.save_tasks()
            self.refresh_display()
    
    def edit_task(self, path: List[int]):
        """Edit a task's text"""
        task = self.get_task_from_path(path)
        if task is None:
            return
        
        # Custom dialog for better styling
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("400x150")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 300, self.root.winfo_rooty() + 200))
        
        tk.Label(dialog, text="Edit Task:", font=('Segoe UI', 12), 
                bg=self.colors['bg'], fg=self.colors['text']).pack(pady=10)
        
        entry = tk.Entry(dialog, font=('Segoe UI', 11), bg=self.colors['card_bg'], 
                        fg=self.colors['text'], relief='flat', bd=10)
        entry.pack(fill='x', padx=20, pady=5)
        entry.insert(0, task['text'])
        entry.focus()
        entry.select_range(0, tk.END)
        
        def save_edit():
            new_text = entry.get().strip()
            if new_text:
                task['text'] = new_text
                self.save_tasks()
                self.refresh_display()
            dialog.destroy()
        
        def cancel_edit():
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        save_btn = self.create_modern_button(btn_frame, "Save", save_edit, self.colors['success'])
        save_btn.pack(side='left', padx=5)
        
        cancel_btn = self.create_modern_button(btn_frame, "Cancel", cancel_edit, self.colors['danger'])
        cancel_btn.pack(side='left', padx=5)
        
        entry.bind('<Return>', lambda e: save_edit())
        dialog.bind('<Escape>', lambda e: cancel_edit())
    
    def delete_task(self, path: List[int]):
        """Delete a task after confirmation"""
        task = self.get_task_from_path(path)
        if task is None:
            return
        
        result = messagebox.askyesno("Delete Task", 
                                   f"Delete '{task['text']}'?\n\nThis will also delete all subtasks.",
                                   icon='warning')
        if result:
            parent_list = self.get_parent_list_from_path(path)
            task_index = path[-1]
            if parent_list is not None and 0 <= task_index < len(parent_list):
                parent_list.pop(task_index)
                self.save_tasks()
                self.refresh_display()
    
    def add_subtask(self, path: List[int]):
        """Add a subtask to the specified task"""
        # Custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Subtask")
        dialog.geometry("400x150")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 300, self.root.winfo_rooty() + 200))
        
        tk.Label(dialog, text="Add Subtask:", font=('Segoe UI', 12), 
                bg=self.colors['bg'], fg=self.colors['text']).pack(pady=10)
        
        entry = tk.Entry(dialog, font=('Segoe UI', 11), bg=self.colors['card_bg'], 
                        fg=self.colors['text'], relief='flat', bd=10)
        entry.pack(fill='x', padx=20, pady=5)
        entry.focus()
        
        def add_sub():
            text = entry.get().strip()
            if text:
                self.add_task_to_path(text, path)
            dialog.destroy()
        
        def cancel_add():
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        add_btn = self.create_modern_button(btn_frame, "Add", add_sub, self.colors['success'])
        add_btn.pack(side='left', padx=5)
        
        cancel_btn = self.create_modern_button(btn_frame, "Cancel", cancel_add, self.colors['danger'])
        cancel_btn.pack(side='left', padx=5)
        
        entry.bind('<Return>', lambda e: add_sub())
        dialog.bind('<Escape>', lambda e: cancel_add())
    
    def create_task_widget(self, task: Dict[Any, Any], path: List[int], depth: int = 0) -> tk.Frame:
        """Create a modern widget for a single task"""
        # Main container with subtle shadow effect
        task_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg'])
        
        # Task card with modern styling
        card_bg = self.colors['hover'] if task.get('done', False) else self.colors['card_bg']
        task_card = tk.Frame(task_frame, bg=card_bg, relief='flat', bd=1)
        task_card.pack(padx=(depth * 40 + 100, 100), pady=3)  # Add equal padding on both sides
        
        # Inner content with padding
        content_frame = tk.Frame(task_card, bg=card_bg)
        content_frame.pack(fill='x', padx=20, pady=15)
        
        # Left side - checkbox and text
        left_frame = tk.Frame(content_frame, bg=card_bg)
        left_frame.pack(side='left', fill='x', expand=True)
        
        # Custom checkbox
        checkbox_frame = tk.Frame(left_frame, bg=card_bg, width=20, height=20)
        checkbox_frame.pack(side='left', padx=(0, 15))
        checkbox_frame.pack_propagate(False)
        
        is_done = task.get('done', False)
        check_bg = self.colors['success'] if is_done else self.colors['border']
        check_text = "✓" if is_done else ""
        
        checkbox = tk.Button(checkbox_frame, text=check_text, bg=check_bg, fg='white',
                           relief='flat', bd=0, font=('Segoe UI', 10, 'bold'),
                           command=lambda: self.toggle_task(path[:]), cursor='hand2')
        checkbox.pack(fill='both', expand=True)
        
        # Task text with modern typography
        text_color = self.colors['text_muted'] if is_done else self.colors['text']
        font_style = ('Segoe UI', 11, 'overstrike') if is_done else ('Segoe UI', 11)
        
        text_label = tk.Label(left_frame, text=task['text'], font=font_style,
                             fg=text_color, bg=card_bg, anchor='w')
        text_label.pack(side='left', fill='x', expand=True)
        
        # Right side - modern action buttons
        button_frame = tk.Frame(content_frame, bg=card_bg)
        button_frame.pack(side='right')
        
        # Action buttons with icons
        add_btn = self.create_modern_button(button_frame, "＋", 
                                           lambda: self.add_subtask(path[:]), 
                                           self.colors['primary'], 30, 30)
        add_btn.pack(side='left', padx=2)
        
        edit_btn = self.create_modern_button(button_frame, "✎", 
                                            lambda: self.edit_task(path[:]), 
                                            self.colors['warning'], 30, 30)
        edit_btn.pack(side='left', padx=2)
        
        delete_btn = self.create_modern_button(button_frame, "✕", 
                                              lambda: self.delete_task(path[:]), 
                                              self.colors['danger'], 30, 30)
        delete_btn.pack(side='left', padx=2)
        
        return task_frame
    
    def refresh_display(self):
        """Refresh the entire task display"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.tasks_tree:
            # Modern empty state
            empty_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg'])
            empty_frame.pack(fill='both', expand=True, pady=100)
            
            empty_label = tk.Label(empty_frame, text="🎯\n\nNo tasks yet!\nAdd your first task above to get started.",
                                  font=('Segoe UI', 16), fg=self.colors['text_muted'], 
                                  bg=self.colors['bg'], justify='center')
            empty_label.pack(padx=200, pady=3,expand=True)
        else:
            # Display all tasks
            for i, task in enumerate(self.tasks_tree):
                self.display_task_recursive(task, [i], 0)
    
    def display_task_recursive(self, task: Dict[Any, Any], path: List[int], depth: int):
        """Recursively display a task and its subtasks"""
        # Create and pack the task widget
        task_widget = self.create_task_widget(task, path, depth)
        task_widget.pack(fill='x', pady=1)
        
        # Display subtasks
        if 'subtasks' in task and task['subtasks']:
            for i, subtask in enumerate(task['subtasks']):
                self.display_task_recursive(subtask, path + [i], depth + 1)
    
    def on_closing(self):
        """Handle application closing"""
        self.save_tasks()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ModernTodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()