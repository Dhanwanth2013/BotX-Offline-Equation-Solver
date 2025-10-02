# 🧮 botX AI Math Assistant

![botX Logo](https://via.placeholder.com/800x200/3498db/ffffff?text=botX+AI+Math+Assistant) <!-- Placeholder for logo; replace with actual image if available -->

Welcome to **botX**! 🚀 A modern, interactive GUI application built with Python that serves as your personal AI-powered math assistant. botX helps you solve mathematical equations symbolically or numerically, plot functions, and explore solutions across different domains (real, complex, or imaginary). Whether you're a student, teacher, or math enthusiast, botX makes solving equations fun and intuitive through a sleek chat-like interface. 💬

This project combines the power of **SymPy** for symbolic mathematics, **Tkinter** for the GUI, **Matplotlib** for plotting, and more to create a user-friendly tool. No more scribbling on paper—let botX do the heavy lifting! 📐✨

## 📋 Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Supported Equations](#supported-equations)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## ✨ Features
botX is packed with powerful features to make math solving effortless:

- **Equation Solving** 🔍
  - Solve equations symbolically (exact solutions) or numerically (approximate values with 6 decimal places).
  - Supports multiple domains: **Real** (default), **Complex**, and **Imaginary** numbers.
  - Handles polynomials, trigonometric functions, logarithms, and more using SymPy's `solveset` and `nsolve`.

- **Plotting Capabilities** 📈
  - Visualize equations in a new window using Matplotlib.
  - Plots the function `f(x) = 0` (or `lhs - rhs = 0`) over a range (-10 to 10).
  - Includes grid, axes, and legends for clarity.
  - Only available in the real domain for simplicity.

- **Interactive Chat Interface** 💬
  - Modern, scrollable chat window with avatars (🤖 for bot, 👤 for user).
  - Message bubbles with colors: Blue for bot responses, gray for user inputs.
  - Auto-scrolls to the bottom and supports mousewheel, arrow keys, and page navigation.

- **Mode Toggle** ⚙️
  - **Symbolic Mode** (default): Exact solutions in LaTeX-rendered images.
  - **Numerical Mode**: Approximate solutions for tough equations where symbolic solving fails.
  - Toggle via checkbox; updates status bar and notifies in chat.

- **Domain Selection** 🌐
  - Dropdown for Real, Complex, or Imaginary domains.
  - Filters solutions accordingly (e.g., only imaginary parts in Imaginary mode).

- **User -Friendly UI** 🎨
  - Dark theme with gradient backgrounds (#2c3e50, #34495e).
  - Status bar showing message count, domain, and mode.
  - Placeholder text in input field for guidance.
  - Buttons for Solve, Plot, and Clear chat.
  - Error handling with friendly messages (e.g., invalid syntax suggestions).

- **Advanced Solving Fallbacks** 🛡️
  - If symbolic solving returns no results, falls back to numerical `nsolve` with multiple initial guesses (-10 to 10).
  - Duplicate detection in numerical solutions to avoid repeats.
  - Handles complex guesses in complex domains.

- **LaTeX Rendering** 📝
  - Symbolic solutions rendered as images using Matplotlib (inline math with `$...$`).
  - Fallback to plain text if rendering fails.

- **Extensibility** 🔧
  - Easy to add more solvers or features (e.g., integration, differentiation).
  - Modular code structure: Separate solver functions, GUI class, and event handlers.

## 📸 Screenshots
Here are some visuals of botX in action (descriptions; add actual images for a real repo):

1. **Main Interface** 🖥️
   - Header with logo (🧮) and title.
   - Chat area with welcome message.
   - Input bar: Domain dropdown, Numerical toggle, Equation entry, Solve/Plot/Clear buttons.
   - Status bar at bottom.

   ![Main Interface](https://via.placeholder.com/800x600/34495e/ffffff?text=Main+Interface+Screenshot)

2. **Solving an Equation** 🧩
   - User enters `x**2 = 4`.
   - Bot responds with LaTeX-rendered solution: `{ -2, 2 }`.
   - Numerical mode shows: `-2.000000, 2.000000`.
   - Plot suggestion button appears.

   ![Solving Example](https://via.placeholder.com/800x600/3498db/ffffff?text=Solving+x%5E2+%3D+4)

3. **Plot Window** 📊
   - Separate popup with Matplotlib plot of `y = x^2 - 4`.
   - Blue line, grid, axes, and title with LaTeX.

   ![Plot Example](https://via.placeholder.com/800x600/ffffff/000000?text=Plot+Window)

4. **Complex Domain Example** 🔄
   - Equation: `x**2 + 1 = 0` in Complex mode.
   - Solution: `{I, -I}` (imaginary units).

   ![Complex Example](https://via.placeholder.com/800x600/34495e/ffffff?text=Complex+Domain+Solution)

5. **Error Handling** ⚠️
   - Invalid input: "abc = 1" shows helpful error message.

   ![Error Example](https://via.placeholder.com/800x600/e74c3c/ffffff?text=Error+Message)

## 🛠️ Installation
botX requires **Python 3.6+**. Follow these steps to get started:

1. **Clone or Download the Repository** 📥
git clone <your-repo-url> cd botX-math-assistant

2. **Install Dependencies** 📦
Use pip to install required packages. Tkinter is included in standard Python, but others need installation:
pip install sympy matplotlib numpy pillow
- **SymPy**: For symbolic math solving (`solveset`, `nsolve`, `lambdify`).
- **Matplotlib**: For plotting and LaTeX rendering to images.
- **NumPy**: For numerical computations in plots.
- **Pillow (PIL)**: For image handling in Tkinter.

**Note**: On some systems (e.g., Linux), you may need `sudo apt install python3-tk` for Tkinter.

3. **Run the Application** ▶️
python BotX.py
The GUI will launch in a 1200x800 window. No additional configuration needed!

4. **Optional: Virtual Environment** 🐍
For isolation:
python -m venv botx-env source botx-env/bin/activate # On Windows: botx-env\Scripts\activate pip install sympy matplotlib numpy pillow python main.py

## 🚀 Usage
1. **Launch botX** and read the welcome message. 👋
2. **Select Domain**: Use the dropdown (Real/Complex/Imaginary). 🌐
3. **Toggle Mode**: Check "Numerical Mode" for approximations if symbolic fails. ⚙️
4. **Enter Equation**: Type in the input field, e.g.:
- `x**2 = 4` (polynomial)
- `sin(x) = 0.5` (trigonometric)
- `log(x) = 1` (logarithmic; note: `ln` auto-converts to `log`)
- `x**2 + 1 = 0` (for complex roots)
Use `**` for exponents (e.g., `x**2`), and standard math functions.
5. **Press Solve** or hit Enter. 🔍 The bot will respond in the chat.
6. **View Solution**: Symbolic results show as rendered math images; numerical as text.
7. **Plot (Optional)**: If in real domain, click "Plot Equation" for a graph. 📈
8. **Clear Chat**: Use the Clear button to reset. 🗑️
9. **Quit**: Type `quit` or close the window.

**Pro Tip**: For multi-root equations, numerical mode tries multiple guesses to find them all! 🔍

## 🔍 How It Works
Under the hood, botX is architecturally clean and modular:

### Core Components
- **Solver Functions** (`solveX` & `get_solution`):
- Parses input string into SymPy equation (handles `=` or assumes `=0`).
- Symbolic: Uses `solveset` with domain filtering.
- Numerical: `nsolve` with guesses; deduplicates results.
- Fallback: If no solutions, tries numerical even in symbolic mode.

- **GUI Class** (`ModernBotXGUI`):
- **Initialization**: Sets up Tkinter window, styles (clam theme, dark colors), and widgets.
- **Chat System**: Canvas with inner frame for dynamic messages; proper scrolling (mousewheel, keys).
- **Input Handling**: Replaces `^` with `**`, binds Enter key.
- **Rendering**: Uses Matplotlib to generate PNG images from LaTeX for display.
- **Plotting**: Lambdifies expression, evaluates over linspace, masks NaN/Inf.
- **Events**: Binds for focus, scrolling, and mode toggles.

### Data Flow
1. User input → Parse & replace symbols → Sympify to equation.
2. Solve based on mode/domain → Format (LaTeX or numerical string).
3. Render: If symbolic, create image; else text.
4. Display in chat bubble → Enable plot if applicable.
5. Plot: New Toplevel window with Matplotlib canvas.

### Key Techniques
- **Error Resilience**: Try-except blocks for parsing, solving, and plotting.
- **Performance**: Limits guesses and linspace points for speed.
- **Accessibility**: Keyboard navigation, focus management.

## 📝 Supported Equations
botX shines with:
- **Polynomials**: `x**3 - 6*x**2 + 11*x - 6 = 0` → Roots: 1, 2, 3.
- **Trigonometric**: `cos(x) = 0` → `π/2 + kπ` (principal values).
- **Exponential/Log**: `e**x = 2` or `log(x+1) = 0`.
- **Rational**: `1/x = 2` (with domain checks).
- **Complex**: `x**2 = -1` → `I, -I`.

**Not Supported Yet**:
- Systems of equations (single variable only).
- Unevaluated integrals/derivatives.
- Custom symbols (assumes `x`).

## ⚠️ Limitations
- **Plot Range**: Fixed to -10 to 10; may miss roots outside.
- **Numerical Accuracy**: Depends on guesses; may miss roots or converge slowly.
- **LaTeX Rendering**: Requires Matplotlib; falls back to text on errors.
- **Complex Plotting**: Not implemented (real-only for simplicity).
- **Performance**: Heavy equations may lag due to SymPy.
- **Platform**: Tkinter works best on desktop; no mobile support.
- **Imaginary Domain**: Filters to pure imaginary solutions only.

If you encounter issues, check the console for SymPy errors! 🐛

## 🤝 Contributing
Contributions are welcome! 🌟 Help make botX even better.

1. **Fork the Repo** and clone your fork.
2. **Create a Branch**: `git checkout -b feature/amazing-new-solver`.
3. **Make Changes**: Add features, fix bugs, improve docs.
4. **Test**: Run the app and verify.
5. **Commit**: `git commit -m "Add support for quadratic formulas"`.
6. **Push**: `git push origin feature/amazing-new-solver`.
7. **Pull Request**: Open a PR with a clear description.

**Guidelines**:
- Follow PEP 8 for code style.
- Add tests if possible (e.g., unit tests for solvers).
- Update README if you add features.
- Issues? Open a ticket on GitHub.

Thanks for contributing! 🙌

## 📄 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.


## 👏 Acknowledgments
- **SymPy Team**: For the amazing symbolic math library. 🧮
- **Matplotlib & NumPy**: Plotting and numerical backbone. 📊
- **Tkinter**: Standard GUI toolkit. 🖥️
- **PIL/Pillow**: Image rendering. 🖼️
- Inspired by chatbots like ChatGPT but focused on math! 🤖
- Emoji icons from Twemoji for visual appeal. 😊

If you found botX helpful, star the repo or share it! ⭐ Questions? Open an issue.

**Happy Solving!** 🎉
