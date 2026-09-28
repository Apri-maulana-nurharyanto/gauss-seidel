import re
import numpy as np

def parse_equation(eq_str):
    eq_str = eq_str.replace(" ", "")
    left, right = eq_str.split("=")
    b_val = float(right)

    pattern = r"([+-]?\d*\.?\d*)([a-zA-Z])"
    matches = re.findall(pattern, left)

    coeffs = {}
    for coeff_str, var in matches:
        if coeff_str == "" or coeff_str == "+":
            coeff = 1.0
        elif coeff_str == "-":
            coeff = -1.0
        else:
            coeff = float(coeff_str)
        coeffs[var] = coeff

    return coeffs, b_val


def gauss_seidel(A, b, x0, var_list, tol=1e-3, max_iter=100):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    x = np.array(x0, dtype=float)
    n = len(b)

    print("\n" + "=" * 65)
    # Header rapi tanpa teks formatting yang bocor
    header_vars = " ".join([f"{var:<12}" for var in var_list])
    header = f"{'Iter':<6} {header_vars} {'Error':<12}"
    print(header)
    print("=" * 65)

    x_str = " ".join([f"{val:<12.6f}" for val in x])
    print(f"{0:<6} {x_str} {'-':<12}")

    for iteration in range(1, max_iter + 1):
        x_new = np.copy(x)

        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        error = np.linalg.norm(x_new - x, ord=np.inf)
        x_str = " ".join([f"{val:<12.6f}" for val in x_new])
        print(f"{iteration:<6} {x_str} {error:<12.6f}")

        if error < tol:
            print("=" * 65)
            print(f"Konvergen pada iterasi ke-{iteration}")
            return x_new

        x = x_new

    print("=" * 65)
    print("Mencapai batas iterasi maksimum.")
    return x

# --- INPUT PROGRAM ---
n = int(input("Masukkan jumlah persamaan: "))

print("\n--- Masukkan Persamaan ---")
parsed_eqs = []
all_vars = set()

for i in range(n):
    eq_str = input(f"Persamaan {i+1}: ")
    coeffs, b_val = parse_equation(eq_str)
    parsed_eqs.append((coeffs, b_val))
    all_vars.update(coeffs.keys())

var_list = sorted(list(all_vars))

A = []
b = []
for coeffs, b_val in parsed_eqs:
    baris = [coeffs.get(var, 0.0) for var in var_list]
    A.append(baris)
    b.append(b_val)

print("\n--- Masukkan Nilai Tebakan Awal (x0) ---")
x0 = list(
    map(
        float,
        input(
            f"Masukkan {n} nilai tebakan awal urut {var_list} (beri spasi tiap nilai tebakan): "
        ).split(),
    )
)

tol = float(input("\nMasukkan nilai toleransi error : "))

solusi = gauss_seidel(A, b, x0, var_list, tol)

print("\n--- HASIL AKHIR ---")
for i, var in enumerate(var_list):
    print(f"{var} = {solusi[i]:.6f}")