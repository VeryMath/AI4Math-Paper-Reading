"""Evaluate exact ODE solutions and bounds used by the flow-stability SkillCard.

Run from any directory with Python's standard library. This computes mathematical
examples directly; it does not invoke an agent, an ODE solver, or another script.
"""

import math


def kernel_factor(lipschitz, final_time):
    """L2 norm of exp(L * (T-s)) for a constant nonnegative L."""
    if lipschitz == 0:
        return math.sqrt(final_time)
    return math.sqrt(math.expm1(2 * lipschitz * final_time) / (2 * lipschitz))


def report(label, exact, bound, relation):
    holds = exact <= bound + 1e-12 if relation == "<=" else exact > bound
    print(f"{label}: exact_W2={exact:.12g}, bound={bound:.12g}, "
          f"expected {relation}: {'confirmed' if holds else 'FAILED'}")
    if not holds:
        raise ValueError(f"Mathematical comparison failed: {label}")


def main():
    # Translation of equal-variance Gaussian laws: W2 equals their mean gap.
    a, delta, final_time = 1.0, 0.1, 1.0
    gap = delta * math.expm1(a * final_time) / a
    epsilon = delta * math.sqrt(final_time)
    report("affine Gaussian perturbation", gap,
           kernel_factor(abs(a), final_time) * epsilon, "<=")

    # X'=-2X, Y'=-2Y+delta*t. Variation of constants gives this mean gap.
    delta, final_time = 0.1, 2.0
    gap = delta * (final_time / 2 - (1 - math.exp(-2 * final_time)) / 4)
    epsilon = delta * math.sqrt(final_time ** 3 / 3)
    report("time-dependent forcing of a contracting flow", gap,
           kernel_factor(2, final_time) * epsilon, "<=")

    # The learned field |y|+delta is Lipschitz but not differentiable at 0.
    # From a common Dirac initial law at 0, its unique solution is nonnegative.
    delta, final_time = 0.2, 1.0
    gap = delta * math.expm1(final_time)
    report("nondifferentiable Lipschitz field", gap,
           kernel_factor(1, final_time) * delta * math.sqrt(final_time), "<=")

    # Three false generalizations, evaluated on exact solutions.
    a, delta, final_time = 3.0, 0.1, 1.0
    gap = delta * math.expm1(a * final_time) / a
    report("reject removal of stability amplification", gap, delta, ">")

    delta, final_time = 0.2, 4.0
    gap = delta * final_time
    epsilon = delta * math.sqrt(final_time)
    report("reject unit-interval formula at T=4", gap, epsilon, ">")
    report("restore time factor at T=4", gap,
           kernel_factor(0, final_time) * epsilon, "<=")

    # X'=0, X0=1; Y'=Y, Y0=1. Drift error under the unrelated law delta_0 is 0.
    gap = math.expm1(1)
    report("reject drift error under an unrelated path law", gap, 0.0, ">")
    report("use drift error along the exact path instead", gap,
           kernel_factor(1, 1), "<=")

    # Without uniqueness/Lipschitz control, Y'=2 sqrt(|Y|), Y0=0 admits
    # both Y=0 and Y=t^2, while X=0 has zero drift mismatch along its path.
    report("reject omission of uniqueness and Lipschitz control", 1.0, 0.0, ">")


if __name__ == "__main__":
    main()
