import sympy as sp
import random
import matplotlib.pyplot as plt
import io

plt.rcParams.update({
    "text.usetex": False,
    "mathtext.fontset": "cm"
})

def generate_substitution_problem():
    x = sp.Symbol('x')
    # Pick two random "building blocks"
    blocks1 = [sp.sin(x), sp.exp(x), sp.ln(x), x**random.randint(1, 4), sp.sqrt(x), sp.cos(x), sp.tan(x), 1/x]
    F1 = random.choice(blocks1)
    F = F1
    if random.randint(1, 10) == 1: #one in ten will be insane
        blocks2 = [sp.exp(x), sp.ln(x), x**2, 1/x, x]
        if F1 == sp.cos(x):
            blocks2.append(sp.sin(x))
        F2 = random.choice(blocks2)
        match random.randint(1, 4):
            case 1: F = F1+F2
            case 2: F = F1*F2
            case 3: F = F1-F2
            case 4: F = F1/F2

    # Differentiate to get the "problem"
    f = sp.simplify(sp.diff(F, x))

    # Simplify or expand to hide the structure
    problem = F.subs(x, f) * f
    y = sp.Symbol('y')
    if problem == problem.subs(x, y): #if problem is constant
        return generate_substitution_problem()
    from_ = random.randint(-10, 6)
    to_ = random.randint(from_+1, 10)
    problem = sp.Integral(problem, (x, from_, to_))
    answer = sp.simplify(problem.doit())
    return problem, answer #returns problem and its numerical solution

def generate_IBP_problem():
    #pick from blocks
    x = sp.Symbol('x')
    blocks = [sp.sin(x), sp.exp(x), sp.ln(x), sp.sqrt(x), sp.cos(x), sp.tan(x), 1/x, sp.sin(x)**random.randint(1, 4), sp.cos(x)**random.randint(1, 4)]
    F = random.choice(blocks)
    problem = sp.diff(F, x) * F

    y = sp.Symbol('y')
    if problem in blocks: #if it's just basic function
        return generate_IBP_problem()
    elif problem == problem.subs(x, y): #if it's constant
        return generate_IBP_problem()
    from_ = random.randint(-10, 6)
    to_ = random.randint(from_+1, 10)
    problem = sp.Integral(problem, (x, from_, to_))
    answer = sp.simplify(problem.doit())
    return problem, answer #returns problem and its numerical solution

def generate_integral(seed=random.randint(1, 1000000000)):
    random.seed(seed)
    match random.randint(1, 2):
        case 1: return generate_substitution_problem()
        case 2: return generate_IBP_problem()
    print("Something went wrong!")
    return generate_substitution_problem()

def save_as_latex_image_io(integral_obj):
    # Convert the SymPy object to a LaTeX string
    latex_str = sp.latex(integral_obj)
    
    # Use Matplotlib to render the LaTeX
    plt.figure(figsize=(6, 3))
    plt.text(0.5, 0.5, f"${latex_str}$".replace("\\limits", ""), fontsize=24, ha='center', va='center')
    plt.axis('off')
    
    # Save with high DPI for clarity
    buf = io.BytesIO()
    plt.savefig(buf, bbox_inches='tight', dpi=300)
    plt.close()
    buf.seek(0)
    return buf

def save_as_latex_image(integral_obj, filename="integral_problem.png"):
    # Convert the SymPy object to a LaTeX string
    latex_str = sp.latex(integral_obj)
    
    # Use Matplotlib to render the LaTeX
    plt.figure(figsize=(6, 3))
    plt.text(0.5, 0.5, f"${latex_str}$", fontsize=24, ha='center', va='center')
    plt.axis('off')
    
    # Save with high DPI for clarity
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Success! Saved problem to {filename}")

def main():
    #show example of each problem
    problem1 = generate_substitution_problem()
    problem2  = generate_IBP_problem()
    print(problem1)
    print(problem2)
    save_as_latex_image(problem1[0], filename="p1.png")
    save_as_latex_image(problem2[0], filename="p2.png")

if __name__ == "__main__":
    main()
