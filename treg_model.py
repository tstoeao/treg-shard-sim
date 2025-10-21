import numpy as np
import matplotlib.pyplot as plt

# Treg shard model (core)
def treg_equilibrium(inflammation, suppression):
    """V = E * Y: Immune equilibrium yield."""
    return inflammation * suppression

# Expanded: Simulate tolerance assay (e.g., suppression index under IL-2 stress)
def simulate_treg_stress(e_levels, y_base=0.76, stress_factor=0.2):
    """Hyp: Y-invariance ~0.76; droop <0.5 on knockout."""
    v_yields = []
    for e in e_levels:
        # Base V
        v_base = treg_equilibrium(e, y_base)
        # Stress perturbation (e.g., IL-2 flux)
        y_stressed = y_base * (1 - np.random.normal(stress_factor, 0.05))
        v_stressed = treg_equilibrium(e, max(y_stressed, 0.5))  # Falsifiable floor
        v_yields.append((v_base, v_stressed, y_stressed))
    return np.array(v_yields)

if __name__ == "__main__":
    # Example run: MLR-like assay
    e_inflammation = np.linspace(1, 10, 50)  # Antigen loads
    results = simulate_treg_stress(e_inflammation)

    # Plot: V equilibrium curve + Y invariance
    plt.figure(figsize=(8, 5))
    plt.plot(e_inflammation, results[:, 0], label='Base V (Y=0.76)', color='blue')
    plt.plot(e_inflammation, results[:, 1], label='Stressed V', color='red', alpha=0.7)
    plt.axhline(y=0.76, color='green', linestyle='--', label='Y-Invariance Threshold')
    plt.xlabel('Inflammatory Load E')
    plt.ylabel('Equilibrium V / Suppression Y')
    plt.title('Treg Shard Dynamics: Tolerance Assay Sim')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('examples/treg_equilibrium.png')  # Saves to examples/ (create folder next if needed)
    plt.show()

    # Stats: Mean Y under stress
    print(f"Mean Y-invariance: {np.mean(results[:, 2]):.3f} (target: 0.76)")
