"""
Proyecto Final U5 · Cálculo Vectorial · TecNM Campus Ensenada
Dron de reparto en un campo de viento: PLANTILLA DEL EQUIPO

Instrucciones
1. En la consola, carguen su código y copien el bloque "Datos para Python (Colab)"
   (botón "Copiar bloque"). Péguenlo en la sección 0, en lugar de las dos líneas CODIGO y PARAMS.
2. Cada integrante completa los bloques de su rol (busquen "TODO").
3. Ejecuten:  python dron_plantilla.py
   Debe imprimir los resultados y generar mapa_<codigo>.png, energia_<codigo>.png y vuelo_<codigo>.gif.
4. Comparen los números con su desarrollo a mano y con el verificador de la consola.

Requisitos: numpy, scipy, matplotlib  (pip install numpy scipy matplotlib). En Google Colab ya vienen instalados.
Unidades: distancias en km, fuerzas en N, trabajo y energía en kJ (1 N·km = 1 kJ).
"""
import math
import numpy as np
from scipy.integrate import quad, dblquad
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ------------------------------------------------------------------
# 0. Parámetros del equipo
#    PEGUEN AQUÍ el bloque "Datos para Python (Colab)" de la consola, reemplazando
#    las dos líneas siguientes (vienen con los datos DEMO). No cambien nada más.
# ------------------------------------------------------------------
CODIGO = "DEMO"
PARAMS = dict(L=6, k=0.15, u=1, b=0.3, a=0.15, e=0.05, c=2.5, d=7.5, eps=12, Eb=90)
L, k, u, b, a, e, c, d, eps, Eb = (PARAMS[s] for s in ("L", "k", "u", "b", "a", "e", "c", "d", "eps", "Eb"))
R = L / 2

# ------------------------------------------------------------------
# 1. Ingeniero de Dinámica · campo, divergencia y rotacional (5.7, 5.9)
#    F(x, y) = < -u + b x + a y^2 ,  d + e y^2 - c x >
# ------------------------------------------------------------------
def F(x, y):
    """Regresa np.array([P, Q]). Debe funcionar con escalares y con arreglos de numpy."""
    # TODO: escribir P y Q
    raise NotImplementedError("F(x, y)")

def div(x, y):
    # TODO: dP/dx + dQ/dy  (derívenlo a mano y escriban el resultado)
    raise NotImplementedError("div")

def rot(x, y):
    # TODO: dQ/dx - dP/dy
    raise NotImplementedError("rot")

# ------------------------------------------------------------------
# 2. Ingeniero de Logística · rutas e integral de línea (5.8)
#    Cada ruta es (r(t), r'(t), t0, t1) y va de A=(0,0) a B=(L,0).
# ------------------------------------------------------------------
RUTAS = {
    1: (lambda t: np.array([t, 0.0]), lambda t: np.array([1.0, 0.0]), 0.0, L),   # recta (completa)
    # TODO: Ruta 2, parábola y = k x (L - x), con x = t
    # 2: (lambda t: ..., lambda t: ..., 0.0, L),
    # TODO: Ruta 3, semicircunferencia superior de centro (R, 0). Ojo: theta va de pi a 0
    # 3: (lambda t: ..., lambda t: ..., math.pi, 0.0),
}

def trabajo(i):
    """W_i = ∫ F(r(t)) · r'(t) dt  con scipy.integrate.quad."""
    r, dr, t0, t1 = RUTAS[i]
    # TODO: integrando = F(*r(t)) @ dr(t)
    raise NotImplementedError("trabajo")

# ------------------------------------------------------------------
# 3. Analista de Zona · integrales dobles del rotacional (5.3, 5.4)
# ------------------------------------------------------------------
def doble_D2():
    """∬ rot dA sobre D2: 0<=x<=L, 0<=y<=k x (L-x). Ojo: dblquad integra f(y, x)."""
    # TODO
    raise NotImplementedError("doble_D2")

def doble_D3():
    """∬ rot dA sobre el semidisco, en polares centradas en (R, 0). No olviden el factor r."""
    # TODO
    raise NotImplementedError("doble_D3")

# ------------------------------------------------------------------
# 4. Gerente de Calidad · teorema de Green (5.10)
# ------------------------------------------------------------------
def verificar_green(W, I2, I3, tol=1e-6):
    """Green con el contorno A->B por la recta y regreso por la ruta curva (antihorario):
       W1 - W2 = ∬_D2 rot dA   y   W1 - W3 = ∬_D3 rot dA."""
    # TODO: regresar (True/False, True/False) comparando ambos lados
    raise NotImplementedError("verificar_green")

# ------------------------------------------------------------------
# 5. Equipo · longitud, energía y decisión
# ------------------------------------------------------------------
def longitud(i):
    """l_i = ∫ ||r'(t)|| dt (valor absoluto: la Ruta 3 se recorre con t decreciente)."""
    # TODO
    raise NotImplementedError("longitud")

def energia(W, ell):
    """E_i = eps * l_i - W_i  (kJ). Regresa un dict {1: E1, 2: E2, 3: E3}."""
    # TODO
    raise NotImplementedError("energia")

# ------------------------------------------------------------------
# 6. Figuras y animación (ya funcionan cuando lo anterior esté completo)
# ------------------------------------------------------------------
COL = {1: "#14213a", 2: "#e5671f", 3: "#7a3fd1"}

def dibujar_base(ax, E, mejor):
    xs, ys = np.linspace(-0.6, L + 0.6, 200), np.linspace(-1.0, R + 0.8, 120)
    X, Y = np.meshgrid(xs, ys)
    cf = ax.contourf(X, Y, rot(X, Y) + 0 * X, levels=20, cmap="Blues_r")
    plt.colorbar(cf, ax=ax, label="rot F · k (N/km)", shrink=.8)
    xq, yq = np.meshgrid(np.linspace(0, L, 11), np.linspace(-0.7, R + 0.6, 9))
    Fx, Fy = F(xq, yq)
    ax.quiver(xq, yq, Fx, Fy, color="#14213a", alpha=.75, width=.003)
    for i, (r, dr, t0, t1) in RUTAS.items():
        P = np.array([r(t0 + (t1 - t0) * s) for s in np.linspace(0, 1, 300)])
        ax.plot(P[:, 0], P[:, 1], color=COL[i], lw=3 if i == mejor else 2, label=f"Ruta {i}: E = {E[i]:.2f} kJ")
    ax.plot([0, L], [0, 0], "o", color="white", mec="#14213a", ms=8)
    ax.set_aspect("equal"); ax.set_xlabel("x (km)"); ax.set_ylabel("y (km)")
    ax.set_xlim(-0.6, L + 0.6); ax.set_ylim(-1.0, R + 0.8); ax.legend(loc="upper right", fontsize=8)

def animar(E, mejor, cuadros=90):
    fig, ax = plt.subplots(figsize=(8, 4.8)); dibujar_base(ax, E, mejor)
    ax.set_title(f"Vuelo simultáneo por las tres rutas · {CODIGO}")
    drones = {i: ax.plot([], [], "o", ms=11, color=COL[i], mec="white", mew=2)[0] for i in RUTAS}
    def cuadro(n):
        s = n / (cuadros - 1)
        for i, (r, dr, t0, t1) in RUTAS.items():
            # posición del dron i cuando lleva la fracción s de su parámetro
            x, y = r(t0 + (t1 - t0) * s)
            drones[i].set_data([x], [y])
        return list(drones.values())
    anim = FuncAnimation(fig, cuadro, frames=cuadros, interval=60, blit=True)
    anim.save(f"vuelo_{CODIGO}.gif", writer=PillowWriter(fps=15)); plt.close(fig)

# ------------------------------------------------------------------
# Programa principal
# ------------------------------------------------------------------
if __name__ == "__main__":
    W = {i: trabajo(i) for i in RUTAS}
    ell = {i: longitud(i) for i in RUTAS}
    E = energia(W, ell)
    I2, I3 = doble_D2(), doble_D3()
    V = (L / 2, k * L**2 / 4)
    mejor = min(E, key=E.get)

    print(f"Equipo {CODIGO}")
    for i in RUTAS:
        estado = "factible" if E[i] <= 0.8 * Eb else "NO factible"
        print(f"  Ruta {i}: W = {W[i]:.4f} kJ  l = {ell[i]:.4f} km  E = {E[i]:.4f} kJ  ({estado})")
    print(f"  div F(V) = {div(*V):.4f}   rot F(V) = {rot(*V):.4f}  N/km")
    print(f"  ∬_D2 rot dA = {I2:.4f}   ∬_D3 rot dA = {I3:.4f}  kJ")
    print("  Green (D2, D3):", verificar_green(W, I2, I3))
    print(f"  Ruta más económica: {mejor}  E = {E[mejor]:.4f} kJ")

    fig, ax = plt.subplots(figsize=(8, 4.8)); dibujar_base(ax, E, mejor)
    ax.set_title(f"Rutas del dron y viento · {CODIGO}"); fig.tight_layout()
    fig.savefig(f"mapa_{CODIGO}.png", dpi=170); plt.close(fig)
    # TODO (equipo): gráfica de barras de E1, E2, E3 con una línea horizontal en 0.8*Eb -> energia_<codigo>.png
    animar(E, mejor)
