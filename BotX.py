# By Dhanwanth
import sympy as sp
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Frame, Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from PIL import Image, ImageTk
import io

# --- Solver functions ---
def solveX(eq, symbols, domain="real"):
    if not isinstance(symbols, (list, tuple)):
        symbols = [symbols]
    if domain.lower() == "real":
        dom = sp.S.Reals
        filter_imag = False
    elif domain.lower() == "complex":
        dom = sp.S.Complexes
        filter_imag = False
    elif domain.lower() == "imaginary":
        dom = sp.S.Complexes
        filter_imag = True
    else:
        raise ValueError("Domain must be 'real', 'complex', or 'imaginary'")
    
    solutions = []
    for sym in symbols:
        try:
            sol = sp.solveset(eq, sym, domain=dom)
        except Exception:
            sol = sp.ConditionSet(sym, eq, dom)

        # If we get nothing useful, try nsolve numerically
        if isinstance(sol, sp.ConditionSet) or sol == sp.EmptySet:
            try:
                # Try a few initial guesses to catch multiple roots
                numeric_solutions = []
                for guess in [0.1, 1, 2, 5, 10]:
                    try:
                        nsol = sp.nsolve(eq, sym, guess)
                        if nsol not in numeric_solutions:
                            numeric_solutions.append(nsol)
                    except:
                        pass
                if numeric_solutions:
                    sol = sp.FiniteSet(*numeric_solutions)
            except Exception:
                pass

        if filter_imag and isinstance(sol, (sp.FiniteSet, set)):
            sol = sp.FiniteSet(*[s for s in sol if s.is_imaginary])

        solutions.append(sol)

    if len(solutions) == 1:
        return solutions[0]
    return solutions

def get_solution(eq_str, domain="real", numerical=False):
    x = sp.symbols('x')
    if '=' in eq_str:
        lhs_str, rhs_str = eq_str.split('=', 1)
        lhs = sp.sympify(lhs_str.strip())
        rhs = sp.sympify(rhs_str.strip())
        eq = sp.Eq(lhs, rhs)
    else:
        expr = sp.sympify(eq_str, evaluate=False)
        eq = sp.Eq(expr, 0)
    
    if numerical:
        # Force numerical solving with multiple guesses
        numeric_sols = []
        guesses = [-10, -5, -2, -1, -0.5, 0, 0.5, 1, 2, 5, 10]
        for guess in guesses:
            try:
                # For complex domains, use complex guess if needed
                if domain.lower() == "complex":
                    guess = complex(guess, 0)
                sol = sp.nsolve(eq, x, guess)
                # Check for duplicates (with tolerance)
                if all(abs(sol - existing) > 1e-6 for existing in numeric_sols):
                    numeric_sols.append(sol)
            except:
                pass
        solutions = sp.FiniteSet(*numeric_sols) if numeric_sols else sp.EmptySet
    else:
        solutions = solveX(eq, x, domain)
    return solutions, eq

# --- Modern Chatbot GUI with LaTeX and Plotting (Fixed Scrolling) ---
class ModernBotXGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("botX AI Math Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Initialize attributes early
        self.message_count = 0
        self.last_equation = None
        self.numerical_var = tk.BooleanVar(value=False)  # New toggle for numerical mode
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TLabel', background='#2c3e50', foreground='white')
        self.style.configure('TButton', background='#3498db', foreground='white')
        self.style.configure('TCombobox', fieldbackground='#ecf0f1', background='#ecf0f1')
        self.style.configure('TEntry', fieldbackground='#ecf0f1', background='#ecf0f1')
        self.style.configure('TCheckbutton', background='#2c3e50', foreground='white')
        
        # Main container
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with logo and title
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Logo placeholder
        self.logo_label = ttk.Label(header_frame, text="🧮", font=('Arial', 24))
        self.logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ttk.Label(header_frame, text="botX AI Math Assistant", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Chat area with modern design - PROPER SCROLLBAR PLACEMENT
        chat_container = ttk.Frame(main_frame)
        chat_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chat display with gradient background
        self.chat_canvas = Canvas(chat_container, bg='#34495e', highlightthickness=0)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create scrollbar for chat - PROPERLY SIZED AND PLACED
        self.scrollbar = ttk.Scrollbar(chat_container, orient=tk.VERTICAL, command=self.chat_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create frame inside canvas for messages
        self.chat_inner_frame = ttk.Frame(self.chat_canvas, style='TFrame')
        self.chat_window = self.chat_canvas.create_window((0, 0), window=self.chat_inner_frame, anchor="nw")
        
        # Input area - SEPARATED FROM CHAT AREA
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Domain selection
        domain_frame = ttk.Frame(input_frame)
        domain_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(domain_frame, text="Domain:").pack()
        self.domain_var = tk.StringVar(value="real")
        domain_combo = ttk.Combobox(domain_frame, textvariable=self.domain_var, 
                                  values=["real", "complex", "imaginary"],
                                  state="readonly", width=12)
        domain_combo.pack()
        
        # Numerical mode toggle
        mode_frame = ttk.Frame(input_frame)
        mode_frame.pack(side=tk.LEFT, padx=(0, 10))
        self.mode_check = ttk.Checkbutton(mode_frame, text="Numerical Mode", 
                                        variable=self.numerical_var,
                                        command=self.on_mode_toggle)
        self.mode_check.pack()
        
        # Equation input
        self.input_entry = ttk.Entry(input_frame, font=('Arial', 12), width=50)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.insert(0, "Enter equation (e.g., x^2 = 4)")
        self.input_entry.bind("<FocusIn>", self.clear_placeholder)
        self.input_entry.bind("<Return>", self.send_message)
        
        # Action buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(side=tk.RIGHT)
        
        self.send_btn = ttk.Button(button_frame, text="Solve", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.plot_btn = ttk.Button(button_frame, text="Plot", command=self.plot_equation, state="disabled")
        self.plot_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_chat)
        self.clear_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready | Domain: real | Mode: Symbolic")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Welcome message
        self.add_bot_message("Hello! I'm botX, your AI math assistant. I can solve equations, plot functions, and explain mathematical concepts. Try entering an equation like 'x^2 = 4' or 'sin(x) = 0.5'! Toggle 'Numerical Mode' for approximate solutions.")
        
        # Bind events for scrolling
        self.chat_inner_frame.bind("<Configure>", self.on_frame_configure)
        self.chat_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Mousewheel support
        self.chat_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.chat_canvas.bind("<Button-4>", self.on_mousewheel)
        self.chat_canvas.bind("<Button-5>", self.on_mousewheel)
        
        # Arrow key binding for scrolling
        self.chat_canvas.bind("<Up>", lambda e: self.chat_canvas.yview_scroll(-1, "units"))
        self.chat_canvas.bind("<Down>", lambda e: self.chat_canvas.yview_scroll(1, "units"))
        self.chat_canvas.bind("<Prior>", lambda e: self.chat_canvas.yview_scroll(-1, "pages"))  # Page Up
        self.chat_canvas.bind("<Next>", lambda e: self.chat_canvas.yview_scroll(1, "pages"))   # Page Down
        self.chat_canvas.bind("<Home>", lambda e: self.chat_canvas.yview_moveto(0.0))
        self.chat_canvas.bind("<End>", lambda e: self.chat_canvas.yview_moveto(1.0))
        
        # Focus the canvas to enable arrow key scrolling
        self.chat_canvas.focus_set()
        
        # Make sure chat area gets focus when clicked
        self.chat_canvas.bind("<Button-1>", lambda e: self.chat_canvas.focus_set())
        
    def on_mode_toggle(self):
        """Update status when mode is toggled."""
        self.update_status()
        if self.numerical_var.get():
            self.add_bot_message("Switched to Numerical Mode: Solutions will be approximate values.")
        else:
            self.add_bot_message("Switched to Symbolic Mode: Solutions will be exact/simplified.")
    
    def clear_placeholder(self, event):
        if self.input_entry.get() == "Enter equation (e.g., x^2 = 4)":
            self.input_entry.delete(0, tk.END)
    
    def on_frame_configure(self, event):
        """Update scrollregion when inner frame changes size."""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas resizes."""
        self.chat_canvas.itemconfig(self.chat_window, width=event.width)
    
    def on_mousewheel(self, event):
        """Handle mousewheel scrolling."""
        if event.delta:
            scroll_amount = -1 * (event.delta // 120)
        elif event.num == 4:
            scroll_amount = -1
        elif event.num == 5:
            scroll_amount = 1
        else:
            return
        
        self.chat_canvas.yview_scroll(scroll_amount, "units")
        return "break"
    
    def add_message(self, sender, message, is_bot=True):
        """Add a message to the chat with appropriate styling."""
        message_frame = ttk.Frame(self.chat_inner_frame)
        message_frame.pack(fill=tk.X, pady=5)
        
        # Avatar
        avatar_text = "🤖" if is_bot else "👤"
        avatar = ttk.Label(message_frame, text=avatar_text, font=('Arial', 16),
                          background='#34495e', foreground='white')
        avatar.pack(side=tk.LEFT, padx=(10, 5))
        
        # Message bubble
        bubble_frame = ttk.Frame(message_frame)
        bubble_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        bubble = ttk.Frame(bubble_frame)
        bubble.pack(fill=tk.X, expand=True)
        
        # Different colors for bot and user
        bg_color = '#3498db' if is_bot else '#95a5a6'
        text_color = 'white' if is_bot else 'black'
        
        message_label = ttk.Label(bubble, text=message, wraplength=600, justify=tk.LEFT,
                                background=bg_color, foreground=text_color,
                                font=('Arial', 11), padding=10,
                                borderwidth=2, relief='raised')
        message_label.pack(fill=tk.X, expand=True)
        
        if not hasattr(self, 'message_count'):
            self.message_count = 0
        self.message_count += 1
        self.update_status()
        
        # Update scroll region and scroll to bottom
        self.chat_canvas.update_idletasks()
        self.on_frame_configure(None)
        self.chat_canvas.yview_moveto(1.0)
    
    def add_bot_message(self, message):
        self.add_message("botX", message, True)
    
    def add_user_message(self, message):
        self.add_message("You", message, False)
    
    def render_latex(self, latex_str):
        """Render LaTeX string to image"""
        try:
            fig = Figure(figsize=(6, 2), dpi=100)
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f"${latex_str}$", fontsize=16, ha='center', va='center')
            ax.axis('off')
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
            buf.seek(0)
            
            image = Image.open(buf)
            photo = ImageTk.PhotoImage(image)
            
            return photo
        except:
            return None
    
    def format_solution(self, solutions, domain, numerical=False):
        """Format solutions with LaTeX rendering or numerical display"""
        if solutions == sp.EmptySet:
            return "No solutions found in the specified domain."
        
        if numerical:
            # Format numerical solutions
            try:
                nums = [str(s.evalf(6)) for s in solutions]
                return ", ".join(nums)
            except:
                return str(solutions)
        else:
            # Symbolic LaTeX
            try:
                latex_str = sp.latex(solutions)
                return latex_str
            except:
                return str(solutions)
    
    def plot_equation(self):
        """Plot the equation if it's plottable"""
        if self.last_equation is None:
            self.add_bot_message("Please solve an equation first before plotting.")
            return
        
        try:
            equation = self.last_equation
            x = sp.symbols('x')
            
            if self.domain_var.get() != "real":
                self.add_bot_message("Plotting is only supported in the 'real' domain.")
                return
            
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Equation Plot")
            plot_window.geometry("800x600")
            
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            if equation.rhs == 0:
                expr = equation.lhs
            else:
                expr = equation.lhs - equation.rhs
            
            try:
                f = sp.lambdify(x, expr, 'numpy')
            except Exception as e:
                self.add_bot_message(f"Could not create plottable function: {str(e)}")
                plot_window.destroy()
                return
            
            x_vals = np.linspace(-10, 10, 400)
            try:
                y_vals = f(x_vals)
                mask = np.isfinite(y_vals)
                x_vals = x_vals[mask]
                y_vals = y_vals[mask]
            except Exception as e:
                self.add_bot_message(f"Error evaluating function: {str(e)}")
                plot_window.destroy()
                return
            
            if len(x_vals) == 0:
                self.add_bot_message("No valid points to plot (function may be undefined).")
                plot_window.destroy()
                return
            
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'y = {sp.latex(expr)}')
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'Plot of ${sp.latex(expr)}$')
            ax.legend()
            
            canvas = FigureCanvasTkAgg(fig, plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.add_bot_message("I've created a plot of your equation in a new window!")
            
        except Exception as e:
            self.add_bot_message(f"Could not plot the equation: {str(e)}")
    
    def update_status(self):
        mode_text = "Numerical" if self.numerical_var.get() else "Symbolic"
        self.status_var.set(f"Messages: {self.message_count} | Domain: {self.domain_var.get()} | Mode: {mode_text}")
    
    def clear_chat(self):
        for widget in self.chat_inner_frame.winfo_children():
            widget.destroy()
        self.message_count = 0
        self.last_equation = None
        self.plot_btn.config(state="disabled")
        self.update_status()
        self.on_frame_configure(None)
        self.add_bot_message("Chat cleared. Ready to solve more equations!")
    
    def send_message(self, event=None):
        user_input = self.input_entry.get().strip()
        if not user_input or user_input == "Enter equation (e.g., x^2 = 4)":
            return
        
        user_input = user_input.replace('^', '**').replace('ln','log')
        self.add_user_message(user_input)
        self.input_entry.delete(0, tk.END)
        
        if user_input.lower() == 'quit':
            self.root.quit()
            return
        
        try:
            numerical = self.numerical_var.get()
            if numerical and self.domain_var.get() != "real":
                self.add_bot_message("⚠️ Numerical mode is best suited for real domain. Proceeding with approximations anyway.")
            
            solutions, equation = get_solution(user_input, self.domain_var.get(), numerical)
            self.last_equation = equation
            self.plot_btn.config(state="normal")
            
            formatted = self.format_solution(solutions, self.domain_var.get(), numerical)
            latex_image = self.render_latex(formatted) if not numerical else None
            
            if latex_image and not numerical:
                message_frame = ttk.Frame(self.chat_inner_frame)
                message_frame.pack(fill=tk.X, pady=5)
                avatar = ttk.Label(message_frame, text="🤖", font=('Arial', 16),
                                 background='#34495e', foreground='white')
                avatar.pack(side=tk.LEFT, padx=(10, 5))
                
                bubble_frame = ttk.Frame(message_frame)
                bubble_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # LaTeX image label
                latex_label = ttk.Label(bubble_frame, image=latex_image,
                                      background='#3498db')
                latex_label.image = latex_image
                latex_label.pack(pady=10)
                
                # Add text explanation
                explanation = "Here's the solution to your equation:"
                if solutions == sp.EmptySet:
                    explanation = "No solutions found in the specified domain."
                
                text_label = ttk.Label(bubble_frame, text=explanation,
                                     background='#3498db', foreground='white',
                                     font=('Arial', 11), padding=5)
                text_label.pack(fill=tk.X)
                
            else:
                # For numerical or if LaTeX fails, use text message
                if numerical:
                    explanation = "Numerical solutions (approx. to 6 decimals):"
                else:
                    explanation = "Symbolic solution:"
                if solutions == sp.EmptySet:
                    explanation = "No solutions found in the specified domain."
                
                msg = f"{explanation}\n{formatted}"
                self.add_bot_message(msg)
            
            # Plot suggestion for real domain
            if self.domain_var.get() == "real" and solutions != sp.EmptySet and self.last_equation is not None:
                plot_frame = ttk.Frame(self.chat_inner_frame)
                plot_frame.pack(fill=tk.X, pady=5)
                
                plot_label = ttk.Label(plot_frame, text="Would you like to see a plot of this equation?",
                                    background='#34495e', foreground='white')
                plot_label.pack(side=tk.LEFT, padx=(10, 5))
                
                plot_btn = ttk.Button(plot_frame, text="Plot Equation", 
                                    command=self.plot_equation)
                plot_btn.pack(side=tk.LEFT)
                
        except sp.SympifyError as e:
            self.add_bot_message(f"❌ I couldn't understand that equation. Please use proper mathematical syntax.\nExample: x**2 = 4 or sin(x) = 0.5")
        except Exception as e:
            self.add_bot_message(f"❌ Error solving equation: {str(e)}\nPlease check your input and try again.")

# --- Run the application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBotXGUI(root)
    root.mainloop()
