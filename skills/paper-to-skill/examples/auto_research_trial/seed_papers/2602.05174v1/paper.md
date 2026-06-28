# Total Variation Rates for Riemannian Flow Matching

Yunrui Guan $^{1}$ , Krishnakumar Balasubramanian $^{2}$ , and Shiqian Ma $^{1}$

$^{1}$ Department of Computational Applied Mathematics and Operations Research, Rice University.

$^{2}$ Department of Statistics, University of California, Davis.

$^{1}\{\mathrm{yg83, sqma}\} \text{@rice.edu}$

$^{2}\{\mathrm{kbal}\} @$ ucdavis.edu

# Abstract

Riemannian flow matching (RFM) extends flow-based generative modeling to data supported on manifolds by learning a time-dependent tangent vector field whose flow-ODE transports a simple base distribution to the data law. We develop a nonasymptotic Total Variation (TV) convergence analysis for RFM samplers that use a learned vector field together with Euler discretization on manifolds. Our key technical ingredient is a differential inequality governing the evolution of TV between two manifold ODE flows, which expresses the time-derivative of TV through the divergence of the vector-field mismatch and the score of the reference flow; controlling these terms requires establishing new bounds that explicitly account for parallel transport and curvature. Under smoothness assumptions on the population flow-matching field and either uniform (compact manifolds) or mean-square (Hadamard manifolds) approximation guarantees for the learned field, we obtain explicit bounds of the form $\mathrm{TV} \leq C_{\mathrm{Lip}} h + C_{\varepsilon} \varepsilon$ (with an additional higher-order $\varepsilon^2$ term on compact manifolds), cleanly separating numerical discretization and learning errors. Here, $h$ is the step-size and $\varepsilon$ is the target accuracy. Instantiations yield explicit polynomial iteration complexities on the hypersphere $S^d$ , and on the $\mathrm{SPD}(n)$ manifolds under mild moment conditions.

# Contents

1 Introduction 2

2 Basics and Problem Formulation 4

2.1 Riemannian Geometry Basics 4   
2.2 Riemannian Flow Matching 5

3 Total Variation Rates: Compact Manifolds 7   
4 Total Variation Rates: Hadamard Manifolds 9

5 Proof Sketch and Intermediate Results 10

5.1 Continuous Time Interpolation 11   
5.2 Discretization analysis 12

5.2.1 Score Regularity and Vector Field Regularity 12   
5.2.2 The Divergence Term 13

# A Additional Background for Riemannian Geometry 17

A.1 Distances used 17

A.2 Comparison Theorem 17   
A.3 Riemannian Submanifolds 18

# B Proof of Main Theorem 18

B.1 Proof for Lemma 5.1 19   
B.2 Velocity Vector Term 20   
B.3 Divergence Term 23   
B.4 Results on Riemannian manifolds 26   
B.5 Main Theorem 30   
B.6 Example: Hypersphere 32   
B.7 Example: SPD Manifold 35

# C Auxiliary Results for Proof of Main Theorems 36

C.1 Jacobi Equation 36   
C.2 Divergence Term 39

# D Hypersphere Regularity Results 42

D.1 Auxiliary Lemmas 45   
D.2 Regularity for Flow Matching Vector Field 53   
D.3 Regularity for Divergence 56   
D.4 Regularity of $\mathbf{v}(\mathbf{t},\mathbf{x})$ and log pt 62   
D.5 Finiteness of Score Regularity: Proof of Proposition 5.3 63

# E SPD Manifold Regularity Results 65

E.1 Proof of Proposition 5.4 68   
E.2 Auxiliary Results for Regularity for Hadamard and SPD manifolds 70

E.2.1 Expectation Control 70   
E.2.2 Regularity Control 73

E.3 Auxiliary Bounds on Derivatives 79   
E.4 Bounding Third Derivative of Exp Map 87   
E.5 Bounds involving Riemannian Log 96   
E.6 Auxiliary results 99

# 1 Introduction

Flow-based generative modeling offers a conceptually clean sampling paradigm by representing a complex target distribution as the endpoint of a continuous-time transport from a simple reference law. In flow matching, one fixes a family of interpolating measures $(\pi_t)_{t \in [0,1]}$ between an easy base distribution $\pi_0$ and the data distribution $\pi_1$ , and learns a time-dependent vector field whose flow pushes $\pi_0$ to $\pi_1$ . When the data lie on a Riemannian manifold $(M,g)$ , particles evolve according to an intrinsic ODE $\dot{X}_t = v_t(X_t)$ , and the associated densities satisfy the manifold continuity equation $\partial_t p_t + \mathrm{div}_g(p_t v_t) = 0$ , yielding a sampler that respects the geometry by construction. Crucially, because Riemannian Flow Matching (RFM) is purely deterministic and relies only on integrating intrinsic ODEs, it avoids discretizing manifold-valued Brownian motion as required by Riemannian diffusion models (De Bortoli et al., 2022), where both theoretical analysis and practical simulation are considerably more delicate.

Despite their ever-increasing practical usage (Yue et al., 2025; Sriram et al., 2024; Mathieu and Nickel, 2020; Miller et al., 2024; Collas et al., 2025; Luo et al., 2025), a central theoretical question is unexplored: how fast does a discretized RFM sampler with a learned velocity field converge to the target distribution, in distributional metrics? Our main contribution is to provide the first non-asymptotic Total Variation (TV) bounds for RFM samplers on both compact and Hadamard manifolds. We develop intrinsic stability estimates for solutions of the Riemannian continuity equation under perturbations of the driving vector field, yielding explicit control of $\mathrm{TV}(\hat{\pi}_T,\pi_T)$ for $T = 1 - \delta$ , $(\delta >0)$ in terms of (i) the approximation quality of the learned field $\hat{v}_{t}$ to an ideal field $v_{t}$ in geometry-aware norms, (ii) regularity of the dynamics (e.g., bounds on covariant derivatives and divergence), and (iii) geometric characteristics of $(M,g)$ that govern volume distortion. We then combine these stability estimates with a careful analysis of discretized flows to obtain end-to-end guarantees for practical samplers, isolating the statistical and computational contributions. The resulting theory clarifies which properties of the learned velocity field are truly required for strong sampling accuracy on manifolds, and how curvature and anisotropy enter the constants and rates, providing a principled foundation for understanding Riemannian flow matching algorithms.

Related works. Generative modeling on Riemannian manifolds was introduced by De Bortoli et al. (2022), who generalized score-based generative modeling (Song et al., 2021) from Euclidean space to Riemannian manifolds, and proved an error bound of sampling error. The error bound in De Bortoli et al. (2022) fails to be polynomial, which is caused by technical difficulties in analyzing discretization error in manifold Brownian motion simulation. Other works including Huang et al. (2022) and Lou et al. (2023) also studied generative modeling on mainfolds without theoretical guarantees.

This difficulty is related to sampling on Riemannian manifolds via diffusion processes. Early work analyzed KL divergence along Langevin diffusions, e.g., on hyperspheres (Li and Erdogdu, 2023) and Hessian manifolds (Gatmiry and Vempala, 2022). Later, Cheng et al. (2022) used a geometric approach with coupling to obtain $W_{1}$ bounds; see also Kong and Tao (2024) for Lie groups and Guan et al. (2025) for high-accuracy proximal sampling. These results highlight that Riemannian Brownian motion—the basic component of Riemannian diffusion models—is challenging both theoretically and computationally: discretization analyses are largely geometric and typically give Wasserstein error bounds (e.g., Cheng et al. (2022)), while exact simulation is generally unavailable since its transition density lacks a closed form except in special cases. This in turn complicates denoising score matching and sample generation for Riemannian diffusion models.

More recently, Xu et al. (2026, Lemma 19) established a polynomial discretization error bound in total variation distance. Building on this, Xu et al. (2026) further proved a polynomial iteration complexity for Riemannian score-based generative models. However, the established bounds are only qualitative and do not reveal the precise dependencies on the problem parameters.

Another line of research is the Riemannian Flow Matching method, first proposed in Chen and Lipman (2024) and later explored by Cheng et al. (2025) and Wu et al. (2025). We remark that, due to its deterministic formulation, RFM does not require access to the heat kernel or simulation of manifold Brownian motion, thereby avoiding the main bottleneck of Riemannian diffusion models.

From the case of Euclidean flow matching, works including Li et al. (2025) and Huang et al. (2025) established discretization error bounds in TV distance for probability flow ODEs with polynomial dependence on the Lipschitz constant. For flow matching with deterministic samplers via ODE discretization, Benton et al. (2024); Bansal et al. (2024); Zhou and Liu (2025); Guan et al. (2026) establish bounds in the Wasserstein distance, and Su et al. (2025) considered KL divergence. However, without a contraction/dissipativity-type structure for the score or flow-matching vector field, the bounds typically do not yield polynomial rates in the associated Lipschitz constants. To

obtain a fully polynomial error bound, existing works (Li et al., 2024a, 2025) analyze flow matching samplers in the TV distance. Liu et al. (2025) provided a polynomial error bound for stochastic interpolant (which can be understood as a smoothed variant of flow matching) with deterministic sampling, by making use of the framework in Li et al. (2025). Very recently, Roy et al. (2026) examined adaptivity of Euclidean FM to low-dimensional structures. To the best of our knowledge, no prior discretization error analysis is available for flow matching on general Riemannian manifolds.

# 2 Basics and Problem Formulation

# 2.1 Riemannian Geometry Basics

Let $(M,g)$ be a $d$ -dimensional Riemannian manifold, not necessarily realized as a submanifold of Euclidean space, where $g$ denotes the Riemannian metric. Unless otherwise specified, $\| \cdot \|$ denotes the norm induced by $g$ . We use $T_{x}M$ to denote tangent space at location $x \in M$ , and remark that $\| \cdot \|$ is well-defined on each tangent space $T_{x}M$ . We let $\mathrm{Exp}$ to denote exponential map, and also define the inverse of the exponential map, i.e., the logarithm map: Given $X_0, X_1 \in M$ , $\operatorname{Log}_{X_0}(X_1) \in T_{X_0}M$ is such that $\operatorname{Exp}_{X_0}(\operatorname{Log}_{X_0}(X_1)) = X_1$ . We use $P_x^y$ to denote the parallel transport from $x$ to $y$ , along the minimizing geodesic, unless otherwise specified. Based on this, we can define geodesic interpolation as follows.

$$
X _ {t} := \operatorname {E x p} _ {X _ {0}} (t \log_ {X _ {0}} (X _ {1})) \tag {1}
$$

Note that $X_{t}^{\prime} = P_{X_{0}}^{X_{t}}\operatorname{Log}_{X_{0}}(X_{1}) = \frac{1}{1 - t}\operatorname{Log}_{X_{t}}(X_{1})$

We use grad to denote the Riemannian gradient, div the Riemannian divergence, and $\nabla$ the Levi-Civita connection on $(M,g)$ . For a smooth function $f$ , the gradient $\operatorname{grad} f$ is the unique vector field satisfying $\langle \operatorname{grad} f, v \rangle = df(v)$ for all $v \in T_x M$ . For a smooth vector field $u$ , the divergence is defined by $\operatorname{div} u := \operatorname{tr} (\nabla u)$ ; equivalently, for any local $g$ -orthonormal frame $\{e_i\}_{i=1}^d$ , $\operatorname{div} u(x) = \sum_{i=1}^d \langle \nabla_{e_i} u, e_i \rangle_x$ . For a vector field $u$ and a tangent vector $v \in T_x M$ , the covariant derivative $\nabla_v u(x)$ is defined as follows: choose any smooth local vector field $V$ with $V(x) = v$ , and set $\nabla_v u(x) := (\nabla_V u)(x)$ ; this is well-defined (i.e., independent of the extension $V$ ) because $\nabla$ is $C^\infty(M)$ -linear in its first argument. The map $\nabla u(x)$ may be viewed as a $(1,1)$ -tensor (an endomorphism) $\nabla u(x): T_x M \to T_x M$ defined by $(\nabla u(x))(v) := \nabla_v u(x)$ . Accordingly, we define the operator norm induced by $g$ as

$$
\| \nabla u (x) \| _ {\mathrm {o p}} := \sup  _ {v \neq 0} \frac {\| \nabla_ {v} u (x) \|}{\| v \|} = \sup  _ {\| v \| = 1} \| \nabla_ {v} u (x) \|.
$$

We now provide some intuition on Levi-Civita connection and covariant derivatives. On a manifold, the tangent spaces $T_xM$ and $T_yM$ at different points are distinct vector spaces, so one cannot subtract vectors at $x$ and $y$ directly. The Levi-Civita connection $\nabla$ provides a canonical way to differentiate vector fields by comparing nearby tangent vectors in a manner that is compatible with the metric $(\nabla g = 0)$ and has no torsion. Along a curve $\gamma$ , the induced covariant derivative $D_t \coloneqq \nabla_{\gamma'(t)}$ plays the role of a directional derivative: it measures the intrinsic rate of change of a vector field along $\gamma$ after accounting for the variation of tangent spaces, and it is the notion of derivative that makes "constant velocity" along $\gamma$ coincide with the geodesic equation.

Let $x \in M$ . The injectivity radius at $x$ , denoted $\operatorname{inj}(x)$ , is defined as

$$
\operatorname {i n j} (x) := \sup \Bigl \{a > 0: \left. \operatorname {E x p} _ {x} \right| _ {B _ {a} (0)}: B _ {a} (0) \subset T _ {x} M \to M \mathrm {i s a d i f f e o m o r p h i s m o n t o i t s i m a g e} \Bigr \},
$$

where $B_{a}(0)$ is the open metric ball in $(T_xM, g_x)$ . The injectivity radius of $M$ is $\operatorname{inj}(M) \coloneqq \inf_{x \in M} \operatorname{inj}(x)$ .

Let $R$ denote the (Riemann) curvature tensor associated with $\nabla$ , defined for smooth vector fields $X, Y, Z$ by $R(X, Y)Z \coloneqq \nabla_X \nabla_Y Z - \nabla_Y \nabla_X Z - \nabla_{[X,Y]} Z$ . For linearly independent $u, v \in T_xM$ , the sectional curvature of the plane $\sigma = \operatorname{span}\{u, v\}$ is

$$
K (\sigma) := \frac {\langle R (u , v) v , u \rangle_ {x}}{\| u \| ^ {2} \| v \| ^ {2} - \langle u , v \rangle_ {x} ^ {2}},
$$

and in particular, if $u\perp v$ and $\| u\| = \| v\| = 1$ , then $K(u,v) = \langle R(u,v)v,u\rangle_{x}$

Let $\gamma :[a,b]\to M$ be a geodesic, and write $D_{t}\coloneqq \nabla_{\gamma^{\prime}(t)}$ for the covariant derivative along $\gamma$ . A vector field $J$ along $\gamma$ is called a Jacobi field if it satisfies the Jacobi equation $D_t^2 J + R(J,\gamma ')\gamma ' = 0$ . Let $p = \gamma (a)$ and $q = \gamma (b)$ . We say that $p$ and $q$ are conjugate along $\gamma$ if there exists a nonzero Jacobi field $J$ along $\gamma$ such that $J(a) = J(b) = 0$ .

For a unit-speed geodesic $\gamma : [0, \infty) \to M$ with $\gamma(0) = p$ , define its cut time $t_{\mathrm{cut}}(\gamma) := \sup \{t > 0 : \gamma|_{[0, t]} \text{ minimizes distance between its endpoints}\}$ . If $t_{\mathrm{cut}}(\gamma) < \infty$ , the cut point of $p$ along $\gamma$ is $\gamma(t_{\mathrm{cut}}(\gamma))$ . The cut locus of $p$ , denoted $\mathrm{Cut}(p)$ , is the set of all cut points of $p$ over all unit-speed geodesics emanating from $p$ . It is a classical fact that along any geodesic starting at $p$ , the cut time occurs no later than the first conjugate time (if a conjugate point occurs at all); moreover, a cut point may occur strictly before the first conjugate point when there are multiple minimizing geodesics to the same endpoint.

We now provide some intuition on the above concepts. The curvature tensor quantifies how covariant derivatives fail to commute; it encodes the intrinsic bending of the manifold. Sectional curvature reduces this information to a 2-dimensional direction $\sigma$ : positive sectional curvature tends to make nearby geodesics in $\sigma$ focus toward each other, while negative curvature tends to make them spread apart. Jacobi fields describe the infinitesimal separation between nearby geodesics (they arise from variations of geodesics), so zeros of a Jacobi field correspond to a loss of local uniqueness/minimality of geodesics. Conjugate points describe a differential property, corresponding to the degeneracy of $d\exp$ , hence naturally enter comparison theory used for our analysis later (see Section A.2). On the other hand, cut points describe a geometric property, describing when geodesics cease to be minimizing, as well as when $\log_x$ stops being single-valued.

# 2.2 Riemannian Flow Matching

Let $\pi_0$ and $\pi_1$ be two probability distributions supported on a Riemannian manifold $M$ . The Riemannian Flow Matching (RFM) framework aims to learn a time-dependent vector field $v(t,x)$ whose induced flow transports samples from $\pi_0$ to $\pi_1$ . Concretely, RFM seeks $v$ such that if $X_0 \sim \pi_0$ , then the solution $\{X_t\}_{t \in [0,1]}$ to the ODE

$$
d X _ {t} = v \left(t, X _ {t}\right) d t, \quad X _ {0} \sim \pi_ {0}, \tag {2}
$$

satisfies $X_{1} \sim \pi_{1}$ . The ODE exhibits a maximal solution as long as $v$ is continuous in time and locally-Lipschitz in space; see, for example (Lang, 2012, Chapter IV). Moreover, if the manifold is complete and $v(t,x)$ satisfies a linear growth bound, the solution exists globally in time. We also remark here that Wan et al. (2025) provided more refined conditions that hold more generally for the case of Euclidean spaces.

A key geometric constraint is that for every $(t,x)$ , the velocity must lie in the tangent space at the current point:

$$
v (t, x) \in T _ {x} M, \qquad t \in [ 0, 1 ].
$$

That is, $v(t,x)$ represents a valid instantaneous direction of motion along the manifold at $x$ . This is where the Riemannian setting differs fundamentally from the Euclidean one. When $M = \mathbb{R}^d$ , all tangent spaces are canonically identical, i.e., $T_x\mathbb{R}^d \cong \mathbb{R}^d$ for all $x$ , so we can view the vector field simply as a global map $v:[0,1] \times \mathbb{R}^d \to \mathbb{R}^d$ with a single, fixed vector space as codomain.

On a general manifold $M$ , however, the tangent spaces $\{T_xM\}_{x \in M}$ form a family of different vector spaces attached to different points. Although each $T_xM$ has the same dimension, there is no canonical identification between $T_xM$ and $T_yM$ when $x \neq y$ . As a consequence, the "output space" of $v(t, \cdot)$ depends on $x$ : $v$ is a section of the tangent bundle rather than a map into a single fixed $\mathbb{R}^d$ . This location-dependence forms a main source of technical differences between Euclidean flow matching and RFM, and it will matter in the analysis later.

In flow matching, one typically parameterizes the time-dependent vector field with a neural network and learns it by minimizing the conditional flow matching objective. In the Riemannian setting, choosing the coupling between the endpoints to be the independent coupling, i.e., sampling $X_0 \sim \pi_0$ and $X_1 \sim \pi_1$ independently, yields the training loss

$$
\min  _ {u} \mathbb {E} _ {t, X _ {0} \sim \pi_ {0}, X _ {1} \sim \pi_ {1}} \left[ \| u (X _ {t}, t) - P _ {X _ {0}} ^ {X _ {t}} \log_ {X _ {0}} (X _ {1}) \| ^ {2} \right], \tag {3}
$$

where $\operatorname{Log}_x(\cdot)$ is the Riemannian logarithm map, and $P_{a}^{b}$ denotes parallel transport along the interpolation curve from $a$ to $b$ . In Euclidean space, the standard choice is the straight-line interpolation $X_{t} \coloneqq tX_{1} + (1 - t)X_{0}$ between $X_{0}$ and $X_{1}$ ; on a Riemannian manifold, this naturally generalizes to the geodesic interpolation $X_{t}$ in (1). We denote the population minimizer by $v(t,x)$ and the learned (neural) approximation by $\hat{v}(t,x)$ .

It is useful to note that the population minimizer admits a closed-form expression as a conditional expectation (see, e.g., Guan et al. (2026)). Specifically, for any fixed $t < 1$ and $x \in M$ ,

$$
\begin{array}{l} v (t, x) = \mathbb {E} \left[ P _ {X _ {0}} ^ {x} \operatorname {L o g} _ {X _ {0}} \left(X _ {1}\right) \mid X _ {t} = x \right] = \frac {1}{1 - t} \mathbb {E} \left[ \operatorname {L o g} _ {x} \left(X _ {1}\right) \mid X _ {t} = x \right] \tag {4} \\ = \frac {1}{1 - t} \int_ {M} \operatorname {L o g} _ {x} (x _ {1}) p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}), \\ \end{array}
$$

where $p_t(x_1 \mid x)$ denotes the conditional density of $X_1$ given $X_t = x$ under the above independent coupling and the chosen interpolation, and $dV_g$ is the Riemannian volume measure.

# Algorithm 1 RFM with Early Stopping

1: Denote the learned vector field by $\hat{v} (t,x)$   
2: Choose step size schedule $\{h_i\}$ for Euler discretization and early stopping time $T \in [0,1)$ such that $\sum_{i=0}^{N-1} h_i = T$ , where $N$ is the total number of steps.   
3: Perform Euler discretization for $N$ steps:   
4: Generate $x_0 \sim \pi_0$ , set $t_0 = 0$ .   
5: for $k = 0$ to $N - 1$ do   
6: $x_{t_{k + 1}} = \mathrm{Exp}_{x_{t_k}}(h_k\hat{v} (t_k,x_{t_k})).$   
7: $t_{k + 1}\gets t_k + h_k.$   
8: end for   
9: Output a sample $x_{T} \coloneqq x_{t_{N}} \sim \hat{\pi}_{T}$ .

To generate samples, we numerically simulate the learned flow-matching ODE in Algorithm 1. While the ideal (population) flow driven by the true minimizer $v$ would transport $\pi_0$ to $\pi_1$ at time $t = 1$ , in practice we only have access to a learned approximation $\hat{v}$ and a time-discretized integrator. A key difficulty is the behavior of the conditional flow-matching vector field near the terminal time. Note from (4) that the population minimizer contains an explicit $1/(1 - t)$ factor. Along the exact geodesic bridge used to define $X_t$ , the term $\mathbb{E}[\log_x(X_1) \mid X_t = x]$ typically scales like

$(1 - t)$ so that $v(t,x)$ remains finite; however, this cancellation is fragile. Any mismatch between the learned field $\hat{v}$ and the population field $v$ , or any deviation of the simulated trajectory from the

training interpolation, can destroy the cancellation and make the effective dynamics increasingly stiff as $t \to 1$ (large velocities and/or large sensitivities with respect to $x$ ).

This stiffness directly motivates early stopping. In Algorithm 1, we use $\{h_i\}$ to denote the step size schedule. In the constant step size case, we simply have $h_i \equiv h, \forall i$ . With a pre-designed step size schedule and early stopping time $T$ , the algorithm generates $\{x_{t_k}\}$ where $t_k \coloneqq \sum_{i=0}^{k-1} h_i$ and consequently by definition $t_N = T$ . The Euler discretization accumulates both numerical discretization error and statistical/approximation error from learning $\hat{v}$ . Near $t = 1$ , the factor $\frac{1}{1-t}$ amplifies errors in estimating the small conditional mean $\mathbb{E}[\log_x(X_1) \mid X_t = x]$ : a small absolute error in this conditional expectation can translate into a much larger error in the velocity, which then produces an $O(1)$ perturbation over the last few integration steps and shifts the terminal law away from $\pi_1$ . For this reason, following existing probability-flow analyses in the Euclidean setting (e.g., Li et al. (2025, 2024a)) we establish convergence rates to an approximate distribution at a terminal time $T < 1$ , corresponding to stopping the integration before the most ill-conditioned regime.

# 3 Total Variation Rates: Compact Manifolds

We now establish TV error bounds for compact manifolds, which covers application including SO(3) (Yue et al., 2025), Tori and hypersphere (Mathieu and Nickel, 2020; Sriram et al., 2024). We then specialize to the case of hypersphere to obtain explicit iteration complexity results. We start with the following assumption on curvature of manifold.

Assumption 1 (Assumptions on Riemannian Manifold). $M$ is a complete manifold without boundary. There exists $L_{R} \geq 0$ s.t. $\| R(u,v)v\| \leq L_{R}\| u\| \| v\|^{2}, \forall u,v,w \in T_{x}M$ , and all sectional curvatures of $M$ are bounded below by $K_{\min}$ and bounded above by $K_{\max}$ .

This assumption enforces standard global regularity of the geometry of $M$ : completeness guarantees geodesics and the exponential map are well-defined for all times. The bound $\| R(u,v)v\| \leq L_R\| u\| \| v\| ^2$ controls the norm of the curvature operator, ensuring that curvature-induced deviations along geodesics are uniformly bounded. Finally, the two-sided sectional curvature bound $K_{\mathrm{min}}\leq K\leq K_{\mathrm{max}}$ prevents the manifold from being too positively curved (excessive focusing of geodesics) or too negatively curved (overly rapid divergence), which is crucial for stability and comparison estimates. We impose the following assumptions on flow matching vector field $v$ .

Assumption 2. (Regularity of Flow Matching Vector Field) The true vector field $v(t,x)$ is at least $C^2$ in $t,x$ and satisfies the following for $\forall x\in M,t\in [0,1)$ :

(1) $\| \nabla v(t,x)\|_{\mathrm{op}}\leq L_t^{v,x}.$   
(2) $\| v(t,x)\| \leq L_v$ and $\left\| \frac{d}{dt} v(t,x)\right\| \leq L_t^{v,t}$ .   
(3) $\| \operatorname{grad}_x \operatorname{div} v(t,x) \| \leq L_t^{\operatorname{div},x}$ and $\left|\frac{d}{dt} \operatorname{div} v(t,x)\right| \leq L_t^{\operatorname{div},t}$ .

The above conditions require the population vector field $v(t,x)$ to be smooth and uniformly well-behaved so that the induced flow depends stably on time and initial conditions. The bounds on $\| \nabla v(t,x)\|_{\mathrm{op}}$ , $\| v(t,x)\|$ , and $\left\| \frac{d}{dt} v(t,x)\right\|$ ensure the dynamics are Lipschitz in space and controlled in magnitude and time variation, preventing trajectories from separating too quickly or developing instabilities as $t$ evolves. In Euclidean space $M = \mathbb{R}^d$ with the standard metric, $\nabla v(t,x)$ reduces to the Jacobian $D_xv(t,x)$ , so $\| \nabla v(t,x)\|_{\mathrm{op}}$ is exactly the usual spectral/operator norm $\| D_xv(t,x)\|_{2\to 2}$ (i.e., the Lipschitz constant of $v(t,\cdot)$ at $x$ ). The bounds on $\| \operatorname{grad}_x\operatorname{div}v(t,x)\|$ and $\left|\frac{d}{dt}\operatorname{div}v(t,x)\right|$

control how local volume change induced by the flow varies across space and time, and is important for analyzing how densities evolve under the continuity equation.

Assumption 3. (Estimation Error) Tthere exists some small $\varepsilon >0$ such that the followings hold, $\forall x\in M,t\in [0,1)$ : (1) $\| \hat{v} (t,x) - v(t,x)\| \leq \varepsilon$ , and (2) $\| \nabla \hat{v} (t,x) - \nabla v(t,x)\|_{\mathrm{op}}\leq \varepsilon$

We remark that such an assumption on estimation accuracy for derivative of $v(t,x)$ is standard in the literature for error analysis of ODE based generative models (Li et al., 2024a, 2025; Liu et al., 2025). The second item implies an error bound on uniform divergence estimation error, which together with the first item, helps bounding the discretization error. We also emphasize that uniform estimation error bounds obtainable on compact manifolds (Yarotsky, 2017; Mena et al., 2025).

Under our assumptions, we can prove the following bound on TV distance (see Definition A.1).

Theorem 1. Let Assumptions 1, 2 and 3 hold. Define

$$
C _ {L i p} := 3 \sqrt {L _ {t} ^ {\text {s c o r e}}} L _ {t} ^ {v, x} L ^ {v} + \sqrt {L _ {t} ^ {\text {s c o r e}}} L _ {t} ^ {v, t} + 3 L ^ {v} L _ {t} ^ {\operatorname {d i v}, x} + L _ {t} ^ {\operatorname {d i v}, t} + L _ {R} (L ^ {v}) ^ {2} d \tag {5}
$$

$$
C _ {e p s} := \sqrt {2 L _ {t} ^ {\text {s c o r e}}} + 1 + 2 \sqrt {L _ {t} ^ {\text {s c o r e}}} L ^ {v} + \sqrt {L _ {t} ^ {\text {s c o r e}}} L _ {t} ^ {v, x} + L _ {t} ^ {\text {d i v}, x} + 2 L _ {R} d L ^ {v} \tag {6}
$$

Picking the constant step size $h$ to satisfy the requirements in Lemma 5.2, we have

$$
\mathrm {T V} \left(\pi_ {T}, \hat {\pi} _ {T}\right) \leq h C _ {L i p} + \varepsilon C _ {e p s} + \varepsilon^ {2} (\sqrt {L _ {t} ^ {s c o r e}} + L _ {R} d).
$$

We imposed an upper bound on the step size (as in Lemma 5.2) to ensure that each Euler step remains within a controlled neighborhood—in particular, within the injectivity-radius regime where the exponential map does not "fold" and the map $F_{t_k,h}(x) = \mathrm{Exp}_x(h\hat{v} (t_k,x))$ stays invertible—so that the continuous-time interpolation and the associated vector field $\tilde{v}$ are well defined. For more details, see Section 5 on the choice of $h$ . At a high level, the constant $C_{\mathrm{Lip}}$ aggregates the Lipschitz regularity moduli of the population flow (and the score) that control how local Euler truncation errors are amplified when transported through time; thus it governs the $\mathcal{O}(h)$ discretization contribution in the TV bound. In contrast, $C_{\mathrm{eps}}$ collects the same geometric and score-dependent stability factors but attached to the estimation perturbation $\hat{v} - v$ (and its divergence), quantifying how an $\varepsilon$ -accurate field estimate propagates through the continuity equation; this is why it multiplies the leading $\mathcal{O}(\varepsilon)$ term, with the remaining $\varepsilon^2 (\sqrt{L_t^{\mathrm{score}}} + L_R d)$ capturing higher-order interactions between score regularity and field mismatch.

Remark 1. The early stopping error can be controlled in the Wasserstein distance (see Definition A.1) as: $W_{1}(\pi_{1},\pi_{T}) \lesssim 1 - T$ . On a compact manifold, TV bound implies a $W_{1}$ bound, as $W_{1}(\pi_{T},\hat{\pi}_{T}) \leq \mathrm{diam}(M)\mathrm{TV}(\pi_{T},\hat{\pi}_{T})$ (Villani, 2008, Theorem 6.15). Thus we can convert our TV bound into a bound in $W_{1}$ distance, and obtain an error bound for $W_{1}(\hat{\pi}_{T},\pi_{1})$ , consider both sampling error and early stopping error.

We now provide explicit rates on the $d$ -dimensional hypersphere. Following Li et al. (2024a, 2025); Liu et al. (2025), we consider the case when the vector field is well-estimated (i.e., $\varepsilon \approx 0$ ) and report the number of sampling steps $N$ required to get $\varepsilon_{target}$ close to $\pi_T$ .

Proposition 3.1. For some finite $d \geq 4$ , let $M = S^d$ , and $T < 1$ be the early stopping time. Assume $\pi_1$ has a smooth density and satisfies $0 < m_1 \leq p_1(x) \leq M_1$ . Pick $\pi_0(x)$ to be uniform on the hypersphere. Then Assumption 2 is satisfied and the constants in Assumption 2 are of polynomial order (see Lemma B.5). Now if Assumption 3 is satisfied, to reach $\varepsilon_{\text{target}}$ accuracy in TV distance,

- For constant step size as in (14), the complexity is $N = \mathcal{O}(d^2 / \varepsilon_{\text{target}}(1 - T)^2)$ .   
- For a carefully designed step size schedule as in (15), it can be improved to $N = \mathcal{O}(d^2 / \varepsilon_{\text{target}}(1 - T))$ .

# 4 Total Variation Rates: Hadamard Manifolds

In this section, we establish error bounds in terms of total variation distance on Hadamard manifolds (which are non-compact), which covers applications including SPD manifolds (Li et al., 2024b; Collas et al., 2025). While retaining the same curvature condition in Assumption 1, we modify Assumption 2 and 3 as follows, to naturally handle the non-compactness of Hadamard manifolds.

Assumption 4 (Regularity of the true Vector Field). The true vector field $v$ satisfies $\forall t \in [0,1)$ :

(1) $\mathbb{E}_{x_t}\| \nabla v(t,x_t)\|_{\mathrm{op}}^2\leq (L_t^{v,x})^2$ and $\mathbb{E}_{x_t}\left\| \frac{d}{dt} v(t,x_t)\right\| ^2\leq (L_t^{v,t})^2.$   
(2) $\mathbb{E}_{x_t}\Big|\frac{d}{dt}\mathrm{div}v(t,x_t)\Big|\leq L_t^{\mathrm{div},t}$ and $\mathbb{E}_{x_t}\| \operatorname {grad}_x\operatorname {div}v(t,x_t)\| ^2\leq (L_t^{\mathrm{div},x})^2.$   
(3) $\mathbb{E}_{x_t}\| v(t,x_t)\| ^2\leq (L_t^v)^2.$

Assumption 5 (Regularity of Learned Vector Field). Assume that the learned vector field $\hat{v}$ satisfies: (1) $\| \hat{v} (t,x)\| \leq L_t^{\hat{v}}$ , (2) $\| \nabla \hat{v} (t,x)\| \leq L_t^{\hat{v},x}$ and (3) $\| \operatorname {grad}\operatorname {div}\hat{v} (t,x)\| \leq L_t^{\operatorname {div}\hat{v},x}$ , where $L_{t}^{\hat{v}},L_{t}^{\hat{v},x},L_{t}^{\operatorname {div}\hat{v},x}$ are of the same order as $L_{t}^{v},L_{t}^{v,x},L_{t}^{\operatorname {div},x}$ .

Assumption 6 (Estimation Error). There exists some small $\varepsilon >0$ s.t. the following hold $\forall t\in$ $\{t_k\}_{k = 0}^{N - 1}$ : (1) $\mathbb{E}_{x_t}[||\hat{v} (t_k,X_{t_k}) - v(t_k,X_{t_k})||^2 ]\leq \varepsilon$ , (2) $\mathbb{E}_{x_t}[||\mathrm{div}\hat{v} (t_k,X_{t_k}) - \mathrm{div}v(t_k,X_{t_k})|]\leq \varepsilon$

The conditions in Assumption 4, 5 and 6 serve the same purpose as Assumption 2 and 3. We remark that on a non-compact manifold, similar to the Euclidean space, it is more natural to assume regularity holds in expectation instead of holding uniformly. Compared to the compact case, we need to additionally enforce Assumption 5, which is of essential importance to guarantee the well-behavedness of the sampling ODE. The condition that the Lipschitz constants of the learned vector field are of the same order of the true field is made purely for convenience to avoid a more complicated looking bound. Note that for the compact case, since we can assume point-wise regularity, the condition made in Assumption 5 is a direct consequence of Assumption 2 and 3. We also remark that for existing works in Euclidean space, Liu et al. (2025) and Huang et al. (2025) assumed uniformly bounded regularity for the learned vector field, and estimation error in expectation, which are similar in spirit to Assumptions 5 and 6. Below, we present our rates.

Theorem 2 (Sampling Error for Hadamard Manifold). Let Assumptions 1, 4, 5 and 6, hold. Picking the step size $h$ to satisfy the requirements in Lemma 5.2, we have

$$
\operatorname {T V} \left(\pi_ {T}, \hat {\pi} _ {T}\right) \leq h C _ {L i p} + \varepsilon C _ {e p s, 1},
$$

where $\mathsf{C}_{Lip}$ is as in (5) and $\mathsf{C}_{eps,1}$ defined in (13) represents the (vector field) estimation error.

We now specialize our results to the case when $M \equiv \mathrm{SPD}(n) \coloneqq \{X \in \mathbb{R}^{n \times n} : X \succ 0, X^T = X\}$ , the manifold of symmetric positive definite matrices endowed with the affine invariant metric $g_X(U, V) = \operatorname{tr}(X^{-1}UX^{-1}V)$ . To do so, we compute the explicit order of regularity constants $C_{\mathrm{Lip}}$ and $C_{\mathrm{eps},1}$ (see Proposition B.6), which in turn yields the result below.

Proposition 4.1. Let $M = \mathrm{SPD}(n)$ for which the dimension $d = n(n + 1)/2$ . We adopt early stopping, i.e., simulate the ODE on the interval $[0,T] \subsetneq [0,1]$ . Choose prior distribution as $\pi_0(x) \propto \exp\left(-\frac{n(n + 1)d_g(x,I)^2}{2}\right)$ being a Riemannian Gaussian distribution (the center of Riemannian Gaussian is arbitrary, here we set as $I \in \mathrm{SPD}(n)$ for notation simplicity). We further assume the data distribution $\pi_1$ satisfies

$$
\max  \left\{\mathbb {E} [ d (X _ {1}, I) ^ {2} e ^ {\lambda_ {1} d (X _ {1}, I)} ], \mathbb {E} [ e ^ {\lambda_ {1} d (X _ {1}, I)} ] \right\} \leq M _ {\lambda_ {1}}, \quad \text {w h e r e} \quad \lambda_ {1} = 2 4 \max  \{1, \kappa \}, \tag {7}
$$

for some constant $M_{\lambda_1}$ . Then Assumption 4 is satisfied and the constants in Assumption 4 are of polynomial order (see Proposition B.6 for explicit bounds). Under Assumption 1, 5 and Assumption 6, (with constant step size) the iteration complexity to reach $\varepsilon_{target}$ accuracy in TV distance is $N = \mathcal{O}(d^{24}L_R^3M_{\lambda_1}^{\frac{3}{2}} / \varepsilon_{target}(1 - T)^3)$ .

Here the moment condition (7) plays a role analogous to finite-moment conditions (e.g., $\mathbb{E}[\|X_1\|^4] < \infty$ and stronger conditions like bounded support) appeared in Euclidean discretization analysis (Liu et al., 2025; Li et al., 2025; Zhou and Liu, 2025). The appearance of exponential moments is due to curvature distortion: the model function $s_{K_{\min}}(r)$ grows linearly in $r$ when $K_{\min} = 0$ but exponentially in $r$ when $K_{\min} < 0$ (see Section 5.2.1). Although the order of $d$ is polynomial, we expect it could be improved further by more refined computation and additional assumptions.

# 5 Proof Sketch and Intermediate Results

We now outline the main ideas behind the proof of our principal TV-rate bound. At a high level, we view both the population flow-matching dynamics and its numerical approximation as deterministic transports on the manifold driven by (possibly different) time-dependent vector fields. Randomness enters only through the initialization, so the objects of interest are the time-marginal laws $(p_t)_{t\in [0,1]}$ and $(q_{t})_{t\in [0,1]}$ induced by these transports. Our argument has three conceptual steps:

1. (TV stability under transport) derive a differential identity for $\partial_t\mathrm{TV}(p_t,q_t)$ in terms of the mismatch between the driving vector fields (Lemma 5.1);   
2. (continuous-time interpolation of Euler) construct an interpolation of the Euler scheme that is itself an ODE on $M$ , so that Lemma 5.1 applies;   
3. (term-by-term control) bound the resulting RHS by establishing (i) score regularity for $p_t$ , (ii) regularity of the relevant vector fields, and (iii) a curvature-dependent estimate for the divergence of the interpolated field.

Integrating the differential inequality over time then yields a bound on the terminal sampling error $\operatorname{TV}(X_1, Y_1)$ (or, when needed, the limit $t \uparrow 1$ ).

We begin with the key TV-derivative lemma, which is the Riemannian analogue of (Li et al., 2025, Lemma 4.2). The proof involves the following steps: (i) write the evolution of $p$ and $q$ through the continuity equation, and (ii) differentiate $\int (p - q)_+$ , and integrate by parts—but all differential operators must be interpreted intrinsically (gradient, divergence, and the Riemannian volume form). The second line of (10) is obtained by taking absolute values and applying Cauchy-Schwarz to the inner-product term.

Lemma 5.1. Let $X_{t}, Y_{t}$ be stochastic processes on $M$ , satisfying the following ODE:

$$
d X _ {t} = v (t, X _ {t}) d t, \quad X _ {0} \sim p _ {0} \tag {8}
$$

$$
d Y _ {t} = \tilde {v} (t, Y _ {t}) d t, \quad Y _ {0} \sim q _ {0} \tag {9}
$$

Let $p(t,x)$ be the law of $X_{t}$ and $q(t,x)$ be the law of $Y_{t}$ . Define $\Omega_{t} = \{x\in M:p(t,x) - q(t,x) > 0\}$ . Then we have

$$
\begin{array}{l} \frac {\partial \operatorname {T V} (X _ {t} , Y _ {t})}{\partial t} = \int_ {\Omega_ {t}} p (t, x) (\operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) + \langle \operatorname {g r a d} \log p (t, x), \tilde {v} (x, t) - v (x, t) \rangle) d V _ {g} (x) \\ \leq \mathbb {E} [ | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | ] + \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \| \tilde {v} (x, t) - v (x, t) \| ]. \tag {10} \\ \end{array}
$$

# 5.1 Continuous Time Interpolation

We now explain how Lemma 5.1 is used to analyze the Euler discretization error. We take (8) to be the flow-matching ODE driven by the (population) vector field $v(t,\cdot)$ , and we want (9) to represent the numerical method. A direct interpolation of the Euler scheme would be

$$
y _ {t} = \operatorname {E x p} _ {y _ {k}} \big ((t - t _ {k}) \hat {v} (t _ {k}, y _ {k}) \big), \qquad t \in [ t _ {k}, t _ {k + 1}),
$$

i.e., the velocity is frozen at the left endpoint. However, this curve is not immediately of the form $dy_{t} = \tilde{v}(t,y_{t})dt$ with a vector field $\tilde{v}(t,\cdot)$ on $M$ , because the frozen vector $\hat{v}(t_k,y_k)$ lives in $T_{y_k}M$ , whereas the ODE requires the instantaneous velocity to belong to $T_{y_t}M$ .

The natural remedy is to transport the frozen velocity along the curve. Concretely, for $t \in [t_k, t_{k+1})$ we set

$$
\tilde {v} (t, y _ {t}) := P _ {y _ {k}} ^ {y _ {t}} \hat {v} (t _ {k}, y _ {k}), \qquad \text {s o t h a t} \qquad d y _ {t} = \tilde {v} (t, y _ {t})   d t,
$$

where $P_{y_k}^{yt}$ denotes parallel transport along the (interpolated) trajectory. This ensures $\tilde{v}(t, y_t) \in T_{y_t}M$ for all $t$ , so the interpolation is an honest ODE on $M$ . To apply Lemma 5.1, we further need $\tilde{v}$ to be defined as a function of $(t, x)$ (not implicitly through a particular path). This requires that, given $(t, x)$ , we can uniquely recover the footpoint $y_k$ that generated $x$ under the Euler interpolation. Equivalently, we need the map $y_k \longmapsto \mathrm{Exp}_{y_k}\big((t - t_k)\hat{v}(t_k, y_k)\big)$ to be invertible on the relevant step size range.

For notational convenience, for $t \in [0,1)$ and $h \geq 0$ we define $F_{t,h}(x) \coloneqq \mathrm{Exp}_x(h\hat{v} (t,x))$ . In particular, for $t \in [t_k,t_{k + 1})$ , the Euler interpolation can be written as $F_{t_k,t - t_k}(x_k) = \mathrm{Exp}_{x_k}((t - t_k)\hat{v} (t_k,x_k))$ . Lemma 5.2 below shows that for sufficiently small $h$ the map $F_{t_k,h}$ is invertible. Assuming invertibility, we can express the interpolation vector field at an arbitrary point $x$ by pulling back to the unique preimage $x_{k} = F_{t_{k},t - t_{k}}^{-1}(x)$ and then parallel-transporting the frozen velocity to $T_{x}M$ :

$$
\tilde {v} (t, x) = P _ {F _ {t _ {k}, t - t _ {k}} ^ {- 1} (x)} ^ {x} \hat {v} (t _ {k}, F _ {t _ {k}, t - t _ {k}} ^ {- 1} (x)),
$$

where, for a trajectory $(x_{t})$ of (9), we have $F_{t_k,t - t_k}^{-1}(x_t) = x_{t_k}$ .

Lemma 5.2. Let $M$ be simply connected Riemannian manifold that satisfies Assumption 1. Let $b$ be any vector field on $M$ , satisfying $\| b(x) \| \leq B, \forall x \in M$ . Assume $\| \nabla_v b(x) \| \leq L_\nabla \| v \|$ . Let $R = \operatorname{inj}(M)$ . To guarantee $F_{t_k, t - t_k}$ being invertible, we require

$$
h <   \min \{\frac {R}{B}, \frac {1}{4 L _ {\nabla}}, \sqrt \frac {3}{4 \| b (x) \| ^ {2} L _ {R} (2 + 2 L _ {\nabla} \max \{\frac {1}{\sqrt {K _ {\min}} , 1 \})}} \}, \qquad \text {i f} K _ {\min } > 0,
$$

$$
h <   \min \{\frac {R}{B}, \frac {1}{4 L _ {\nabla}}, \sqrt {\frac {3}{4 \| b (x) \| ^ {2} L _ {R} (2 \frac {\sinh (\sqrt {- K _ {\min}})}{\sqrt {- K _ {\min}}} + 4 \frac {\cosh (\sqrt {- K _ {\min}}) - 1}{- K _ {\min}} L _ {\nabla})}} \}, \quad i f \quad K _ {\min} <   0,
$$

$$
h <   \min \{\frac {R}{B}, \frac {1}{4 L _ {\nabla}}, \sqrt {\frac {3}{4 \| b (x) \| ^ {2} L _ {R} (2 + h L _ {\nabla})}} \}, \qquad \qquad \qquad \text {i f} \quad K _ {\min } = 0.
$$

The invertibility requirement is precisely the condition that the exponential map used in one Euler step stays in a regime where it does not "fold" the manifold (e.g., by crossing conjugate points or exiting the injectivity radius). If $(t - t_k)\hat{v} (t_k,Y_{t_k})$ is too large, the map $x\mapsto \mathrm{Exp}_x((t - t_k)\hat{v} (t_k,x))$ may fail to be injective, and then multiple preimages could map to the same $Y_{t}$ . Lemma 5.2 enforces a step-size restriction that prevents this pathology by combining (i) injectivity-radius control and

(ii) bounds on the differential of $F_{t,h}$ via curvature comparison and covariant-derivative estimates. When $\operatorname{inj}(M) = \infty$ (e.g., $M = \mathbb{R}^d$ or $M = \mathrm{SPD}(n)$ ), the injectivity-radius constraint becomes vacuous and the step-size condition simplifies accordingly.

# 5.2 Discretization analysis

Although (8) and (9) are deterministic ODEs, the random initialization makes $(X_{t})$ and $(Y_{t})$ stochastic processes through their induced laws. To isolate discretization error, we couple them by taking the same initial distribution: $X_0\sim \pi_0$ , and $Y_{0}\sim \pi_{0}$ . Then $\mathrm{TV}(X_t,Y_t)$ measures the discrepancy between the population flow-matching transport and the transport induced by the Euler interpolation. In particular, at terminal time (or in the limit $t\uparrow 1$ ), $\mathrm{TV}(X_1,Y_1)$ is exactly the sampling error attributable to time discretization (and, if present, to the use of $\hat{v}$ instead of $v$ ).

Applying Lemma 5.1 with $p(t, \cdot)$ the law of $X_{t}$ and $q(t, \cdot)$ the law of $Y_{t}$ , and integrating in time, yields

$$
\begin{array}{l} \operatorname {T V} \left(X _ {1}, Y _ {1}\right) \leq \operatorname {T V} \left(X _ {0}, Y _ {0}\right) + \int_ {0} ^ {1} \left(\mathbb {E} [ | \operatorname {d i v} (\tilde {v} (t, X _ {t}) - v (t, X _ {t})) ] ] + \right. \\ \mathbb {E} [ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| \| \tilde {v} (t, X _ {t}) - v (t, X _ {t}) \| ]) d t. \\ \end{array}
$$

Since TV $(X_0,Y_0) = 0$ under the shared initialization, the task reduces to controlling the two error terms on the RHS. A convenient way to organize the analysis is to bound three quantities that repeatedly appear in the argument: $\mathbb{E}\big[\| \mathrm{grad}\log p_t(X_t)\| ^2\big]$ , $\mathbb{E}\big[\| \tilde{v} (t,X_t) - v(t,X_t)\| ^2\big]$ , and $\mathbb{E}\big[|\operatorname {div}(\tilde{v} (t,X_t) - v(t,X_t))|\big]$ . Specifically, the second expectation in (10) can be decoupled via Cauchy-Schwarz:

$$
\mathbb {E} [ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| \| \tilde {v} (t, X _ {t}) - v (t, X _ {t}) \| ] \leq \sqrt {\mathbb {E} [ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} ]} \sqrt {\mathbb {E} [ \| \tilde {v} (t , X _ {t}) - v (t , X _ {t}) \| ^ {2} ]}.
$$

Thus, once we establish suitable bounds for these three terms (uniformly for $t$ away from 1, and with explicit dependence on $t$ as $t \uparrow 1$ ), we can integrate over time to obtain a quantitative TV-rate.

# 5.2.1 Score Regularity and Vector Field Regularity

We now summarize the regularity inputs needed to control the score term and the vector-field mismatch. The score bound is the main "density regularity" ingredient, while the vector-field bounds ensure that (i) the Euler interpolation is well defined and (ii) the mismatch $\tilde{v} - v$ can be quantified in geometry-aware norms.

- Score regularity. We show that there exists a (possibly time-dependent) constant $L_{t}^{\mathrm{score}}$ such that, for all $t \in [0,1)$ , $\mathbb{E}\big[\| \operatorname{grad} \log p_t(X_t)\|^2\big] \leq L_t^{\mathrm{score}}$ . The bound is allowed to deteriorate as $t \uparrow 1$ ; this is unavoidable in general and matches the behavior of population conditional flow fields near the terminal time. We establish this in Proposition 5.3 for compact manifolds and in Proposition 5.4 for Hadamard manifolds (both stated below). A crucial point is that the existence of such an $L_{t}^{\mathrm{score}}$ relies on sufficient smoothness/positivity of $p_t$ ; without it, grad $\log p_t$ may not be square-integrable and the bound can fail even for $t < 1$ .   
- Regularity on compact manifolds. On compact manifolds, curvature is bounded and distances are uniformly controlled, but the presence of cut points can obstruct smoothness of conditional densities such as $p_t(x_1 \mid x_t = x)$ , which enter the explicit formulae for the population flow field. We verify Assumption 2 on $S^d$ in Appendix D by exploiting explicit computations on the sphere. For more general compact geometries, controlling smoothness across the cut locus is substantially more delicate and is the main reason we phrase the required assumptions abstractly.

- Regularity on Hadamard manifolds. On Hadamard manifolds, the absence of cut points guarantees global smoothness of the exponential map and of the relevant conditional densities, which greatly simplifies differentiability issues. The trade-off is that negative curvature and unbounded distance can amplify derivative bounds along geodesics. In particular, pointwise bounds for derivatives of $v(t,x)$ typically involve factors that are Poly $(d)$ , Poly $(1 / (1 - t))$ and Poly $(s_{K_{\min}}(d(x_0,x_1)))$ , where for $K_{\min} < 0$ the model function $s_{K_{\min}}(r) = \frac{\sinh(r\sqrt{-K_{\min}})}{\sqrt{-K_{\min}}}$ grows exponentially in $r$ . This motivates seeking regularity in expectation rather than uniform-in- $x$ bounds. We verify Assumption 4 for SPD $(n)$ in Appendix E by combining curvature comparison with a moment condition (7), which plays the role of a Euclidean second-moment bound and compensates for curvature-induced growth.

Proposition 5.3. Let $M$ be a compact manifold satisfying Assumption 1. Under Assumption 2, exists some finite number $L_{t}^{\mathrm{score}}$ that depends on $t$ s.t. $\mathbb{E}\big[\| \operatorname {grad}\log p_t(X_t)\| ^2\big]\leq L_t^{\mathrm{score}},\forall t\in [0,1)$

Proposition 5.4. Let $M$ be a Hadamard manifold with sectional curvature satisfying $-\kappa^2 = K_{\min} \leq \sec \leq 0$ . For prior being chosen as $X_0 \sim e^{-dd(x_0,z)^2}$ , we have

$$
\mathbb {E} \big [ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} \big ] \lesssim M \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} d ^ {2 \lambda_ {s c o r e}},
$$

where $\lambda_{score} = 6\max \{1,\kappa \}$ and $M = \mathbb{E}_{X_1}[e^{\lambda d(x_1,z)}]$ depends on the data distribution.

# 5.2.2 The Divergence Term

Finally, we comment on the divergence contribution $\mathbb{E}\big[|\mathrm{div}(\tilde{v} (t,X_t) - v(t,X_t))|\big]$ . This is the most geometry-specific part of the discretization analysis. In Euclidean space, the Euler interpolation simply freezes the velocity and no parallel transport is required; consequently, $\mathrm{div}\tilde{v}$ can be handled with elementary calculus. On a manifold, by contrast, our interpolated field $\tilde{v}$ is defined through (i) parallel transport and (ii) an implicit inverse mapping $F_{t_k,t - t_k}^{-1}$ . Both operations contribute nontrivially to $\nabla \tilde{v}$ and hence to $\mathrm{div}\tilde{v}$ .

Our approach is to explicitly differentiate the representation

$$
\tilde {v} (t, x) = P _ {F _ {t _ {k}, t - t _ {k}} ^ {- 1} (x)} ^ {x} \hat {v} \big (t _ {k}, F _ {t _ {k}, t - t _ {k}} ^ {- 1} (x) \big),
$$

for $t \in [t_k, t_{k+1})$ , along the interpolation geodesic under a parallel orthonormal frame, and decompose $\operatorname{div} \tilde{v}(t,x) = \sum_{i=1}^{d} \left\langle \nabla_{E_i(t)} \tilde{v}(t,x), E_i(t) \right\rangle$ into two pieces:

1. Derivatives of $\hat{v}(t_k, \cdot)$ evaluated at the preimage point;   
2. Curvature distortion from differentiating parallel transport.

Combining these estimates and using the curvature bounds in Assumption 1, we obtain a bound on $\operatorname{div} \tilde{v}$ and hence on $\operatorname{div}(\tilde{v} - v)$ , stated precisely in Lemma C.4. This divergence control, together with the score/vector-field regularity results above, completes the term-by-term bounds needed to integrate (10) and prove the stated TV-rate.

# Acknowledgements

KB is supported in part by National Science Foundation (NSF) grant DMS-2413426.

# References

F. Alimisis, A. Orvieto, G. Bécigneul, and A. Lucchi. A continuous-time perspective for modeling acceleration in Riemannian optimization. In International Conference on Artificial Intelligence and Statistics, pages 1297-1307. PMLR, 2020. (Cited on page 54.)   
V. Bansal, S. Roy, P. Sarkar, and A. Rinaldo. On the Wasserstein Convergence and Straightness of Rectified Flow. arXiv preprint arXiv:2410.14949, 2024. (Cited on page 3.)   
J. Benton, G. Deligiannidis, and A. Doucet. Error bounds for flow matching methods. Transactions on Machine Learning Research, 2024. (Cited on page 3.)   
J. Cheeger, D. G. Ebin, and D. G. Ebin. Comparison theorems in Riemannian geometry, volume 9. North-Holland publishing company Amsterdam, 1975. (Cited on pages 17, 18, and 38.)   
R. T. Q. Chen and Y. Lipman. Flow matching on general geometries. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=g7ohD1TITL. (Cited on page 3.)   
A. H. Cheng, A. Lo, K. L. K. Lee, S. Miret, and A. Aspuru-Guzik. Stiefel Flow Matching for Moment-Constrained Structure Elucidation. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=84WmbzikPP. (Cited on page 3.)   
X. Cheng, J. Zhang, and S. Sra. Efficient sampling on Riemannian manifolds via Langevin MCMC. Advances in Neural Information Processing Systems, 35:5995-6006, 2022. (Cited on page 3.)   
A. Collas, C. Ju, N. Salvy, and B. Thirion. Riemannian flow matching for brain connectivity matrices via pullback geometry. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. URL https://openreview.net/forum?id=NY3LzmUX17. (Cited on pages 3 and 9.)   
C. Criscitiello and N. Boumal. An accelerated first-order method for non-convex optimization on manifolds. Foundations of Computational Mathematics, 23(4):1433-1509, 2023. (Cited on page 36.)   
V. De Bortoli, E. Mathieu, M. Hutchinson, J. Thornton, Y. W. Teh, and A. Doucet. Riemannian score-based generative modelling. Advances in neural information processing systems, 35:2406-2422, 2022. (Cited on pages 2 and 3.)   
K. Gatmiry and S. S. Vempala. Convergence of the Riemannian Langevin algorithm. arXiv preprint arXiv:2204.10818, 2022. (Cited on page 3.)   
Y. Guan, K. Balasubramanian, and S. Ma. Riemannian Proximal Sampler for High-accuracy Sampling on Manifolds. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. URL https://openreview.net/forum?id=KxhCJc8B0g. (Cited on page 3.)   
Y. Guan, K. Balasubramanian, and S. Ma. Mirror flow matching with heavy-tailed priors for generative modeling on convex domains. In The Fourteenth International Conference on Learning Representations, 2026. URL https://openreview.net/forum?id=dZKl7uc0XQ. (Cited on pages 3, 6, and 42.)   
H. Hirai, H. Nieuwboer, and M. Walter. Interior-point methods on manifolds: theory and applications. In 2023 IEEE 64th Annual Symposium on Foundations of Computer Science (FOCS), pages 2021-2030. IEEE, 2023. (Cited on page 98.)

C.-W. Huang, M. Aghajohari, J. Bose, P. Panangaden, and A. C. Courville. Riemannian diffusion models. Advances in Neural Information Processing Systems, 35:2750-2761, 2022. (Cited on page 3.)   
D. Z. Huang, J. Huang, and Z. Lin. Convergence analysis of probability flow ODE for score-based generative models. IEEE Transactions on Information Theory, 2025. (Cited on pages 3 and 9.)   
S. Kobayashi. Transformation groups in differential geometry. Springer, 1972. (Cited on page 98.)   
L. Kong and M. Tao. Convergence of kinetic Langevin Monte Carlo on Lie groups. In The Thirty-Seventh Annual Conference on Learning Theory, pages 3011-3063. PMLR, 2024. (Cited on page 3.)   
S. Lang. Differential and Riemannian manifolds, volume 160. Springer Science & Business Media, 2012. (Cited on page 5.)   
J. M. Lee. Introduction to Smooth Manifolds. Springer, New York, 2012. ISBN 978-1-4419-9982-5. (Cited on page 45.)   
J. M. Lee. Introduction to Riemannian manifolds, volume 2. Springer, 2018. (Cited on pages 18, 27, 36, 51, 57, 87, and 98.)   
M. Lezcano-Casado. Curvature-dependent global convergence rates for optimization on manifolds of bounded geometry. arXiv preprint arXiv:2008.02517, 2020. (Cited on pages 17, 87, 89, 91, 92, 93, 94, and 95.)   
G. Li, Y. Wei, Y. Chi, and Y. Chen. A sharp convergence theory for the probability flow odes of diffusion models. arXiv preprint arXiv:2408.02320, 2024a. (Cited on pages 4, 7, and 8.)   
M. Li and M. A. Erdogdu. Riemannian Langevin algorithm for solving semidefinite programs. Bernoulli, 29(4):3093-3113, 2023. (Cited on page 3.)   
R. Li, Q. Di, and Q. Gu. Unified convergence analysis for score-based diffusion models with deterministic samplers. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=HrdVqFSn1e. (Cited on pages 3, 4, 7, 8, and 10.)   
Y. Li, Z. Yu, G. He, Y. Shen, K. Li, X. Sun, and S. Lin. SPD-DDPM: Denoising diffusion probabilistic models in the symmetric positive definite space. In Proceedings of the AAAI conference on artificial intelligence, volume 38, pages 13709-13717, 2024b. (Cited on page 9.)   
Y. Liu, R. Hu, Y. Chen, and L. Huang. Finite-Time Convergence Analysis of ODE-based Generative Models for Stochastic Interpolants. arXiv preprint arXiv:2508.07333, 2025. (Cited on pages 4, 8, 9, and 10.)   
A. Lou, M. Xu, A. Farris, and S. Ermon. Scaling Riemannian diffusion models. Advances in Neural Information Processing Systems, 36:80291-80305, 2023. (Cited on page 3.)   
X. Luo, Z. Wang, Q. Wang, X. Shao, J. Lv, L. Wang, Y. Wang, and Y. Ma. Crystalflow: a flow-based generative model for crystalline materials. Nature Communications, 16(1):9267, 2025. (Cited on page 3.)   
J. E. Marsden, T. Ratiu, and R. Abraham. *Manifolds, Tensor Analysis, and Applications*. Applied Mathematical Sciences. Springer, 3rd edition, 2002. ISBN 0-201-10168-S. (Cited on pages 19 and 45.)   
E. Mathieu and M. Nickel. Riemannian continuous normalizing flows. Advances in neural information processing systems, 33:2503-2515, 2020. (Cited on pages 3 and 7.)

G. Mena, A. K. Kuchibhotla, and L. Wasserman. Statistical properties of rectified flow. arXiv preprint arXiv:2511.03193, 2025. (Cited on page 8.)   
B. K. Miller, R. T. Q. Chen, A. Sriram, and B. M. Wood. FlowMM: Generating materials with Riemannian flow matching. In Proceedings of the 41st International Conference on Machine Learning, volume 235, pages 35664-35686, 2024. URL https://proceedings.mlr.press/v235/miller24a.html. (Cited on page 3.)   
S. Roy, A. Rinaldo, and P. Sarkar. Low-Dimensional Adaptation of Rectified Flow: A New Perspective through the Lens of Diffusion and Stochastic Localization. arXiv preprint arXiv:2601.15500, 2026. (Cited on page 4.)   
Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, and B. Poole. Score-based generative modeling through stochastic differential equations. In International Conference on Learning Representations, 2021. URL https://openreview.net/forum?id=PxTIG12RRHS. (Cited on page 3.)   
A. Sriram, B. K. Miller, R. T. Chen, and B. M. Wood. FlowLLM: Flow matching for material generation with large language models as base distributions. Advances in Neural Information Processing Systems, 37:46025-46046, 2024. (Cited on pages 3 and 7.)   
M. Su, J. Y.-C. Hu, S. Pi, and H. Liu. On flow matching kI divergence. arXiv preprint arXiv:2511.05480, 2025. (Cited on page 3.)   
C. Villani. Optimal transport: old and new, volume 338. Springer, 2008. (Cited on page 8.)   
Z. Wan, Q. Wang, G. Mishne, and Y. Wang. Elucidating Flow Matching ODE Dynamics via Data Geometry and Denoisers. In *Forty-second International Conference on Machine Learning*, 2025. URL https://openreview.net/forum?id=f5czhqYK3H. (Cited on page 5.)   
J. Wu, B. Chen, Y. Zhou, Q. Meng, R. Zhu, and Z.-M. Ma. Riemannian Neural Geodesic Interpolant. arXiv preprint arXiv:2504.15736, 2025. (Cited on pages 3 and 19.)   
X. Xu, Z. Zhang, Y. Nakahira, G. Qu, and Y. Chi. Polynomial Convergence of Riemannian Diffusion Models. arXiv preprint arXiv:2601.02499, 2026. (Cited on page 3.)   
D. Yarotsky. Error bounds for approximations with deep ReLU networks. Neural networks, 94: 103-114, 2017. (Cited on page 8.)   
A. Yue, Z. Wang, and H. Xu. ReQFlow: Rectified quaternion flow for efficient and high-quality protein backbone generation. In *Forty-second International Conference on Machine Learning*, 2025. URL https://openreview.net/forum?id=f375uEmYDf. (Cited on pages 3 and 7.)   
Z. Zhou and W. Liu. An Error Analysis of Flow Matching for Deep Generative Modeling. In Forty-second International Conference on Machine Learning, 2025. URL https://openreview.net/forum?id=vES22INUKm. (Cited on pages 3, 10, and 42.)

# A Additional Background for Riemannian Geometry

# A.1 Distances used

Definition A.1 (Total variation distance and $W_{1}$ distance). Let $(M,g)$ be a Riemannian manifold, let $d$ denote the geodesic distance induced by $g$ , and let $\rho_1,\rho_2$ be probability measures on the Borel $\sigma$ -algebra $\mathcal{B}(M)$ .

- The total variation distance between $\rho_{1}$ and $\rho_{2}$ is

$$
\operatorname {T V} \left(\rho_ {1}, \rho_ {2}\right) := \sup  _ {A \in \mathcal {B} (M)} \left| \rho_ {1} (A) - \rho_ {2} (A) \right|.
$$

If $\rho_{1}$ and $\rho_{2}$ are absolutely continuous with respect to the Riemannian volume measure $dV_{g}$ , with densities $p_{1} = \frac{d\rho_{1}}{dV_{g}}$ and $p_{2} = \frac{d\rho_{2}}{dV_{g}}$ , then

$$
\mathrm {T V} \left(\rho_ {1}, \rho_ {2}\right) = \frac {1}{2} \int_ {M} \left| p _ {1} (x) - p _ {2} (x) \right| d V _ {g} (x) = \int_ {\left\{p _ {1} > p _ {2} \right\}} \left(p _ {1} (x) - p _ {2} (x)\right) d V _ {g} (x).
$$

- The 1-Wasserstein distance (induced by $d$ ) is defined for measures with finite first moment (e.g., $\int_{M} d(x_0, x) d\rho_i(x) < \infty$ for some $x_0 \in M$ and $i \in \{1,2\}$ ) by

$$
W _ {1} (\rho_ {1}, \rho_ {2}) := \inf  _ {\gamma \in \Pi (\rho_ {1}, \rho_ {2})} \int_ {M \times M} d (x, y) d \gamma (x, y),
$$

where $\Pi (\rho_1,\rho_2)$ denotes the set of couplings of $(\rho_{1},\rho_{2})$ , i.e., probability measures $\gamma$ on $M\times M$ whose first and second marginals are $\rho_{1}$ and $\rho_{2}$ , respectively.

# A.2 Comparison Theorem

Comparison theorems (Cheeger et al., 1975) will be used frequently throughout the Appendix. For example, we used Rauch theorem in Appendix C.1, which is a key step in proving Lemma 5.2; we also use comparison theorems frequently in Appendix E to verify Assumption 4.

Here we provide a brief introduction to comparison theory, focusing on intuition. Let $k \in \mathbb{R}$ be some constant, and assume we have functions $f, g \geq 0$ defined on $[0, t]$ . If both $f, g$ share the same initial value $f(0) = g(0)$ , and we further assume $f'(0) \leq g'(0)$ . If we know, for second order ODEs, $f'' + \kappa f \leq g'' + \kappa g$ , then we can conclude, at least locally, $f \leq g$ . For more details, see, for example Lezcano-Casado (2020, Lemma 4.8). Such an observation suggests a more general comparison principle, which is the key idea behind comparison theorems in Riemannian geometry. For example, we have the following theorem.

Theorem 3 (Proposition 4.9 in Lezcano-Casado (2020)). Let $M$ be a Riemannian manifold with bounded sectional curvature satisfying $K_{\mathrm{min}} \leq \mathrm{Sec} \leq K_{\mathrm{max}}$ . Let $\gamma : [0, r] \to M$ be a geodesic, and let

$X, Y$ be vector fields along $\gamma$ with $X, Y \perp \gamma'$ satisfying the following ODE ( $X'$ is covariant derivative of $X$ along $\gamma$ ):

$$
X ^ {\prime \prime} + R (X, \gamma^ {\prime}) \gamma^ {\prime} = Y, \qquad X (0) = 0, X ^ {\prime} (0) = 0.
$$

Assume that there exists a continuous function $\eta$ that upper bounds $Y$ : $\| Y\| \leq \eta$ on $[0,r]$ . Then $\rho$ defined as the solution of $\rho '' + K_{\min}\rho = \eta, \rho (0) = 0, \rho '(0) = 0$ upper bounds $X$ : $\| X\| \leq \rho$ .

To summarize, using the comparison principle for ODE, we can make use of curvature information to establish bounds for certain vector fields defined on a Riemannian manifold, as long as the vector field satisfies some specific ODE. For a comprehensive discussion on comparison theorems, see for example Lee (2018) and Cheeger et al. (1975).

# A.3 Riemannian Submanifolds

We briefly introduce some results of Riemannian submanifolds following Lee (2018), and these results will be used in proving Lemma E.15. Let $N \subseteq M$ be a Riemannian submanifold of $M$ , with induced metric. To avoid ambiguity, we denote $\nabla^M$ to be the connection on $M$ , and $\nabla^N$ to be the connection on $N$ . Let $X, Y$ be vector fields on $N$ . We can extend them to vector fields on $M$ , and the covariant derivative $(\nabla^M)_X Y$ can be decomposed as

$$
(\nabla^ {M}) _ {X} Y = ((\nabla^ {M}) _ {X} Y) ^ {\perp} + ((\nabla^ {M}) _ {X} Y) ^ {\parallel}.
$$

The normal component $((\nabla^{M})_{X}Y)^{\perp}$ defines the second fundamental form, which is a map from $\mathfrak{X}(N)\times \mathfrak{X}(N)$ to a section of the normal bundle of $N$ , formally defined as

$$
\Pi (X, Y) := ((\nabla^ {M}) _ {X} Y) ^ {\perp}.
$$

Gauss formula (Lee, 2018, Theorem 8.2) states that, for $X, Y$ being vector fields on $N$ and extended arbitrarily to $M$ , then

$$
(\nabla^ {M}) _ {X} Y = (\nabla^ {N}) _ {X} Y + \mathrm {I I} (X, Y).
$$

A closely related terminology is totally geodesic manifold. $N$ is said to be totally geodesic if every geodesic in $N$ is also a geodesic in $M$ . Furthermore, by Lee (2018, Proposition 8.12), we know the following are equivalent:

- $N$ is a totally geodesic submanifold of $M$ .   
- The second fundamental form of $N$ vanishes identically.   
- Every geodesic in $N$ is also a geodesic in $M$ .

# B Proof of Main Theorem

This Section is organized as follows. We first prove Lemma 5.1 in Appendix B.1, which provides a way to control the propagation of TV distance along ODE simulation:

$$
\frac {\partial \operatorname {T V} (X _ {t} , Y _ {t})}{\partial t} = \int_ {\Omega_ {t}} p (t, x) (\operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) + \langle \operatorname {g r a d} \log p (t, x), \tilde {v} (x, t) - v (x, t) \rangle) d V _ {g} (x).
$$

Note that the time derivative of TV distance consists of two parts:

- We control the the "velocity vector" term $p(t,x) \langle \operatorname{grad} \log p(t,x), \tilde{v}(x,t) - v(x,t) \rangle$ in Appendix B.2.   
- We control the "divergence term" $p(t,x)$ div $(\tilde{v} (x,t) - v(x,t))$ in Appendix B.3.

Moreover, recall that the well-definedness of $\tilde{v}$ depends on the invertibility of $F_{t,h}(x)\coloneqq \mathrm{Exp}_x(h\hat{v} (t,x))$ , which we justify in Appendix B.4. The proof of the main results (sampling error bound in Theorems 1 and 2) is presented in Appendix B.5. Finally, we present proofs for iteration complexity on the hypersphere and SPD manifold in Appendix B.6 and B.7, respectively

Appendix C contains auxiliary results needed in the proofs of Theorems 1 and 2. Finally, Appendix D and E proves the required regularity results needed for proving Propositions 3.1 and 4.1.

# B.1 Proof for Lemma 5.1

We start with the following result.

Theorem 4 (Transport Theorem (Marsden et al., 2002, Theorem 8.1.12)). Let $(M,\mu)$ be a volume manifold and $X$ be a vector field on $M$ with flow $F_{t}$ . For smooth function $f$ defined on $\mathcal{F}(M\times \mathbb{R})$ , let $f_{t}(m) = f(m,t)$ . We have that for any open set $U\subseteq M$ ,

$$
\frac {d}{d t} \int_ {F _ {t} (U)} f _ {t} \mu = \int_ {F _ {t} (U)} \left(\frac {\partial f}{\partial t} + \operatorname {d i v} _ {\mu} \left(f _ {t} X\right)\right) \mu .
$$

Proof. [Proof of Lemma 5.1] We can write

$$
\operatorname {T V} \left(X _ {t}, Y _ {t}\right) = \int_ {\Omega_ {t}} p (t, x) - q (t, x) d V _ {g} (x).
$$

By transport Theorem,

$$
\begin{array}{l} \frac {\partial \operatorname {T V} (X _ {t} , Y _ {t})}{\partial t} = \frac {d}{d t} \int_ {\Omega_ {t}} p (t, x) - q (t, x) d V _ {g} (x) \\ = \int_ {\Omega_ {t}} \left(\frac {\partial (p (t , x) - q (t , x))}{\partial t} + \operatorname {d i v} \left((p (t, x) - q (t, x)) X\right)\right) d V _ {g} (x) \\ = \int_ {\Omega_ {t}} \frac {\partial (p (t , x) - q (t , x))}{\partial t} d V _ {g} (x) + \int_ {\partial \Omega_ {t}} (p (t, x) - q (t, x)) \langle X, n \rangle d V _ {\hat {g}} (x) \\ = \int_ {\Omega_ {t}} \frac {\partial (p (t , x) - q (t , x))}{\partial t} d V _ {g} (x) + \int_ {\partial \Omega_ {t}} 0 \times \langle X, n \rangle d V _ {\hat {g}} (x) \\ = \int_ {\Omega_ {t}} \frac {\partial (p (t , x) - q (t , x))}{\partial t} d V _ {g} (x). \\ \end{array}
$$

The following continuity equation was proved in Wu et al. (2025, Theorem 2). We provide a proof for completeness. For any test function $\varphi$ that is smooth (and of bounded support if the manifold is non-compact and does not have boundary), we have

$$
\begin{array}{l} \int_ {M} \varphi (x) \frac {\partial}{\partial t} p (t, x) d V _ {g} (x) = \frac {d}{d t} \int_ {M} \varphi (x) p (t, x) d V _ {g} (x) = \frac {d}{d t} \mathbb {E} [ \varphi (x _ {t}) ] = \mathbb {E} [ \nabla \varphi (x _ {t}) \circ \frac {d}{d t} x _ {t} ] \\ = \int_ {M} \langle \operatorname {g r a d} \varphi (x), v (x, t) \rangle p (t, x) d V _ {g} (x) \\ \end{array}
$$

$$
= - \int_ {M} \varphi (x) \operatorname {d i v} (v (x, t) p (t, x)) d V _ {g} (x).
$$

Hence we conclude that

$$
\frac {\partial}{\partial t} p (t, x) = - \operatorname {d i v} \left(v (x, t) p (t, x)\right).
$$

Therefore

$$
\begin{array}{l} \frac {\partial \operatorname {T V} (X _ {t} , Y _ {t})}{\partial t} = \int_ {\Omega_ {t}} \frac {\partial (p (t , x) - q (t , x))}{\partial t} d V _ {g} (x) \\ = \int_ {\Omega_ {t}} - \operatorname {d i v} (v (x, t) p (t, x)) + \operatorname {d i v} (\tilde {v} (x, t) q (t, x)) d V _ {g} (x) \\ = \int_ {\partial \Omega_ {t}} - p (t, x) \langle v (x, t), n \rangle + q (t, x) \langle \tilde {v} (x, t), n \rangle d V _ {\hat {g}} (x) \\ = \int_ {\partial \Omega_ {t}} p (t, x) \langle \tilde {v} (x, t) - v (x, t), n \rangle d V _ {\hat {g}} (x) \\ = \int_ {\Omega_ {t}} \operatorname {d i v} \left(\left(\tilde {v} (x, t) - v (x, t)\right) p (t, x)\right) d V _ {g} (x) \\ = \int_ {\Omega_ {t}} p (t, x) \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) + \langle \operatorname {g r a d} p (t, x), \tilde {v} (x, t) - v (x, t) \rangle d V _ {g} (x) \\ = \int_ {\Omega_ {t}} p (t, x) \left(\operatorname {d i v} \left(\tilde {v} (x, t) - v (x, t)\right) + \langle \operatorname {g r a d} \log p (t, x), \tilde {v} (x, t) - v (x, t) \rangle\right) d V _ {g} (x), \\ \end{array}
$$

where observe that $p = q$ on $\partial \Omega_t$ , and the last equality is due to the product rule of divergence. Note that $\operatorname{grad} p(t, x) = p(t, x)$ $\operatorname{grad} \log p(t, x)$ , thereby concluding the proof.

# B.2 Velocity Vector Term

In this section, we bound the velocity vector term. We remark that Lemma B.1 and Lemma B.2 are essentially the same, except that they are under different assumptions.

Lemma B.1. Under Assumption 2 and 3, we can bound

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] \\ \leq \varepsilon \sqrt {2 L _ {t} ^ {s c o r e}} + \left(L _ {t} ^ {s c o r e} (2 (t - t _ {k}) ^ {2} (L _ {t} ^ {\hat {v}, x} L ^ {\hat {v}} + L ^ {v} L _ {t} ^ {\hat {v}, x} + L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}) ^ {2})\right) ^ {\frac {1}{2}}. \\ \end{array}
$$

Proof. Using triangle inequality, we can write

$$
\begin{array}{l} \| \tilde {v} (t, X _ {t}) - v (t, X _ {t}) \| \\ \leq \| P _ {X _ {t}} ^ {X _ {t _ {k}}} \tilde {v} (t, X _ {t}) - \hat {v} (t _ {k}, X _ {t _ {k}}) \| + \| \hat {v} (t _ {k}, X _ {t _ {k}}) - v (t _ {k}, X _ {t _ {k}}) \| + \| v (t _ {k}, X _ {t _ {k}}) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \|. \\ \end{array}
$$

Denote $X_{t\to t_k} = F_{t_k,t - t_k}^{-1}(X_t)$

For the first term above, we have

$$
\begin{array}{l} \| P _ {X _ {t}} ^ {X _ {t _ {k}}} \tilde {v} (t, X _ {t}) - \hat {v} (t _ {k}, X _ {t _ {k}}) \| \\ = \| P _ {X _ {t}} ^ {X _ {t _ {k}}} P _ {X _ {t \rightarrow t _ {k}}} ^ {X _ {t}} \hat {v} \left(t _ {k}, X _ {t \rightarrow t _ {k}}\right) - \hat {v} \left(t _ {k}, X _ {t _ {k}}\right) \| = \| P _ {X _ {t \rightarrow t _ {k}}} ^ {X _ {t}} \hat {v} \left(t _ {k}, X _ {t \rightarrow t _ {k}}\right) - P _ {X _ {t _ {k}}} ^ {X _ {t}} \hat {v} \left(t _ {k}, X _ {t _ {k}}\right) \| \\ \end{array}
$$

$$
\begin{array}{l} \leq \| P _ {X _ {t \rightarrow t _ {k}}} ^ {X _ {t}} \hat {v} (t _ {k}, X _ {t \rightarrow t _ {k}}) - \hat {v} (t _ {k}, X _ {t}) \| + \| \hat {v} (t _ {k}, X _ {t}) - P _ {X _ {t _ {k}}} ^ {X _ {t}} \hat {v} (t _ {k}, X _ {t _ {k}}) \| \\ \leq L _ {t} ^ {\hat {v}, x} d \left(X _ {t \rightarrow t _ {k}}, X _ {t}\right) + L _ {t} ^ {\hat {v}, x} d \left(X _ {t}, X _ {t _ {k}}\right) = L _ {t} ^ {\hat {v}, x} \left(d \left(F _ {t _ {k}, t - t _ {k}} ^ {- 1} (X _ {t}), X _ {t}\right) + d \left(X _ {t}, X _ {t _ {k}}\right)\right), \\ \end{array}
$$

where we used the fact that parallel transport preserve norm.

Note that $X_{t}$ is the trajectory of $X$ at time $t$ . Starting from $X_{t\rightarrow t_k}$ , we have

$$
\operatorname {E x p} _ {X _ {t \rightarrow t _ {k}}} ((t - t _ {k}) \hat {v} (t, X _ {t \rightarrow t _ {k}})) = X _ {t}.
$$

Hence

$$
d \left(F _ {t _ {k}, t - t _ {k}} ^ {- 1} \left(X _ {t}\right), X _ {t}\right) = \left(t - t _ {k}\right) \| \hat {v} \left(t, X _ {t \rightarrow t _ {k}}\right) \| \leq \left(t - t _ {k}\right) L ^ {\hat {v}}.
$$

Also, we know $d(X_{t},X_{t_{k}})$ is the distance of ODE trajectory, hence

$$
d \left(X _ {t}, X _ {t _ {k}}\right) \leq \int_ {t _ {k}} ^ {t} \| v (s, X _ {s}) \| d s \leq \left(t - t _ {k}\right) L ^ {v}.
$$

Now, for the second term, we have by assumption that $\| \hat{v} (t_k,X_{t_k}) - v(t_k,X_{t_k})\| \leq \varepsilon$ . For the third term,

$$
\begin{array}{l} \left\| v \left(t _ {k}, X _ {t _ {k}}\right) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \right\| = \left\| v \left(t _ {k}, X _ {t _ {k}}\right) - v (t, X _ {t _ {k}}) \right\| + \left\| v (t, X _ {t _ {k}}) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \right\| \\ \leq \left(t - t _ {k}\right) L _ {t} ^ {v, t} + d \left(X _ {t}, X _ {t _ {k}}\right) L _ {t} ^ {v, x} \leq \left(t - t _ {k}\right) \left(L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}\right). \\ \end{array}
$$

Putting the above estimates together, we obtain

$$
\begin{array}{l} \left\| \tilde {v} (t, X _ {t}) - v (t, X _ {t}) \right\| ^ {2} \\ \leq \left(\left(t - t _ {k}\right) L _ {t} ^ {\hat {v}, x} \left(L ^ {\hat {v}} + L ^ {v}\right) + \varepsilon + \left(t - t _ {k}\right) \left(L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}\right)\right) ^ {2} \\ \leq 2 \varepsilon^ {2} + 2 (t - t _ {k}) ^ {2} (L _ {t} ^ {\hat {v}, x} L ^ {\hat {v}} + L ^ {v} L _ {t} ^ {\hat {v}, x} + L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}) ^ {2}. \\ \end{array}
$$

Hence

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] \\ \leq \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ \| \tilde {v} (x, t) - v (x, t) \| ^ {2} ] ^ {\frac {1}{2}} \\ \leq \left(L _ {t} ^ {\mathrm {s c o r e}} (2 \varepsilon^ {2} + 2 (t - t _ {k}) ^ {2} \left(L _ {t} ^ {\hat {v}, x} L ^ {\hat {v}} + L ^ {v} L _ {t} ^ {\hat {v}, x} + L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}\right) ^ {2}\right) ^ {\frac {1}{2}} \\ \leq \varepsilon \sqrt {2 L _ {t} ^ {\mathrm {s c o r e}}} + \left(L _ {t} ^ {\mathrm {s c o r e}} (2 (t - t _ {k}) ^ {2} (L _ {t} ^ {\hat {v}, x} L ^ {\hat {v}} + L ^ {v} L _ {t} ^ {\hat {v}, x} + L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}) ^ {2})\right) ^ {\frac {1}{2}}, \\ \end{array}
$$

where note that $\sqrt{\mathbb{E}[A + B]} \leq \sqrt{\mathbb{E}[A]} + \sqrt{\mathbb{E}[B]}$ .

For Hadamard manifolds, when regularity conditions hold in expectation, we have the following result. Note that the proof strategy is essentially the same as the previous case.

Lemma B.2. Under Assumption 4, 5 and 6, we can bound

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] \\ \leq \varepsilon \sqrt {3 L _ {t} ^ {s c o r e}} + \left(L _ {t} ^ {s c o r e} (6 (t - t _ {k}) ^ {2} \left((L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {\hat {v}}) ^ {2} + (L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {v}) ^ {2} + (L _ {t} ^ {v, t}) ^ {2} + (L _ {t} ^ {v}) ^ {2} (L _ {t} ^ {v, x}) ^ {2}\right))\right) ^ {\frac {1}{2}}. \\ \end{array}
$$

Proof. Using triangle inequality, we can write

$$
\begin{array}{l} \| \tilde {v} (t, X _ {t}) - v (t, X _ {t}) \| \\ \leq \| P _ {X _ {t}} ^ {X _ {t _ {k}}} \tilde {v} (t, X _ {t}) - \hat {v} (t _ {k}, X _ {t _ {k}}) \| + \| \hat {v} (t _ {k}, X _ {t _ {k}}) - v (t _ {k}, X _ {t _ {k}}) \| + \| v (t _ {k}, X _ {t _ {k}}) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \|. \\ \end{array}
$$

Hence using Cauchy-Schwarz,

$$
\begin{array}{l} \mathbb {E} [ \| \tilde {v} (t, X _ {t}) - v (t, X _ {t}) \| ^ {2} ] \\ \leq \mathbb {E} [ 3 \| P _ {X _ {t}} ^ {X _ {t _ {k}}} \tilde {v} (t, X _ {t}) - \hat {v} (t _ {k}, X _ {t _ {k}}) \| ^ {2} + 3 \| \hat {v} (t _ {k}, X _ {t _ {k}}) - v (t _ {k}, X _ {t _ {k}}) \| ^ {2} + 3 \| v (t _ {k}, X _ {t _ {k}}) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \| ^ {2} ]. \\ \end{array}
$$

Denote $X_{t\rightarrow t_k} = F_{t_k,t - t_k}^{-1}(X_t)$

For the first term, we have

$$
\begin{array}{l} \mathbb {E} \| P _ {X _ {t}} ^ {X _ {t _ {k}}} \tilde {v} (t, X _ {t}) - \hat {v} \left(t _ {k}, X _ {t _ {k}}\right) \| ^ {2} \\ = \mathbb {E} \| P _ {X _ {t}} ^ {X _ {t _ {k}}} P _ {X _ {t \rightarrow t _ {k}}} ^ {X _ {t}} \hat {v} (t _ {k}, X _ {t \rightarrow t _ {k}}) - \hat {v} (t _ {k}, X _ {t _ {k}}) \| ^ {2} = \mathbb {E} \| P _ {X _ {t \rightarrow t _ {k}}} ^ {X _ {t}} \hat {v} (t _ {k}, X _ {t \rightarrow t _ {k}}) - P _ {X _ {t _ {k}}} ^ {X _ {t}} \hat {v} (t _ {k}, X _ {t _ {k}}) \| ^ {2} \\ \leq 2 \mathbb {E} \left[ \| P _ {X _ {t \rightarrow t _ {k}}} ^ {X _ {t}} \hat {v} \left(t _ {k}, X _ {t \rightarrow t _ {k}}\right) - \hat {v} \left(t _ {k}, X _ {t}\right) \| ^ {2} + 2 \| \hat {v} \left(t _ {k}, X _ {t}\right) - P _ {X _ {t _ {k}}} ^ {X _ {t}} \hat {v} \left(t _ {k}, X _ {t _ {k}}\right) \| ^ {2} \right] \\ \leq 2 \left(L _ {t} ^ {\hat {v}, x}\right) ^ {2} \mathbb {E} \left[ d \left(X _ {t \rightarrow t _ {k}}, X _ {t}\right) ^ {2} \right] + 2 \left(L _ {t} ^ {\hat {v}, x}\right) ^ {2} \mathbb {E} \left[ d \left(X _ {t}, X _ {t _ {k}}\right) ^ {2} \right] \\ = 2 (L _ {t} ^ {\hat {v}, x}) ^ {2} \mathbb {E} \left[ d (F _ {t _ {k}, t - t _ {k}} ^ {- 1} (X _ {t}), X _ {t}) ^ {2} + d (X _ {t}, X _ {t _ {k}}) ^ {2} \right], \\ \end{array}
$$

where we used the fact that parallel transport preserve norm.

Note that $X_{t}$ is the trajectory of $X$ at time $t$ . Starting from $X_{t\rightarrow t_k}$ , we have

$$
\operatorname {E x p} _ {X _ {t \rightarrow t _ {k}}} ((t - t _ {k}) \hat {v} (t, X _ {t \rightarrow t _ {k}})) = X _ {t}.
$$

Hence

$$
\mathbb {E} \left[ d \left(F _ {t _ {k}, t - t _ {k}} ^ {- 1} (X _ {t}), X _ {t}\right) ^ {2} \right] = \mathbb {E} \left[ (t - t _ {k}) ^ {2} \| \hat {v} (t, X _ {t \rightarrow t _ {k}}) \| ^ {2} \right] \leq (t - t _ {k}) ^ {2} \left(L _ {t} ^ {\hat {v}}\right) ^ {2}.
$$

Also, we know $d(X_{t},X_{t_{k}})$ is the distance of ODE trajectory, hence

$$
\begin{array}{l} \mathbb {E} \left[ d \left(X _ {t}, X _ {t _ {k}}\right) ^ {2} \right] \leq \mathbb {E} \left[ \left(\int_ {t _ {k}} ^ {t} \| v (s, X _ {s}) \| d s\right) ^ {2} \right] \leq (t - t _ {k}) \mathbb {E} \left[ \int_ {t _ {k}} ^ {t} \| v (s, X _ {s}) \| ^ {2} d s \right] \\ = (t - t _ {k}) \int_ {t _ {k}} ^ {t} \mathbb {E} [ \| v (s, X _ {s}) \| ^ {2} ] d s \leq (t - t _ {k}) ^ {2} \left(L _ {t} ^ {v}\right) ^ {2}. \\ \end{array}
$$

Now, for the second term, we have

$$
\mathbb {E} \| \hat {v} (t _ {k}, X _ {t _ {k}}) - v (t _ {k}, X _ {t _ {k}}) \| ^ {2} \leq \varepsilon^ {2}.
$$

Finally, for the third term, by swapping the order of the derivative and parallel transport, we get

$$
\left\| v \left(t _ {k}, X _ {t _ {k}}\right) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \right\| \leq \int_ {t _ {k}} ^ {t} \left\| \frac {D}{d s} P _ {X _ {s}} ^ {X _ {t _ {k}}} v (s, X _ {s}) \right\| d s = \int_ {t _ {k}} ^ {t} \left\| \partial_ {s} v (s, X _ {s}) + \nabla_ {\dot {X} _ {s}} v (s, X _ {s}) \right\| d s.
$$

Therefore,

$$
\mathbb {E} \| v (t _ {k}, X _ {t _ {k}}) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \| ^ {2} \leq (t - t _ {k}) \int_ {t _ {k}} ^ {t} \mathbb {E} \bigg \| \partial_ {s} v (s, X _ {s}) + \nabla_ {\dot {X} _ {s}} v (s, X _ {s}) \bigg \| ^ {2} d s.
$$

Notice that

$$
\left\| \partial_ {s} v (s, X _ {s}) + \nabla_ {\dot {X} _ {s}} v (s, X _ {s}) \right\| ^ {2} \lesssim \| \partial_ {s} v (s, X _ {s}) \| ^ {2} + \| \nabla v (s, X _ {s}) \| ^ {2} \| v (s, X _ {s}) \| ^ {2},
$$

so we have

$$
\begin{array}{l} \mathbb {E} \| v (t _ {k}, X _ {t _ {k}}) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \| ^ {2} \leq (t - t _ {k}) \int_ {t _ {k}} ^ {t} \mathbb {E} \left\| \partial_ {s} v (s, X _ {s}) + \nabla_ {\dot {X} _ {s}} v (s, X _ {s}) \right\| ^ {2} d s \\ \lesssim (t - t _ {k}) ^ {2} \mathbb {E} [ \| \partial_ {s} v (s, X _ {s}) \| ^ {2} + \| \nabla v (s, X _ {s}) \| ^ {2} \| v (s, X _ {s}) \| ^ {2} ] \\ \lesssim (t - t _ {k}) ^ {2} \left(\left(L _ {t} ^ {v, t}\right) ^ {2} + \left(L _ {t} ^ {v, x} L _ {t} ^ {v}\right) ^ {2}\right). \\ \end{array}
$$

Putting the above estimates together, we obtain

$$
\begin{array}{l} \mathbb {E} [ \| \tilde {v} (t, X _ {t}) - v (t, X _ {t}) \| ^ {2} ] \\ \leq \mathbb {E} [ 3 \| P _ {X _ {t}} ^ {X _ {t _ {k}}} \tilde {v} (t, X _ {t}) - \hat {v} (t _ {k}, X _ {t _ {k}}) \| ^ {2} + 3 \| \hat {v} (t _ {k}, X _ {t _ {k}}) - v (t _ {k}, X _ {t _ {k}}) \| ^ {2} + 3 \| v (t _ {k}, X _ {t _ {k}}) - P _ {X _ {t}} ^ {X _ {t _ {k}}} v (t, X _ {t}) \| ^ {2} ] \\ \leq 6 \left(L _ {t} ^ {\hat {v}, x}\right) ^ {2} \left(\left(t - t _ {k}\right) ^ {2} \left(L _ {t} ^ {\hat {v}}\right) ^ {2} + \left(t - t _ {k}\right) ^ {2} \left(L _ {t} ^ {v}\right) ^ {2}\right) + 3 \varepsilon^ {2} + 6 \left(t - t _ {k}\right) ^ {2} \left(\left(L _ {t} ^ {v, t}\right) ^ {2} + \left(L _ {t} ^ {v}\right) ^ {2} \left(L _ {t} ^ {v, x}\right) ^ {2}\right) \\ = 6 (t - t _ {k}) ^ {2} \left((L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {\hat {v}}) ^ {2} + (L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {v}) ^ {2} + (L _ {t} ^ {v, t}) ^ {2} + (L _ {t} ^ {v}) ^ {2} (L _ {t} ^ {v, x}) ^ {2}\right) + 3 \varepsilon^ {2}. \\ \end{array}
$$

Hence

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] \\ \leq \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ \| \tilde {v} (x, t) - v (x, t) \| ^ {2} ] ^ {\frac {1}{2}} \\ \leq \Big (L _ {t} ^ {\mathrm {s c o r e}} (6 (t - t _ {k}) ^ {2} \left((L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {\hat {v}}) ^ {2} + (L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {v}) ^ {2} + (L _ {t} ^ {v, t}) ^ {2} + (L _ {t} ^ {v}) ^ {2} (L _ {t} ^ {v, x}) ^ {2}\right) + 3 \varepsilon^ {2}) \Big) ^ {\frac {1}{2}} \\ \leq \varepsilon \sqrt {3 L _ {t} ^ {\mathrm {s c o r e}}} + \Big (L _ {t} ^ {\mathrm {s c o r e}} (6 (t - t _ {k}) ^ {2} \left((L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {\hat {v}}) ^ {2} + (L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {v}) ^ {2} + (L _ {t} ^ {v, t}) ^ {2} + (L _ {t} ^ {v}) ^ {2} (L _ {t} ^ {v, x}) ^ {2}\right)) \Big) ^ {\frac {1}{2}}. \\ \end{array}
$$

# B.3 Divergence Term

In this section, we bound the divergence term. We remark that Lemma B.3 and Lemma B.4 are essentially the same, except that they are under different assumptions.

Denote $z = F_{t_k,t - t_k}^{-1}(x)$ . We know $\mathrm{Exp}_z((t - t_k)\hat{v} (t_k,z)) = x$ . Recall we denote

$$
\tilde {v} (t, x) = P _ {F _ {t _ {k}, t - t _ {k}} ^ {- 1} (x)} ^ {x} \hat {v} (t _ {k}, F _ {t _ {k}, t - t _ {k}} ^ {- 1} (x)),
$$

by simply,

$$
\tilde {v} (x) = P _ {z} ^ {\operatorname {E x p} _ {z} (h \hat {v} (z))} \hat {v} (z)
$$

for notational simplicity.

Lemma B.3. Under Assumption 2 and 3, we have

$$
\mathbb {E} _ {p (t, x)} [ \operatorname {d i v} (\tilde {v} (x, t) - v (t, X _ {t})) ] \leq \varepsilon + (t - t _ {k}) \Big (L _ {t} ^ {\operatorname {d i v}, x} (L ^ {\hat {v}} + 2 L ^ {v}) + L _ {t} ^ {\operatorname {d i v}, t} + L _ {R} (L ^ {\hat {v}}) ^ {2} d \Big).
$$

Proof. By Lemma C.4, we have

$$
\begin{array}{l} \mathbb {E} _ {p (t, x)} [ \operatorname {d i v} (\tilde {v} (x, t) - v (t, X _ {t})) ] \\ \leq \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (t, X _ {t}) | ] + L _ {R} (t - t _ {k}) d \mathbb {E} _ {p (t, x)} [ \| \hat {v} (t _ {k}, z) \| ^ {2} ] \\ \leq \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, z) | ] + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, X _ {t _ {k}}) | ] \\ + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) - \operatorname {d i v} v (t, X _ {t}) | ] + L _ {R} (t - t _ {k}) \left(L ^ {\hat {v}}\right) ^ {2} d. \\ \end{array}
$$

Recall

$$
\begin{array}{l} d \left(F _ {t _ {k}, t - t _ {k}} ^ {- 1} \left(X _ {t}\right), X _ {t}\right) = \left(t - t _ {k}\right) \| \hat {v} (t, X _ {t \rightarrow t _ {k}}) \| \leq \left(t - t _ {k}\right) L ^ {\hat {v}}, \\ d \left(X _ {t}, X _ {t _ {k}}\right) \leq \int_ {t _ {k}} ^ {t} \| v (s, X _ {s}) \| d s \leq (t - t _ {k}) L ^ {v}. \\ \end{array}
$$

For the first term, we simply have

$$
\mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, z) | ] \leq \varepsilon .
$$

For the second term, we have

$$
\begin{array}{l} \mathbb {E} _ {p (t, x)} \left[ \left| \operatorname {d i v} v \left(t _ {k}, z\right) - \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) \right| \right] \leq L _ {t} ^ {\operatorname {d i v}, x} \mathbb {E} _ {p (t, x)} \left[ d \left(z, X _ {t _ {k}}\right) \right] \\ \leq L _ {t} ^ {\operatorname {d i v}, x} \left(\mathbb {E} \left[ d \left(F _ {t _ {k}, t - t _ {k}} ^ {- 1} \left(X _ {t}\right), X _ {t}\right) + d \left(X _ {t}, X _ {t _ {k}}\right) \right]\right) \\ \leq L _ {t} ^ {\operatorname {d i v}, x} (t - t _ {k}) \left(L ^ {\hat {v}} + L ^ {v}\right). \\ \end{array}
$$

Similarly, for the third term,

$$
\begin{array}{l} \mathbb {E} _ {p (t, x)} \left[ | \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) - \operatorname {d i v} v \left(t, X _ {t}\right) | \right] \\ \leq \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) - \operatorname {d i v} v \left(t, X _ {t _ {k}}\right) | ] + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v \left(t, X _ {t _ {k}}\right) - \operatorname {d i v} v \left(t, X _ {t}\right) | ] \\ \leq L _ {t} ^ {\operatorname {d i v}, t} (t - t _ {k}) + L _ {t} ^ {\operatorname {d i v}, x} d \left(X _ {t}, X _ {t _ {k}}\right) \leq (t - t _ {k}) \left(L _ {t} ^ {\operatorname {d i v}, t} + L _ {t} ^ {\operatorname {d i v}, x} L ^ {v}\right). \\ \end{array}
$$

Putting the above estimates together, we obtain

$$
\begin{array}{l} \mathbb {E} _ {p (t, x)} [ \operatorname {d i v} (\tilde {v} (x, t) - v (t, X _ {t})) ] \\ \leq \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, z) | ] + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, X _ {t _ {k}}) | ] \\ + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) - \operatorname {d i v} v (t, X _ {t}) | ] + L _ {R} (t - t _ {k}) \left(L ^ {\hat {v}}\right) ^ {2} d \\ \leq \varepsilon + L _ {t} ^ {\operatorname {d i v}, x} (t - t _ {k}) \left(L ^ {\hat {v}} + L ^ {v}\right) + (t - t _ {k}) \left(L _ {t} ^ {\operatorname {d i v}, t} + L _ {t} ^ {\operatorname {d i v}, x} L ^ {v}\right) + L _ {R} (t - t _ {k}) \left(L ^ {\hat {v}}\right) ^ {2} d \\ \leq \varepsilon + (t - t _ {k}) \left(L _ {t} ^ {\operatorname {d i v}, x} (L ^ {\hat {v}} + 2 L ^ {v}) + L _ {t} ^ {\operatorname {d i v}, t} + L _ {R} (L ^ {\hat {v}}) ^ {2} d\right). \\ \end{array}
$$

Lemma B.4. Under Assumption 4, 5 and 6, we have

$$
\begin{array}{l} \mathbb {E} _ {p (t, x)} [ \operatorname {d i v} (\tilde {v} (x, t) - v (t, X _ {t})) ] \\ \leq 3 \varepsilon + (t - t _ {k}) \Big (L _ {t} ^ {\mathrm {d i v} \hat {v}, x} (L _ {t} ^ {\hat {v}} + L _ {t} ^ {v}) + L _ {t} ^ {\mathrm {d i v}, x} L _ {t} ^ {v} + L _ {t} ^ {\mathrm {d i v}, t} + L _ {R} (L _ {t} ^ {\hat {v}}) ^ {2} d \Big). \\ \end{array}
$$

Proof. By Lemma C.4, we have

$$
\begin{array}{l} \mathbb {E} _ {p (t, x)} [ \operatorname {d i v} (\tilde {v} (x, t) - v (t, X _ {t})) ] \\ \leq \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (t, X _ {t}) | ] + L _ {R} (t - t _ {k}) d \mathbb {E} _ {p (t, x)} [ \| \hat {v} (t _ {k}, z) \| ^ {2} ] \\ \leq \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, z) | ] + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, X _ {t _ {k}}) | ] \\ + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v (t _ {k}, X _ {t _ {k}}) - \operatorname {d i v} v (t, X _ {t}) | ] + L _ {R} (t - t _ {k}) (L ^ {\hat {v}}) ^ {2} d. \\ \end{array}
$$

Recall

$$
\begin{array}{l} \mathbb {E} [ d (F _ {t _ {k}, t - t _ {k}} ^ {- 1} (X _ {t}), X _ {t}) ^ {2} ] \leq (t - t _ {k}) ^ {2} (L _ {t} ^ {\hat {v}}) ^ {2}, \\ \mathbb {E} \left[ d \left(X _ {t}, X _ {t _ {k}}\right) ^ {2} \right] \leq \left(t - t _ {k}\right) ^ {2} \left(L _ {t} ^ {v}\right) ^ {2}. \\ \end{array}
$$

For the first term, we simply have

$$
\mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, z) | ] \leq \varepsilon .
$$

For the second term, by triangle inequality, we have

$$
\begin{array}{l} \left| \operatorname {d i v} v \left(t _ {k}, z\right) - \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) \right| \leq \left| \operatorname {d i v} v \left(t _ {k}, z\right) - \operatorname {d i v} \hat {v} \left(t _ {k}, z\right) \right| \\ + \left| \operatorname {d i v} \hat {v} \left(t _ {k}, z\right) - \operatorname {d i v} \hat {v} \left(t _ {k}, X _ {t _ {k}}\right) \right| \\ + \left| \operatorname {d i v} \hat {v} \left(t _ {k}, X _ {t _ {k}}\right) - \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) \right|. \\ \end{array}
$$

Taking expectation under $p(t,x)$ and using Assumption 6,

$$
\mathbb {E} _ {p (t, x)} \big [ \big | \operatorname {d i v} v (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, X _ {t _ {k}}) \big | \big ] \leq 2 \varepsilon + \mathbb {E} _ {p (t, x)} \big [ \big | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} \hat {v} (t _ {k}, X _ {t _ {k}}) \big | \big ].
$$

Moreover, by the pointwise spatial regularity of $\hat{v}$ (equivalently, a pointwise bound on $\| \operatorname{grad}_x \operatorname{div} \hat{v}(t_k, \cdot) \|$ ), the function $\operatorname{div} \hat{v}(t_k, \cdot)$ is Lipschitz:

$$
\left| \operatorname {d i v} \hat {v} \left(t _ {k}, z\right) - \operatorname {d i v} \hat {v} \left(t _ {k}, X _ {t _ {k}}\right) \right| \leq L _ {t} ^ {\operatorname {d i v} \hat {v}, x} d \left(z, X _ {t _ {k}}\right).
$$

Finally, using $d(z,X_{t_k})\leq d(z,X_t) + d(X_t,X_{t_k})$ and the bounds

$$
\mathbb {E} \left[ d (z, X _ {t}) \right] \leq \left(t - t _ {k}\right) L _ {t} ^ {\hat {v}},
$$

$$
\mathbb {E} \left[ d \left(X _ {t}, X _ {t _ {k}}\right) \right] \leq \left(t - t _ {k}\right) L _ {t} ^ {v},
$$

we obtain

$$
\mathbb {E} _ {p (t, x)} \left[ \left| \operatorname {d i v} v \left(t _ {k}, z\right) - \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) \right| \right] \leq 2 \varepsilon + \left(t - t _ {k}\right) L _ {t} ^ {\operatorname {d i v} \hat {v}, x} \left(L _ {t} ^ {\hat {v}} + L _ {t} ^ {v}\right).
$$

For the third term, by the fundamental theorem of calculus along the curve, we have

$$
\operatorname {d i v} v (t, X _ {t}) - \operatorname {d i v} v (t _ {k}, X _ {t _ {k}}) = \int_ {t _ {k}} ^ {t} \left(\partial_ {s} \operatorname {d i v} v (s, X _ {s}) + \langle \operatorname {g r a d} _ {x} \operatorname {d i v} v (s, X _ {s}), \dot {X} _ {s} \rangle\right) d s.
$$

Equivalently,

$$
\left| \operatorname {d i v} v (t, X _ {t}) - \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) \right| \leq \int_ {t _ {k}} ^ {t} \left| \partial_ {s} (\operatorname {d i v} v) (s, X _ {s}) + \left\langle \operatorname {g r a d} _ {x} \operatorname {d i v} v (s, X _ {s}), v (s, X _ {s}) \right\rangle \right| d s.
$$

Hence we obtain

$$
\mathbb {E} _ {p (t, x)} \left[ \left| \operatorname {d i v} v (t, X _ {t}) - \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) \right| \right]
$$

$$
\begin{array}{l} \leq \mathbb {E} _ {p (t, x)} \left[ \int_ {t _ {k}} ^ {t} | \partial_ {s} (\operatorname {d i v} v) (s, X _ {s}) + \langle \operatorname {g r a d} _ {x} \operatorname {d i v} v (s, X _ {s}), v (s, X _ {s}) \rangle | d s \right] \\ \leq \int_ {t _ {k}} ^ {t} \mathbb {E} _ {p (t, x)} \Big [ | \partial_ {s} (\operatorname {d i v} v) (s, X _ {s}) | + | \langle \operatorname {g r a d} _ {x} \operatorname {d i v} v (s, X _ {s}), v (s, X _ {s}) \rangle | \Big ] d s \\ \lesssim (t - t _ {k}) \left(L _ {t} ^ {\operatorname {d i v}, t} + L _ {t} ^ {\operatorname {d i v}, x} L _ {t} ^ {v}\right). \\ \end{array}
$$

Putting together, the above estimates, we obtain

$$
\begin{array}{l} \mathbb {E} _ {p (t, x)} [ \operatorname {d i v} (\tilde {v} (x, t) - v (t, X _ {t})) ] \\ \leq \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, z) | ] + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v (t _ {k}, z) - \operatorname {d i v} v (t _ {k}, X _ {t _ {k}}) | ] \\ + \mathbb {E} _ {p (t, x)} [ | \operatorname {d i v} v \left(t _ {k}, X _ {t _ {k}}\right) - \operatorname {d i v} v (t, X _ {t}) | ] + L _ {R} (t - t _ {k}) \left(L _ {t} ^ {\hat {v}}\right) ^ {2} d \\ \leq 3 \varepsilon + L _ {t} ^ {\mathrm {d i v} \hat {v}, x} (t - t _ {k}) (L _ {t} ^ {\hat {v}} + L _ {t} ^ {v}) + (t - t _ {k}) (L _ {t} ^ {\mathrm {d i v}, t} + L _ {t} ^ {\mathrm {d i v}, x} L _ {t} ^ {v}) + L _ {R} (t - t _ {k}) (L _ {t} ^ {\hat {v}}) ^ {2} d \\ \leq 3 \varepsilon + (t - t _ {k}) \Big (L _ {t} ^ {\mathrm {d i v} \hat {v}, x} (L _ {t} ^ {\hat {v}} + L _ {t} ^ {v}) + L _ {t} ^ {\mathrm {d i v}, x} L _ {t} ^ {v} + L _ {t} ^ {\mathrm {d i v}, t} + L _ {R} (L _ {t} ^ {\hat {v}}) ^ {2} d \Big). \\ \end{array}
$$

# B.4 Results on Riemannian manifolds

Note that in Lemma 5.1, we do not require vector fields $v, \tilde{v}$ to be the flow matching vector field. To apply the Lemma for analyzing the discretization scheme, we will set $v$ to be the true vector field for flow matching, and $\tilde{v}$ to be corresponds to the learned vector field.

But however, there is a discrepancy between continuous time ODE $dY_{t} = \tilde{v}(t,Y_{t})dt$ and the Euler discretization scheme. Hence, to apply the Lemma to discretization (the actual method in Algorithm 1), we need to define a continuous time interpolation.

Define $F$ as $F_{t,h}(x)\coloneqq \mathrm{Exp}_x(h\hat{v} (t,x))$ . Note that

$$
F _ {t _ {k}, t - t _ {k}} (x _ {k}) = \mathrm {E x p} _ {x _ {k}} ((t - t _ {k}) \hat {v} (t _ {k}, x _ {k}))
$$

corresponds to the continuous time interpolation of Euler discretization. Then we are able to define a interpolation vector field: we want to define

$$
d Y _ {t} = P _ {Y _ {t _ {k}}} ^ {Y _ {t}} \hat {v} (t _ {k}, Y _ {t _ {k}}) d t := \tilde {v} (t, Y _ {t}) d t.
$$

Here we use the question mark to emphasize that $\tilde{v}$ has not yet been proved to be well defined. We want to write the right hand side as a function of $(t,Y_{t}) = (t,F_{t_{k},t - t_{k}}(Y_{t_{k}}))$

Lemma (Restated Lemma 5.2). Let $M$ be simply connected Riemannian manifold that satisfies Assumption 1. Let $b$ be any vector field on $M$ , satisfying $\| b(x) \| \leq B, \forall x \in M$ . Assume $\| \nabla_v b(x) \| \leq L_{\nabla} \| v \|$ . Let $R = \operatorname{inj}(M)$ . To guarantee $F_{t_k, t - t_k}$ being invertible:

1. If $K_{\min} > 0$ , we require

$$
h <   \min \{\frac {R}{B}, \frac {1}{4 L _ {\nabla}}, \sqrt \frac {3}{4 \| b (x) \| ^ {2} L _ {R} (2 + 2 L _ {\nabla} \max \{\frac {1}{\sqrt {K _ {\min}} , 1 \})}} \}.
$$

2. If $K_{\min} < 0$ , we require

$$
h <   \min \{\frac {R}{B}, \frac {1}{4 L _ {\nabla}}, \sqrt {\frac {3}{4 \| b (x) \| ^ {2} L _ {R} (2 \frac {\sinh (\sqrt {- K _ {\min}})}{\sqrt {- K _ {\min}}} + 4 \frac {\cosh (\sqrt {- K _ {\min}}) - 1}{- K _ {\min}} L _ {\nabla})}} \}.
$$

3. If $K_{\min} = 0$ , we require

$$
h <   \min \bigl \{\frac {R}{B}, \frac {1}{4 L _ {\nabla}}, \sqrt {\frac {3}{4 \| b (x) \| ^ {2} L _ {R} (2 + h L _ {\nabla})}} \bigr \}.
$$

Proof. [Proof of Lemma 5.2] For ease of notation, we use $h$ to denote the time step and $b$ to denote the learned vector field, for the map $F$ . That is, for $h \in \mathbb{R}$ and $b \in \mathfrak{X}(M)$ , we write

$$
F _ {h}: M \to M, \qquad F _ {h} (x) := \operatorname {E x p} _ {x} \left(h b (x)\right).
$$

We first compute the derivative of $F$ . Let $x \in M$ and $v \in T_xM$ . Note that $dF_h(x)$ can be viewed as an operator that maps $v \in T_xM$ to $dF_h(x)v \in T_{F_h(x)}M$ . We compute $dF_h(x)v$ . Let $c(s)$ be a smooth curve s.t. $c(0) = x$ and $c'(0) = v$ .

Define a variation through geodesics as

$$
\Lambda : (- \epsilon , \epsilon) \times [ 0, 1 ] \to M, \qquad \Lambda (s, t) := \operatorname {E x p} _ {c (s)} \left(t h b (c (s))\right).
$$

For each fixed $s$ , the $t$ direction is the geodesic starting at $c(s)$ with initial velocity $hb(c(s))$ . In particular, for every $s$ we have

$$
F _ {h} (b (c (s))) = \operatorname {E x p} _ {c (s)} (h b (c (s))) = \Lambda (s, 1).
$$

Now define a vector field $J_{v}$ along the central geodesic $\gamma (t)\coloneqq \Lambda (0,t) = \mathrm{Exp}_x\left(thb(x)\right)$ by

$$
J _ {v} (t) := \partial_ {s} \Lambda (0, t).
$$

Then, by construction (view the left hand side as directional derivative along the curve induced by $v$ ),

$$
d F _ {h} (x) (v) = \frac {d}{d s} F _ {h} (b (c (s))) \Big | _ {s = 0} = \partial_ {s} \Lambda (0, 1) = J _ {v} (1).
$$

This expresses the differential of $F_{h}$ at $x$ applied to $v$ as the value at $t = 1$ of the variation field $J_{v}$ along the geodesic $\gamma$ . Note that $J_{v}$ is a Jacobi field, hence satisfies the Jacobi equation, see Lee (2018, Theorem 10.1). We have initial conditions $J_{v}(0) = v$ , and $D_{t}J_{v}(0) = D_{t}\partial_{s}\Lambda(0,0) = D_{s}\partial_{t}\Lambda(0,0) = h\nabla_{v}b(x) \eqqcolon \omega$ .

Now we analyze conditions that guarantee the invertibility of $F$ . Define

$$
Y (t) = P _ {\gamma (t)} ^ {\gamma (0)} J _ {v} (t).
$$

To show that $dF_{h}(x)$ is invertible, it suffices to show $\inf_v\frac{\|dF_h(x)v\|}{\|v\|} >0$ , equivalently,

$$
\| d F _ {h} (x) v \| = \| P _ {\gamma (1)} ^ {\gamma (0)} J _ {v} (1) \| = \| Y (1) \| \geq C \| v \| > 0, \forall v \neq 0
$$

for some constant $C > 0$ .

Applying Lemma C.5 with $c = \gamma$ and $Y = J_{v}$ , we obtain

$$
Y ^ {\prime} (t) = \frac {d}{d t} \Big (P _ {\gamma (t)} ^ {\gamma (0)} J _ {v} (t) \Big) = P _ {\gamma (t)} ^ {\gamma (0)} D _ {t} J _ {v} (t).
$$

Differentiating once more and using the same lemma with $Y = D_{t}J_{v}$ , we get

$$
Y ^ {\prime \prime} (t) = \frac {d}{d t} \Big (P _ {\gamma (t)} ^ {\gamma (0)} D _ {t} J _ {v} (t) \Big) = P _ {\gamma (t)} ^ {\gamma (0)} D _ {t} ^ {2} J _ {v} (t).
$$

Apply the Jacobi equation $D_t^2 J_v(t) + R(J_v(t), \gamma'(t))\gamma'(t) = 0$ we obtain

$$
Y ^ {\prime \prime} (t) = P _ {\gamma (t)} ^ {\gamma (0)} D _ {t} ^ {2} J _ {v} (t) = - P _ {\gamma (t)} ^ {\gamma (0)} \left(R (J _ {v} (t), \gamma^ {\prime} (t)) \gamma^ {\prime} (t)\right).
$$

Using $J_{v}(t) = P_{\gamma (0)}^{\gamma (t)}Y(t)$ , we rewrite the curvature term and obtain

$$
Y ^ {\prime \prime} (t) + P _ {\gamma (t)} ^ {\gamma (0)} \Big (R \big (P _ {\gamma (0)} ^ {\gamma (t)} Y (t), \gamma^ {\prime} (t) \big) \gamma^ {\prime} (t) \Big) = 0.
$$

Now we apply Taylor's theorem with integral remainder entry-wisely to $Y(t)$ .

$$
\begin{array}{l} Y (t) = Y (0) + t Y ^ {\prime} (0) + \int_ {0} ^ {t} (t - s) Y ^ {\prime \prime} (s) d s \\ = v + t h \nabla_ {v} b (x) - \int_ {0} ^ {t} (t - s) P _ {\gamma (s)} ^ {\gamma (0)} \Bigl (R \bigl (P _ {\gamma (0)} ^ {\gamma (s)} Y (s), \gamma^ {\prime} (s) \bigr) \gamma^ {\prime} (s) \Bigr) d s. \\ \end{array}
$$

In particular, for $t = 1$

$$
Y (1) - v - h \nabla_ {v} b (x) = - \int_ {0} ^ {1} (1 - s) P _ {\gamma (s)} ^ {\gamma (0)} \Big (R \big (P _ {\gamma (0)} ^ {\gamma (s)} Y (s), \gamma^ {\prime} (s) \big) \gamma^ {\prime} (s) \Big) d s.
$$

Since we assumed $\| R(u,v)w\| \leq L_R\| u\| \| v\| \| w\|$ ,

$$
\| R \big (P _ {\gamma (0)} ^ {\gamma (t)} Y (t), \gamma^ {\prime} (t) \big) \gamma^ {\prime} (t) \| \leq L _ {R} \| \gamma^ {\prime} (t) \| ^ {2} \| Y (t) \|.
$$

Taking norms, we get

$$
\begin{array}{l} \| Y (1) - v - h \nabla_ {v} b (x) \| \leq \int_ {0} ^ {1} (1 - s) L _ {R} \| \gamma^ {\prime} (s) \| ^ {2} \| Y (s) \| d s \\ \leq h ^ {2} \| b (x) \| ^ {2} L _ {R} \int_ {0} ^ {1} \| Y (s) \| d s. \\ \end{array}
$$

where note $\| \gamma'(s) \| = h \| b(x) \|$ . We remark that it suffices to upper bound $\int_0^1 \| Y(s) \| ds$ . Then we can simply apply triangle inequality as $\| Y(1) \| \geq \| v + h \nabla_v b(x) \| - \| Y(1) - v - h \nabla_v b(x) \|$ .

Now we bound $\int_0^1\| Y(s)\| ds$ through comparison theory. Since the computation that involves comparison theory is complicated, we summarize them into a separate Lemma, see Lemma C.2.

By Lemma C.2, when $K_{\mathrm{min}} > 0$ , we have

$$
\begin{array}{l} \int_ {0} ^ {1} \| Y (t) \| d t \leq \| v ^ {\|} \| + \| \omega^ {\|} \| + \frac {\| \omega^ {\perp} \|}{\sqrt {K _ {\min}}} + \| v ^ {\perp} \| \leq 2 \| v \| + 2 h \| \nabla_ {v} b (x) \| \max  \left\{\frac {1}{\sqrt {K _ {\min}}}, 1 \right\} \\ \leq \| v \| \left(2 + 2 h L _ {\nabla} \max  \left\{\frac {1}{\sqrt {K _ {\operatorname* {m i n}}}}, 1 \right\}\right) =: C _ {+}, \\ \end{array}
$$

where note that we did orthogonal decomposition on $v,\omega$

$$
\| Y (1) - v - h \nabla_ {v} b (x) \| \leq h ^ {2} \| b (x) \| ^ {2} L _ {R} C _ {+}.
$$

By triangle inequality,

$$
\begin{array}{l} \| Y (1) \| \geq \| v + h \nabla_ {v} b (x) \| - \| Y (1) - v - h \nabla_ {v} b (x) \| \\ \geq \| v \| - h \| \nabla_ {v} b (x) \| - h ^ {2} \| b (x) \| ^ {2} L _ {R} C _ {+} \\ \geq \| v \| \left(1 - h L _ {\nabla} - h ^ {2} \| b (x) \| ^ {2} L _ {R} \left(2 + 2 h L _ {\nabla} \max  \left\{\frac {1}{\sqrt {K _ {\operatorname* {m i n}}}}, 1 \right\}\right)\right). \\ \end{array}
$$

Clearly $h < 1$ is required, so we only need to find $h$ s.t.

$$
\begin{array}{l} 1 - h L _ {\nabla} > h ^ {2} \| b (x) \| ^ {2} L _ {R} (2 + 2 L _ {\nabla} \max \{\frac {1}{\sqrt {K _ {\mathrm {m i n}}}}, 1 \}) \\ > h ^ {2} \| b (x) \| ^ {2} L _ {R} (2 + 2 h L _ {\nabla} \max \{\frac {1}{\sqrt {K _ {\mathrm {m i n}}}}, 1 \}). \\ \end{array}
$$

If $h \leq \frac{1}{4L_{\nabla}}$ , then $1 - hL_{\nabla} \geq \frac{3}{4}$ . The value $h \leq \sqrt{\frac{3}{4\|b(x)\|^2L_R(2 + 2L_{\nabla}\max\{\frac{1}{\sqrt{K_{\min}}},1\})}}$ suffices.

When $K_{\mathrm{min}} < 0$ , we have

$$
\begin{array}{l} \int_ {0} ^ {1} \| Y (t) \| d t \leq \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| + \frac {\cosh (\sqrt {- K _ {\operatorname* {m i n}}}) - 1}{- K _ {\operatorname* {m i n}}} \| \omega^ {\perp} \| + \frac {\sinh (\sqrt {- K _ {\operatorname* {m i n}}})}{\sqrt {- K _ {\operatorname* {m i n}}}} \| v ^ {\perp} \| \\ \leq \| v \| \left(2 \frac {\sinh (\sqrt {- K _ {\operatorname* {m i n}}})}{\sqrt {- K _ {\operatorname* {m i n}}}} + 4 \frac {\cosh (\sqrt {- K _ {\operatorname* {m i n}}}) - 1}{- K _ {\operatorname* {m i n}}} h L _ {\nabla}\right) =: C _ {-}. \\ \end{array}
$$

Then we have

$$
\| Y (1) - v - h \nabla_ {v} b (x) \| \leq h ^ {2} \| b (x) \| ^ {2} L _ {R} C _ {-}.
$$

By triangle inequality,

$$
\begin{array}{l} \| Y (1) \| \geq \| v + h \nabla_ {v} b (x) \| - \| Y (1) - v - h \nabla_ {v} b (x) \| \\ \geq \| v \| - h \| \nabla_ {v} b (x) \| - h ^ {2} \| b (x) \| ^ {2} L _ {R} C _ {-} \\ \geq \| v \| \left(1 - h L _ {\nabla} - h ^ {2} \| b (x) \| ^ {2} L _ {R} \left(2 \frac {\sinh \left(\sqrt {- K _ {\operatorname* {m i n}}}\right)}{\sqrt {- K _ {\operatorname* {m i n}}}} + 4 \frac {\cosh \left(\sqrt {- K _ {\operatorname* {m i n}}}\right) - 1}{- K _ {\operatorname* {m i n}}} h L _ {\nabla}\right)\right). \\ \end{array}
$$

Cleraly $h < 1$ is required, so we only need to find $h$ s.t.

$$
\begin{array}{l} 1 - h L _ {\nabla} > h ^ {2} \| b (x) \| ^ {2} L _ {R} \left(2 \frac {\sinh \left(\sqrt {- K _ {\operatorname* {m i n}}}\right)}{\sqrt {- K _ {\operatorname* {m i n}}}} + 4 \frac {\cosh \left(\sqrt {- K _ {\operatorname* {m i n}}}\right) - 1}{- K _ {\operatorname* {m i n}}} L _ {\nabla}\right) \\ > h ^ {2} \| b (x) \| ^ {2} L _ {R} \left(2 \frac {\sinh \left(\sqrt {- K _ {\operatorname* {m i n}}}\right)}{\sqrt {- K _ {\operatorname* {m i n}}}} + 4 \frac {\cosh \left(\sqrt {- K _ {\operatorname* {m i n}}}\right) - 1}{- K _ {\operatorname* {m i n}}} h L _ {\nabla}\right). \\ \end{array}
$$

If $h \leq \frac{1}{4L_{\nabla}}$ , then $1 - hL_{\nabla} \geq \frac{3}{4}$ . The value $h \leq \sqrt{\frac{3}{4\|b(x)\|^2L_R(2\frac{\sinh(\sqrt{-K_{\min}})}{\sqrt{-K_{\min}}} + 4\frac{\cosh(\sqrt{-K_{\min}}) - 1}{-K_{\min}}L_{\nabla})}}$ suffices.

When $K_{\min} = 0$ , we have

$$
\begin{array}{l} \int_ {0} ^ {1} \| Y (t) \| d t \leq \| v ^ {\parallel} \| + \frac {1}{2} \| \omega^ {\parallel} \| + \frac {1}{2} \| \omega^ {\perp} \| + \| v ^ {\perp} \| \\ \leq \| v \| (2 + h L _ {\nabla}) =: C _ {=} \\ \end{array}
$$

Then we have

$$
\| Y (1) - v - h \nabla_ {v} b (x) \| \leq h ^ {2} \| b (x) \| ^ {2} L _ {R} C _ {=}
$$

By triangle inequality,

$$
\begin{array}{l} \| Y (1) \| \geq \| v + h \nabla_ {v} b (x) \| - \| Y (1) - v - h \nabla_ {v} b (x) \| \\ \geq \| v \| - h \| \nabla_ {v} b (x) \| - h ^ {2} \| b (x) \| ^ {2} L _ {R} C = \\ \geq \left\| v \right\| \left(1 - h L _ {\nabla} - h ^ {2} \| b (x) \| ^ {2} L _ {R} (2 + h L _ {\nabla})\right). \\ \end{array}
$$

Cleraly $h < 1$ is required, so we only need to find $h$ s.t.

$$
1 - h L _ {\nabla} > h ^ {2} \| b (x) \| ^ {2} L _ {R} (2 + L _ {\nabla}) > h ^ {2} \| b (x) \| ^ {2} L _ {R} (2 + h L _ {\nabla}).
$$

If $h \leq \frac{1}{4L_{\nabla}}$ , then $1 - hL_{\nabla} \geq \frac{3}{4}$ . The value $h \leq \sqrt{\frac{3}{4\|b(x)\|^2L_R(2 + hL_{\nabla})}}$ suffices.

![](images/d3782907d297ac7325b213c0b008986a7c530030cd312a43816ebf7101a10d49.jpg)

# B.5 Main Theorem

Now we prove our main theorem. We remark that the proof of Theorem 1 and 2 are essentially the same.

Proof. [Proof of Theorem 1] By Lemma 5.1, we have

$$
\begin{array}{l} \operatorname {T V} \left(\pi_ {T}, \hat {\pi} _ {T}\right) = \operatorname {T V} \left(\pi_ {t _ {N}}, \hat {\pi} _ {t _ {N}}\right) \\ \leq \operatorname {T V} \left(\pi_ {t _ {0}}, \hat {\pi} _ {t _ {0}}\right) + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ \langle \operatorname {g r a d} \log p (t, x), \tilde {v} (x, t) - v (x, t) \rangle ] d t + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | ] d t \\ \leq \operatorname {T V} \left(\pi_ {t _ {0}}, \hat {\pi} _ {t _ {0}}\right) + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] d t + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | ] d t, \\ \end{array}
$$

where $\pi_t, \hat{\pi}_t$ denote the law for $X_t, Y_t$ respectively.

Notice that

$$
\int_ {t _ {k}} ^ {t _ {k + 1}} \left(t - t _ {k}\right) d t = \left(\frac {1}{2} t ^ {2} - t t _ {k}\right) \big | _ {t _ {k}} ^ {t _ {k + 1}} = \frac {1}{2} t _ {k + 1} ^ {2} - \frac {1}{2} t _ {k} ^ {2} - t _ {k} \left(t _ {k + 1} - t _ {k}\right) = \frac {1}{2} \left(t _ {k + 1} - t _ {k}\right) ^ {2}. \tag {11}
$$

Hence using constant step size for discretization, we obtain

$$
\begin{array}{l} \operatorname {T V} \left(\pi_ {T}, \hat {\pi} _ {T}\right) = \operatorname {T V} \left(X _ {t _ {N}}, Y _ {t _ {N}}\right) \\ \leq \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] d t + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | ] d t \\ \leq \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + \frac {1}{2} N h ^ {2} \left(\sqrt {2 L _ {t} ^ {\text {s c o r e}}} \left(L _ {t} ^ {\hat {v}, x} L ^ {\hat {v}} + L ^ {v} L _ {t} ^ {\hat {v}, x} + L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}\right) \right. \\ \left. + L _ {t} ^ {\mathrm {d i v}, x} \left(L ^ {\hat {v}} + 2 L ^ {v}\right) + L _ {t} ^ {\mathrm {d i v}, t} + L _ {R} \left(L ^ {\hat {v}}\right) ^ {2} d\right) + N h \left(\varepsilon \sqrt {2 L _ {t} ^ {\mathrm {s c o r e}}} + \varepsilon\right) \\ \leq \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + h \left(\sqrt {L _ {t} ^ {\text {s c o r e}}} \left(L _ {t} ^ {\hat {v}, x} L ^ {\hat {v}} + L ^ {v} L _ {t} ^ {\hat {v}, x} + L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}\right) \right. \\ \left. + L _ {t} ^ {\mathrm {d i v}, x} \left(L ^ {\hat {v}} + 2 L ^ {v}\right) + L _ {t} ^ {\mathrm {d i v}, t} + L _ {R} \left(L ^ {\hat {v}}\right) ^ {2} d\right) + (\varepsilon \sqrt {2 L _ {t} ^ {\mathrm {s c o r e}}} + \varepsilon). \\ = \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + h C _ {\text {L i p}} + \varepsilon C _ {\text {e p s}}, \\ \end{array}
$$

where note that $Nh < 1$ and we compute

$$
\begin{array}{l} \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} ((L _ {t} ^ {v, x} + \varepsilon) (L ^ {v} + \varepsilon) + L ^ {v} (L _ {t} ^ {v, x} + \varepsilon) + L _ {t} ^ {v, t} + L ^ {v} L _ {t} ^ {v, x}) \\ + L _ {t} ^ {\operatorname {d i v}, x} \left(3 L ^ {v} + \varepsilon\right) + L _ {t} ^ {\operatorname {d i v}, t} + L _ {R} \left(L ^ {v} + \varepsilon\right) ^ {2} d \\ = \varepsilon^ {2} (\sqrt {L _ {t} ^ {\mathrm {s c o r e}}} + L _ {R} d) + \varepsilon (2 \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} L ^ {v} + \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} L _ {t} ^ {v, x} + L _ {t} ^ {\mathrm {d i v}, x} + 2 L _ {R} d L ^ {v}) \\ + 3 \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} L _ {t} ^ {v, x} L ^ {v} + \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} L _ {t} ^ {v, t} + 3 L ^ {v} L _ {t} ^ {\mathrm {d i v}, x} + L _ {t} ^ {\mathrm {d i v}, t} + L _ {R} (L ^ {v}) ^ {2} d, \\ \end{array}
$$

and denote

$$
\begin{array}{l} \mathsf {C} _ {\mathrm {L i p}} := 3 \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} L _ {t} ^ {v, x} L ^ {v} + \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} L _ {t} ^ {v, t} + 3 L ^ {v} L _ {t} ^ {\mathrm {d i v}, x} + L _ {t} ^ {\mathrm {d i v}, t} + L _ {R} (L ^ {v}) ^ {2} d, \\ C _ {\mathrm {e p s}} := \sqrt {2 L _ {t} ^ {\mathrm {s c o r e}}} + 1 + 2 \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} L ^ {v} + \sqrt {L _ {t} ^ {\mathrm {s c o r e}}} L _ {t} ^ {v, x} + L _ {t} ^ {\mathrm {d i v}, x} + 2 L _ {R} d L ^ {v} + \varepsilon (\sqrt {L _ {t} ^ {\mathrm {s c o r e}}} + L _ {R} d). \\ \end{array}
$$

![](images/80340d12f884db8326c1103a0247b1d2f897439d99215db3cb4d8a01fd751a85.jpg)

Proof. [Proof of Theorem 2] We have that

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] \\ \leq \varepsilon \sqrt {3 L _ {t} ^ {\mathrm {s c o r e}}} + (t - t _ {k}) \Bigg (6 L _ {t} ^ {\mathrm {s c o r e}} \left((L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {\hat {v}}) ^ {2} + (L _ {t} ^ {\hat {v}, x}) ^ {2} (L _ {t} ^ {v}) ^ {2} + (L _ {t} ^ {v, t}) ^ {2} + (L _ {t} ^ {v}) ^ {2} (L _ {t} ^ {v, x}) ^ {2}\right) \Bigg) ^ {\frac {1}{2}}, \\ \end{array}
$$

and

$$
\mathbb {E} _ {p (t, x)} [ \mathrm {d i v} (\tilde {v} (x, t) - v (t, X _ {t})) ] \leq 3 \varepsilon + (t - t _ {k}) \Big (L _ {t} ^ {\mathrm {d i v} \hat {v}, x} (L _ {t} ^ {\hat {v}} + L _ {t} ^ {v}) + L _ {t} ^ {\mathrm {d i v}, x} L _ {t} ^ {v} + L _ {t} ^ {\mathrm {d i v}, t} + L _ {R} (L _ {t} ^ {\hat {v}}) ^ {2} d \Big).
$$

Also recall

$$
\begin{array}{l} \mathrm {T V} \left(\pi_ {T}, \hat {\pi} _ {T}\right) = \mathrm {T V} \left(\pi_ {t _ {N}}, \hat {\pi} _ {t _ {N}}\right) \\ \leq \operatorname {T V} \left(\pi_ {t _ {0}}, \hat {\pi} _ {t _ {0}}\right) + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ \langle \operatorname {g r a d} \log p (t, x), \tilde {v} (x, t) - v (x, t) \rangle ] d t + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | ] d t \\ \leq \operatorname {T V} \left(\pi_ {t _ {0}}, \hat {\pi} _ {t _ {0}}\right) + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] d t + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | ] d t. \\ \end{array}
$$

Notice that

$$
\int_ {t _ {k}} ^ {t _ {k + 1}} (t - t _ {k}) d t = \left(\frac {1}{2} t ^ {2} - t t _ {k}\right) \big | _ {t _ {k}} ^ {t _ {k + 1}} = \frac {1}{2} t _ {k + 1} ^ {2} - \frac {1}{2} t _ {k} ^ {2} - t _ {k} (t _ {k + 1} - t _ {k}) = \frac {1}{2} (t _ {k + 1} - t _ {k}) ^ {2}. \tag {12}
$$

Hence using constant step size for discretization, we obtain

$$
\begin{array}{l} \mathrm {T V} (\pi_ {T}, \hat {\pi} _ {T}) \\ \leq \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] d t + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | ] d t \\ \leq \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + \frac {1}{2} N h ^ {2} \left(\sqrt {6 L _ {t} ^ {\text {s c o r e}}} \left(\left(L _ {t} ^ {\hat {v}, x}\right) ^ {2} \left(L _ {t} ^ {\hat {v}}\right) ^ {2} + \left(L _ {t} ^ {\hat {v}, x}\right) ^ {2} \left(L _ {t} ^ {v}\right) ^ {2} + \left(L _ {t} ^ {v, t}\right) ^ {2} + \left(L _ {t} ^ {v}\right) ^ {2} \left(L _ {t} ^ {v, x}\right) ^ {2}\right) \right. \\ \left. + \left(L _ {t} ^ {\operatorname {d i v} \hat {v}, x} \left(L _ {t} ^ {\hat {v}} + L _ {t} ^ {v}\right) + L _ {t} ^ {\operatorname {d i v}, x} L _ {t} ^ {v} + L _ {t} ^ {\operatorname {d i v}, t} + L _ {R} \left(L _ {t} ^ {\hat {v}}\right) ^ {2} d\right)\right) + N h \left(\varepsilon \sqrt {2 L _ {t} ^ {\mathrm {s c o r e}}} + 3 \varepsilon\right) \tag {13} \\ \leq \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + h C _ {\text {L i p}} + \varepsilon C _ {\text {e p s}, 1}, \\ \end{array}
$$

where note that $Nh < 1$ . Take $t_0 = 0$ , $t_N = T < 1$ , we obtain

$$
\operatorname {T V} \left(\pi_ {T}, \hat {\pi} _ {T}\right) \leq h C _ {\text {L i p}} + \varepsilon C _ {\text {e p s , 1}}.
$$

# B.6 Example: Hypersphere

For compact manifolds, under uniform estimation error (Assumption 3, we can establish the regularity for $\hat{v}$ . In particular, under Assumption 3 and Assumption 2, since $\| \nabla \hat{v} (x)\|_{\mathrm{op}} = \| \nabla \hat{v} (x) - \nabla v(x) + \nabla v(x)\|_{\mathrm{op}}$ , we have

1. $\| \hat{v} (t,x)\| \leq L^{\hat{v}} = L^{v} + \varepsilon$   
2. $\hat{v}(t,x)$ is Lipschitz in $x$ variable with $L_t^{\hat{v},x} = L_t^{v,x} + \varepsilon$ .

Lemma B.5. On $S^d$ , Assumption 2 holds with the following constants.

1. $L_{t}^{v,x} = \frac{12\pi M_{1}(d - 1)}{m_{1}(1 - t)}$ , $L_{t}^{\hat{v},x} = \varepsilon + \frac{12\pi M_{1}(d - 1)}{m_{1}(1 - t)}$ .   
2. $L_{t}^{v,t}\coloneqq \frac{8\pi^{2}d}{1 - t}\frac{M_{1}}{m_{1}}.$   
3. $L_{t}^{\mathrm{div},x}\coloneqq \frac{128\pi(d - 1)^{2}}{(1 - t)^{3}}\frac{M_{1}}{m_{1}}.$   
4. $L_{t}^{\mathrm{div},t} \coloneqq \frac{128\pi^{2}(d - 1)^{2}}{(1 - t)^{3}} \frac{M_{1}}{m_{1}}.$   
5. $L_{t}^{score} \coloneqq \frac{8(d - 1)^{2}}{(1 - t)^{2}}\frac{M_{1}}{m_{1}}.$   
6. $L^v = \pi$   
7. $L_{R} = 1$

As the proof is technical, we defer it to Appendix D.

Now we prove Proposition 3.1. Proof. [Proof of Proposition 3.1] We first recall the extra condition on $h$ imposed by Lemma 5.2:

$$
h <   \min \{\frac {R}{\| b (x) \|}, \frac {1}{4 L _ {\nabla}}, \sqrt {\frac {3}{4 \| b (x) \| ^ {2} L _ {R} (2 + 2 L _ {\nabla} \max \{\frac {1}{\sqrt {K _ {\mathrm {m i n}}}} , 1 \})}} \}.
$$

Since $\| \hat{v}(t,x) \| \leq L^{\hat{v}} = L^{v} + \varepsilon$ , we know $\| b(x) \|$ is of constant order, consequently $\frac{R}{\|b(x)\|}$ is of constant order. Thus such an condition is dominated by the term $\frac{1}{L_{\nabla}}$ , which in our case is exactly $\frac{1}{L_t^{\hat{v},x}}$ . Plug in constants in Lemma B.5, we obtain

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] \\ \leq \varepsilon \sqrt {2 \frac {8 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}} + (t - t _ {k}) \left(\frac {8 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} (2 ((\varepsilon + \frac {1 2 \pi M _ {1} (d - 1)}{m _ {1} (1 - t)}) (\pi + \varepsilon) \right. \\ + \pi (\varepsilon + \frac {1 2 \pi M _ {1} (d - 1)}{m _ {1} (1 - t)}) + \frac {8 \pi^ {2} d}{1 - t} \frac {M _ {1}}{m _ {1}} + \pi \frac {1 2 \pi M _ {1} (d - 1)}{m _ {1} (1 - t)} ^ {2}) \bigg) ^ {\frac {1}{2}} \\ \leq 4 \varepsilon \frac {d - 1}{1 - t} \sqrt {\frac {M _ {1}}{m _ {1}}} + (t - t _ {k}) 4 \frac {d - 1}{1 - t} \sqrt {\frac {M _ {1}}{m _ {1}}} \big ((\varepsilon + \frac {1 2 \pi M _ {1} (d - 1)}{m _ {1} (1 - t)}) (\pi + \varepsilon) \\ + \pi (\varepsilon + \frac {1 2 \pi M _ {1} (d - 1)}{m _ {1} (1 - t)}) + \frac {8 \pi^ {2} d}{1 - t} \frac {M _ {1}}{m _ {1}} + \pi \frac {1 2 \pi M _ {1} (d - 1)}{m _ {1} (1 - t)}) \\ \lesssim \varepsilon \frac {d - 1}{1 - t} \Big (\frac {M _ {1}}{m _ {1}} \Big) ^ {\frac {1}{2}} + (t - t _ {k}) \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} \Big (\frac {M _ {1}}{m _ {1}} \Big) ^ {\frac {3}{2}}. \\ \end{array}
$$

And similarly,

$$
\begin{array}{l} \mathbb {E} _ {p (t, x)} [ \operatorname {d i v} (\tilde {v} (x, t) - v (t, X _ {t})) ] \leq \varepsilon + (t - t _ {k}) \Big (L _ {t} ^ {\operatorname {d i v}, x} (L ^ {\hat {v}} + 2 L ^ {v}) + L _ {t} ^ {\operatorname {d i v}, t} + L _ {R} (L ^ {\hat {v}}) ^ {2} d \Big) \\ \leq \varepsilon + (t - t _ {k}) \Big (\frac {1 2 8 \pi (d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}} (3 \pi + \varepsilon) + \frac {1 2 8 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}} + (\pi + \varepsilon) ^ {2} d \Big) \\ \lesssim \varepsilon + (t - t _ {k}) \Big (\frac {(d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}} + d \Big). \\ \end{array}
$$

With early stopping, we terminate the sampling algorithm (Algorithm 1) at time $T < 1$ (i.e., $t_0 = 0, t_N = T$ )

$$
\begin{array}{l} \operatorname {T V} \left(\pi_ {T}, \hat {\pi} _ {T}\right) = \operatorname {T V} \left(X _ {t _ {N}}, Y _ {t _ {N}}\right) \\ \leq \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ \| \operatorname {g r a d} \log p (t, x) \| \cdot \| \tilde {v} (x, t) - v (x, t) \| ] d t + \int_ {t _ {0}} ^ {t _ {N}} \mathbb {E} [ | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | ] d t \\ \lesssim \sum_ {i = 0} ^ {N - 1} \int_ {t _ {i}} ^ {t _ {i + 1}} \varepsilon \frac {d - 1}{1 - t} \left(\frac {M _ {1}}{m _ {1}}\right) ^ {\frac {1}{2}} + (t - t _ {i}) \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} \left(\frac {M _ {1}}{m _ {1}}\right) ^ {\frac {3}{2}} d t + \sum_ {i = 0} ^ {N - 1} \int_ {t _ {i}} ^ {t _ {i + 1}} \varepsilon + (t - t _ {i}) \left(\frac {(d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}} + d\right) d t \\ \lesssim \left(\frac {M _ {1}}{m _ {1}}\right) ^ {\frac {1}{2}} (d - 1) \varepsilon \sum_ {i = 0} ^ {N - 1} \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {1}{1 - t} d t + \left(\frac {M _ {1}}{m _ {1}}\right) ^ {\frac {3}{2}} (d - 1) ^ {2} \sum_ {i = 0} ^ {N - 1} \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {t - t _ {i}}{(1 - t) ^ {3}} d t. \\ \end{array}
$$

We first discuss the case of constant step size. Using

$$
\sum_ {i = 0} ^ {N - 1} \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {1}{1 - t} d t = - \log (1 - t _ {N})
$$

and (using $s\coloneqq 1 - t$ so that $ds = -dt$ )

$$
\begin{array}{l} \sum_ {i = 0} ^ {N - 1} \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {t - t _ {i}}{(1 - t) ^ {3}} d t \leq h \sum_ {i = 0} ^ {N - 1} \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {1}{(1 - t) ^ {3}} d t = h \sum_ {i = 0} ^ {N - 1} \int_ {1 - t _ {i + 1}} ^ {1 - t _ {i}} \frac {1}{s ^ {3}} \\ = h \sum_ {i = 0} ^ {N - 1} - \frac {1}{(1 - t _ {i}) ^ {2}} + \frac {1}{(1 - t _ {i + 1}) ^ {2}} \lesssim h \frac {1}{(1 - T) ^ {2}}, \\ \end{array}
$$

we can finally bound the error as

$$
\varepsilon \Big (\frac {M _ {1}}{m _ {1}} \Big) ^ {\frac {1}{2}} (d - 1) \log (\frac {1}{1 - T}) + h \Big (\frac {M _ {1}}{m _ {1}} \Big) ^ {\frac {3}{2}} (d - 1) ^ {2} \frac {1}{(1 - T) ^ {2}}.
$$

Now we have

$$
\operatorname {T V} \left(X _ {T}, Y _ {T}\right) \lesssim \varepsilon \left(\frac {M _ {1}}{m _ {1}}\right) ^ {\frac {1}{2}} (d - 1) \log \left(\frac {1}{1 - T}\right) + h \left(\frac {M _ {1}}{m _ {1}}\right) ^ {\frac {3}{2}} (d - 1) ^ {2} \frac {1}{(1 - T) ^ {2}}.
$$

To obtain a sample up to $\varepsilon_{\mathrm{target}}$ accuracy, we assume $\varepsilon$ is sufficiently small. Then we need

$$
h \left(\frac {M _ {1}}{m _ {1}}\right) ^ {\frac {3}{2}} (d - 1) ^ {2} \frac {1}{(1 - T) ^ {2}} = \mathcal {O} (\varepsilon_ {\mathrm {t a r g e t}}),
$$

which means

$$
h = \frac {\varepsilon_ {\text {t a r g e t}} (1 - T) ^ {2}}{(d - 1) ^ {2}} \left(\frac {m _ {1}}{M _ {1}}\right) ^ {\frac {3}{2}}. \tag {14}
$$

Next, we discuss a specific step size schedule that can improve the dependency on $\frac{1}{1 - T}$ . Denote $h_k = t_{k+1} - t_k$ . Then

$$
\begin{array}{l} \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {1 - t _ {i}}{(1 - t) ^ {3}} d t = \frac {1}{2} (1 - t _ {i}) (\frac {1}{(1 - t _ {i + 1}) ^ {2}} - \frac {1}{(1 - t _ {i}) ^ {2}}) = \frac {1}{2} (1 - t _ {i}) (\frac {t _ {i} ^ {2} - 2 t _ {i} - t _ {i + 1} ^ {2} + 2 t _ {i + 1}}{(1 - t _ {i + 1}) ^ {2} (1 - t _ {i}) ^ {2}}) \\ = \frac {1}{2} (1 - t _ {i}) \frac {(t _ {i + 1} - t _ {i}) (2 - t _ {i} - t _ {i + 1})}{(1 - t _ {i + 1}) ^ {2} (1 - t _ {i}) ^ {2}} = \frac {1}{2} (1 - t _ {i}) h _ {i} \frac {2 - t _ {i} - t _ {i + 1}}{(1 - t _ {i + 1}) ^ {2} (1 - t _ {i}) ^ {2}}, \\ \end{array}
$$

$$
\int_ {t _ {i}} ^ {t _ {i + 1}} \frac {t - 1}{(1 - t) ^ {3}} d t = - \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {1}{(1 - t) ^ {2}} d t = \frac {1}{1 - t _ {i}} - \frac {1}{1 - t _ {i + 1}} = - \frac {h _ {i}}{(1 - t _ {i + 1}) (1 - t _ {i})}.
$$

Together,

$$
\begin{array}{l} \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {t - t _ {i}}{(1 - t) ^ {3}} d t = \frac {1}{2} (1 - t _ {i}) h _ {i} \frac {2 - t _ {i} - t _ {i + 1}}{(1 - t _ {i + 1}) ^ {2} (1 - t _ {i}) ^ {2}} - \frac {h _ {i}}{(1 - t _ {i + 1}) (1 - t _ {i})} \\ = \frac {h _ {i}}{(1 - t _ {i + 1}) (1 - t _ {i})} (- 1 + \frac {1}{2} \frac {2 - t _ {i} - t _ {i + 1}}{(1 - t _ {i + 1})}) \\ = \frac {h _ {i} ^ {2}}{2 (1 - t _ {i + 1}) ^ {2} (1 - t _ {i})} \lesssim \frac {h _ {i} ^ {2}}{(1 - t _ {i + 1}) ^ {3}}. \\ \end{array}
$$

Now we want to control

$$
\sum_ {i = 0} ^ {N - 1} \int_ {t _ {i}} ^ {t _ {i + 1}} \frac {t - t _ {i}}{(1 - t) ^ {3}} d t \lesssim \sum_ {i = 0} ^ {N - 1} \frac {h _ {i} ^ {2}}{(1 - t _ {i + 1}) ^ {3}}.
$$

With $t_i = 1 - \frac{1}{(1 + \eta i)^2}$ . Then $h_i = \frac{1}{(1 + \eta i)^2} - \frac{1}{(1 + \eta(i + 1))^2} = \frac{\eta(2 + \eta(2i + 1))}{(1 + \eta i)^2(1 + \eta(i + 1))^2}$ .

$$
\begin{array}{l} \sum_ {i = 0} ^ {N - 1} \frac {h _ {i} ^ {2}}{(1 - t _ {i + 1}) ^ {3}} = \sum_ {i = 0} ^ {N - 1} \frac {\eta^ {2} (2 + \eta (2 i + 1)) ^ {2}}{(1 + \eta i) ^ {4} (1 + \eta (i + 1)) ^ {4}} (1 + \eta (i + 1)) ^ {6} \\ = \eta^ {2} \sum_ {i = 0} ^ {N - 1} \frac {(2 + \eta (2 i + 1)) ^ {2}}{(1 + \eta i) ^ {4}} (1 + \eta (i + 1)) ^ {2} \\ \lesssim 4 N \eta^ {2}. \\ \end{array}
$$

Note that by construction of early stopping, it must hold that $1 - \frac{1}{(1 + \eta N)^2} = T$ , which implies $\frac{\frac{1}{\sqrt{1 - T}} - 1}{\eta} = N$ . Hence

$$
\sum_ {i = 0} ^ {N - 1} \frac {h _ {i} ^ {2}}{(1 - t _ {i}) ^ {3}} \lesssim 4 N \eta^ {2} \lesssim \eta \frac {1}{\sqrt {1 - T}}.
$$

We want to reach

$$
\left(\frac {M _ {1}}{m _ {1}}\right) ^ {\frac {3}{2}} (d - 1) ^ {2} \eta \frac {1}{\sqrt {1 - T}} = \mathcal {O} (\varepsilon_ {\mathrm {t a r g e t}}).
$$

So we need

$$
\eta \lesssim \left(\frac {\varepsilon_ {\mathrm {t a r g e t}} \sqrt {1 - T}}{(d - 1) ^ {2}}\right).
$$

and consequently

$$
N = \frac {\frac {1}{\sqrt {1 - T}} - 1}{\eta} = \mathcal {O} (\frac {\frac {1}{\sqrt {1 - T}} - 1}{\frac {\varepsilon_ {\mathrm {t a r g e t}} \sqrt {1 - T}}{(d - 1) ^ {2}}}) = \mathcal {O} (\frac {d ^ {2}}{(1 - T) \varepsilon_ {\mathrm {t a r g e t}}}).
$$

We remark that the step size schedule can be described by the discretized time points as follows:

$$
t _ {i} = 1 - \frac {1}{(1 + \eta i) ^ {2}}, \quad \text {w h e r e} \quad \eta = \mathcal {O} \left(\frac {\varepsilon_ {\mathrm {t a r g e t}} \sqrt {1 - T}}{(d - 1) ^ {2}}\right). \tag {15}
$$

![](images/ef51c097a92913b99c65490468a02781e6d4b9cf62d0cd75dee4e4bb96867893.jpg)

# B.7 Example: SPD Manifold

We first state the following result proved later in Appendix E.

Proposition B.6. Let $M$ be SPD(n). Assume Assumption 1. We impose the following moment condition: there exists $M_{\lambda_1}$ be such that

$$
\max  \left\{\mathbb {E} [ d (X _ {1}, z) ^ {2} e ^ {\lambda_ {1} d (X _ {1}, z)} ], \mathbb {E} [ e ^ {\lambda_ {1} d (X _ {1}, z)} ] \right\} \leq M _ {\lambda_ {1}}, \quad \text {w h e r e} \quad \lambda_ {1} = 2 4 \max  \{1, \kappa \}.
$$

We choose the prior distribution to be a Riemannian Gaussian distribution centered at some $z \in M$ : $p_0(x) \propto \exp \left(-dd(x,z)^2\right)$ . We then have the following regularity results.

$$
\mathbb {E} [ \| v (t, x) \| ^ {2} ] \lesssim d,
$$

$$
\mathbb {E} [ \| \nabla v (t, x) \| ] \lesssim \frac {d ^ {2 + 6 \lambda}}{1 - t} L _ {R} M _ {\lambda_ {1}} ^ {\frac {1}{2}},
$$

$$
\mathbb {E} [ \| \nabla v (t, x) \| ^ {2} ] \lesssim \frac {d ^ {3 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {2} M _ {\lambda_ {1}} ^ {\frac {1}{2}},
$$

$$
\mathbb {E} [ | \frac {d}{d t} v (t, x) | ] \lesssim \frac {d ^ {2 + 6 \lambda}}{1 - t} L _ {R} M _ {\lambda_ {1}} ^ {\frac {1}{2}},
$$

$$
\mathbb {E} [ | \frac {d}{d t} v (t, x) | ^ {2} ] \lesssim \frac {d ^ {3 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {2} M _ {\lambda_ {1}} ^ {\frac {1}{2}},
$$

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| ] \lesssim \frac {d ^ {3 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {3},
$$

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| ^ {2} ] \lesssim \frac {d ^ {5 + 2 4 \lambda}}{(1 - t) ^ {4}} L _ {R} ^ {6} M _ {\lambda_ {1}},
$$

$$
\mathbb {E} \left[ \left| \frac {d}{d t} \operatorname {d i v} v (t, x) \right| \right] \lesssim \frac {d ^ {3 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {3} M _ {\lambda_ {1}} ^ {\frac {1}{2}},
$$

where $\lambda = \max \{1,\kappa \}$

Proof. [Proof of Proposition 4.1] Using Proposition B.6, and following Theorem 2, we have

$$
\begin{array}{l} \operatorname {T V} \left(\pi_ {T}, \hat {\pi} _ {T}\right) = \operatorname {T V} \left(X _ {t _ {N}}, Y _ {t _ {N}}\right) \\ \leq \operatorname {T V} \left(X _ {t _ {0}}, Y _ {t _ {0}}\right) + \frac {1}{2} N h ^ {2} \Big (\sqrt {6 L _ {t} ^ {\text {s c o r e}}} \left(\left(L _ {t} ^ {\hat {v}, x}\right) ^ {2} \left(L _ {t} ^ {\hat {v}}\right) ^ {2} + \left(L _ {t} ^ {\hat {v}, x}\right) ^ {2} \left(L _ {t} ^ {v}\right) ^ {2} + \left(L _ {t} ^ {v, t}\right) ^ {2} + \left(L _ {t} ^ {v}\right) ^ {2} \left(L _ {t} ^ {v, x}\right) ^ {2}\right) \\ \left. \left. + \left(L _ {t} ^ {\operatorname {d i v} \hat {v}, x} \left(L _ {t} ^ {\hat {v}} + L _ {t} ^ {v}\right) + L _ {t} ^ {\operatorname {d i v}, x} L _ {t} ^ {v} + L _ {t} ^ {\operatorname {d i v}, t} + L _ {R} \left(L _ {t} ^ {\hat {v}}\right) ^ {2} d\right)\right) + N h \left(\varepsilon \sqrt {2 L _ {t} ^ {\mathrm {s c o r e}}} + \varepsilon\right) \right. \\ \lesssim N h ^ {2} \left(\frac {d ^ {5 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {2} M _ {\lambda_ {1}} \sqrt {M \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} d ^ {1 2 \lambda}}\right) + N h (\varepsilon \sqrt {M \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} d ^ {1 2 \lambda}} + \varepsilon) \\ \lesssim h \left(\frac {d ^ {6 + 1 8 \lambda}}{(1 - t) ^ {3}} L _ {R} ^ {3} M _ {\lambda_ {1}} ^ {\frac {3}{2}}\right) + \left(\frac {d ^ {6 \lambda + 1}}{1 - t} L _ {R}\right) M _ {\lambda_ {1}} ^ {\frac {1}{2}} \varepsilon . \\ \end{array}
$$

Thus to reach $\varepsilon_{\mathrm{target}}$ accuracy, we need

$$
h = \mathcal {O} \left(\frac {\varepsilon_ {\mathrm {t a r g e t}} (1 - T) ^ {3}}{d ^ {6 + 1 8 \lambda} L _ {R} ^ {3} M _ {\lambda_ {1}} ^ {\frac {3}{2}}}\right).
$$

Consequently, the iteration complexity would be

$$
N = \mathcal {O} \left(\frac {d ^ {6 + 1 8 \lambda} L _ {R} ^ {3} M _ {\lambda_ {1}} ^ {\frac {3}{2}}}{\varepsilon_ {\mathrm {t a r g e t}} (1 - T) ^ {3}}\right).
$$

We remark that since $K_{\mathrm{min}} = -\frac{1}{2}$ (Criscitiello and Boumal, 2023), so $\lambda = \max \{1, \kappa\} = 1$ . In the meanwhile, the upper bound on $h$ required by Lemma 5.2 can be reduced to be of order

$$
\min \{\frac {1}{L _ {\nabla}}, \sqrt {\frac {1}{\| b (x) \| ^ {2} L _ {R} L _ {\nabla}}} \} = \frac {1 - T}{d ^ {8} L _ {R} M _ {\lambda_ {1}} ^ {\frac {1}{2}}},
$$

which is lower than our required order of $h$ .

Therefore, we conclude the iteration complexity as

$$
N = \mathcal {O} \left(\frac {d ^ {6 + 1 8 \lambda} L _ {R} ^ {3} M _ {\lambda_ {1}} ^ {\frac {3}{2}}}{\varepsilon_ {\mathrm {t a r g e t}} (1 - T) ^ {3}}\right) = \mathcal {O} \left(\frac {d ^ {2 4} L _ {R} ^ {3} M _ {\lambda_ {1}} ^ {\frac {3}{2}}}{\varepsilon_ {\mathrm {t a r g e t}} (1 - T) ^ {3}}\right).
$$

![](images/1de319a200fb8dcd6ac14ff2dcc673f076ef529113b8ace4abceaf78c2aa02e4.jpg)

# C Auxiliary Results for Proof of Main Theorems

# C.1 Jacobi Equation

Lemma C.1 (Solution for Jacobi equation). Let $M$ be of constant sectional curvature $c$ . Let $J$ be a normal Jacobi field along $\gamma$ , with initial condition $J(0) = v^{\perp}$ , $J'(0) = 0$ . Then we have

$$
J (t) = s _ {c} ^ {(2)} (t) \| v ^ {\perp} \| E (t) := \left\{ \begin{array}{l l} \| v ^ {\perp} \| E (t), & \text {i f c = 0}, \\ \| v ^ {\perp} \| \cos (\sqrt {c t}) E (t), & \text {i f c > 0}, \\ \| v ^ {\perp} \| \cosh (\sqrt {- c t}) E (t), & \text {i f c <   0}. \end{array} \right.
$$

where $E$ is a parallel normal unit vector field with $E(0) = \frac{v^{\perp}}{\|v^{\perp}\|}$ .

Proof. [Proof of Lemma C.1] Similar to the proof of Lee (2018, Proposition 10.12), the solution is of the form $J(t) = f(t)E(t)$ where $E(t)$ is a parallel unit normal vector field along $\gamma$ . Since the curvature is constant and $J$ is a normal Jacobi field, the Jacobi equation reduces to $D_t^2 J + cJ = 0$ , thus we only need to solve for $f''(t) + cf(t) = 0$ , where $f(t) \in \mathbb{R}, \forall t$ .

- When $c = 0$ , we obtain $f''(t) = 0$ , hence (to satisfy initial condition) $f(t) = \| v^{\perp} \|$ .   
- When $c > 0$ , we obtain $f(t) = \| v^{\perp} \| \cos(\sqrt{c} t)$ .   
- When $c < 0$ , we obtain $f(t) = \| v^{\perp} \| \frac{e^{\sqrt{-c} t} + e^{-\sqrt{-c} t}}{2} = \| v^{\perp} \| \cosh(\sqrt{c} t)$ .

Note that $E(0) = \frac{v^{\perp}}{\|v^{\perp}\|}$ . Therefore,

$$
J (t) = \left\{ \begin{array}{l l} \| v ^ {\perp} \| E (t), & \text {i f} c = 0, \\ \| v ^ {\perp} \| \cos (\sqrt {c t}) E (t), & \text {i f} c > 0, \\ \| v ^ {\perp} \| \cosh (\sqrt {- c t}) E (t), & \text {i f} c <   0. \end{array} \right.
$$

![](images/c8483389d8f289e0ccb29c48a03aae4d25a83ff68dde2ff5d6e63386dd4ce569.jpg)

Lemma C.2. Let $J_{v}(t)$ be a Jacobi field along $\gamma(t) = \mathrm{Exp}_{x}(thb(x))$ , with $J_{v}(0) = v$ , $J_{v}'(0) = \omega$ . Define $Y(t) = P_{\gamma(t)}^{\gamma(0)} J_{v}(t)$ . Up to the first conjugate point of $x$ , we have

$$
\| Y (t) \| \leq \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| t + s _ {K _ {\min }} (t) \| \omega^ {\perp} \| + \frac {s _ {K _ {\min }} (t)}{s _ {K _ {\min }} (t _ {0})} \| v ^ {\perp} \|.
$$

Take $h < \frac{R}{\|b(x)\|}$ , we have

$$
\int_ {0} ^ {1} \| Y (t) \| d t \leq \left\{ \begin{array}{l l} \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| + \frac {\| \omega^ {\perp} \|}{\sqrt {K _ {\mathrm {m i n}}}} + \| v ^ {\perp} \|, & i f K _ {\mathrm {m i n}} > 0, \\ \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| + \frac {\cosh (\sqrt {- K _ {\mathrm {m i n}}}) - 1}{- K _ {\mathrm {m i n}}} \| \omega^ {\perp} \| + \frac {\sinh (\sqrt {- K _ {\mathrm {m i n}}})}{\sqrt {- K _ {\mathrm {m i n}}}} \| v ^ {\perp} \|, & i f K _ {\mathrm {m i n}} <   0, \\ \| v ^ {\parallel} \| + \frac {1}{2} \| \omega^ {\parallel} \| + \frac {1}{2} \| \omega^ {\perp} \| + \| v ^ {\perp} \|, & i f K _ {\mathrm {m i n}} = 0. \end{array} \right.
$$

Proof. [Proof of Lemma C.2] Using isometric property of parallel transport, $\| Y(t)\| = \| J_v(t)\|$ . Decompose $v = v^{\parallel} + v^{\perp}$ , where $v^{\parallel}$ is the component in $\gamma '(0)$ direction, and $\langle v^{\perp},\gamma '(0)\rangle = 0$ . Similarly, we decompose $\omega = \omega^{\parallel} + \omega^{\perp}$ .

Define $J_{v} \eqqcolon J^{(0)} + J^{(1)} + J^{(2)}$ , where

$$
J ^ {(0)} (0) = v ^ {\parallel}, \quad D _ {t} J ^ {(0)} (0) = \omega^ {\parallel};
$$

$$
J ^ {(1)} (0) = 0, \quad D _ {t} J ^ {(1)} (0) = \omega^ {\perp};
$$

$$
J ^ {(2)} (0) = v ^ {\perp}, D _ {t} J ^ {(2)} (0) = 0.
$$

Note that both $J^{(1)}(0), D_t J^{(1)}(0)$ are orthogonla to $\gamma'(0)$ , so $J^{(1)}(t)$ is a normal Jacobi field.

We know $J^{(0)}$ is a tangential Jacobi field, so it has the form

$$
J ^ {(0)} (t) = (a + b t) \gamma^ {\prime} (t).
$$

Plug in the initial value, we get (note that $D_{t}\gamma^{\prime}(0) = 0$ )

$$
a \gamma^ {\prime} (0) = v ^ {\parallel}, \quad b \gamma^ {\prime} (0) = \omega^ {\parallel}.
$$

Hence $|a| = \frac{\|\boldsymbol{v}^{\parallel}\|}{\|\gamma'(0)\|}$ , and $|b| = \frac{\|\omega^{\parallel}\|}{\|\gamma'(0)\|}$ .

By definition, $\| \gamma '(0)\| = \| hb(x)\| = \| \gamma '(t)\|$ . So we get

$$
\| J ^ {(0)} (t) \| \leq \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| t.
$$

If all sectional curvatures of $M$ are bounded below by a constant $K_{\mathrm{min}}$ , Jacobi field comparison theorem yield

$$
\| J ^ {(1)} (t) \| \leq s _ {K} (t) \| D _ {t} J ^ {(1)} (0) \| = s _ {K _ {\min }} (t) \| \omega^ {\perp} \|.
$$

Now consider the term $J^2(0)$ . By Cheeger et al. (1975, Theorem 1.34) applied with Jacobi field formula given in Lemma C.1, we obtain $\| J^{(2)}(t) \| \leq \| \tilde{J}(t) \|$ . We remark that the focal point free condition is saying $J^{(2)}(t) \neq 0$ . As long as Cut locus is not reached, the geodesic is minimizing. Hence it suffices to guarantee that the geodesic $\gamma$ satisfies $\| \gamma'(0) \| < \inf(M)$ .

Finally, recall $\| Y(t)\| = \| J_v(t)\|$

$$
\begin{array}{l} \| Y (t) \| = \| J _ {v} (t) \| = \| J ^ {(0)} (t) + J ^ {(1)} (t) + J ^ {(2)} (t) \| \\ \leq \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| t + | s _ {K _ {\min}} (t) | \| \omega^ {\perp} \| + | s _ {K _ {\min}} ^ {(2)} (t) | \| v ^ {\perp} \|. \\ \end{array}
$$

We split into cases. The first case is $K_{\min} > 0$ . In this case we denote $R = \operatorname{inj}(M)$ and

$$
\int_ {0} ^ {1} | s _ {K _ {\min }} (t) | d t = \frac {1}{\sqrt {K _ {\min }}} \int_ {0} ^ {1} | \sin (t \sqrt {K _ {\min }}) | d t \leq \frac {1}{\sqrt {K _ {\min }}}.
$$

Also,

$$
\int_ {0} ^ {1} \left| s _ {K _ {\min }} ^ {(2)} (t) \right| d t = \int_ {0} ^ {1} \left| \cos \left(\sqrt {K _ {\min }} t\right) \right| d t \leq 1.
$$

To summarize, when $h < \frac{R}{\|b(x)\|}$ ,

$$
\int_ {0} ^ {1} \| Y (t) \| d t \leq \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| + \frac {\| \omega^ {\perp} \|}{\sqrt {K _ {\operatorname* {m i n}}}} + \| v ^ {\perp} \|.
$$

The second case is $K_{\mathrm{min}} < 0$ .

Then $s_{K_{\min}}(t) = \frac{1}{\sqrt{-K_{\min}}} \sinh(\sqrt{-K_{\min}} t)$ . Consider $0 < t \leq h < 1$ .

$$
\int_ {0} ^ {1} s _ {K _ {\mathrm {m i n}}} (t) d t = \int_ {0} ^ {1} \frac {1}{\sqrt {- K _ {\mathrm {m i n}}}} \sinh t \sqrt {- K _ {\mathrm {m i n}}} d t = \frac {1}{- K _ {\mathrm {m i n}}} (\cosh (\sqrt {- K _ {\mathrm {m i n}}}) - 1).
$$

For the second integral,

$$
\int_ {0} ^ {1} \cosh (\sqrt {- K _ {\mathrm {m i n}}} t) d t = \frac {\sinh (\sqrt {- K _ {\mathrm {m i n}}})}{\sqrt {- K _ {\mathrm {m i n}}}}.
$$

To summarize, when $h < \frac{R}{\|b(x)\|}$ ,

$$
\int_ {0} ^ {1} \| Y (t) \| d t \leq \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| + \frac {\cosh (\sqrt {- K _ {\operatorname* {m i n}}}) - 1}{- K _ {\operatorname* {m i n}}} \| \omega^ {\perp} \| + \| v ^ {\perp} \| \frac {\sinh (\sqrt {- K _ {\operatorname* {m i n}}})}{\sqrt {- K _ {\operatorname* {m i n}}}}.
$$

The third case is $K_{\mathrm{min}} = 0$ . In this case $s_{K_{\mathrm{min}}} (t) = t$ .

$$
\begin{array}{l} \| Y (t) \| = \| J _ {v} (t) \| = \| J ^ {(0)} (t) + J ^ {(1)} (t) + J ^ {(2)} (t) \| \\ \leq \| v ^ {\parallel} \| + \| \omega^ {\parallel} \| t + \| \omega^ {\perp} \| t + \| v ^ {\perp} \|. \\ \end{array}
$$

Then we have

$$
\int_ {0} ^ {1} \| Y (t) \| d t \leq \| v ^ {\parallel} \| + \frac {1}{2} \| \omega^ {\parallel} \| + \frac {1}{2} \| \omega^ {\perp} \| + \| v ^ {\perp} \|.
$$

# C.2 Divergence Term

Lemma C.3. Let $c$ denote the geodesic with $c(0) = z$ , $c(h) = x$ . Define a variation of geodesics $\Lambda(s, t)$ as $\Lambda(s, t) = \mathrm{Exp}_{c(t)}(sP_{c(0)}^{c(t)}E_i(t))$ where $E_i(t)$ is basis vector field along $c$ . Let $V$ be a vector field. For every $z$ , we can obtain a new vector field by parallel transport, denote as $P_{c(0)}^{c(t)}V(z)$ . Then

$$
D _ {s} P _ {c (0)} ^ {c (h)} V (z) = P _ {c (0)} ^ {c (h)} D _ {s} V (z) - P _ {c (0)} ^ {c (h)} \int_ {0} ^ {h} P _ {c (\tau)} ^ {c (t _ {k})} R (\partial_ {s} \Lambda (0, \tau), \partial_ {t} \Lambda (0, \tau)) P _ {c (t _ {k})} ^ {c (\tau)} V (z) d \tau ,
$$

where $D_{s}$ denote the covariant derivative along $E_{i}(t)$ .

Note that the $s$ direction is actually arbitrary. The goal is to compute the divergence at a point, so we can enumerate over all possible $s$ direction, in all basis vectors. Each $s$ direction, roughly speaking, defines a $D_{s}$ .

Proof. [Proof of Lemma C.3] By construction, it holds that

$$
\Lambda (0, 0) = z, \Lambda (0, h) = x.
$$

and the parallel transport $P_{z}^{x} = P_{\Lambda (0,0)}^{\Lambda (0,h)}$ is along $c$ . Define $W(s,t) = P_{\Lambda (s,0)}^{\Lambda (s,t)}V(\Lambda (s,0))$ , where we perform parallel transport along curve $t\mapsto \Lambda (s,t)$ which might not be a geodesic. By definition of parallel transport, $D_{t}W(s,t) = 0,\forall s$ .

We know

$$
- D _ {t} D _ {s} W (s, t) = D _ {s} D _ {t} W (s, t) - D _ {t} D _ {s} W (s, t) = R (\partial_ {s} \Lambda (s, t), \partial_ {t} \Lambda (s, t)) W (s, t).
$$

Hence evaluating at $s = 0$ , we obtain

$$
D _ {t} D _ {s} W (0, t) = - R (\partial_ {s} \Lambda (0, t), \partial_ {t} \Lambda (0, t)) W (0, t).
$$

We perform parallel transport $P_{c(t)}^{c(0)}$ on both sides of the equation, and by Lemma C.5 we have

$$
\frac {d}{d t} P _ {c (t)} ^ {c (0)} D _ {s} W (0, t) = P _ {c (t)} ^ {c (0)} D _ {t} D _ {s} W (0, t) = - P _ {c (t)} ^ {c (0)} R (\partial_ {s} \Lambda (0, t), \partial_ {t} \Lambda (0, t)) W (0, t).
$$

Observe that both side of the equation is a time dependent vector field in $T_{c(0)}M = T_zM$ . Hence we can perform integration

$$
\int_ {0} ^ {h} \frac {d}{d \tau} P _ {c (\tau)} ^ {c (t _ {k})} D _ {s} W (0, \tau) d \tau = - \int_ {0} ^ {h} P _ {c (\tau)} ^ {c (t _ {k})} R (\partial_ {s} \Lambda (0, \tau), \partial_ {t} \Lambda (0, \tau)) W (0, \tau) d \tau .
$$

Hence

$$
P _ {c (h)} ^ {c (0)} D _ {s} W (0, h) = D _ {s} W (0, 0) - \int_ {0} ^ {h} P _ {c (\tau)} ^ {c (t _ {k})} R (\partial_ {s} \Lambda (0, \tau), \partial_ {t} \Lambda (0, \tau)) W (0, \tau) d \tau .
$$

Note that $D_{s}W(0,0) = D_{s}V(\Lambda (0,0))$ . Perform parallel transport $P_{c(0)}^{c(h)}$ on both sides of the equation, we have

$$
D _ {s} W (0, h) = P _ {c (0)} ^ {c (h)} D _ {s} V (\Lambda (0, 0)) - P _ {c (0)} ^ {c (h)} \int_ {0} ^ {h} P _ {c (\tau)} ^ {c (t _ {k})} R (\partial_ {s} \Lambda (0, \tau), \partial_ {t} \Lambda (0, \tau)) W (0, \tau) d \tau .
$$

Recall $W(s,t) = P_{\Lambda (s,0)}^{\Lambda (s,t)}V(\Lambda (s,0))$

$$
D _ {s} P _ {c (0)} ^ {c (h)} V (\Lambda (0, 0)) = P _ {c (0)} ^ {c (h)} D _ {s} V (\Lambda (0, 0)) - P _ {c (0)} ^ {c (h)} \int_ {0} ^ {h} P _ {c (\tau)} ^ {c (t _ {k})} R (\partial_ {s} \Lambda (0, \tau), \partial_ {t} \Lambda (0, \tau)) P _ {c (t _ {k})} ^ {c (\tau)} V (z) d \tau .
$$

Notice that $\tilde{v}$ is defined through $\hat{v}$ and the inverse of $F$ . We need to control $\operatorname{div} \tilde{v}(x, t)$ in our analysis, by writing it as some expression involving $\operatorname{div} \hat{v}$ .

Lemma C.4. Under Assumption 1, we have

$$
\left| \operatorname {d i v} \left(\tilde {v} (x, t) - v (x, t)\right) \right| \leq \left| \operatorname {d i v} \hat {v} (t _ {k}, z) - \operatorname {d i v} v (x, t) \right| + L _ {R} (t - t _ {k}) d \| \hat {v} (t _ {k}, z) \| ^ {2}.
$$

where $\mathrm{Exp}_z((t - t_k)\hat{v} (t_k,z)) = x$

Proof. [Proof of Lemma C.4] We follow the setting in Lemma C.3 with $V$ replaced by $\hat{v}$ . We use $\{E_i(t)\}_{i=1}^d$ to denote an orthonormal basis vector field along geodesic $c$ . Note that a slight difference is the time shift, where in Lemma C.3 we have the curve is from time 0 to $h$ , but here we are from $t_k$ to $t$ (so we have $h = t - t_k$ ). We denote our time variable as $\tau$ . In most cases we mean the variable $\tau$ is in $[t_k, t]$ .

By definition, $\mathrm{Exp}_z((t - t_k)\hat{v} (t_k,z)) = x$ . So we know $\Lambda (0,\tau) = \mathrm{Exp}_{z}((\tau -t_{k})\hat{v} (t_{k},z))$ . By construction,

$$
\partial_ {t} \Lambda (0, \tau) = P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z), \quad \partial_ {s} \Lambda (0, \tau) = E _ {i} (\tau).
$$

By Lemma C.3 with $c(\tau) = \mathrm{Exp}_z((\tau -t_k)\hat{v} (t_k,z))$

$$
D _ {s} P _ {c (t _ {k})} ^ {c (t)} \hat {v} (t _ {k}, z) = P _ {c (t _ {k})} ^ {c (t)} D _ {s} \hat {v} (t _ {k}, z) - P _ {c (t _ {k})} ^ {c (t)} \int_ {t _ {k}} ^ {t} P _ {c (\tau)} ^ {c (t _ {k})} R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z) d \tau .
$$

By definition of Riemannian divergence,

$$
\begin{array}{l} \operatorname {d i v} \tilde {v} (t, x) = \sum_ {i = 1} ^ {d} \langle \nabla_ {E _ {i} (t)} \tilde {v} (t, x), E _ {i} (t) \rangle = \sum_ {i = 1} ^ {d} \langle \nabla_ {E _ {i} (t)} P _ {F _ {t _ {k}, t - t _ {k}} ^ {- 1} (x)} ^ {x} \hat {v} (t _ {k}, F _ {t _ {k}, t - t _ {k}} ^ {- 1} (x)), E _ {i} (t) \rangle \\ = \sum_ {i = 1} ^ {d} \langle D _ {s} ^ {(i)} P _ {c (t _ {k})} ^ {c (t)} \hat {v} (t _ {k}, z), E _ {i} (t) \rangle \\ = \sum_ {i = 1} ^ {d} \langle P _ {c (t _ {k})} ^ {c (t)} D _ {s} ^ {(i)} \hat {v} (t _ {k}, z) - P _ {c (t _ {k})} ^ {c (t)} \int_ {t _ {k}} ^ {t} P _ {c (\tau)} ^ {c (t _ {k})} R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z) d \tau , E _ {i} (t) \rangle \\ = \sum_ {i = 1} ^ {d} \langle P _ {c (t _ {k})} ^ {c (t)} \nabla_ {E _ {i} (t _ {k})} \hat {v} (t _ {k}, z) - P _ {c (t _ {k})} ^ {c (t)} \int_ {t _ {k}} ^ {t} P _ {c (\tau)} ^ {c (t _ {k})} R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z) d \tau , E _ {i} (t) \rangle \\ = \sum_ {i = 1} ^ {d} \left\langle P _ {c (t _ {k})} ^ {c (t)} \nabla_ {E _ {i} (t _ {k})} \hat {v} (t _ {k}, z), E _ {i} (t) \right\rangle \\ - \sum_ {i = 1} ^ {d} \langle P _ {c (t _ {k})} ^ {c (t)} \int_ {t _ {k}} ^ {t} P _ {c (\tau)} ^ {c (t _ {k})} R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z) d \tau , E _ {i} (t) \rangle \\ \end{array}
$$

$$
= \mathrm {d i v} \hat {v} (t _ {k}, z) - \sum_ {i = 1} ^ {d} \langle P _ {c (t _ {k})} ^ {c (t)} \int_ {t _ {k}} ^ {t} P _ {c (\tau)} ^ {c (t _ {k})} R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z) d \tau , E _ {i} (t) \rangle ,
$$

where $D_{s}^{(i)}$ represent the covariant derivative corresponds to $E_{i}(\tau)$ .

We have

$$
\begin{array}{l} \sum_ {i = 1} ^ {d} \langle P _ {c (t _ {k})} ^ {c (t)} \int_ {t _ {k}} ^ {t} P _ {c (\tau)} ^ {c (t _ {k})} R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z) d \tau , E _ {i} (t) \rangle \\ = \sum_ {i = 1} ^ {d} \int_ {t _ {k}} ^ {t} \langle P _ {c (\tau)} ^ {c (t _ {k})} R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z), E _ {i} (t _ {k}) \rangle d \tau \\ = \sum_ {i = 1} ^ {d} \int_ {t _ {k}} ^ {t} \langle R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z), E _ {i} (\tau) \rangle d \tau \\ \leq \sum_ {i = 1} ^ {d} \int_ {t _ {k}} ^ {t} L _ {R} \| \hat {v} (t _ {k}, z) \| ^ {2} d \tau \leq (t - t _ {k}) d L _ {R} \| \hat {v} (t _ {k}, z) \| ^ {2}. \\ \end{array}
$$

It follows that

$$
\begin{array}{l} | \operatorname {d i v} (\tilde {v} (x, t) - v (x, t)) | \\ = | \operatorname {d i v} \hat {v} (t _ {k}, z) - \sum_ {i = 1} ^ {d} \langle P _ {c (t _ {k})} ^ {c (t)} \int_ {t _ {k}} ^ {t} P _ {c (\tau)} ^ {c (t _ {k})} R (E _ {i} (\tau), P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z)) P _ {c (t _ {k})} ^ {c (\tau)} \hat {v} (t _ {k}, z) d \tau , E _ {i} (t) \rangle - \operatorname {d i v} v (x, t) | \\ \leq \left| \operatorname {d i v} \hat {v} \left(t _ {k}, z\right) - \operatorname {d i v} v (x, t) \right| + L _ {R} \left(t - t _ {k}\right) d \| \hat {v} \left(t _ {k}, z\right) \| ^ {2}. \\ \end{array}
$$

Lemma C.5. We have that

$$
\frac {d}{d t} P _ {c (t)} ^ {c (0)} Y (t) = P _ {c (t)} ^ {c (0)} D _ {t} Y (t).
$$

Proof. [Proof of Lemma C.5] Denote the geodesic along $t$ direction as $c(t)$ . Let $v \in T_{c(0)}M$ be arbitrary, and define $Z(t) = P_{c(0)}^{c(t)}v$ .

$$
\frac {d}{d t} \langle P _ {c (t)} ^ {c (0)} Y (t), v \rangle = \frac {d}{d t} \langle Y (t), P _ {c (0)} ^ {c (t)} v \rangle = \langle D _ {t} Y (t), P _ {c (0)} ^ {c (t)} v \rangle + 0 = \langle D _ {t} Y (t), P _ {c (0)} ^ {c (t)} v \rangle = \langle P _ {c (t)} ^ {c (0)} D _ {t} Y (t), v \rangle .
$$

On the other hand,

$$
\frac {d}{d t} \langle P _ {c (t)} ^ {c (0)} Y (t), v \rangle = \langle \frac {d}{d t} P _ {c (t)} ^ {c (0)} Y (t), v \rangle .
$$

Since the above holds for any $v$ , we have

$$
\frac {d}{d t} P _ {c (t)} ^ {c (0)} Y (t) = P _ {c (t)} ^ {c (0)} D _ {t} Y (t).
$$

□

# D Hypersphere Regularity Results

Recall that

$$
v (t, x) = \frac {1}{1 - t} \int_ {M} \mathrm {L o g} _ {x} (x _ {1}) p _ {t} (x _ {1} | x) d V _ {g} (x _ {1}).
$$

To establish regularity of $v$ , it is natural to study the formula for conditional density, $p_t(x_1|x)$ . In a Euclidean space, with Gaussian distribution as prior $p_0$ , we have that $p_t(x_1 \mid x_t = x) \propto p_1(x_1)\exp(-\frac{\|tx_1 - x\|^2}{2(1 - t)^2})$ . This is a standard result for flow matching, see for example Guan et al. (2026) and Zhou and Liu (2025). But on a Riemannian manifold, the curvature would introduce an extra term due to the change of variable formula, and the existence of cut points would introduce an extra indicator function. We provide the formula for conditional density on the hypersphere $S^d$ with uniform distribution as prior, and geodesic interpolation. See Lemma D.1 below.

Lemma D.1 (Conditional density on $S^d$ for geodesic interpolation). Let $S^d$ be the unit sphere with round metric, $d \geq 2$ . Let $X_1 \sim p_1$ be the data distribution with smooth densities $p_1 > 0$ w.r.t. $dV_g$ , and $X_0 \sim p_0$ being uniform distribution independent of $X_1$ . Consider geodesic interpolation with minimizing geodesic. Fix $t \in [0,1)$ and $x, x_1 \in S^d$ . Write $r = d(x, x_1)$ . Denote

$$
\begin{array}{l} J _ {t} (x \mid x _ {1}) = \frac {1}{1 - t} \left(\frac {\sin (r / (1 - t))}{\sin r}\right) ^ {d - 1} \mathbf {1} _ {\{d (x, x _ {1}) <   (1 - t) \pi \}} \\ = \left\{ \begin{array}{l l} \frac {1}{1 - t} \Big (\frac {\sin \big (r / (1 - t) \big)}{\sin r} \Big) ^ {d - 1}, & i f r <   (1 - t) \pi , \\ 0, & i f r \geq (1 - t) \pi . \end{array} \right. \\ \end{array}
$$

Then the conditional density of $X_{1}$ given $X_{t} = x$ is

$$
p _ {t} (x _ {1} \mid x) = \frac {p _ {1} (x _ {1}) J _ {t} (x \mid x _ {1})}{\int_ {S ^ {d}} p _ {1} (z) J _ {t} (x \mid z) d V _ {g} (z)}.
$$

Proof. The proof strategy is as follows. We first write out the joint distribution of $X_0, X_1$ , and then use the change of variable formula to obtain joint distribution of $X_t, X_1$ .

We apply the change of variable formula. We need a diffeomorphism between $(X_0, X_1)$ and $(X_t, X_1)$ . Fix $t \in (0, 1)$ and $x_1 \in S^d$ . Use polar coordinates at $x_1$ : every $y \in S^d \setminus \{-x_1\}$ can be written uniquely as $y = \mathrm{Exp}_{x_1}(r\omega)$ for some $r \in (0, \pi), \omega \in S^{d-1}$ . And we know the Riemannian volume element is

$$
d V _ {g} (y) = (\sin r) ^ {d - 1} d r d \omega .
$$

In particular, for any $x_0$ , we set $r_0 = d(x_0, x_1) \in (0, \pi)$ and $\omega = \frac{\operatorname{Log}_{x_1}(x_0)}{\|\operatorname{Log}_{x_1}(x_0)\|}$ . Then we can write

$$
x _ {0} = \operatorname {E x p} _ {x _ {1}} (r _ {0} \omega), \qquad x _ {1} = \operatorname {E x p} _ {x _ {1}} (0 \cdot \omega).
$$

and

$$
X _ {t} = \operatorname {E x p} _ {x _ {0}} \big (t \operatorname {L o g} _ {x _ {0}} (x _ {1}) \big) = \operatorname {E x p} _ {x _ {1}} \big ((1 - t) r _ {0} \omega \big).
$$

Thus we can define the desired diffeomorphism as $F_{t}:(r_{0},\omega)\mapsto (r,\omega)$ satisfying

$$
F _ {t, x _ {1}} (r _ {0}, \omega) = ((1 - t) r _ {0}, \omega), \qquad F _ {t, x _ {1}} ^ {- 1} (r, \omega) = (\frac {r}{1 - t}, \omega).
$$

But however, note that we have to restrict $r < (1 - t)\pi$ , otherwise $\frac{r}{1 - t} \notin (0,\pi)$ , consequently $F_{t,x_1}^{-1}(r,\omega)$ is no longer under the polar coordinate.

Now recall the change of variable formula. We should have

$$
\int_ {S ^ {d}} p _ {0} \left(F _ {t, x _ {1}} ^ {- 1} (x)\right) | \det  d F _ {t, x _ {1}} ^ {- 1} | d V _ {g} (x) = \int_ {S ^ {d}} p _ {0} \left(x _ {0}\right) d V _ {g} \left(x _ {0}\right).
$$

Written in polar coordinates: the volume element at $x_0$ and $x$ are

$$
d V _ {g} (x _ {0}) = (\sin r _ {0}) ^ {d - 1} d r _ {0} d \omega , \qquad d V _ {g} (x) = (\sin r) ^ {d - 1} d r d \omega .
$$

Define a function $J_{t}(x \mid x_{1})$ to satisfy

$$
d V _ {g} \left(x _ {0}\right) = J _ {t} \left(x \mid x _ {1}\right) d V _ {g} (x).
$$

Using $r_0 = r / (1 - t)$ (hence $dr_0 = dr / (1 - t)$ ), we get

$$
\left(\sin r _ {0}\right) ^ {d - 1} d r _ {0} d \omega = J _ {t} (x \mid x _ {1}) (\sin r) ^ {d - 1} d r d \omega
$$

$$
\left. (\sin (r / (1 - t))) ^ {d - 1} \frac {d r}{1 - t} d \omega = J _ {t} (x \mid x _ {1}) (\sin r) ^ {d - 1} d r d \omega , \right.
$$

Now we derive the density. Note that by our construction of geodesic interpolation, given any $x_0$ and $t$ , the resulting $x$ must satisfy $d(x_1, x) = (1 - t)d(x_1, x_0) \leq (1 - t)\pi$ . Hence

$$
J _ {t} (x \mid x _ {1}) = \frac {1}{1 - t} \left(\frac {\sin (r / (1 - t))}{\sin r}\right) ^ {d - 1}, \qquad r = d (x, x _ {1}),
$$

for all $r < (1 - t)\pi$ , and $J_{t}(x \mid x_{1}) = 0$ otherwise. Thus, we can equivalently write

$$
J _ {t} (x \mid x _ {1}) = \frac {1}{1 - t} \left(\frac {\sin (r / (1 - t))}{\sin r}\right) ^ {d - 1} \mathbf {1} _ {\{d (x, x _ {1}) <   (1 - t) \pi \}}.
$$

The joint density of $(X_0, X_1)$ is

$$
p \left(x _ {0}, x _ {1}\right) = p _ {0} \left(x _ {0}\right) p _ {1} \left(x _ {1}\right)
$$

with respect to $dV_{g}(x_{0})dV_{g}(x_{1})$ . By the change of variable formula,

$$
p _ {t} (x, x _ {1}) = p _ {0} \left(F _ {t, x _ {1}} ^ {- 1} (x)\right) p _ {1} (x _ {1}) J _ {t} (x \mid x _ {1}).
$$

Finally, since $p_t(x,x_1) = p_t(x_1\mid x)p_t(x) = p_t(x_1\mid x)\int_{S^d}p_t(x,z)dV_g(z)$ , the conditional density of $X_{1}$ given $X_{t} = x$ is

$$
p _ {t} \left(x _ {1} \mid x\right) = \frac {p _ {t} \left(x , x _ {1}\right)}{\int_ {S ^ {d}} p _ {t} \left(x , z\right) d V _ {g} (z)},
$$

which gives the formula stated in the lemma.

Following Lemma D.1, we can derive the following formula for interpolated density.

Lemma D.2. We can write the interpolated density as

$$
p _ {t} (x) = \int_ {S ^ {d}} p _ {t} (x, x _ {1}) d V _ {g} (x _ {1}) = \frac {1}{\operatorname {V o l} \left(S ^ {d}\right)} \int_ {S ^ {d}} p _ {1} (x _ {1}) J _ {t} (x \mid x _ {1}) d V _ {g} (x _ {1}).
$$

Proof. Following Lemma D.1, we have

$$
p _ {t} (x, x _ {1}) = p _ {0} (F _ {t, x _ {1}} ^ {- 1} (x)) p _ {1} (x _ {1}) J _ {t} (x \mid x _ {1}).
$$

Consequently, we have (note that $p_0$ is uniform distribution)

$$
p _ {t} (x) = \int_ {S ^ {d}} p _ {t} (x, x _ {1}) d V _ {g} (x _ {1}) = \frac {1}{\operatorname {V o l} \left(S ^ {d}\right)} \int_ {S ^ {d}} p _ {1} (x _ {1}) J _ {t} (x \mid x _ {1}) d V _ {g} (x _ {1}).
$$

Before justifying the regularity of $v$ , we first need to show that its smoothness is not destroyed by the indicator function, which corresponds to the cut point. In the following Lemma, we show that on a Hypersphere, the sin function (that appeared in the conditional density function) would smooth out the indicator function, resulting in a smooth vector field.

Lemma D.3. Let $S^d$ be the unit hypersphere with round metric, $d \geq 2$ . Let $x_1 \in S^d$ and define, for $t \in [0,1)$ and $x \in S^d$ . Denote $r(x) = d(x,x_1)$ as the radial distance function. Then for integer $m$ with $0 \leq m \leq d - 2$ , the function $J(t,x \mid x_1)$ viewed as a function on $[0,1) \times S^d$ is $C^m$ .

Consequently, $v(t,x)$ as a conditional expectation is $C^2$ in $(t,x)$ for $t \in [0,1)$ . As a result, the solution for flow matching ODE exists and unique.

Proof. Denote $\mathcal{U} := \{(t,x) \in [0,1) \times \mathcal{S}^d : r(x) < (1 - t)\pi\}$ . We first show the smoothness on $\mathcal{U}$ . Fix $(t_0,x_0) \in \mathcal{U}$ where $x_0 \neq x_1$ , and write $r_0 := r(x_0) > 0$ . Since $r_0 < (1 - t_0)\pi < \pi$ , we have $x_0 \neq -x_1$ . Moreover, by continuity of $r(\cdot)$ there exists a neighborhood $\mathcal{V}$ of $(t_0,x_0)$ such that for all $(t,x) \in \mathcal{V}$ , $\mathbf{1}_{\{r(x) < (1 - t)\pi\}} \equiv 1$ , and consequently

$$
J (t, x \mid x _ {1}) = \frac {1}{1 - t} \Big (\frac {\sin \big (r (x) / (1 - t) \big)}{\sin r (x)} \Big) ^ {d - 1}.
$$

Since $r = d(x, x_1)$ is smooth when $x \notin \{x_1, -x_1\}$ , $J$ is smooth as a composition of smooth functions.

It remains to check the smoothness of $J(t,x\mid x_1)$ at point $x = x_{1}$ ( $r = 0$ ). Introduce normal coordinates at $x_{1}$ : for $x$ near $x_{1}$ write

$$
v := \operatorname {L o g} _ {x _ {1}} (x) \in T _ {x _ {1}} \mathcal {S} ^ {d}, \qquad r (x) = d (x, x _ {1}) = \| v \|.
$$

It suffices to show that under normal coordinates, $J$ viewed as a function of $v$ , is smooth. Notice that $\| v \|$ is not differentiable at $v = 0$ , hence functions such as $v \mapsto \sin \| v \|$ are not $C^1$ at 0. But notice that in $J$ , the "non-smooth" part on $\| v \|$ cancels. By checking smoothness of

$$
\frac {\sin (\| v \| / (1 - t))}{\sin \| v \|},
$$

we conclude the smoothness of $J$ on $U$ .

We extend the smoothness result by checking the boundary $r = (1 - t)\pi$ . To prove $C^m$ , fix $(t_0, x_0)$ with $r(x_0) = (1 - t_0)\pi$ . Since $r(x_0) \in (0, \pi)$ , we have $x \mapsto r(x)$ is smooth near $x_0$ . Set $s(t, x)$ as follows, describing how far will $x$ reach the boundary:

$$
s (t, x) := (1 - t) \pi - r (x).
$$

On the side $s > 0$ we have $u\coloneqq r / (1 - t)\in (0,\pi)$ and

$$
\sin \left(\frac {r}{1 - t}\right) = \sin \left(\pi - \frac {s}{1 - t}\right) = \sin \left(\frac {s}{1 - t}\right).
$$

Therefore, for $s > 0$ ,

$$
J (t, x \mid x _ {1}) = \frac {1}{1 - t} \Big (\frac {\sin \big (s (t , x) / (1 - t) \big)}{\sin r (x)} \Big) ^ {d - 1} = s (t, x) ^ {d - 1} (1 - t) ^ {- d} \left(\frac {\frac {\sin \big (s (t , x) / (1 - t) \big)}{s (t , x) / (1 - t)}}{\sin r (x)}\right) ^ {d - 1}.
$$

On the whole manifold $S^d$ , we have

$$
J (t, x \mid x _ {1}) = \big (s (t, x) \big) _ {+} ^ {d - 1} (1 - t) ^ {- d} \left(\frac {\frac {\sin \big (s (t , x) / (1 - t) \big)}{s (t , x) / (1 - t)}}{\sin r (x)}\right) ^ {d - 1}, \qquad (s) _ {+} := \max  \{s, 0 \}.
$$

Since $s \mapsto (s)_{+}^{d - 1}$ is $C^m$ as a one-dimensional function for every $m \leq d - 2$ , and since $s(t,x)$ is smooth in $(t,x)$ , the composition $\big(s(t,x)\big)_{+}^{d - 1}$ is $C^m$ in $(t,x)$ for all $m \leq d - 2$ . It follows that $J$ is $C^m$ , as a product of a smooth function and $\big(s(t,x)\big)_{+}^{d - 1}$ .

Remark 2. The fact that $v$ being $C^2$ in $(t,x)$ for $t \in [0,1)$ follows from smoothness of $J$ , and the following properties of $\operatorname{Log}:(1)$ Log being uniformly bounded, and (2) singularity of derivatives of $\operatorname{Log}_x(x_1)$ as $x_{1} \to -x$ is well controlled under polar coordinates.

The existence and uniqueness of flow matching ODE follows from classical theory on time-dependent flow, see for example (Marsden et al., 2002, Section 4.1) and (Lee, 2012, Theorem 9.48).

# D.1 Auxiliary Lemmas

The following result studies the derivative of a function that only depends on the radial distance. In other words, if a function $\phi(x)$ on $M$ only depends on $x$ through $r(x) = d(x, x_1)$ for some fixed $x_1$ , then we can control its derivative through derivative of $r$ .

Lemma D.4. Fix $x_1 \in S^d$ and define $r(x) \coloneqq d(x, x_1)$ . Assume $x \notin \operatorname{Cut}(x_1)$ , so that $r$ is smooth in a neighborhood of $x$ and $\| \operatorname{grad}_x r(x) \| = 1$ . Let $F \colon (0, \pi) \to \mathbb{R}$ be $C^2$ and set $\phi(x) \coloneqq F(r(x))$ . Then

$$
\operatorname {g r a d} _ {x} \phi (x) = F ^ {\prime} (r (x)) \operatorname {g r a d} _ {x} r (x), \quad \| \operatorname {g r a d} _ {x} \phi (x) \| = | F ^ {\prime} (r (x)) |.
$$

Moreover,

$$
\| \nabla \operatorname {g r a d} \phi (x) \| _ {\mathrm {o p}} \leq | F ^ {\prime} (r (x)) | \| \nabla \operatorname {g r a d} r (x) \| _ {\mathrm {o p}} + | F ^ {\prime \prime} (r (x)) |.
$$

Proof. We apply the chain rule for the Riemannian gradient. For any $u \in T_x S^d$ , the differential satisfies

$$
d \phi (x) [ u ] = d (F \circ r) (x) [ u ] = F ^ {\prime} (r (x)) d r (x) [ u ].
$$

By the definition of the Riemannian gradient,

$$
\langle \operatorname {g r a d} _ {x} \phi , u \rangle = F ^ {\prime} (r (x)) \langle \operatorname {g r a d} _ {x} r, u \rangle , \quad \forall u \in T _ {x} S ^ {d},
$$

hence

$$
\operatorname {g r a d} _ {x} \phi (x) = F ^ {\prime} (r (x)) \operatorname {g r a d} _ {x} r (x).
$$

Taking norms gives

$$
\| \operatorname {g r a d} _ {x} \phi (x) \| = | F ^ {\prime} (r (x)) | \| \operatorname {g r a d} _ {x} r (x) \|.
$$

Since $x \notin \operatorname{Cut}(x_1)$ , the distance function satisfies $\| \operatorname{grad}_x r(x) \| = 1$ , and therefore

$$
\left\| \operatorname {g r a d} _ {x} \phi (x) \right\| = | F ^ {\prime} (r (x)) |.
$$

Next, for any $u \in T_x S^d$ ,

$$
\begin{array}{l} \nabla_ {u} \operatorname {g r a d} \phi (x) = \nabla_ {u} \left(F ^ {\prime} (r (x)) \operatorname {g r a d} r (x)\right) \\ = F ^ {\prime} (r (x)) \nabla_ {u} \operatorname {g r a d} r (x) + u \left(F ^ {\prime} (r (x))\right) \operatorname {g r a d} r (x) \\ = F ^ {\prime} (r (x)) \nabla_ {u} \operatorname {g r a d} r (x) + F ^ {\prime \prime} (r (x)) u (r (x)) \operatorname {g r a d} r (x) \\ = F ^ {\prime} (r (x)) \nabla_ {u} \operatorname {g r a d} r (x) + F ^ {\prime \prime} (r (x)) \langle \operatorname {g r a d} r (x), u \rangle \operatorname {g r a d} r (x). \\ \end{array}
$$

Hence, for $\| u\| = 1$

$$
\begin{array}{l} \| \nabla_ {u} \operatorname {g r a d} \phi (x) \| \leq | F ^ {\prime} (r (x)) | \| \nabla_ {u} \operatorname {g r a d} r (x) \| + | F ^ {\prime \prime} (r (x)) | | \langle \operatorname {g r a d} r (x), u \rangle | \| \operatorname {g r a d} r (x) \| \\ \leq | F ^ {\prime} (r (x)) | \| \nabla_ {u} \operatorname {g r a d} r (x) \| + | F ^ {\prime \prime} (r (x)) |, \\ \end{array}
$$

using $\| \operatorname{grad} r(x) \| = 1$ and $|\langle \operatorname{grad} r(x), u \rangle| \leq \| u \| = 1$ . Taking the supremum over $\| u \| = 1$ yields

$$
\| \nabla \operatorname {g r a d} \phi (x) \| _ {\mathrm {o p}} \leq | F ^ {\prime} (r (x)) | \| \nabla \operatorname {g r a d} r (x) \| _ {\mathrm {o p}} + | F ^ {\prime \prime} (r (x)) |.
$$

The following result controls the conditional expectation of some certain "functions with singularity", which will be used to establish regularity.

Lemma D.5 (Expectation of $\frac{1}{\sin^a u}$ ). Consider $d \geq 3$ and $a = 1,2$ . Let $r = d(x,x_1)$ and set $u = r / (1 - t) \in (0,\pi)$ . We have

$$
\mathbb {E} \left[ \frac {1}{\sin^ {a} u} \mid X _ {t} = x \right] \leq 2 \frac {M _ {1}}{m _ {1}},
$$

where $0 <   m_{1}\leq p_{1}\leq M_{1}$

Proof. We have

$$
\begin{array}{l} \mathbb {E} \big [ \frac {1}{\sin^ {a} u} \mid X _ {t} = x \big ] = \int_ {S ^ {d}} \frac {1}{\sin^ {a} u} p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}) \\ \leq \frac {M _ {1}}{m _ {1} \operatorname {V o l} (S ^ {d})} \int_ {S ^ {d}} \frac {1}{\sin^ {a} u} J _ {t} (x \mid x _ {1}) d V _ {g} (x _ {1}). \\ \end{array}
$$

Use $r = (1 - t)u$ so that $\frac{1}{1 - t} dr = du$ ,

$$
\begin{array}{l} \int_ {S ^ {d}} \frac {1}{\sin^ {a} u} J _ {t} (x \mid x _ {1}) d V _ {g} (x _ {1}) \\ = \int_ {S ^ {d - 1}} \int_ {0} ^ {\pi} \frac {1}{\sin^ {a} u} J _ {t} (x \mid x _ {1}) (\sin r) ^ {d - 1} d r d \omega \\ = \operatorname {V o l} \left(S ^ {d - 1}\right) \int_ {0} ^ {\pi} \frac {1}{\sin^ {a} u} \sin (u) ^ {d - 1} d u \\ \end{array}
$$

$$
= \operatorname {V o l} \left(S ^ {d - 1}\right) \int_ {0} ^ {\pi} \sin (u) ^ {d - 1 - a} d u.
$$

Therefore

$$
\begin{array}{l} \mathbb {E} \left[ \frac {1}{\sin^ {a} u} \mid X _ {t} = x \right] = \int_ {S ^ {d}} \frac {1}{\sin^ {a} u} p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right) \\ \leq \frac {M _ {1} \operatorname {V o l} \left(S ^ {d - 1}\right)}{m _ {1} \operatorname {V o l} \left(S ^ {d}\right)} \int_ {0} ^ {\pi} \sin (u) ^ {d - 1 - a} d u. \\ = \frac {M _ {1} \operatorname {V o l} \left(S ^ {d - 1}\right)}{m _ {1} \operatorname {V o l} \left(S ^ {d}\right) \operatorname {V o l} \left(S ^ {d - 1 - a}\right)} \operatorname {V o l} \left(S ^ {d - 1 - a}\right) \int_ {0} ^ {\pi} \sin (u) ^ {d - 1 - a} d u \\ = \frac {M _ {1} \operatorname {V o l} \left(S ^ {d - 1}\right)}{m _ {1} \operatorname {V o l} \left(S ^ {d}\right) \operatorname {V o l} \left(S ^ {d - 1 - a}\right)} \operatorname {V o l} \left(S ^ {d - a}\right). \\ \end{array}
$$

Recall

$$
\operatorname {V o l} \left(S ^ {n}\right) = \frac {2 \pi^ {(n + 1) / 2}}{\Gamma ((n + 1) / 2)}.
$$

Hence

$$
\frac {\operatorname {V o l} \left(S ^ {d - 1}\right)}{\operatorname {V o l} \left(S ^ {d}\right)} = \frac {\frac {2 \pi^ {d / 2}}{\Gamma (d / 2)}}{\frac {2 \pi^ {(d + 1) / 2}}{\Gamma ((d + 1) / 2)}} = \pi^ {- 1 / 2} \frac {\Gamma ((d + 1) / 2)}{\Gamma (d / 2)},
$$

$$
\frac {\operatorname {V o l} \left(S ^ {d - a}\right)}{\operatorname {V o l} \left(S ^ {d - 1 - a}\right)} = \frac {\frac {2 \pi^ {(d - a + 1) / 2}}{\Gamma ((d - a + 1) / 2)}}{\frac {2 \pi^ {(d - a) / 2}}{\Gamma ((d - a) / 2)}} = \pi^ {1 / 2} \frac {\Gamma ((d - a) / 2)}{\Gamma ((d - a + 1) / 2)}.
$$

By Kershaw's inequality, for $d \geq 3$ ,

$$
\frac {\Gamma ((d + 1) / 2)}{\Gamma (d / 2)} \leq (d / 2 - \frac {1}{2} + \sqrt {\frac {3}{4}}) ^ {\frac {1}{2}},
$$

and

$$
\frac {\Gamma (d / 2)}{\Gamma ((d - 1) / 2)} \geq (\frac {d}{2} - 1 + \frac {1}{2}) ^ {\frac {1}{2}},
$$

$$
\frac {\Gamma ((d - a + 1) / 2)}{\Gamma ((d - a) / 2)} \geq (\frac {d - a - 1}{2} + \frac {1}{2}) ^ {\frac {1}{2}}.
$$

Together,

$$
\begin{array}{l} \frac {\operatorname {V o l} \left(S ^ {d - 1}\right) \operatorname {V o l} \left(S ^ {d - a}\right)}{\operatorname {V o l} \left(S ^ {d}\right) \operatorname {V o l} \left(S ^ {d - 1 - a}\right)} = \frac {\Gamma ((d + 1) / 2) \Gamma ((d - a) / 2)}{\Gamma (d / 2) \Gamma ((d - a + 1) / 2)} \leq (\frac {d / 2 - \frac {1}{2} + \sqrt {\frac {3}{4}}}{\frac {d - a - 1}{2} + \frac {1}{2}}) ^ {\frac {1}{2}} \\ = \left(\frac {d - a + a - 1 + 2 \sqrt {\frac {3}{4}}}{d - a}\right) ^ {\frac {1}{2}} \leq \left(1 + \frac {a - 1 + 2 \sqrt {\frac {3}{4}}}{d - a}\right) ^ {\frac {1}{2}}. \\ \end{array}
$$

For $a = 1,2$ , we have $\left(1 + \frac{a - 1 + 2\sqrt{\frac{3}{4}}}{d - a}\right)^{\frac{1}{2}} \leq 2$ .

The following results (Lemmas D.6, D.7, D.8, and D.9) provide bounds on the building blocks that appear in the derivative formulas for $v(t,x)$ . For all the results below, we assume $0 < m_{1} \leq p_{1}(x) \leq M_{1}$ .

Lemma D.6 (Moment bounds for $\operatorname{grad}_x \log p_t(X_1 \mid x)$ ). We have

$$
\| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \leq \frac {2 (d - 1)}{(1 - t) \sin u}.
$$

Furthermore,

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x ] \leq \frac {8 (d - 1)}{(1 - t)} \frac {M _ {1}}{m _ {1}},
$$

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| ^ {2} \mid X _ {t} = x ] \leq \frac {8 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}},
$$

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \leq \frac {3 2 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Proof. We first bound $\| \operatorname{grad}_x \log J_t(x \mid x_1) \|$ . Let $r = d(x, x_1)$ and set $u = r / (1 - t) \in (0, \pi)$ . On the set $r < (1 - t)\pi$ ,

$$
\frac {\partial}{\partial r} \log J _ {t} (r) = (d - 1) \Big (\frac {1}{1 - t} \cot \frac {r}{1 - t} - \cot r \Big) = (d - 1) \Big (\frac {1}{1 - t} \cot u - \cot ((1 - t) u) \Big).
$$

By the Lemma D.4,

$$
\| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| = \left| \frac {\partial}{\partial r} \log J _ {t} (r) \right| = (d - 1) \left| \frac {1}{1 - t} \cot u - \cot ((1 - t) u) \right|.
$$

For $u\in (0,\pi)$ , we have $|\cot u|\leq 1 / \sin u$ . Since $\sin ((1 - t)u)\geq (1 - t)\sin u$ , we have

$$
| \cot ((1 - t) u) | \leq \frac {1}{\sin ((1 - t) u)} \leq \frac {1}{(1 - t) \sin u}.
$$

Therefore for all $u\in (0,\pi)$ , we can bound

$$
\begin{array}{l} \left| \frac {1}{1 - t} \cot u - \cot ((1 - t) u) \right| \leq \frac {1}{1 - t} | \cot u | + | \cot ((1 - t) u) | \leq \frac {1}{(1 - t) \sin u} + \frac {1}{(1 - t) \sin u} \\ = \frac {2}{(1 - t) \sin u}. \\ \end{array}
$$

So

$$
\| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \leq \frac {2 (d - 1)}{(1 - t) \sin u}.
$$

Now we bound $\mathbb{E}\| \operatorname{grad}_x\log p_t\|$ by $\mathbb{E}\| \operatorname{grad}_x\log J_t\|$ . Let

$$
Z _ {t} (x) := \int_ {S ^ {d}} p _ {1} (z) J _ {t} (x \mid z) d V _ {g} (z),
$$

so

$$
\log p _ {t} \left(x _ {1} \mid x\right) = \log p _ {1} \left(x _ {1}\right) + \log J _ {t} \left(x \mid x _ {1}\right) - \log Z _ {t} (x).
$$

Since $p_1$ does not depend on $x$ ,

$$
\operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) = \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) - \operatorname {g r a d} _ {x} \log Z _ {t} (x).
$$

Also,

$$
\operatorname {g r a d} _ {x} Z _ {t} (x) = \int_ {S ^ {d}} p _ {1} (z) \operatorname {g r a d} _ {x} J _ {t} (x \mid z) d V _ {g} (z) = \int_ {S ^ {d}} p _ {1} (z) J _ {t} (x \mid z) \operatorname {g r a d} _ {x} \log J _ {t} (x \mid z) d V _ {g} (z),
$$

hence

$$
\operatorname {g r a d} _ {x} \log Z _ {t} (x) = \int_ {S ^ {d}} \operatorname {g r a d} _ {x} \log J _ {t} (x \mid z) p _ {t} (z \mid x) d V _ {g} (z) = \mathbb {E} \left[ \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \mid X _ {t} = x \right].
$$

Therefore

$$
\operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) = \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) - \mathbb {E} \big [ \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \mid X _ {t} = x \big ],
$$

and by triangle inequality,

$$
\mathbb {E} \big [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x \big ] \leq 2 \mathbb {E} \big [ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| \mid X _ {t} = x \big ] \leq \frac {8 (d - 1)}{(1 - t)} \frac {M _ {1}}{m _ {1}},
$$

where we used Lemma D.5.

For second moment, we have

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \leq 4 \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| ^ {2} \mid X _ {t} = x ].
$$

Recall $\| \operatorname{grad}_x \log J_t(x \mid x_1) \| \leq \frac{2(d - 1)}{(1 - t) \sin u}$ , using Lemma D.5,

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| ^ {2} \mid X _ {t} = x ] \leq \frac {4 (d - 1) ^ {2}}{(1 - t) ^ {2}} \mathbb {E} \Bigl [ \frac {1}{\sin^ {2} u} \mid X _ {t} = x \Bigr ] \leq \frac {8 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Hence

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \leq \frac {3 2 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Lemma D.7 (Moment bounds for $\partial_t\log p_t(X_1\mid x).$ ).We have

$$
\mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \right| \mid X _ {t} = x \right] \leq \frac {2}{1 - t} + 4 \pi \frac {d - 1}{1 - t} \frac {M _ {1}}{m _ {1}},
$$

$$
\mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \right| ^ {2} \mid X _ {t} = x \right] \leq \frac {8}{(1 - t) ^ {2}} + \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Proof. Let

$$
Z _ {t} (x) = \int_ {S ^ {d}} p _ {1} (z) J _ {t} (x \mid z) d V _ {g} (z),
$$

so we have $\log p_t(x_1\mid x) = \log p_1(x_1) + \log J_t(x\mid x_1) - \log Z_t(x)$ . Since $p_1$ does not depend on $t$ ,

$$
\frac {\partial}{\partial t} \log p _ {t} (x _ {1} \mid x) = \frac {\partial}{\partial t} \log J _ {t} (x \mid x _ {1}) - \frac {\partial}{\partial t} \log Z _ {t} (x).
$$

Moreover, for $d \geq 2$ the function $\partial_t J_t(x \mid z)$ is integrable against $p_1(z)dV_g(z)$ , and the map $t \mapsto Z_t(x)$ is $C^1$ with

$$
\frac {\partial}{\partial t} Z _ {t} (x) = \int_ {S ^ {d}} p _ {1} (z) \frac {\partial}{\partial t} J _ {t} (x \mid z) d V _ {g} (z) = \int_ {S ^ {d}} p _ {1} (z) J _ {t} (x \mid z) \frac {\partial}{\partial t} \log J _ {t} (x \mid z) d V _ {g} (z).
$$

Dividing by $Z_{t}(x)$ yields

$$
\frac {\partial}{\partial t} \log Z _ {t} (x) = \int_ {S ^ {d}} \frac {\partial}{\partial t} \log J _ {t} (x | z) p _ {t} (z | x) d V _ {g} (z) = \mathbb {E} \Big [ \frac {\partial}{\partial t} \log J _ {t} (x | X _ {1}) | X _ {t} = x \Big ].
$$

Therefore

$$
\frac {\partial}{\partial t} \log p _ {t} (x _ {1} \mid x) = \frac {\partial}{\partial t} \log J _ {t} (x \mid x _ {1}) - \mathbb {E} \Big [ \frac {\partial}{\partial t} \log J _ {t} (x \mid X _ {1}) \mid X _ {t} = x \Big ],
$$

and by triangle inequality,

$$
\begin{array}{l} \mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \right| \mid X _ {t} = x \right] \leq 2 \mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log J _ {t} (x \mid X _ {1}) \right| \mid X _ {t} = x \right], \\ \mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \right| ^ {2} \mid X _ {t} = x \right] \leq 4 \mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log J _ {t} (x \mid X _ {1}) \right| ^ {2} \mid X _ {t} = x \right]. \\ \end{array}
$$

We compute $\partial_t\log J_t$ explicitly and bound its conditional expectation. For $r = d(x,x_1) < (1 - t)\pi$

$$
\log J _ {t} (x \mid x _ {1}) = - \log (1 - t) + (d - 1) \left(\log \sin (r / (1 - t)) - \log \sin r\right).
$$

Holding $r$ fixed and differentiating in $t$ gives

$$
\frac {\partial}{\partial t} \log J _ {t} (x \mid x _ {1}) = \frac {1}{1 - t} + (d - 1) \frac {r}{(1 - t) ^ {2}} \cot (r / (1 - t)).
$$

Write $u = r / (1 - t)\in (0,\pi)$ . Then $r = (1 - t)u$ and

$$
\begin{array}{l} \left| \frac {\partial}{\partial t} \log J _ {t} (x \mid x _ {1}) \right| \leq \frac {1}{1 - t} + \frac {d - 1}{1 - t} | u \cot u |, \\ \left| \frac {\partial}{\partial t} \log J _ {t} (x \mid x _ {1}) \right| ^ {2} \leq 2 \frac {1}{(1 - t) ^ {2}} + 2 \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} | u \cot u | ^ {2}. \\ \end{array}
$$

Hence

$$
\begin{array}{l} \mathbb {E} \Big [ \Big | \frac {\partial}{\partial t} \log J _ {t} (x \mid X _ {1}) \Big | \mid X _ {t} = x \Big ] \leq \frac {1}{1 - t} + \pi \frac {d - 1}{1 - t} \frac {2 M _ {1}}{m _ {1}}, \\ \mathbb {E} \Big [ \left| \frac {\partial}{\partial t} \log J _ {t} (x \mid X _ {1}) \right| ^ {2} \mid X _ {t} = x \Big ] \leq \frac {2}{(1 - t) ^ {2}} + \frac {2 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {2 M _ {1}}{m _ {1}}. \\ \end{array}
$$

where we used $|u\cot u|\leq \frac{\pi}{\sin u}$ . Consequently,

$$
\begin{array}{l} \mathbb {E} \Big [ \Big | \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \Big | \mid X _ {t} = x \Big ] \leq \frac {2}{1 - t} + 4 \pi \frac {d - 1}{1 - t} \frac {M _ {1}}{m _ {1}}, \\ \mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \right| ^ {2} \mid X _ {t} = x \right] \leq \frac {8}{(1 - t) ^ {2}} + \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Lemma D.8. We have

$$
\mathbb {E} \big [ \| \nabla_ {x} ^ {2} \log p _ {t} (X _ {1} \mid x) \| _ {\mathrm {o p}} \mid X _ {t} = x \big ] \leq \frac {6 4 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}},
$$

Proof. Recall that

$$
\operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) = \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) - \operatorname {g r a d} _ {x} \log Z _ {t} (x),
$$

Take derivative again, we obtain

$$
\nabla \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) = \nabla \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) - \nabla \operatorname {g r a d} _ {x} \log Z _ {t} (x),
$$

Recall

$$
\operatorname {g r a d} _ {x} \log Z _ {t} (x) = \mathbb {E} \big [ \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \mid X _ {t} = x \big ].
$$

Hence

$$
\begin{array}{l} \nabla_ {u} \operatorname {g r a d} _ {x} \log Z _ {t} (x) = \nabla_ {u} \mathbb {E} \left[ \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \mid X _ {t} = x \right] \\ = \mathbb {E} \left[ \nabla_ {u} \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \mid X _ {t} = x \right] + \mathbb {E} \left[ \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \nabla_ {u} \log p _ {t} (x _ {1} \mid x) \mid X _ {t} = x \right], \\ \end{array}
$$

and we can bound

$$
\begin{array}{l} \| \nabla \operatorname {g r a d} _ {x} \log Z _ {t} (x) \| _ {\mathrm {o p}} \\ \leq \mathbb {E} \left[ \| \nabla^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\text {o p}} \mid X _ {t} = x \right] \\ + \sqrt {\mathbb {E} \left[ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| ^ {2} \mid X _ {t} = x \right] \mathbb {E} \left[ \| \nabla \log p _ {t} (x _ {1} \mid x) \| ^ {2} \mid X _ {t} = x \right]} \\ \leq \mathbb {E} \left[ \| \nabla^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\mathrm {o p}} \mid X _ {t} = x \right] + \frac {1 6 (d - 1) ^ {2} M _ {1}}{(1 - t) ^ {2} m _ {1}}. \\ \end{array}
$$

To control $\| \nabla^2\log J_t(x\mid X_1)\|_{\mathrm{op}}$ , we consider

$$
\begin{array}{l} \frac {\partial^ {2}}{\partial r ^ {2}} \log J _ {t} (x \mid X _ {1}) = \frac {\partial}{\partial r} (d - 1) (\frac {1}{1 - t} \cot \frac {r}{1 - t} - \cot r) = (d - 1) (- \frac {1}{(1 - t) ^ {2}} \frac {1}{\sin^ {2} \frac {r}{1 - t}} + \frac {1}{\sin^ {2} r}) \\ = (d - 1) \left(\frac {1}{\sin^ {2} (1 - t) u} - \frac {1}{(1 - t) ^ {2}} \frac {1}{\sin^ {2} u}\right). \\ \end{array}
$$

Applying Lemma D.4 with $\phi = \log J_t(r)$ , we have

$$
\begin{array}{l} \| \nabla \operatorname {g r a d} \log J _ {t} (r) \| _ {\mathrm {o p}} \leq | \log J _ {t} ^ {\prime} (r (x)) | \| \nabla \operatorname {g r a d} r (x) \| _ {\mathrm {o p}} + | \log J _ {t} ^ {\prime \prime} (r (x)) | \\ \leq | \log J _ {t} ^ {\prime} (r (x)) | \cot r + | \log J _ {t} ^ {\prime \prime} (r (x)) |, \\ \end{array}
$$

where $\| \nabla \operatorname{grad} r(x) \|_{\mathrm{op}} \leq |\cot r|$ by Lee (2018, Proposition 11.3)

Now using

$$
\frac {\partial}{\partial r} \log J _ {t} (x \mid X _ {1}) = (d - 1) (\frac {1}{1 - t} \cot \frac {r}{1 - t} - \cot r),
$$

$$
\frac {\partial^ {2}}{\partial r ^ {2}} \log J _ {t} (x \mid X _ {1}) = (d - 1) (\frac {1}{\sin^ {2} (1 - t) u} - \frac {1}{(1 - t) ^ {2}} \frac {1}{\sin^ {2} u}),
$$

we obtain

$$
\| \nabla^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\mathrm {o p}} \leq \frac {4 (d - 1)}{(1 - t) ^ {2} \sin^ {2} u},
$$

hence

$$
\mathbb {E} [ \| \nabla^ {2} \log J _ {t} (x \mid X _ {1}) \| \mid X _ {t} = x ] \leq \frac {1 6 (d - 1)}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Now we bound $\mathbb{E}[\| \nabla_x^2\log p_t(X_1\mid x)\|_{\mathrm{op}}\mid X_t = x]$ . Recall

$$
\nabla \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) = \nabla \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) - \nabla \operatorname {g r a d} _ {x} \log Z _ {t} (x),
$$

$$
\| \nabla \operatorname {g r a d} _ {x} \log Z _ {t} (x) \| _ {\mathrm {o p}} \leq \mathbb {E} \big [ \| \nabla^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\mathrm {o p}} \mid X _ {t} = x \big ] + \frac {1 6 (d - 1) ^ {2} M _ {1}}{(1 - t) ^ {2} m _ {1}}.
$$

By triangle inequality, we obtain

$$
\mathbb {E} \big [ \| \nabla_ {x} ^ {2} \log p _ {t} (X _ {1} \mid x) \| _ {\mathrm {o p}} \mid X _ {t} = x \big ] \leq 2 \mathbb {E} \big [ \| \nabla_ {x} ^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\mathrm {o p}} \mid X _ {t} = x \big ] + \frac {1 6 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Finally, using the bound

$$
\mathbb {E} \left[ \| \nabla_ {x} ^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\mathrm {o p}} \mid X _ {t} = x \right] \leq \frac {1 6 (d - 1)}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}},
$$

we conclude

$$
\mathbb {E} \big [ \| \nabla_ {x} ^ {2} \log p _ {t} (X _ {1} \mid x) \| _ {\mathrm {o p}} \mid X _ {t} = x \big ] \leq \frac {3 2 (d - 1)}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} + \frac {1 6 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} <   \frac {6 4 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Lemma D.9. We have

$$
\mathbb {E} [ \| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x ] \leq \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Proof. We have

$$
\begin{array}{l} \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) = \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) - \operatorname {g r a d} _ {x} \log Z _ {t} (x) \\ = \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) - \mathbb {E} \left[ \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \mid X _ {t} = x \right], \\ \end{array}
$$

so we have

$$
\begin{array}{l} \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {t} \left(x _ {1} \mid x\right) \right\| \leq \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} \left(x \mid x _ {1}\right) \right\| + \mathbb {E} \left[ \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} \left(x \mid X _ {1}\right) \right\| \mid X _ {t} = x \right] \\ + \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| | \partial_ {t} \log p _ {t} (X _ {1} \mid x) | \mid X _ {t} = x ]. \\ \end{array}
$$

A direct differentiation at fixed $r$ gives

$$
\begin{array}{l} \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \right\| = \left\| \partial_ {t} \frac {\partial}{\partial r} \log J _ {t} (r) \operatorname {g r a d} r (x) \right\| = (d - 1) \left\| \partial_ {t} \frac {1}{1 - t} \cot u - \cot ((1 - t) u) \right\| \\ = (d - 1) \left\| \frac {1}{(1 - t) ^ {2}} \cot u - \frac {u}{\sin^ {2} (1 - t) u} \right\| \\ \end{array}
$$

$$
\leq \frac {d - 1}{(1 - t) ^ {2}} \frac {2 \pi}{\sin^ {2} u}.
$$

Taking expectation and using $\mathbb{E}[1 / \sin^a u] \leq 2M_1 / m_1$ for $a = 1, 2$ ,

$$
\mathbb {E} [ \| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| \mid X _ {t} = x ] \leq \frac {4 \pi (d - 1)}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}},
$$

Recall that

$$
\begin{array}{l} \mathbb {E} \left[ \left| \partial_ {t} \log p _ {t} (X _ {1} \mid x) \right| ^ {2} \mid X _ {t} = x \right] \leq 4 \mathbb {E} \left[ \left| \partial_ {t} \log J _ {t} \right| ^ {2} \mid X _ {t} = x \right] \\ \leq 4 \mathbb {E} \Big [ \frac {(d - 1) ^ {2} \pi^ {2}}{(1 - t) ^ {2}} \frac {1}{\sin^ {2} u} \mid X _ {t} = x \Big ] \leq \frac {8 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Together with $\| \operatorname{grad}_x \log J_t(x \mid x_1) \| \leq \frac{2(d - 1)}{(1 - t) \sin u}$ , by Cauchy-Schwarz,

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| | \partial_ {t} \log p _ {t} (X _ {1} \mid x) | \mid X _ {t} = x ] \\ \leq \left(\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| ^ {2} \mid X _ {t} = x ]\right) ^ {1 / 2} \left(\mathbb {E} [ | \partial_ {t} \log p _ {t} (X _ {1} \mid x) | ^ {2} \mid X _ {t} = x ]\right) ^ {1 / 2} \\ \leq \sqrt {\frac {8 \pi (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} \frac {8 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}} \leq \frac {8 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Thus

$$
\mathbb {E} [ \| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x ] \leq \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

# D.2 Regularity for Flow Matching Vector Field

In this section, we show that both the spatial derivative (Lemma D.10) and time derivative (Lemma D.11) of $v(t,x)$ are uniformly bounded.

Lemma D.10. Assume $d \geq 3$ and $t \in (0,1)$ . Let $p_1$ be a smooth density on $S^d$ such that

$$
0 <   m _ {1} \leq p _ {1} (z) \leq M _ {1} <   \infty .
$$

For all unit tangent vector $w$ , we have

$$
\| \nabla_ {w} v (t, x) \| \leq \frac {1 2 \pi M _ {1} (d - 1)}{m _ {1} (1 - t)}.
$$

Hence $v(t,x)$ is $L$ -Lipschitz with $L = \frac{12\pi M_1(d - 1)}{m_1(1 - t)}$ .

Proof. Fix $t < 1$ and $x \in M$ , and let $w \in T_xM$ be a unit tangent vector. We consider the covariant derivative of $v$ in the direction $w$ :

$$
\nabla_ {w} v (t, x) = \frac {1}{1 - t} \nabla_ {w} \int_ {M} \mathrm {L o g} _ {x} (x _ {1}) p _ {t} (x _ {1} | x) d V _ {g} (x _ {1})
$$

$$
\begin{array}{l} = \frac {1}{1 - t} \int_ {M} \nabla_ {w} \left(\operatorname {L o g} _ {x} \left(x _ {1}\right)\right) p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right) \\ + \frac {1}{1 - t} \int_ {M} \operatorname {L o g} _ {x} (x _ {1}) \left\langle \operatorname {g r a d} _ {x} p _ {t} (x _ {1} | x), w \right\rangle d V _ {g} (x _ {1}). \\ \end{array}
$$

Define

$$
P (t, x) := \frac {1}{1 - t} \int_ {S ^ {d}} \operatorname {L o g} _ {x} (x _ {1}) \langle \operatorname {g r a d} _ {x} p _ {t} (x _ {1} \mid x), w \rangle d V _ {g} (x _ {1}),
$$

$$
G (t, x) := \frac {1}{1 - t} \int_ {S ^ {d}} \| \nabla_ {w} \operatorname {L o g} _ {x} (x _ {1}) \| p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}).
$$

We show that $\| P(t,x)\| \leq \frac{8\pi M_1(d - 1)}{m_1(1 - t)}, \forall \| w\| = 1$ . We first write $\| P(t,x)\|$ as a conditional moment of $\| \operatorname{grad}_x\log p_t\|$ . Using $\operatorname{grad}_x p_t = p_t \operatorname{grad}_x\log p_t$ and $\| \operatorname{Log}_x(x_1)\| = d(x,x_1)$ ,

$$
\begin{array}{l} \| P (t, x) \| \leq \frac {1}{1 - t} \int_ {S ^ {d}} \| \operatorname {L o g} _ {x} (x _ {1}) \| \| \operatorname {g r a d} _ {x} p _ {t} (x _ {1} \mid x) \| d V _ {g} (x _ {1}) \\ = \frac {1}{1 - t} \int_ {S ^ {d}} \| \operatorname {L o g} _ {x} (x _ {1}) \| p _ {t} (x _ {1} \mid x) \| \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) \| d V _ {g} (x _ {1}) \\ = \frac {1}{1 - t} \mathbb {E} \left[ \| \operatorname {L o g} _ {x} (X _ {1}) \| \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x \right]. \\ \end{array}
$$

On the support of $p_t(\cdot \mid x)$ we have $d(x, X_1) < (1 - t)\pi$ , hence

$$
\| \operatorname {L o g} _ {x} (X _ {1}) \| \leq (1 - t) \pi ,
$$

so

$$
\| P (t, x) \| \leq \pi \mathbb {E} \left[ \| \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right) \| \mid X _ {t} = x \right].
$$

Using Lemma D.6,

$$
\| P (t, x) \| \leq \frac {8 \pi M _ {1} (d - 1)}{m _ {1} (1 - t)}.
$$

Next, we show that $G(t,x) \leq 4\pi \frac{M_1}{m_1(1 - t)}$ .

Notice that $\nabla_w\operatorname{Log}_x(x_1)$ can be related to a Hessian. Denote $r = d(x,x_1)\in (0,\pi)$ , it is easy to show (see, for example, Alimisis et al. (2020, Appendix B, Proof of Lemma 2))

$$
\left\| \nabla_ {w} \operatorname {L o g} _ {x} (x _ {1}) \right\| \leq 1 + | r \cot (r) |.
$$

Now we bound the cot term. On the support of $p_t(\cdot \mid x)$ we have $r < (1 - t)\pi$ . Let $u = r / (1 - t) \in (0,\pi)$ , so $r = (1 - t)u$ . Using $|\cot r| \leq 1 / \sin r$ and the concavity bound $\sin ((1 - t)u) \geq (1 - t)\sin u$ ,

$$
\left| r \cot r \right| \leq \frac {r}{\sin r} = \frac {(1 - t) u}{\sin ((1 - t) u)} \leq \frac {(1 - t) u}{(1 - t) \sin u} = \frac {u}{\sin u} \leq \frac {\pi}{\sin u}.
$$

Therefore for $r < (1 - t)\pi$

$$
\left\| \nabla_ {w} \operatorname {L o g} _ {x} \left(x _ {1}\right) \right\| \leq 1 + \frac {\pi}{\sin u} <   \frac {2 \pi}{\sin u}.
$$

Using the same technique as before,

$$
\int_ {S ^ {d}} \| \nabla_ {w} \operatorname {L o g} _ {x} (x _ {1}) \| p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}) \leq 4 \pi \frac {M _ {1}}{m _ {1}}.
$$

We conclude that Multiplying by $(1 - t)^{-1}$ yields

$$
G (t, x) \leq 4 \pi \frac {M _ {1}}{m _ {1} (1 - t)}.
$$

Lemma D.11. Fix $d \geq 3$ and $t \in (0,1)$ . Let $p_1$ be a smooth density on $S^d$ satisfying

$$
0 <   m _ {1} \leq p _ {1} (z) \leq M _ {1} <   \infty .
$$

For

$$
v (t, x) = \frac {1}{1 - t} \int_ {S ^ {d}} \operatorname {L o g} _ {x} (x _ {1}) p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}),
$$

we have for every $x\in S^d$

$$
\left\| \frac {d}{d t} v (t, x) \right\| \leq \frac {3 \pi}{1 - t} + \frac {4 \pi^ {2} d}{1 - t} \frac {M _ {1}}{m _ {1}} \leq \frac {8 \pi^ {2} d}{1 - t} \frac {M _ {1}}{m _ {1}}.
$$

Proof. Observe that on the support of $p_t(\cdot \mid x)$ we have $d(x,x_1) < (1 - t)\pi$ , hence

$$
\left\| \operatorname {L o g} _ {x} (x _ {1}) \right\| = d (x, x _ {1}) \leq (1 - t) \pi .
$$

Therefore

$$
\| v (t, x) \| \leq \frac {1}{1 - t} \int_ {S ^ {d}} \| \operatorname {L o g} _ {x} (x _ {1}) \| p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}) \leq \frac {1}{1 - t} (1 - t) \pi = \pi .
$$

We differentiate $v(t,x)$ in $t$ . Since $\operatorname{Log}_x(x_1)$ does not depend on $t$ ,

$$
\begin{array}{l} \frac {d}{d t} v (t, x) = \frac {d}{d t} \left(\frac {1}{1 - t}\right) \int_ {S ^ {d}} \operatorname {L o g} _ {x} \left(x _ {1}\right) p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right) + \frac {1}{1 - t} \int_ {S ^ {d}} \operatorname {L o g} _ {x} \left(x _ {1}\right) \frac {\partial}{\partial t} p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right) \\ = \frac {1}{(1 - t) ^ {2}} \int_ {S ^ {d}} \mathrm {L o g} _ {x} (x _ {1}) p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}) + \frac {1}{1 - t} \int_ {S ^ {d}} \mathrm {L o g} _ {x} (x _ {1}) \frac {\partial}{\partial t} p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}). \\ \end{array}
$$

Using

$$
\int_ {S ^ {d}} \operatorname {L o g} _ {x} (x _ {1}) p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}) = (1 - t) v (t, x),
$$

we have

$$
\frac {d}{d t} v (t, x) = \frac {1}{1 - t} v (t, x) + \frac {1}{1 - t} \int_ {S ^ {d}} \mathrm {L o g} _ {x} (x _ {1}) \frac {\partial}{\partial t} p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}).
$$

Since $\int_{S^d} p_t(x_1 \mid x) dV_g(x_1) = 1$ , we have

$$
\int_ {S ^ {d}} \frac {\partial}{\partial t} p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}) = 0.
$$

Also, wherever $p_t(x_1 \mid x) > 0$ ,

$$
\frac {\partial}{\partial t} p _ {t} \left(x _ {1} \mid x\right) = p _ {t} \left(x _ {1} \mid x\right) \frac {\partial}{\partial t} \log p _ {t} \left(x _ {1} \mid x\right).
$$

Hence

$$
\begin{array}{l} \left\| \int_ {S ^ {d}} \operatorname {L o g} _ {x} (x _ {1}) \frac {\partial}{\partial t} p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}) \right\| \leq \int_ {S ^ {d}} \| \operatorname {L o g} _ {x} (x _ {1}) \| p _ {t} (x _ {1} \mid x) \left| \frac {\partial}{\partial t} \log p _ {t} (x _ {1} \mid x) \right| d V _ {g} (x _ {1}) \\ \leq (1 - t) \pi \mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \right| \mid X _ {t} = x \right]. \\ \end{array}
$$

Therefore

$$
\left\| \frac {d}{d t} v (t, x) \right\| \leq \frac {\pi}{1 - t} + \pi \mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \right| \mid X _ {t} = x \right].
$$

Using Lemma D.7,

$$
\begin{array}{l} \left\| \frac {d}{d t} v (t, x) \right\| \leq \frac {\pi}{1 - t} + \pi \mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} \left(X _ {1} \mid x\right) \right| \mid X _ {t} = x \right] \\ \leq \frac {\pi}{1 - t} + 2 \pi \left(\frac {1}{1 - t} + \frac {d - 1}{1 - t} \frac {2 \pi M _ {1}}{m _ {1}}\right) \leq \frac {1}{1 - t} (3 \pi + 4 \pi^ {2} \frac {d M _ {1}}{m _ {1}}). \\ \end{array}
$$

![](images/48c4f024d8f0f2b91b32e381ead8229dcc191590c4ba735c95912503ce9bb0db.jpg)

# D.3 Regularity for Divergence

In this section, we show that both the gradient (Lemma D.12) and the time derivative (Lemma D.13) of $\operatorname{div} v(t,x)$ are uniformly bounded.

Lemma D.12. Assume $d \geq 3$ and $t \in (0,1)$ . Let $p_1$ be a smooth density on $S^d$ such that

$$
0 <   m _ {1} \leq p _ {1} (z) \leq M _ {1} <   \infty .
$$

Then for every $x \in S^d$ we have

$$
\| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| \leq \frac {1 2 8 \pi (d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}}.
$$

Proof. Write

$$
v (t, x) = \frac {1}{1 - t} \int_ {S ^ {d}} \operatorname {L o g} _ {x} (x _ {1}) p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}).
$$

Using $\operatorname{div}(fW) = \langle \operatorname{grad} f, W \rangle + f \operatorname{div} W$ with $f = p_t(\cdot \mid x)$ and $W = \operatorname{Log}_x(\cdot)$ ,

$$
\begin{array}{l} \operatorname {d i v} v (t, x) = \frac {1}{1 - t} \int_ {S ^ {d}} \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(x _ {1}\right) p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right) \\ + \frac {1}{1 - t} \int_ {S ^ {d}} \left\langle \operatorname {g r a d} _ {x} p _ {t} \left(x _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(x _ {1}\right) \right\rangle d V _ {g} \left(x _ {1}\right) \\ = \frac {1}{1 - t} \mathbb {E} [ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) \mid X _ {t} = x ] \\ \end{array}
$$

$$
+ \frac {1}{1 - t} \mathbb {E} [ \langle \mathrm {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \mathrm {L o g} _ {x} (X _ {1}) \rangle \mid X _ {t} = x ].
$$

Differentiate this identity in $x$ along a unit vector $\xi \in T_x S^d$ and take norms. We take gradient, and obtain (for a smooth integrand $F(x, x_1)$ ),

$$
\operatorname {g r a d} _ {x} \mathbb {E} [ F (x, X _ {1}) \mid X _ {t} = x ] = \mathbb {E} [ \operatorname {g r a d} _ {x} F (x, X _ {1}) \mid X _ {t} = x ] + \mathbb {E} [ F (x, X _ {1}) \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \mid X _ {t} = x ].
$$

Applying this formula and using triangle inequality yields

$$
\| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| \leq \frac {1}{1 - t} \Big (T _ {1} + T _ {2} + T _ {3} + T _ {4} \Big),
$$

where

$$
\begin{array}{l} T _ {1} = \mathbb {E} [ \| \operatorname {g r a d} _ {x} \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) \| | X _ {t} = x ], \\ T _ {2} = \mathbb {E} [ | \operatorname {d i v} _ {x} \log_ {x} (X _ {1}) | \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x ], \\ T _ {3} = \mathbb {E} [ \| \operatorname {g r a d} _ {x} \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \| \mid X _ {t} = x ], \\ T _ {4} = \mathbb {E} [ | \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle | \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x ]. \\ \end{array}
$$

Now we compute $\operatorname{div}_x \operatorname{Log}_x(x_1)$ and its $x$ -gradient. Let $r = d(x, x_1) \in (0, \pi)$ . Notice that

$$
\operatorname {L o g} _ {x} (x _ {1}) = - \operatorname {g r a d} _ {x} \frac {1}{2} r ^ {2},
$$

hence

$$
\operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (x _ {1}) = - \operatorname {d i v} _ {x} (r \operatorname {g r a d} r) = - r \Delta r - \langle \operatorname {g r a d} r, \operatorname {g r a d} r \rangle = - (d - 1) r \cot r - 1,
$$

where we used $\Delta r = (d - 1)\cot r$ (see for example (Lee, 2018, Theorem 11.11)) and $\| \operatorname{grad} r\|^2 = 1$ .

Differentiate in $x$ using that $r$ is a radial function and $\| \operatorname{grad} r \| = 1$ :

$$
\operatorname {g r a d} _ {x} \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (x _ {1}) = - (d - 1) \big (\cot r - r \csc^ {2} r \big) \operatorname {g r a d} _ {x} r,
$$

which implies

$$
\| \operatorname {g r a d} _ {x} \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (x _ {1}) \| = (d - 1) \big | \cot r - r \csc^ {2} r \big | = (d - 1) \big | \cot r - r \frac {1}{\sin^ {2} r} \big |.
$$

We bound $T_{1} = \mathbb{E}[\| \operatorname{grad}_{x}\operatorname{div}_{x}\operatorname{Log}_{x}(X_{1})\| \mid X_{t} = x]$ . Using $r = (1 - t)u$ and $\sin ((1 - t)u) \geq (1 - t)\sin u$ (concavity of $\sin$ on $[0,\pi ]$ ),

$$
| \cot r | \leq \frac {1}{\sin r} \leq \frac {1}{(1 - t) \sin u}, \qquad r \frac {1}{\sin^ {2} r} \leq \frac {(1 - t) \pi}{\sin^ {2} r} \leq \frac {\pi}{(1 - t) \sin^ {2} u}.
$$

Hence

$$
\| \operatorname {g r a d} _ {x} \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (x _ {1}) \| \leq (d - 1) \left(\frac {1}{(1 - t) \sin u} + \frac {\pi}{(1 - t) \sin^ {2} u}\right).
$$

Therefore

$$
T _ {1} \leq (d - 1) \frac {1}{1 - t} \frac {M _ {1}}{m _ {1}} (2 \pi + 2).
$$

We bound $T_{2} = \mathbb{E}[|\operatorname{div}_{x}\operatorname{Log}_{x}(X_{1})||\operatorname{grad}_{x}\log p_{t}(X_{1}|x)|||X_{t} = x]$ . Recall $|\operatorname{div}_{x}\operatorname{Log}_{x}(x_{1})| \leq 1 + (d - 1)r|\cot r|$ , so we have

$$
| \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (x _ {1}) | \leq 1 + (d - 1) \pi \frac {1}{\sin r} \leq 1 + (d - 1) \pi \frac {1}{(1 - t) \sin u}.
$$

Thus by Cauchy-Schwarz,

$$
T _ {2} \leq \left(\mathbb {E} [ | \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) | ^ {2} \mid X _ {t} = x ]\right) ^ {1 / 2} \left(\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ]\right) ^ {1 / 2}.
$$

Using $(a + b)^2\leq 2a^2 +2b^2$

$$
\begin{array}{l} \mathbb {E} \left[ \left| \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(X _ {1}\right) \right| ^ {2} \mid X _ {t} = x \right] \leq 2 + 2 (d - 1) ^ {2} \pi^ {2} \frac {1}{(1 - t) ^ {2}} \mathbb {E} \left[ \frac {1}{\sin^ {2} u} \mid X _ {t} = x \right] \\ \leq 2 + 2 (d - 1) ^ {2} \pi^ {2} \frac {1}{(1 - t) ^ {2}} \frac {2 M _ {1}}{m _ {1}}. \\ \end{array}
$$

Also recall

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \leq \frac {3 2 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Hence we obtain

$$
\begin{array}{l} T _ {2} \leq (2 + 2 (d - 1) ^ {2} \pi^ {2} \frac {1}{(1 - t) ^ {2}} \frac {2 M _ {1}}{m _ {1}}) ^ {\frac {1}{2}} \left(\frac {3 2 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}\right) ^ {\frac {1}{2}} \\ \leq \frac {1 6 \pi M _ {1}}{m _ {1}} \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}}. \\ \end{array}
$$

We bound $T_{3} = \mathbb{E}[\| \operatorname{grad}_{x}\langle \operatorname{grad}_{x}\log p_{t}(X_{1}\mid x),\operatorname{Log}_{x}(X_{1})\rangle \| \mid X_{t} = x]$ . We use the product rule: denote $g(x) = \langle g_1(x),g_2(x)\rangle$ . For $g_{1},g_{2}$ , we have (viewing as directional derivative along $u$ and use compatibility)

$$
\langle \operatorname {g r a d} _ {x} \langle g _ {1} (x), g _ {2} (x) \rangle , u \rangle = \nabla_ {u} \langle g _ {1} (x), g _ {2} (x) \rangle = \langle \nabla_ {u} g _ {1} (x), g _ {2} (x) \rangle + \langle g _ {1} (x), \nabla_ {u} g _ {2} (x) \rangle .
$$

Hence we can write

$$
\begin{array}{l} \| \operatorname {g r a d} _ {x} \langle \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x), \operatorname {L o g} _ {x} (x _ {1}) \rangle \| \\ = \| \nabla \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) \| _ {\mathrm {o p}} \| \operatorname {L o g} _ {x} (x _ {1}) \| + \| \nabla \operatorname {L o g} _ {x} (x _ {1}) \| _ {\mathrm {o p}} \| \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) \|, \\ \end{array}
$$

so

$$
\begin{array}{l} T _ {3} \leq \mathbb {E} \left[ \| \nabla \log_ {x} (X _ {1}) \| \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x \right] \\ + \mathbb {E} [ \| \nabla^ {2} \log p _ {t} (X _ {1} \mid x) \| \| \log_ {x} (X _ {1}) \| \mid X _ {t} = x ]. \\ \end{array}
$$

On the support of $p_t(\cdot \mid x)$ , $\| \operatorname{Log}_x(X_1) \| \leq (1 - t)\pi$ , hence

$$
\mathbb {E} [ \| \nabla^ {2} \log p _ {t} (X _ {1} \mid x) \| \| \operatorname {L o g} _ {x} (X _ {1}) \| | X _ {t} = x ] \leq (1 - t) \pi \mathbb {E} [ \| \nabla^ {2} \log p _ {t} (X _ {1} \mid x) \| | X _ {t} = x ].
$$

By Lemma D.8,

$$
\mathbb {E} [ \| \nabla^ {2} \log p _ {t} (X _ {1} \mid x) \| \| \log_ {x} (X _ {1}) \| \mid X _ {t} = x ] \leq \frac {6 4 \pi (d - 1) ^ {2}}{1 - t} \frac {M _ {1}}{m _ {1}}.
$$

Also, on $S^d$

$$
\left\| \nabla \operatorname {L o g} _ {x} \left(x _ {1}\right) \right\| \leq 1 + r | \cot r | <   \pi \frac {2}{(1 - t) \sin u},
$$

so by Cauchy-Schwarz inequality,

$$
\begin{array}{l} \mathbb {E} [ \| \nabla \operatorname {L o g} _ {x} (X _ {1}) \| \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x ] \leq \left(\frac {3 2 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} \frac {8 \pi^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}\right) ^ {\frac {1}{2}} \\ \leq \frac {1 6 \pi M _ {1}}{m _ {1}} \frac {(d - 1)}{(1 - t) ^ {2}}. \\ \end{array}
$$

Hence we get

$$
T _ {3} \leq \frac {1 6 \pi M _ {1}}{m _ {1}} \frac {(d - 1)}{(1 - t) ^ {2}} + \frac {6 4 \pi (d - 1) ^ {2}}{1 - t} \frac {M _ {1}}{m _ {1}} \leq \frac {6 4 \pi M _ {1}}{m _ {1}} \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}}.
$$

We bound $T_{4} = \mathbb{E}[|\langle \operatorname{grad}_{x}\log p_{t}(X_{1}\mid x),\operatorname{Log}_{x}(X_{1})\rangle |\parallel \operatorname{grad}_{x}\log p_{t}(X_{1}\mid x)\parallel |X_{t} = x]$ . We have

$$
\begin{array}{l} T _ {4} \leq \mathbb {E} [ \| \log_ {x} (X _ {1}) \| \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \\ \leq (1 - t) \pi \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \\ \leq (1 - t) \pi \cdot \frac {3 2 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} = \frac {3 2 \pi (d - 1) ^ {2}}{1 - t} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Together,

$$
\begin{array}{l} \| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| \\ \leq \frac {1}{1 - t} \left(T _ {1} + T _ {2} + T _ {3} + T _ {4}\right) \\ \leq \frac {1}{(1 - t)} \frac {M _ {1}}{m _ {1}} \left(\left(d - 1\right) \frac {1}{1 - t} (2 \pi + 2) + 1 6 \pi \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} + 6 4 \pi \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} + \frac {3 2 \pi (d - 1) ^ {2}}{1 - t}\right) \\ \leq \frac {1 2 8 \pi (d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Lemma D.13. Assume $d \geq 3$ and $t \in (0,1)$ . Let $p_1$ be a smooth density on $S^d$ such that

$$
0 <   m _ {1} \leq p _ {1} (z) \leq M _ {1} <   \infty .
$$

Then for every $x \in S^d$ ,

$$
\left| \frac {d}{d t} \operatorname {d i v} v (t, x) \right| \leq \frac {1 2 8 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}}.
$$

Proof. We start by computing the time derivative of divergence. Recall

$$
\operatorname {d i v} v (t, x) = \frac {1}{1 - t} \mathbb {E} [ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) \mid X _ {t} = x ] + \frac {1}{1 - t} \mathbb {E} [ \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \mid X _ {t} = x ].
$$

Let $F(t, x_1)$ be smooth in $t$ and integrable under $p_t(\cdot \mid x)$ . Then

$$
\frac {d}{d t} \mathbb {E} [ F (t, X _ {1}) \mid X _ {t} = x ] = \mathbb {E} [ \partial_ {t} F (t, X _ {1}) \mid X _ {t} = x ] + \mathbb {E} [ F (t, X _ {1}) \partial_ {t} \log p _ {t} (X _ {1} \mid x) \mid X _ {t} = x ].
$$

Applying this with $F(t,x_1) = \operatorname{div}_x\operatorname{Log}_x(x_1)$ and $F(t,x_1) = \langle \operatorname{grad}_x\log p_t(x_1\mid x),\operatorname{Log}_x(x_1)\rangle$ respectively,

$$
\begin{array}{l} \frac {d}{d t} \mathbb {E} [ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) \mid X _ {t} = x ] = \mathbb {E} [ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) \partial_ {t} \log p _ {t} (X _ {1} \mid x) \mid X _ {t} = x ], \\ \frac {d}{d t} \mathbb {E} [ \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \mid X _ {t} = x ] = \mathbb {E} [ \partial_ {t} \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \mid X _ {t} = x ] \\ + \mathbb {E} [ \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \partial_ {t} \log p _ {t} \left(X _ {1} \mid x\right) \mid X _ {t} = x ]. \\ \end{array}
$$

Therefore, for fixed $x$ ,

$$
\begin{array}{l} \frac {d}{d t} \operatorname {d i v} v (t, x) = \frac {1}{(1 - t) ^ {2}} \mathbb {E} \left[ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(X _ {1}\right) + \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \mid X _ {t} = x \right] \\ + \frac {1}{1 - t} \mathbb {E} \left[ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(X _ {1}\right) \partial_ {t} \log p _ {t} \left(X _ {1} \mid x\right) \mid X _ {t} = x \right] \\ + \frac {1}{1 - t} \mathbb {E} \left[ \partial_ {t} \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \mid X _ {t} = x \right] \\ + \frac {1}{1 - t} \mathbb {E} [ \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \partial_ {t} \log p _ {t} (X _ {1} \mid x) \mid X _ {t} = x ]. \\ \end{array}
$$

Define

$$
T _ {1} = \frac {1}{(1 - t) ^ {2}} \mathbb {E} \big [ | \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) + \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle | \mid X _ {t} = x \big ],
$$

$$
T _ {2} = \frac {1}{1 - t} \mathbb {E} [ | \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) \partial_ {t} \log p _ {t} (X _ {1} \mid x) | | X _ {t} = x ],
$$

$$
T _ {3} = \frac {1}{1 - t} \mathbb {E} [ | \partial_ {t} \langle \mathrm {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \mathrm {L o g} _ {x} (X _ {1}) \rangle | \mid X _ {t} = x ],
$$

$$
T _ {4} = \frac {1}{1 - t} \mathbb {E} [ | \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \partial_ {t} \log p _ {t} (X _ {1} \mid x) | \mid X _ {t} = x ].
$$

For $T_{1}$ , recall

$$
\begin{array}{l} \frac {1}{(1 - t) ^ {2}} \mathbb {E} \left[ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(X _ {1}\right) \mid X _ {t} = x \right] \leq \frac {1}{(1 - t) ^ {2}} \mathbb {E} \left[ 1 + (d - 1) \pi \frac {1}{(1 - t) \sin u} \mid X _ {t} = x \right] \\ \leq \pi \frac {(d - 1)}{(1 - t) ^ {3}} \frac {2 M _ {1}}{m _ {1}}, \\ \end{array}
$$

and

$$
\begin{array}{l} \frac {1}{(1 - t) ^ {2}} \mathbb {E} \left[ \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \mid X _ {t} = x \right] \\ \leq \frac {1}{(1 - t) ^ {2}} (1 - t) \pi \mathbb {E} \left[ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x \right] \leq \frac {8 \pi (d - 1)}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Hence

$$
T _ {1} \leq \pi \frac {(d - 1)}{(1 - t) ^ {3}} \frac {2 M _ {1}}{m _ {1}} + \frac {8 \pi (d - 1)}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} \leq \frac {1 6 \pi (d - 1)}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}}.
$$

For $T_{2}$ , recall

$$
\mathbb {E} [ | \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) | ^ {2} \mid X _ {t} = x ] \leq 2 + 2 (d - 1) ^ {2} \pi^ {2} \frac {1}{(1 - t) ^ {2}} \frac {2 M _ {1}}{m _ {1}} \leq \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {4 \pi^ {2} M _ {1}}{m _ {1}}.
$$

Hence we have

$$
\begin{array}{l} T _ {2} = \frac {1}{1 - t} \mathbb {E} [ | \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) \partial_ {t} \log p _ {t} (X _ {1} \mid x) | \mid X _ {t} = x ] \\ \leq \frac {1}{1 - t} \left(\mathbb {E} [ | \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (X _ {1}) | ^ {2} \mid X _ {t} = x ] \mathbb {E} [ | \partial_ {t} \log p _ {t} (X _ {1} \mid x) | ^ {2} \mid X _ {t} = x ]\right) ^ {\frac {1}{2}} \\ \leq \frac {1}{1 - t} \Big (\frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {4 \pi^ {2} M _ {1}}{m _ {1}} \frac {3 2 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} \Big) ^ {\frac {1}{2}} \leq \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}}, \\ \end{array}
$$

where by Lemma D.7,

$$
\mathbb {E} \left[ \left| \frac {\partial}{\partial t} \log p _ {t} (X _ {1} \mid x) \right| ^ {2} \mid X _ {t} = x \right] \leq \frac {8}{(1 - t) ^ {2}} + \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} \leq \frac {3 2 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

For $T_{3}$ , since $\operatorname{Log}_x(x_1)$ does not depend on $t$ ,

$$
\begin{array}{l} \left| \partial_ {t} \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(x _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(x _ {1}\right) \right\rangle \right| \\ \leq \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {t} \left(x _ {1} \mid x\right) \right\| \left\| \operatorname {L o g} _ {x} \left(x _ {1}\right) \right\| \leq (1 - t) \pi \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {t} \left(x _ {1} \mid x\right) \right\|. \\ \end{array}
$$

Using Lemma D.9, we have

$$
\mathbb {E} [ \| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x ] \leq \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Hence

$$
\begin{array}{l} \mathbb {E} \left[ \left| \partial_ {t} \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \right| \mid X _ {t} = x \right] \leq (1 - t) \pi \cdot \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} \\ = \frac {1 6 \pi^ {3} (d - 1) ^ {2}}{(1 - t)} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Last, we bound $T_4$ . Similarly, by Cauchy-Schwarz and the bound we did for $T_3$ ,

$$
\begin{array}{l} \left| \mathbb {E} [ \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \partial_ {t} \log p _ {t} (X _ {1} \mid x) \mid X _ {t} = x ] \right| \\ \leq \left(\mathbb {E} [ | \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle | ^ {2} \mid X _ {t} = x ]\right) ^ {1 / 2} \left(\mathbb {E} [ | \partial_ {t} \log p _ {t} (X _ {1} \mid x) | ^ {2} \mid X _ {t} = x ]\right) ^ {1 / 2}. \\ \end{array}
$$

We bound the first factor by

$$
\begin{array}{l} \mathbb {E} [ | \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle | ^ {2} \mid X _ {t} = x ] \\ \leq (1 - t) ^ {2} \pi^ {2} \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \leq 3 2 \pi^ {2} (d - 1) ^ {2} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Therefore

$$
\begin{array}{l} T _ {4} = \frac {1}{1 - t} \left| \mathbb {E} \left[ \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \partial_ {t} \log p _ {t} \left(X _ {1} \mid x\right) \mid X _ {t} = x \right] \right| \\ \leq 3 2 \pi^ {2} \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

Together,

$$
\left| \frac {d}{d t} \operatorname {d i v} v (t, x) \right| \leq T _ {1} + T _ {2} + T _ {3} + T _ {4}
$$

$$
\begin{array}{l} \leq \frac {1 6 \pi (d - 1)}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}} + \frac {1 6 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}} + \frac {1 6 \pi^ {3} (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} + 3 2 \pi^ {2} \frac {(d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}} \\ \leq \frac {1 2 8 \pi^ {2} (d - 1) ^ {2}}{(1 - t) ^ {3}} \frac {M _ {1}}{m _ {1}}. \\ \end{array}
$$

![](images/2834fd03e89af105b88806dae9e22bf730ce61bb5a629a330082d15955925888.jpg)

# D.4 Regularity of $v(t,x)$ and $\log p_t$

Finally, we bound $\| v(t,x) \|$ and $\mathbb{E}[\| \operatorname{grad} \log p_t(X_t) \|^2]$ in Lemma D.14 and D.15.

Lemma D.14. Assume $d \geq 2$ and $t \in (0,1)$ . Let $p_1$ be a smooth density on $S^d$ such that

$$
0 <   m _ {1} \leq p _ {1} (z) \leq M _ {1} <   \infty .
$$

For every $x\in S^d$

$$
\left\| v (t, x) \right\| \leq \pi .
$$

Proof. Fix $x \in S^d$ . By Jensen and the definition of $v$ ,

$$
\| v (t, x) \| = \frac {1}{1 - t} \left\| \int_ {S ^ {d}} \operatorname {L o g} _ {x} \left(x _ {1}\right) p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right) \right\| \leq \frac {1}{1 - t} \int_ {S ^ {d}} \| \operatorname {L o g} _ {x} \left(x _ {1}\right) \| p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right).
$$

On the support of $p_t(\cdot \mid x)$ we have $d(x, x_1) < (1 - t)\pi$ , hence

$$
\left\| \operatorname {L o g} _ {x} (x _ {1}) \right\| = d (x, x _ {1}) \leq (1 - t) \pi .
$$

Therefore

$$
\left\| v (t, x) \right\| \leq \frac {1}{1 - t} \int_ {S ^ {d}} (1 - t) \pi p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right) = \pi \int_ {S ^ {d}} p _ {t} \left(x _ {1} \mid x\right) d V _ {g} \left(x _ {1}\right) = \pi ,
$$

since $p_t(\cdot \mid x)$ is a probability density.

Lemma D.15. Assume $d \geq 3$ and $t \in (0,1)$ . Let $p_0 \equiv \operatorname{Vol}(S^d)^{-1}$ be the uniform prior on $S^d$ , and let $p_1$ be a smooth density on $S^d$ such that

$$
0 <   m _ {1} \leq p _ {1} (z) \leq M _ {1} <   \infty .
$$

Let $X_0 \sim p_0$ and $X_1 \sim p_1$ be independent, and define the geodesic interpolation

$$
X _ {t} = \mathrm {E x p} _ {X _ {0}} (t \operatorname {L o g} _ {X _ {0}} (X _ {1})).
$$

Let $p_t$ denote the marginal density of $X_t$ with respect to $dV_g$ . Then

$$
\mathbb {E} \left[ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} \right] \leq \frac {8 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

Proof. Using Lemma D.2, notice that $\log p_t(x) = \log Z_t(x) - \log \operatorname{Vol}(S^d)$ , we have

$$
\operatorname {g r a d} \log p _ {t} (x) = \operatorname {g r a d} \log Z _ {t} (x).
$$

Take gradient, we obtain

$$
\operatorname {g r a d} Z _ {t} (x) = \int_ {S ^ {d}} p _ {1} (x _ {1}) \operatorname {g r a d} _ {x} J _ {t} (x \mid x _ {1}) d V _ {g} (x _ {1}).
$$

Using $\operatorname{grad}_x J_t = J_t \operatorname{grad}_x \log J_t$ and the definition of the conditional density

$$
p _ {t} (x _ {1} \mid x) = \frac {p _ {1} (x _ {1}) J _ {t} (x \mid x _ {1})}{Z _ {t} (x)},
$$

we obtain

$$
\begin{array}{l} \operatorname {g r a d} \log Z _ {t} (x) = \frac {\operatorname {g r a d} Z _ {t} (x)}{Z _ {t} (x)} = \int_ {S ^ {d}} \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) p _ {t} (x _ {1} \mid x) d V _ {g} (x _ {1}) \\ = \mathbb {E} \bigl [ \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \mid X _ {t} = x \bigr ]. \\ \end{array}
$$

Now we have

$$
\operatorname {g r a d} \log p _ {t} (X _ {t}) = \mathbb {E} [ \operatorname {g r a d} _ {x} \log J _ {t} (X _ {t} \mid X _ {1}) \mid X _ {t} ],
$$

which implies

$$
\| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} \leq \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (X _ {t} | X _ {1}) \| ^ {2} | X _ {t} ].
$$

Taking expectation again gives

$$
\mathbb {E} [ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} ] \leq \mathbb {E} \Big [ \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (X _ {t} | X _ {1}) \| ^ {2} | X _ {t} ] \Big ] \leq \frac {8 (d - 1) ^ {2}}{(1 - t) ^ {2}} \frac {M _ {1}}{m _ {1}}.
$$

where the last inequality follows from Lemma D.6.

![](images/90b63b9ac9824335dac57e299f51817346ee744c6f7ecc8826d3191a75611a2c.jpg)

# D.5 Finiteness of Score Regularity: Proof of Proposition 5.3

Proof. [Proof of Proposition 5.3] Notice that

$$
\mathbb {E} \big [ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} \big ] = \int_ {M} \| \operatorname {g r a d} \log p _ {t} (x) \| ^ {2} p _ {t} (x) d V _ {g} (x) =: I (p _ {t}),
$$

i.e., it is exactly the (Riemannian) Fisher information of $p_t$ . Consider the continuity equation $\partial_t p_t + \mathrm{div}(p_t v(t, \cdot)) = 0$ . Let $s_t \coloneqq \operatorname{grad} \log p_t$ denote the score.

We first compute time derivative of $I$ . Differentiate and use the ordinary product rule:

$$
\begin{array}{l} \frac {d}{d t} I \left(p _ {t}\right) = \int_ {M} \partial_ {t} \left(\left\langle s _ {t}, s _ {t} \right\rangle\right) p _ {t} d V _ {g} + \int_ {M} \left\langle s _ {t}, s _ {t} \right\rangle \partial_ {t} p _ {t} d V _ {g} \\ = 2 \int_ {M} \left\langle \partial_ {t} s _ {t}, s _ {t} \right\rangle p _ {t} d V _ {g} + \int_ {M} \| s _ {t} \| ^ {2} \partial_ {t} p _ {t} d V _ {g}. \\ \end{array}
$$

Observe that

$$
\begin{array}{l} \partial_ {t} \log p _ {t} = - \frac {1}{p _ {t}} \operatorname {d i v} (p _ {t} v) = - \operatorname {d i v} v - \frac {1}{p _ {t}} \langle \operatorname {g r a d} p _ {t}, v \rangle \\ = - \operatorname {d i v} v - \left\langle \operatorname {g r a d} \log p _ {t}, v \right\rangle = - \operatorname {d i v} v - \left\langle s _ {t}, v \right\rangle . \\ \end{array}
$$

Taking the gradient yields

$$
\partial_ {t} s _ {t} = \operatorname {g r a d} \left(\partial_ {t} \log p _ {t}\right) = - \operatorname {g r a d} (\operatorname {d i v} v) - \operatorname {g r a d} \left(\langle s _ {t}, v \rangle\right).
$$

We compute the terms in the time derivative of $I(p_{t})$ separately. For the first term,

$$
\begin{array}{l} 2 \int_ {M} \left\langle \partial_ {t} s _ {t}, s _ {t} \right\rangle p _ {t} d V _ {g} = 2 \int_ {M} \left\langle - \operatorname {g r a d} \left(\operatorname {d i v} v\right) - \operatorname {g r a d} \left(\left\langle s _ {t}, v \right\rangle\right), s _ {t} \right\rangle p _ {t} d V _ {g} \\ = - 2 \int_ {M} \left\langle \operatorname {g r a d} (\operatorname {d i v} v), s _ {t} \right\rangle p _ {t} d V _ {g} - 2 \int_ {M} \left\langle \operatorname {g r a d} \left(\langle s _ {t}, v \rangle\right), s _ {t} \right\rangle p _ {t} d V _ {g} \\ = - 2 \int_ {M} \left\langle \operatorname {g r a d} (\operatorname {d i v} v), s _ {t} \right\rangle p _ {t} d V _ {g} - 2 \int_ {M} \left\langle \nabla_ {s _ {t}} s _ {t}, v \right\rangle p _ {t} + \left\langle \nabla_ {s _ {t}} v, s _ {t} \right\rangle p _ {t} d V _ {g}. \\ \end{array}
$$

For the second term,

$$
\begin{array}{l} \int_ {M} \| s _ {t} \| ^ {2} \partial_ {t} p _ {t} d V _ {g} = - \int_ {M} \| s _ {t} \| ^ {2} \operatorname {d i v} (p _ {t} v) d V _ {g} = \int_ {M} \left\langle \operatorname {g r a d} \| s _ {t} \| ^ {2}, v \right\rangle p _ {t} d V _ {g} \\ = 2 \int_ {M} \left\langle \nabla_ {v} s _ {t}, s _ {t} \right\rangle p _ {t} d V _ {g}. \\ \end{array}
$$

SinceHessis symmetric,we have

$$
\left\langle \nabla_ {v} s _ {t}, s _ {t} \right\rangle = \left\langle \nabla_ {v} \operatorname {g r a d} \log p _ {t}, s _ {t} \right\rangle = \left(\operatorname {H e s s} \log p _ {t}\right) (v, s _ {t}) = \left\langle \nabla_ {s _ {t}} \operatorname {g r a d} \log p _ {t}, v \right\rangle = \left\langle \nabla_ {s _ {t}} s _ {t}, v \right\rangle .
$$

Together,

$$
\frac {d}{d t} I (p _ {t}) = - 2 \int_ {M} \langle s _ {t}, \nabla_ {s _ {t}} v \rangle p _ {t} d V _ {g} - 2 \int_ {M} \langle \operatorname {g r a d} (\operatorname {d i v} v), s _ {t} \rangle p _ {t} d V _ {g}.
$$

Now we derive an ODE that helps to bound $I$ . Using Cauchy-Schwarz and the pointwise bounds $\| \nabla v(t,x)\|_{\mathrm{op}}\leq L_t^{v,x}$ and $\| \operatorname {grad}\operatorname {div}v(t,x)\| \leq L_t^{\operatorname {div},x}$ (from Assumption 2), we obtain

$$
\begin{array}{l} \frac {d}{d t} I (p _ {t}) \leq 2 L _ {t} ^ {v, x} I (p _ {t}) + 2 L _ {t} ^ {\operatorname {d i v}, x} \int_ {M} \| s _ {t} (x) \| p _ {t} (x) d V _ {g} (x) \\ \leq 2 L _ {t} ^ {v, x} I \left(p _ {t}\right) + 2 L _ {t} ^ {\operatorname {d i v}, x} \sqrt {I \left(p _ {t}\right)}. \tag {16} \\ \end{array}
$$

Let $y(t)\coloneqq \sqrt{I(p_t)}$ . Since $I^{\prime} = 2yy^{\prime}$ , (16) implies

$$
y ^ {\prime} (t) \leq L _ {t} ^ {v, x} y (t) + L _ {t} ^ {\mathrm {d i v}, x}.
$$

It remains to solve the ODE and obtain a finite upper bound. Define

$$
A (t) := \int_ {0} ^ {t} L _ {s} ^ {v, x} d s, \quad \mu (t) := e ^ {- A (t)}.
$$

Then $\mu$ is absolutely continuous and

$$
\mu^ {\prime} (t) = - L _ {t} ^ {v, x} e ^ {- A (t)} = - L _ {t} ^ {v, x} \mu (t) \quad \text {f o r a . e .} t.
$$

Multiply by $\mu (t)$

$$
\mu (t) y ^ {\prime} (t) \leq \mu (t) L _ {t} ^ {v, x} y (t) + \mu (t) L _ {t} ^ {\operatorname {d i v}, x}.
$$

Using the product rule and the identity for $\mu^{\prime}(t)$

$$
\begin{array}{l} \frac {d}{d t} \left(\mu (t) y (t)\right) = \mu^ {\prime} (t) y (t) + \mu (t) y ^ {\prime} (t) \\ = - L _ {t} ^ {v, x} \mu (t) y (t) + \mu (t) y ^ {\prime} (t) \\ \leq - L _ {t} ^ {v, x} \mu (t) y (t) + \mu (t) L _ {t} ^ {v, x} y (t) + \mu (t) L _ {t} ^ {\operatorname {d i v}, x} \\ = \mu (t) L _ {t} ^ {\operatorname {d i v}, x}. \\ \end{array}
$$

Hence, for a.e. $t$

$$
\frac {d}{d t} \big (\mu (t) y (t) \big) \leq \mu (t) L _ {t} ^ {\mathrm {d i v}, x}.
$$

Integrating over $[0,t]$ yields

$$
\mu (t) y (t) - \mu (0) y (0) \leq \int_ {0} ^ {t} \mu (s) L _ {s} ^ {\operatorname {d i v}, x} d s.
$$

Since $\mu (0) = e^{-A(0)} = 1$ , we obtain

$$
\mu (t) y (t) \leq y (0) + \int_ {0} ^ {t} e ^ {- A (s)} L _ {s} ^ {\operatorname {d i v}, x} d s.
$$

Multiply both sides by $e^{A(t)}$ :

$$
\begin{array}{l} y (t) \leq e ^ {A (t)} \left(y (0) + \int_ {0} ^ {t} e ^ {- A (s)} L _ {s} ^ {\operatorname {d i v}, x} d s\right) \\ = \exp \left(\int_ {0} ^ {t} L _ {s} ^ {v, x} d s\right) \left(y (0) + \int_ {0} ^ {t} L _ {s} ^ {\operatorname {d i v}, x} \exp \left(- \int_ {0} ^ {s} L _ {r} ^ {v, x} d r\right) d s\right). \\ \end{array}
$$

Therefore, for all $t < 1$

$$
\sqrt {I (p _ {t})} \leq \exp \left(\int_ {0} ^ {t} L _ {s} ^ {v, x} d s\right) \left(\sqrt {I (p _ {0})} + \int_ {0} ^ {t} L _ {s} ^ {\mathrm {d i v}, x} \exp \left(- \int_ {0} ^ {s} L _ {r} ^ {v, x} d r\right) d s\right),
$$

and hence

$$
\mathbb {E} \left[ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} \right] = I (p _ {t}) \leq L _ {t} ^ {\mathrm {s c o r e}}
$$

for some finite number $L_{t}^{\mathrm{score}}$ .

# E SPD Manifold Regularity Results

In this section, we work on the SPD manifold with affine invariant metric, denoted as $\mathrm{SPD}(n)$ .

We briefly discuss the similarity and difference between the regularity analysis in this section and that of the hypersphere.

- On a hypersphere, there exist cut points, resulting indicator function in the conditional density. We provide the formula for the conditional density function, on a general Hadamard manifold see Lemma E.1. We see that with non-positive curvature, there would be no cut points. Consequently, there would be no indicator function in the expression of the conditional density guaranteeing better smoothness.   
- The hypersphere is a compact manifold, but $\operatorname{SPD}(n)$ is non-compact. On a compact manifold the vector field $v(t,x)$ itself is uniformly bounded. But on a non-compact manifold, $\| v(t,x)\|$ could possibly blow up. Therefore, on $\operatorname{SPD}(n)$ , it's unlikely that regularity will hold pointwise but we can still expect its norm to be bounded, in expectation.   
- Moreover, from a high-level idea, the procedure for providing upper bounds on derivatives of $v(t,x)$ remains the same. For example, in Lemma D.12, we expanded the gradient of $\operatorname{div} v(t,x)$ as terms involving $\mathbb{E}[\| \operatorname{grad}_x \operatorname{div}_x \operatorname{Log}_x(X_1) \| | X_t = x]$ , $\mathbb{E}[\| \operatorname{grad}_x \log p_t(X_1 | x) \|^2 | X_t = x]$ just to name a few. To establish regularity on $\operatorname{SPD}(n)$ , we still have roughly the same expansion, involving the same collection of terms. The difference is that, instead of obtaining uniform upper bounds (as in Lemma D.6, D.7, D.8, and D.9), our bounds for $\operatorname{SPD}(n)$ will depend on radial distance function $r(x) = d(x,x_0)$ for some $x_0$ .

Throughout this section, we use the following notation: $\kappa \coloneqq \sqrt{-K_{\mathrm{min}}} > 0$ and the model function is defined as

$$
s _ {K _ {\min }} (r) := \frac {1}{\kappa} \sinh (\kappa r), \qquad r \geq 0.
$$

Define the radial contraction map and its inverse by

$$
\Phi_ {t, x _ {1}} (x) := \operatorname {E x p} _ {x _ {1}} \left((1 - t) \log_ {x _ {1}} (x)\right),
$$

$$
\Psi_ {t, x _ {1}} (x) := \operatorname {E x p} _ {x _ {1}} \left(\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)\right).
$$

and note that under our geodesic interpolation, $x_{t} = \Phi_{t,x_{1}}(x_{0})$ , and $x_0 = \Psi_{t,x_1}(x)$ .

We first provide the density formula.

Lemma E.1 (Density of $p_t(x_1 \mid x)$ on a Hadamard manifold). Let $(M, g)$ be a complete, simply-connected, $d$ -dimensional Riemannian manifold with non-positive curvature. Let $p_0, p_1$ be the prior and target distributions, assuming independence. Then the conditional density of $X_1$ given $X_t = x$ is

$$
p _ {t} \left(x _ {1} \mid x\right) = \frac {p _ {1} \left(x _ {1}\right) p _ {0} \left(\Psi_ {t , x _ {1}} (x)\right) J _ {t} \left(x \mid x _ {1}\right)}{\int_ {M} p _ {1} (z) p _ {0} \left(\Psi_ {t , z} (x)\right) J _ {t} \left(x \mid z\right) d V _ {g} (z)},
$$

$$
w h e r e \quad J _ {t} (x \mid x _ {1}) = (1 - t) ^ {- d} \frac {\left| \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right|}{\left| \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \right|}.
$$

Furthermore, we have

$$
p _ {t} (x) = \int_ {M} p _ {1} (z) p _ {0} \left(\Psi_ {t, z} (x)\right) J _ {t} (x \mid z) d V _ {g} (z).
$$

# Proof.

Notice that $\Phi_{t,x_1}$ is a global diffeomorphism, and $\Psi_{t,x_1}$ is its inverse. For fixed $x_1$ and $x$ , the change-of-variables formula gives

$$
d V _ {g} \left(\Psi_ {t, x _ {1}} (x)\right) = \left| \det  \left(d \Psi_ {t, x _ {1}}\right) _ {x} \right| d V _ {g} (x),
$$

which implies

$$
p (\Psi_ {t, x _ {1}} (x), x _ {1}) d V _ {g} (\Psi_ {t, x _ {1}} (x)) d V _ {g} (x _ {1}) = p _ {0} \big (\Psi_ {t, x _ {1}} (x) \big) p _ {1} (x _ {1}) \left| \det (d \Psi_ {t, x _ {1}}) _ {x} \right| d V _ {g} (x) d V _ {g} (x _ {1}).
$$

We define

$$
J _ {t} (x \mid x _ {1}) := \left| \det  (d \Psi_ {t, x _ {1}}) _ {x} \right|.
$$

Equivalently, the joint measure of $(X_{t},X_{1})$ can be written as

$$
p _ {t} (x, x _ {1}) d V _ {g} (x) d V _ {g} (x _ {1}) = p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) p _ {1} (x _ {1}) J _ {t} (x \mid x _ {1}) d V _ {g} (x) d V _ {g} (x _ {1}),
$$

Integrating the joint density over $x_{1}$ yields the marginal

$$
p _ {t} (x) = \int_ {M} p _ {1} (z) p _ {0} \left(\Psi_ {t, z} (x)\right) J _ {t} (x \mid z) d V _ {g} (z).
$$

Therefore, by Bayes' rule,

$$
p _ {t} (x _ {1} \mid x) = \frac {p _ {t} (x , x _ {1})}{p _ {t} (x)} = \frac {p _ {1} (x _ {1}) p _ {0} \left(\Psi_ {t , x _ {1}} (x)\right) J _ {t} (x \mid x _ {1})}{\int_ {M} p _ {1} (z) p _ {0} \left(\Psi_ {t , z} (x)\right) J _ {t} (x \mid z) d V _ {g} (z)}.
$$

It remains to compute $J_{t}(x \mid x_{1})$ . Recall that $\Psi_{t,x_1}(x) = \mathrm{Exp}_{x_1}\left(\frac{1}{1 - t}\mathrm{Log}_{x_1}(x)\right)$ . Using chain rule,

$$
\left(d \Psi_ {t, x _ {1}}\right) _ {x} = \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {v} \circ \left(\left(1 - t\right) ^ {- 1} I d\right) \circ \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x}.
$$

Using $(d\operatorname{Log}_{x_1})_x = \left((d\operatorname{Exp}_{x_1})_{\operatorname{Log}_{x_1}(x)}\right)^{-1}$ , we have

$$
(d \Psi_ {t, x _ {1}}) _ {x} = (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \circ ((1 - t) ^ {- 1} I d) \circ ((d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)}) ^ {- 1}.
$$

Taking determinants,

$$
J _ {t} (x \mid x _ {1}) = (d \Psi_ {t, x _ {1}}) _ {x} = (1 - t) ^ {- d} \frac {\left| \det (d \mathrm {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \mathrm {L o g} _ {x _ {1}} (x)} \right|}{\left| \det (d \mathrm {E x p} _ {x _ {1}}) _ {\mathrm {L o g} _ {x _ {1}} (x)} \right|}.
$$

Now we prove Proposition B.6, which verifies Assumption 4.

Proof. [Proof of Proposition B.6] The desired result is directly implied by Lemma E.4 and Lemma E.6:

$$
\mathbb {E} [ \| v (t, x) \| ^ {2} ] \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] \lesssim d,
$$

$$
\begin{array}{l} \mathbb {E} [ \| \nabla v (t, x) \| ] \lesssim \frac {d}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}} \\ \lesssim \frac {d ^ {2 + 6 \lambda}}{1 - t} L _ {R} M _ {\lambda_ {1}} ^ {\frac {1}{2}}, \\ \end{array}
$$

$$
\mathbb {E} [ | \frac {d}{d t} v (t, x) | ] \lesssim \frac {d}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}}
$$

$$
\lesssim \frac {d ^ {2 + 6 \lambda}}{1 - t} L _ {R} M _ {\lambda_ {1}} ^ {\frac {1}{2}},
$$

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| ] \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ] \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {3} \lesssim \frac {d ^ {3 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {3}, \\ \mathbb {E} \left[ \left| \frac {d}{d t} \operatorname {d i v} v (t, x) \right| \right] \lesssim \mathbb {E} \left[ d \left(x _ {0}, x _ {1}\right) ^ {2} \right] ^ {\frac {1}{2}} \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {3} \mathbb {E} \left[ d \left(x _ {1}, x _ {0}\right) ^ {2} s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {1 2} \right] ^ {\frac {1}{2}} \\ \lesssim \frac {d ^ {3 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {3} M _ {\lambda_ {1}} ^ {\frac {1}{2}}, \\ \end{array}
$$

and

$$
\begin{array}{l} \mathbb {E} [ \| \nabla v (t, x) \| ^ {2} ] \lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {4} ] ^ {\frac {1}{2}} \mathbb {E} [ s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] ^ {\frac {1}{2}} \lesssim \frac {d ^ {3 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {2} M _ {\lambda_ {1}} ^ {\frac {1}{2}}, \\ \mathbb {E} [ | \frac {d}{d t} v (t, x) | ^ {2} ] \lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {4} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {1 2} ] ^ {\frac {1}{2}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {4} ] ^ {\frac {1}{2}} \lesssim \frac {d ^ {3 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {2} M _ {\lambda_ {1}} ^ {\frac {1}{2}}, \\ \mathbb {E} [ \| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| ^ {2} ] \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] \frac {d ^ {4}}{(1 - t) ^ {4}} L _ {R} ^ {6} \lesssim \frac {d ^ {5 + 2 4 \lambda}}{(1 - t) ^ {4}} L _ {R} ^ {6} M _ {\lambda_ {1}}. \\ \end{array}
$$

![](images/848a48900313d820816035f23aa90b63f15450462716ae64da7726847cb34dd8.jpg)

# E.1 Proof of Proposition 5.4

We start to prove the score regularity result. In the following Lemma, we decompose $\mathbb{E}\big[\| \operatorname {grad}\log p_t(X_t)\| ^2\big]$ as the sum of two terms.

Lemma E.2. For $X_{t}\sim p_{t}$

$$
\mathbb {E} \big [ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} \big ] \leq 2 \mathbb {E} \bigg [ \big \| \operatorname {g r a d} _ {x} \log p _ {0} (\Psi_ {t, X _ {1}} (X _ {t})) \big \| ^ {2} \bigg ] + 2 \mathbb {E} \bigg [ \big \| \operatorname {g r a d} _ {x} \log J _ {t} (X _ {t} \mid X _ {1}) \big \| ^ {2} \bigg ].
$$

Proof. By Lemma E.1,

$$
p _ {t} (x) = \int_ {M} p _ {1} (z) p _ {0} \left(\Psi_ {t, z} (x)\right) J _ {t} (x \mid z) d V _ {g} (z).
$$

Taking the Riemannian gradient with respect to $x$ and differentiating under the integral sign,

$$
\operatorname {g r a d} p _ {t} (x) = \int_ {M} p _ {1} (z) \operatorname {g r a d} _ {x} \left(p _ {0} \left(\Psi_ {t, z} (x)\right) J _ {t} (x \mid z)\right) d V _ {g} (z). \tag {17}
$$

Using the identity $\operatorname{grad}(\phi) = \phi$ $\log \phi$ , we have

$$
\operatorname {g r a d} _ {x} \left(p _ {0} (\Psi_ {t, z} (x)) J _ {t} (x \mid z)\right) = p _ {0} (\Psi_ {t, z} (x)) J _ {t} (x \mid z) \operatorname {g r a d} _ {x} \log \left(p _ {0} (\Psi_ {t, z} (x)) J _ {t} (x \mid z)\right).
$$

Plugging into (17) and dividing by $p_t(x)$ yields

$$
\operatorname {g r a d} \log p _ {t} (x) = \frac {\operatorname {g r a d} p _ {t} (x)}{p _ {t} (x)} = \int_ {M} \operatorname {g r a d} _ {x} \log \left(p _ {0} \left(\Psi_ {t, z} (x)\right) J _ {t} (x \mid z)\right) \frac {p _ {1} (z) p _ {0} \left(\Psi_ {t , z} (x)\right) J _ {t} (x \mid z)}{p _ {t} (x)} d V _ {g} (z).
$$

Observe that

$$
\frac {p _ {1} (z) p _ {0} \left(\Psi_ {t , z} (x)\right) J _ {t} (x \mid z)}{p _ {t} (x)} = \frac {p _ {1} (z) p _ {0} \left(\Psi_ {t , z} (x)\right) J _ {t} (x \mid z)}{\int_ {M} p _ {1} (z) p _ {0} \left(\Psi_ {t , z} (x)\right) J _ {t} (x \mid z) d V _ {g} (z)} = p _ {t} (z \mid x).
$$

Hence we have

$$
\begin{array}{l} \operatorname {g r a d} \log p _ {t} (x) = \operatorname {g r a d} \log p _ {t} (x) = \int_ {M} \operatorname {g r a d} _ {x} \log \Big (p _ {0} (\Psi_ {t, z} (x)) J _ {t} (x \mid z) \Big) p _ {t} (z \mid x) d V _ {g} (z) \\ = \mathbb {E} \left[ \operatorname {g r a d} _ {x} \log \left(p _ {0} \left(\Psi_ {t, X _ {1}} (x)\right) J _ {t} (x \mid X _ {1})\right) \mid X _ {t} = x \right]. \\ \end{array}
$$

Next, apply Jensen's inequality,

$$
\begin{array}{l} \mathbb {E} [ \| \operatorname {g r a d} \log p _ {t} (x) \| ^ {2} ] = \mathbb {E} \left[ \| \mathbb {E} [ \operatorname {g r a d} _ {x} \log \left(p _ {0} \left(\Psi_ {t, X _ {1}} (x)\right) J _ {t} (x \mid X _ {1})\right) \mid X _ {t} = x ] \| ^ {2} \right] \\ \leq \mathbb {E} \left[ \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log \left(p _ {0} \left(\Psi_ {t, X _ {1}} (x)\right) J _ {t} (x \mid X _ {1})\right) \| ^ {2} \mid X _ {t} = x ] \right] \\ = \mathbb {E} \left[ \| \operatorname {g r a d} _ {x} \log \left(p _ {0} \left(\Psi_ {t, X _ {1}} (x)\right) J _ {t} (x \mid X _ {1})\right) \| ^ {2} \right]. \\ \end{array}
$$

The result follows from

$$
\operatorname {g r a d} _ {x} \log \left(p _ {0} (\Psi) J _ {t}\right) = \operatorname {g r a d} _ {x} \log p _ {0} (\Psi) + \operatorname {g r a d} _ {x} \log J _ {t}, \qquad \| a + b \| ^ {2} \leq 2 \| a \| ^ {2} + 2 \| b \| ^ {2}.
$$

![](images/f467a791cad92831f902723d500ce4ec66683f2994b3eb74c4aaf1b79f5bad50.jpg)

Now we prove Proposition 5.4.

Proof. [Proof of Proposition 5.4] From Lemma E.2, we have

$$
\mathbb {E} \big [ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} \big ] \leq 2 \mathbb {E} \Big [ \| \operatorname {g r a d} _ {x} \log p _ {0} (\Psi_ {t, X _ {1}} (X _ {t})) \| ^ {2} \Big ] + 2 \mathbb {E} \Big [ \| \operatorname {g r a d} _ {x} \log J _ {t} (X _ {t} \mid X _ {1}) \| ^ {2} \Big ].
$$

We show the following in Appendix E.3 (Lemma E.7 and Lemma E.8):

$$
\begin{array}{l} \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \leq d \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left(\frac {1}{1 - t} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| + \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right), \\ \left\| \operatorname {g r a d} _ {x} \log p _ {0} (\Psi_ {t, X _ {1}} (X _ {t})) \right\| \leq 2 d d (x _ {0}, z) \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}. \\ \end{array}
$$

We also prove the following in Lemma E.10 and Lemma E.12:

$$
\begin{array}{l} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| \leq 1, \\ \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \leq s _ {K _ {\min}} (\| \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x) \|) / \| \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x) \| = s _ {K _ {\min}} (d (x _ {0}, x _ {1})) / d (x _ {0}, x _ {1}), \\ \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \leq \frac {1 6}{3} s _ {K _ {\min }} (d (x _ {0}, x _ {1}) / 2) ^ {2} L _ {R} s _ {K _ {\min }} (d (x _ {0}, x _ {1})). \\ \end{array}
$$

So together,

$$
\begin{array}{l} \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \lesssim \frac {d}{1 - t} L _ {R} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {3}, \\ \left\| \operatorname {g r a d} _ {x} \log p _ {0} \left(\Psi_ {t, X _ {1}} \left(X _ {t}\right)\right) \right\| \lesssim \frac {d}{1 - t} s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) d \left(x _ {0}, z\right). \\ \end{array}
$$

Using Lemma E.4, we have

$$
\begin{array}{l} \mathbb {E} \left[ \| \operatorname {g r a d} \log p _ {t} (X _ {t}) \| ^ {2} \right] \lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} \left[ s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {6} \right] \lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} \left[ s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {6} \right] \\ \lesssim \frac {d ^ {2 + 1 2 \lambda}}{(1 - t) ^ {2}} L _ {R} ^ {2} M, \\ \end{array}
$$

where $\lambda = \max \{1,\kappa \}$

# E.2 Auxiliary Results for Regularity for Hadamard and SPD manifolds

# E.2.1 Expectation Control

Due to the non-compact nature of a Hadamard manifold as well as curvature distortion, bounding expectations of the form

$$
\mathbb {E} [ d (X _ {0}, X _ {1}) ^ {2} s _ {K _ {\min}} \big (d (X _ {0}, X _ {1}) \big) ^ {a} ], \quad a \in \mathbb {N},
$$

is a key step to establish regularity. We show that by choosing $X_0$ following a Riemannian Gaussian distribution, the above expectation can be controlled for a class of data distribution $X_1$ satisfying certain moment condition (7).

Lemma E.3. Let $(M,g)$ be a complete, simply connected $d$ -dimensional Riemannian manifold (Hadamard) and assume

$$
K _ {\min} \leq \sec \leq 0, \quad \text {w h e r e} K _ {\min} <   0 \text {i s i n d e p e n d e n t o f} d.
$$

Fix a basepoint $z \in M$ and set $r(x) := d(x,z)$ . Define

$$
p _ {0} (x) = \frac {1}{Z} e ^ {(- \beta r (x) ^ {m})}, \qquad Z := \int_ {M} e ^ {- \beta r (x) ^ {m}} d V _ {g} (x), \qquad w h e r e \qquad \beta = d, m = 2.
$$

Let $\lambda \geq 0$ be independent of $d$ . Then for $b \in \{0,1,2,3,4\}$ ,

$$
\mathbb {E} _ {p _ {0}} \big [ r (x) ^ {b} e ^ {\lambda r (x)} \big ] = \mathcal {O} (d ^ {2 \lambda} (\log d) ^ {b}).
$$

Proof. We first write the expectation as an integral over tangent space. Since $M$ is Hadamard, $\mathrm{Exp}_z: T_zM \to M$ is a global $C^\infty$ diffeomorphism. We equip the vector space $T_zM$ with the inner product $g$ , and denote by $dv$ the corresponding Lebesgue measure. For any measurable $F: M \to [0, \infty]$ , the change-of-variables formula gives

$$
\int_ {M} F (x) d V _ {g} (x) = \int_ {T _ {z} M} F (\operatorname {E x p} _ {z} (v)) | \det  (d (\operatorname {E x p} _ {z}) _ {v}) | d v.
$$

We now apply this formula with $F_{1}(x) = e^{-dr(x)^{2}}$ , $F_{2}(x) = r(x)^{b}e^{\lambda r(x)}e^{-dr(x)^{2}}$ . Since $r(\operatorname{Exp}_{z}(v)) = \| v\|$ , we obtain

$$
\mathbb {E} _ {p _ {0}} \left[ r ^ {b} e ^ {\lambda r} \right] = \frac {\int_ {T _ {z} M} \| v \| ^ {b} e ^ {\lambda \| v \|} e ^ {- d \| v \| ^ {2}} \left| \det  (d (\operatorname {E x p} _ {z}) _ {v}) \right| d v}{\int_ {T _ {z} M} e ^ {- d \| v \| ^ {2}} \left| \det  (d (\operatorname {E x p} _ {z}) _ {v}) \right| d v}. \tag {18}
$$

Recall that using comparison theorem (note that the $d - 1$ comes from det) we have

$$
1 \leq \left| \det  \left(d \left(\operatorname {E x p} _ {z}\right) _ {r \theta}\right) \right| \leq \left(\frac {s _ {K _ {\min }} (r)}{r}\right) ^ {d - 1}, \quad \forall r > 0. \tag {19}
$$

Since $\frac{s_{K_{\min}}(r)}{r} = \frac{\sinh(\kappa r)}{\kappa r} \leq e^{\kappa r}$ , we have

$$
\left| \det  \left(d \left(\operatorname {E x p} _ {z}\right) _ {r \theta}\right) \right| \leq e ^ {\kappa (d - 1) r}. \tag {20}
$$

We now integrate in $T_{z}M$ using Euclidean polar coordinates: $v = r\theta$ with $r \in [0,\infty)$ , $\theta \in \mathbb{S}^{d - 1}$ , and

$$
d v = r ^ {d - 1} d r d \theta .
$$

We split at $R = 2\log d$ and bound the expectation. Consider the decomposition below

$$
\mathbb {E} _ {p _ {0}} [ r ^ {b} e ^ {\lambda r} ] = \mathbb {E} _ {p _ {0}} [ r ^ {b} e ^ {\lambda r} \mathbf {1} _ {\{r \leq R \}} ] + \mathbb {E} _ {p _ {0}} [ r ^ {b} e ^ {\lambda r} \mathbf {1} _ {\{r > R \}} ].
$$

We first consider the central part. On $\{r\leq R\}$ , $r^b e^{\lambda r}\leq R^b e^{\lambda R}$ , hence

$$
\mathbb {E} _ {p _ {0}} \left[ r ^ {b} e ^ {\lambda r} \mathbf {1} _ {\{r \leq R \}} \right] \leq R ^ {b} e ^ {\lambda R} = (2 \log d) ^ {b} d ^ {2 \lambda}. \tag {21}
$$

We next consider the tail part. Write the tail contribution as $N_{\mathrm{tail}} / Z$ . Using change of variable formula and the upper bound (20), we obtain

$$
\begin{array}{l} N _ {\mathrm {t a i l}} := \int_ {\{x: r (x) > R \}} r (x) ^ {b} e ^ {\lambda r (x)} e ^ {- d r (x) ^ {2}} d V _ {g} (x) \\ = \int_ {\{v: \| v \| > R \}} \| v \| ^ {b} e ^ {\lambda \| v \|} e ^ {- d \| v \| ^ {2}} \left| \det (d (\operatorname {E x p} _ {z}) _ {v}) \right| d v \\ \leq \left| \mathbb {S} ^ {d - 1} \right| \int_ {R} ^ {\infty} r ^ {d - 1 + b} e ^ {(- d r ^ {2} + (\lambda + \kappa (d - 1)) r)} d r. \tag {22} \\ \end{array}
$$

Define

$$
\Psi_ {d} (r) := - d r ^ {2} + (\lambda + \kappa (d - 1)) r + (d - 1 + b) \log r.
$$

We justify that this $\Psi_d(r)$ is dominated by the $-dr^2$ term. For $r \geq R = 2\log d$ , we have $(d - 1 + b)\log r \leq \frac{d}{4} r^2, \forall d \geq 4$ . Also, for $r \geq R$ and $d$ large, $\kappa(d - 1)r \leq \frac{d}{4} r^2$ because this is equivalent to $r \geq 4\kappa(1 - 1/d)$ , which holds once $R \geq 4\kappa$ (i.e. $d \geq e^{2\kappa}$ ). Finally, $\lambda r \leq \frac{d}{8} r^2$ holds for all $r \geq R$ once $d \geq 8\lambda$ . Summing these inequalities yields, there exists some constant $d_1$ s.t. for all $d \geq d_1$ and all $r \geq R$ ,

$$
(\lambda + \kappa (d - 1)) r + (d - 1 + b) \log r \leq \frac {d}{2} r ^ {2}, \quad \text {h e n c e} \quad \Psi_ {d} (r) \leq - \frac {d}{2} r ^ {2}.
$$

Therefore, for $d \geq d_1$ ,

$$
\begin{array}{l} \int_ {R} ^ {\infty} e ^ {\Psi_ {d} (r)} d r \leq \int_ {R} ^ {\infty} e ^ {- (d / 2) r ^ {2}} d r = \int_ {R} ^ {\infty} \frac {1}{r d} (- \frac {d}{d r} e ^ {- (d / 2) r ^ {2}}) d r \leq \frac {1}{R d} \int_ {R} ^ {\infty} (- \frac {d}{d r} e ^ {- (d / 2) r ^ {2}}) d r \\ = \frac {1}{d R} \exp \Big (- \frac {d}{2} R ^ {2} \Big) = \frac {1}{d R} \exp \big (- 2 d (\log d) ^ {2} \big). \\ \end{array}
$$

Plugging into (22) gives

$$
N _ {\text {t a i l}} \leq | \mathbb {S} ^ {d - 1} | \cdot \frac {1}{d R} \exp (- 2 d (\log d) ^ {2}). \tag {23}
$$

For the denominator $Z$ , recall that $\left|\operatorname{det}(d(\operatorname{Exp}_z)_v)\right| \geq 1$ , so we get

$$
\int_ {T _ {z} M} e ^ {- d \| v \| ^ {2}} \big | \det (d (\mathrm {E x p} _ {z}) _ {v}) \big | d v \geq \int_ {T _ {z} M} e ^ {- d \| v \| ^ {2}} d v = \left(\frac {\pi}{d}\right) ^ {d / 2}.
$$

Hence, using (23),

$$
\mathbb {E} _ {p _ {0}} [ r ^ {b} e ^ {\lambda r} \mathbf {1} _ {\{r > R \}} ] = \frac {N _ {\mathrm {t a i l}}}{Z} \leq \frac {| \mathbb {S} ^ {d - 1} |}{d R} \exp \big (- 2 d (\log d) ^ {2} \big) \cdot \left(\frac {d}{\pi}\right) ^ {d / 2} = \frac {| \mathbb {S} ^ {d - 1} |}{2 d \log d} d ^ {- 2 d \log d} \cdot \left(\frac {d}{\pi}\right) ^ {d / 2} \lesssim 1.
$$

Together, we conclude that for all $d \geq d_1$ , combining (21) with the tail bound gives

$$
\mathbb {E} _ {p _ {0}} \left[ r ^ {b} e ^ {\lambda r} \right] \leq (2 \log d) ^ {b} d ^ {2 \lambda} + 1 = \mathcal {O} \left(d ^ {2 \lambda} (\log d) ^ {b}\right).
$$

Now we present intermediate steps.

Lemma E.4 (Auxiliary bounds for expectation of $s_{K_{\min}}$ ). Let $M$ be a Hadamard manifold. Fix $z \in M$ . Choose prior as $X_0 \sim p_0$ where

$$
p _ {0} (x) \propto \exp \left(- d d (x, z) ^ {2}\right).
$$

Assume Assumption 1 holds. Let $\kappa = \sqrt{-K_{\mathrm{min}}}$ and $\lambda_0 = a\max \{1,\kappa \}$ , where $0\leq a\leq a_0$ is some constant. Assume

$$
\max \left\{\mathbb {E} [ d (X _ {1}, z) ^ {4} e ^ {\lambda_ {1} d (X _ {1}, z)} ], \mathbb {E} [ e ^ {\lambda_ {1} d (X _ {1}, z)} ] \right\} \leq M, \quad \text {w h e r e} \quad \lambda_ {1} = a _ {1} \max \{1, \kappa \}.
$$

Then we have, for $b \in \{0,1,2,3,4\}$ ,

$$
\begin{array}{l} \mathbb {E} \left[ d (X _ {0}, X _ {1}) ^ {b} s _ {K _ {\min }} \left(d (X _ {0}, X _ {1})\right) ^ {a} \right] \lesssim M \mathbb {E} _ {X _ {0} \sim p _ {0}} \left[ d (X _ {0}, z) ^ {b} e ^ {\lambda_ {0} d (X _ {0}, z)} \right] \lesssim d ^ {2 \lambda_ {0}} (\log d) ^ {b} M, \\ \mathbb {E} \left[ d (X _ {0}, z) ^ {b} s _ {K _ {\min}} \big (d (X _ {0}, X _ {1}) \big) ^ {a} \right] \lesssim M \mathbb {E} _ {X _ {0} \sim p _ {0}} \left[ d (X _ {0}, z) ^ {b} e ^ {\lambda_ {0} d (X _ {0}, z)} \right] \lesssim d ^ {2 \lambda_ {0}} (\log d) ^ {b} M. \\ \end{array}
$$

Proof. Observe that

$$
s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {a} = \frac {\sinh^ {a} \left(\kappa d \left(x _ {0} , x _ {1}\right)\right)}{\kappa^ {a}} \leq \left(e ^ {\max  \{1, \kappa \} d \left(x _ {0}, x _ {1}\right)}\right) ^ {a}.
$$

Hence

$$
d \left(x _ {0}, x _ {1}\right) ^ {b} s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {a} \leq d \left(x _ {0}, x _ {1}\right) ^ {b} \left(e ^ {\max  \{1, \kappa \} d \left(x _ {0}, x _ {1}\right)}\right) ^ {a}. \tag {24}
$$

Taking expectation, it suffices to bound $\mathbb{E}\bigl [d(x_0,x_1)^b e^{\lambda_0d(x_0,x_1)}\bigr ]$ with $\lambda_0 = a\max \{1,\kappa \}$

The triangle inequality gives

$$
d (x _ {0}, x _ {1}) \leq d (x _ {0}, z) + d (x _ {1}, z).
$$

Therefore,

$$
\begin{array}{l} d \left(x _ {0}, x _ {1}\right) ^ {b} e ^ {\lambda_ {0} d \left(x _ {0}, x _ {1}\right)} \leq \left(d \left(x _ {0}, z\right) + d \left(x _ {1}, z\right)\right) ^ {b} \exp \left(\lambda_ {0} \left(d \left(x _ {0}, z\right) + d \left(x _ {1}, z\right)\right)\right) \\ \lesssim (d (x _ {0}, z) ^ {b} + d (x _ {1}, z) ^ {b}) \exp (\lambda_ {0} d (x _ {0}, z)) \exp (\lambda_ {0} d (x _ {1}, z)). \\ \end{array}
$$

Take expectation and use independence of $X_0$ and $X_1$ :

$$
\begin{array}{l} \mathbb {E} \Big [ d (X _ {0}, X _ {1}) ^ {b} e ^ {\lambda_ {0} d (X _ {0}, X _ {1})} \Big ] \leq 2 \mathbb {E} \Big [ e ^ {\lambda_ {0} d (X _ {1}, z)} \Big ] \mathbb {E} _ {X _ {0} \sim p _ {0}} \Big [ d (X _ {0}, z) ^ {b} e ^ {\lambda_ {0} d (X _ {0}, z)} \Big ] \\ + 2 \mathbb {E} \left[ d (X _ {1}, z) ^ {b} e ^ {\lambda_ {0} d (X _ {1}, z)} \right] \mathbb {E} _ {X _ {0} \sim p _ {0}} \left[ e ^ {\lambda_ {0} d (X _ {0}, z)} \right]. \tag {25} \\ \end{array}
$$

By Assumption, both $\mathbb{E}\Big[e^{\lambda_0d(X_1,z)}\Big]$ and $\mathbb{E}\Big[d(X_1,z)^b e^{\lambda_0d(X_1,z)}\Big]$ are controlled by $M$ . It hence follows that

$$
\mathbb {E} \Big [ d (X _ {0}, X _ {1}) ^ {b} e ^ {\lambda_ {0} d (X _ {0}, X _ {1})} \Big ] \lesssim M \mathbb {E} _ {X _ {0} \sim p _ {0}} \Big [ d (X _ {0}, z) ^ {b} e ^ {\lambda_ {0} d (X _ {0}, z)} \Big ] \lesssim d ^ {2 \lambda_ {0}} (\log d) ^ {b} M,
$$

where we applied Lemma E.3.

![](images/20f734754633d4f9d9bee057bc017dbf10dd5eeab910761f4ce538575a828c2b.jpg)

# E.2.2 Regularity Control

The following lemma summarizes the building blocks needed to establish regularity, serving as the same purpose as Lemma D.6, D.7, D.8, and D.9.

Lemma E.5. On $\mathrm{SPD}(n)$ , with prior distribution being $p_0 \propto \exp(-dd(x_0, z)^2)$ , assume Assumption 1, we have the following bounds.

$$
\| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \lesssim d \frac {1}{1 - t} L _ {R} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {3},
$$

$$
\left\| \operatorname {g r a d} _ {x} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \right\| \lesssim d \frac {1}{1 - t} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) d (x _ {0}, z),
$$

$$
| \partial_ {t} \log J _ {t} (x \mid x _ {1}) | \lesssim \frac {d}{1 - t} d (x _ {0}, x _ {1}) s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {3} L _ {R},
$$

$$
\left| \partial_ {t} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \right| \lesssim \frac {d}{1 - t} d \left(x _ {0}, z\right) s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right),
$$

$$
\| \nabla_ {x} ^ {2} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \| _ {\mathrm {o p}} \lesssim \frac {d}{(1 - t) ^ {2}} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {4} L _ {R} d (x _ {0}, z),
$$

$$
\| \nabla_ {x} ^ {2} \log J _ {t} (x \mid x _ {1}) \| _ {\mathrm {o p}} \lesssim \frac {d}{(1 - t) ^ {2}} L _ {R} ^ {3} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6},
$$

$$
\left\| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \right\| \lesssim d (x _ {0}, z) \frac {d}{(1 - t) ^ {2}} d (x _ {0}, x _ {1}) L _ {R} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {3},
$$

$$
\| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \lesssim \frac {d}{(1 - t) ^ {2}} L _ {R} ^ {3} d (x _ {1}, x _ {0}) s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6},
$$

$$
\| \nabla_ {x} \operatorname {L o g} _ {x} (x _ {1}) \| _ {\mathrm {o p}} ^ {2} \lesssim d (x _ {0}, x _ {1}) ^ {2},
$$

$$
| \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (x _ {1}) | ^ {2} \lesssim d ^ {2} d (x _ {0}, x _ {1}) ^ {2},
$$

$$
\| \operatorname {g r a d} \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (x _ {1}) \| \lesssim d d (x _ {0}, x _ {1}) ^ {\frac {3}{2}}.
$$

Here we emphasize that $\operatorname{Log}_x(x_1)$ is viewed as a vector field, for fixed $x_1$ , so $\nabla \operatorname{Log}_x(x_1)$ is covariant derivative of the vector field $\operatorname{Log}_x(x_1)$ . Consequently,

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} [ s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ],
$$

$$
\mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) \| ^ {4} \mid X _ {t} = x ] \lesssim \frac {d ^ {4}}{(1 - t) ^ {4}} L _ {R} ^ {4} \mathbb {E} [ s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ],
$$

$$
\mathbb {E} [ | \partial_ {t} \log p _ {t} (x _ {1} \mid x) | ^ {2} \mid X _ {t} = x ] \lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ],
$$

$$
\mathbb {E} [ | \partial_ {t} \log p _ {t} (x _ {1} \mid x) | ^ {4} \mid X _ {t} = x ] \lesssim \frac {d ^ {4}}{(1 - t) ^ {4}} L _ {R} ^ {4} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {4} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ],
$$

$$
\begin{array}{l} \mathbb {E} [ \| \nabla_ {x} ^ {2} \log p _ {t} (x _ {1} \mid x) \| _ {\text {o p}} ^ {2} \mid X _ {t} = x ] \lesssim \frac {d ^ {2}}{(1 - t) ^ {4}} L _ {R} ^ {6} \mathbb {E} [ s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] \\ + \frac {d ^ {4}}{(1 - t) ^ {4}} L _ {R} ^ {4} \mathbb {E} [ s _ {K _ {\mathrm {m i n}}} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {2}, \\ \end{array}
$$

$$
\begin{array}{l} \mathbb {E} [ \| \nabla_ {x} ^ {2} \log p _ {t} (x _ {1} \mid x) \| _ {\mathrm {o p}} ^ {4} \mid X _ {t} = x ] \lesssim \frac {d ^ {4}}{(1 - t) ^ {8}} L _ {R} ^ {1 2} \mathbb {E} [ s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {2 4} ] \\ + \frac {d ^ {8}}{(1 - t) ^ {8}} L _ {R} ^ {8} \mathbb {E} \left[ s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {1 2} \right] ^ {2}, \\ \end{array}
$$

$$
\begin{array}{l} \mathbb {E} [ \| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {t} (x _ {1} \mid x) \| ^ {2} \mid X _ {t} = x ] \lesssim \frac {d ^ {2}}{(1 - t) ^ {4}} L _ {R} ^ {6} \mathbb {E} [ d (x _ {1}, x _ {0}) ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] \\ + \frac {d ^ {4}}{(1 - t) ^ {4}} L _ {R} ^ {4} \mathbb {E} \left[ s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {6} \right] \mathbb {E} \left[ d \left(x _ {0}, x _ {1}\right) ^ {2} s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {6} \right]. \\ \end{array}
$$

Proof. Throughout the proof, we use $r(x)$ to denote the radial distance function $d(x,z)$ , where $z$ is the center of $p_0 \propto \exp(-\beta d(x_0,z)^2)$ . We show the following in Appendix E.3 (Lemma E.7 and Lemma E.8):

$$
\begin{array}{l} \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \leq d \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left(\frac {1}{1 - t} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| + \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right), \\ \left\| \operatorname {g r a d} _ {x} \log p _ {0} (\Psi_ {t, X _ {1}} (X _ {t})) \right\| \leq 2 d d _ {g} (x _ {0}, z) \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}. \\ \end{array}
$$

We also prove the following in (Lemma E.10 and Lemma E.12:

$$
\begin{array}{l} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| \leq 1, \\ \left\| \left(\nabla (d \operatorname {L o g} _ {x})\right) _ {y} \right\| \leq \left\| \left(\nabla (d \operatorname {E x p} _ {x})\right) _ {\operatorname {L o g} _ {x} (y)} \right\|, \\ \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \leq s _ {K _ {\min }} (\| \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x) \|) / \| \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x) \| \lesssim s _ {K _ {\min }} (d (x _ {0}, x _ {1})), \\ \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \leq \frac {1 6}{3} s _ {K _ {\min }} (d (x _ {0}, x _ {1}) / 2) ^ {2} L _ {R} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) \lesssim L _ {R} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {3}, \\ \| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \lesssim L _ {R} ^ {3} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {5}. \\ \end{array}
$$

We estimate the terms as follows. For gradient and time derivative, we have

$$
\| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \lesssim d \frac {1}{1 - t} L _ {R} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {3},
$$

$$
\left\| \operatorname {g r a d} _ {x} \log p _ {0} \left(\Psi_ {t, X _ {1}} \left(X _ {t}\right)\right) \right\| \lesssim d \frac {1}{1 - t} s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) d \left(x _ {0}, z\right),
$$

and

$$
\begin{array}{l} | \partial_ {t} \log J _ {t} (x \mid x _ {1}) | \leq \frac {d}{1 - t} + \frac {d}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \\ \lesssim \frac {d}{1 - t} d (x _ {0}, x _ {1}) s _ {K _ {\mathrm {m i n}}} (d (x _ {0}, x _ {1})) ^ {3} L _ {R}, \\ \end{array}
$$

$$
\begin{array}{l} \left| \partial_ {t} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \right| \leq 2 \beta r \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\text {o p}} \frac {1}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \\ \lesssim \frac {d}{1 - t} d \left(x _ {0}, z\right) s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right). \\ \end{array}
$$

For second covariant derivative,

$$
\begin{array}{l} \left\| \nabla_ {x} ^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \right\| _ {\mathrm {o p}} \\ \leq \left(\left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\text {o p}} \frac {1}{1 - t} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\text {o p}}\right) ^ {2} \left(2 \beta + 2 \beta r \| \nabla^ {2} r \| _ {\text {o p}} \right| _ {\Psi_ {t, x _ {1}} (x)}) \\ + \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| \left(\frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}\right) ^ {2} 2 \beta r \\ \end{array}
$$

$$
\begin{array}{l} + \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| \nabla \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| 2 \beta r \\ \lesssim \frac {1}{(1 - t) ^ {2}} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {2} (d d (x _ {0}, z) \kappa \coth (\kappa d (x _ {0}, z))) \\ + \frac {d}{(1 - t) ^ {2}} s _ {K _ {\mathrm {m i n}}} (d (x _ {0}, x _ {1})) ^ {3} L _ {R} d (x _ {0}, z) + \frac {d}{1 - t} d (x _ {0}, z) s _ {K _ {\mathrm {m i n}}} (d (x _ {0}, x _ {1})) ^ {4} L _ {R} \\ \lesssim \frac {d}{(1 - t) ^ {2}} s _ {K _ {\mathrm {m i n}}} (d (x _ {0}, x _ {1})) ^ {4} L _ {R} d (x _ {0}, z), \\ \end{array}
$$

where notice that $x \coth(x)$ is of order $x$ . And we have

$$
\begin{array}{l} \left\| \nabla_ {x} ^ {2} \log J _ {t} (x \mid x _ {1}) \right\| _ {\mathrm {o p}} \\ \leq d \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| ^ {2} \left[ \frac {1}{(1 - t) ^ {2}} \Big (\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \Big) \right. \\ \left. + \left(\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right) \right] \\ + d \left\| \nabla (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| \left(\frac {1}{1 - t} \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| + \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \right\|\right) \\ \lesssim \frac {d}{(1 - t) ^ {2}} (L _ {R} ^ {2} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} + L _ {R} ^ {3} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {5}) + \frac {d}{1 - t} L _ {R} ^ {2} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} \\ \lesssim \frac {d}{(1 - t) ^ {2}} L _ {R} ^ {3} s _ {K _ {\mathrm {m i n}}} (d (x _ {0}, x _ {1})) ^ {6}. \\ \end{array}
$$

For time derivative of gradient,

$$
\begin{array}{l} \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \right\| \\ \leq \left(\left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\text {o p}} \frac {1}{1 - t} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\text {o p}}\right) \times \left(2 \beta + 2 \beta r \| \nabla^ {2} r \| _ {\text {o p}} \Big | _ {\Psi_ {t, x _ {1}} (x)}\right) \\ \times \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\text {o p}} \frac {1}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \\ + \left[ \frac {1}{(1 - t) ^ {2}} \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\mathrm {o p}} \right. \\ \left. + \frac {1}{(1 - t) ^ {3}} \left\| \operatorname {L o g} _ {x _ {1}} (x) \right\| \left\| \nabla \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\mathrm {o p}} \right] 2 \beta r \\ \lesssim \Big (d + d d (x _ {0}, z) \Big) s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {2} \frac {1}{(1 - t) ^ {2}} \\ + d d (x _ {0}, z) \left(\frac {1}{(1 - t) ^ {2}} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) + \frac {1}{(1 - t) ^ {2}} d (x _ {0}, x _ {1}) L _ {R} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {3}\right) \\ \lesssim d (x _ {0}, z) \frac {d}{(1 - t) ^ {2}} d (x _ {0}, x _ {1}) L _ {R} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {3}. \\ \end{array}
$$

And we have

$$
\| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \|
$$

$$
\begin{array}{l} \leq \| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \| \left[ \frac {d}{(1 - t) ^ {2}} \| \nabla \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \right. \\ \left. + \frac {d}{(1 - t) ^ {3}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \Big (\| \nabla \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| \nabla^ {2} \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \Big) \right] \\ \lesssim \frac {d}{(1 - t) ^ {2}} L _ {R} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {3} + \frac {d}{(1 - t) ^ {2}} d (x _ {1}, x _ {0}) \left(L _ {R} ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} + L _ {R} ^ {3} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {5}\right) \\ \lesssim \frac {d}{(1 - t) ^ {2}} L _ {R} ^ {3} d (x _ {1}, x _ {0}) s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6}. \\ \end{array}
$$

The three inequalities on Log follow from Appendix E.5:

$$
\| \nabla_ {x} \operatorname {L o g} _ {x} (y) \| _ {\mathrm {o p}} ^ {2} \leq 2 + 2 d (x, y) ^ {2} \Big (\frac {s _ {K _ {\min}} ^ {\prime} (d (x , y))}{s _ {K _ {\min}} (d (x , y))} \Big) ^ {2},
$$

$$
| \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (y) | ^ {2} \leq 2 + 2 (d - 1) ^ {2} d (x, y) ^ {2} \left(\frac {s _ {K _ {\operatorname* {m i n}}} ^ {\prime} (d (x , y))}{s _ {K _ {\operatorname* {m i n}}} (d (x , y))}\right) ^ {2},
$$

$$
\| \operatorname {g r a d} \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (y) \| \leq \frac {\sqrt {2} d}{2} \left(2 \left(1 + d (x, y) \frac {s _ {K _ {\min}} ^ {\prime} (d (x , y))}{s _ {K _ {\min}} (d (x , y))}\right)\right) ^ {\frac {3}{2}}.
$$

Now we prove the inequalities on derivatives of $\log p_t$ . We remark that due to Lemma E.4, comparing point-wise upper bounds for derivative of $\log J_t$ and that of $\log p_0$ , since the $d(x_0,z)$ term doesn't increase the order of expectation compared with $d(x_0,x_1)$ term, we can treat $d(x_0,z)$ as $d(x_0,x_1)$ and see that derivatives of $\log J_t$ dominate over the same derivative of $\log p_0$ . Thus in computing derivatives of $\log p_t = \log p_0(\Psi_{t,x_1}(x)) + \log J_t(x|x_1) + \mathrm{const}$ , it suffices to consider derivatives of $\log J_t(x|x_1)$ terms.

The first four inequalities are straightforward by applying the Cauchy-Schwarz inequality, and note that they are dominated by the log $J_{t}$ terms. Following Lemma D.8

$$
\begin{array}{l} \| \nabla_ {x} ^ {2} \log p _ {t} (x _ {1} \mid x) \| _ {\mathrm {o p}} ^ {2} \lesssim \| \nabla^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\mathrm {o p}} ^ {2} + \mathbb {E} \left[ \| \nabla^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\mathrm {o p}} ^ {2} \mid X _ {t} = x \right] \\ + \mathbb {E} \left[ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| ^ {2} \mid X _ {t} = x \right] \mathbb {E} \left[ \| \operatorname {g r a d} \log p _ {t} (x _ {1} \mid x) \| ^ {2} \mid X _ {t} = x \right], \\ \end{array}
$$

$$
\begin{array}{l} \| \nabla_ {x} ^ {2} \log p _ {t} (x _ {1} \mid x) \| _ {\mathrm {o p}} ^ {4} \lesssim \| \nabla^ {2} \log J _ {t} (x \mid X _ {1}) \| _ {\mathrm {o p}} ^ {4} \\ + \mathbb {E} \left[ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| ^ {4} \mid X _ {t} = x \right] \mathbb {E} \left[ \| \operatorname {g r a d} \log p _ {t} (x _ {1} \mid x) \| ^ {4} \mid X _ {t} = x \right], \\ \end{array}
$$

and plug in the corresponding expression (using Cauch-Schwarz), we obtain the bounds for the Hessian of $\log p_t$ , and following Lemma D.9,

$$
\begin{array}{l} \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {t} \left(x _ {1} \mid x\right) \right\| \leq \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} \left(x \mid x _ {1}\right) \right\| + \mathbb {E} \left[ \| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} \left(x \mid X _ {1}\right) \| \mid X _ {t} = x \right] \\ + \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid X _ {1}) \| | \partial_ {t} \log p _ {t} (X _ {1} \mid x) | \mid X _ {t} = x ], \\ \end{array}
$$

we plug in the corresponding expressions (using Cauch-Schwarz), we obtain the last inequality.

We summarize the required bound in the following Lemma, which is similar to Lemma D.10, D.11, D.12 and D.13.

Lemma E.6. On $\mathrm{SPD}(n)$ , with prior distribution being $p_0 \propto \exp(-dd(x_0, z)^2)$ , under the conditions in Assumption 1, we have

$$
\mathbb {E} [ \| v (t, x) \| ^ {2} ] \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ],
$$

$$
\begin{array}{l} \mathbb {E} [ \| \nabla v (t, x) \| ] \lesssim \frac {d}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}}, \\ \mathbb {E} [ | \frac {d}{d t} v (t, x) | ] \lesssim \frac {d}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}}, \\ \mathbb {E} [ \| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| ] \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ] \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {3}, \\ \mathbb {E} [ | \frac {d}{d t} \operatorname {d i v} v (t, x) | ] \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {3} \mathbb {E} [ d (x _ {1}, x _ {0}) ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] ^ {\frac {1}{2}}. \\ \end{array}
$$

Furthermore,

$$
\begin{array}{l} \mathbb {E} [ \| \nabla v (t, x) \| ^ {2} ] \lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {4} ] ^ {\frac {1}{2}} \mathbb {E} [ s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] ^ {\frac {1}{2}}, \\ \mathbb {E} [ | \frac {d}{d t} v (t, x) | ^ {2} ] \lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {4} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] ^ {\frac {1}{2}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {4} ] ^ {\frac {1}{2}}, \\ \mathbb {E} [ \| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \| ^ {2} ] \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] \frac {d ^ {4}}{(1 - t) ^ {4}} L _ {R} ^ {6}. \\ \end{array}
$$

Proof. Throughout the proof, we will use the bounds in Lemma E.5. We first control the vector field regularity. This is similar to Lemma D.10 and Lemma D.11. We have

$$
\begin{array}{l} \mathbb {E} \left[ \| \nabla v (t, x) \| \right] \leq \frac {1}{1 - t} \mathbb {E} \left[ \| \operatorname {L o g} _ {x} (X _ {1}) \| \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| \mid X _ {t} = x \right] \\ + \frac {1}{1 - t} \mathbb {E} [ \| \nabla \operatorname {L o g} _ {x} (x _ {1}) \| | X _ {t} = x ] \\ \lesssim \frac {d}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}}, \\ \end{array}
$$

and

$$
\begin{array}{l} \mathbb {E} [ | \frac {d}{d t} v (t, x) | ] = \frac {1}{(1 - t) ^ {2}} \mathbb {E} [ \operatorname {L o g} _ {x} (x _ {1}) \mid X _ {t} = x ] + \frac {1}{1 - t} \mathbb {E} [ \operatorname {L o g} _ {x} (x _ {1}) \partial_ {t} \log p _ {t} (x _ {1} \mid x) \mid X _ {t} = x ] \\ \lesssim \frac {d}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}}. \\ \end{array}
$$

Now we control the divergence regularity. Similar to Lemma D.12 and, we have

$$
\left\| \operatorname {g r a d} _ {x} \operatorname {d i v} v (t, x) \right\| \leq \frac {1}{1 - t} \left(T _ {1} + T _ {2} + T _ {3} + T _ {4}\right),
$$

where

$$
\begin{array}{l} \mathbb {E} [ T _ {1} ] = \mathbb {E} [ \| \operatorname {g r a d} _ {x} \operatorname {d i v} _ {x} \log_ {x} (X _ {1}) \| ] \\ \lesssim d \mathbb {E} \left[ d \left(x _ {0}, x _ {1}\right) ^ {\frac {3}{2}} \right], \\ \end{array}
$$

$$
\begin{array}{l} \mathbb {E} [ T _ {2} ] = \mathbb {E} [ | \operatorname {d i v} _ {x} \log_ {x} (X _ {1}) | \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ] \\ \lesssim \mathbb {E} [ | \operatorname {d i v} _ {x} \log_ {x} (X _ {1}) | ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} ] ^ {\frac {1}{2}} \\ \lesssim \frac {d ^ {2}}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}}, \\ \end{array}
$$

$$
\mathbb {E} [ T _ {3} ] = \mathbb {E} [ \| \operatorname {g r a d} _ {x} \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \| ]
$$

$$
\begin{array}{l} \leq \mathbb {E} [ \| \nabla \log_ {x} (X _ {1}) \| \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ] \\ + \mathbb {E} [ \| \nabla^ {2} \log p _ {t} (X _ {1} \mid x) \| \| \log_ {x} (X _ {1}) \| ] \\ \lesssim \left(\mathbb {E} [ d (x, x _ {1}) ^ {2} ] \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} \left[ s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {6} \right]\right) ^ {\frac {1}{2}} \\ + \left(\frac {d ^ {2}}{(1 - t) ^ {4}} L _ {R} ^ {6} \mathbb {E} \left[ s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {1 2} \right] \mathbb {E} \left[ d (x, x _ {1}) ^ {2} \right]\right) ^ {\frac {1}{2}} \\ \lesssim \frac {d}{1 - t} L _ {R} ^ {3} \mathbb {E} [ s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {1 2} ] ^ {\frac {1}{2}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}}, \\ \end{array}
$$

$$
\begin{array}{l} \mathbb {E} [ T _ {4} ] = \mathbb {E} [ | \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle | | \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) | | ] \\ \leq \mathbb {E} [ \| \log_ {x} (X _ {1}) \| \| \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x) \| ^ {2} ] \\ \lesssim \mathbb {E} [ d (x, x _ {1}) s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ] \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \\ \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ] \frac {d ^ {2}}{1 - t} L _ {R} ^ {2}. \\ \end{array}
$$

Similar to Lemma D.13,

$$
\begin{array}{l} \frac {d}{d t} \operatorname {d i v} v (t, x) = \frac {1}{(1 - t) ^ {2}} \mathbb {E} \left[ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(X _ {1}\right) + \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \mid X _ {t} = x \right] \\ + \frac {1}{1 - t} \mathbb {E} \left[ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(X _ {1}\right) \partial_ {t} \log p _ {t} \left(X _ {1} \mid x\right) \mid X _ {t} = x \right] \\ + \frac {1}{1 - t} \mathbb {E} \left[ \partial_ {t} \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \mid X _ {t} = x \right] \\ + \frac {1}{1 - t} \mathbb {E} [ \langle \operatorname {g r a d} _ {x} \log p _ {t} (X _ {1} \mid x), \operatorname {L o g} _ {x} (X _ {1}) \rangle \partial_ {t} \log p _ {t} (X _ {1} \mid x) \mid X _ {t} = x ]. \\ \end{array}
$$

We bound

$$
\begin{array}{l} \mathbb {E} \left[ T _ {1} \right] = \frac {1}{(1 - t) ^ {2}} \mathbb {E} \left[ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(X _ {1}\right) + \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \right] \\ \lesssim \frac {d}{(1 - t) ^ {2}} \mathbb {E} [ d (x, x _ {1}) ] + \frac {1}{(1 - t) ^ {2}} \mathbb {E} [ d (x, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}} \\ \lesssim \frac {d}{1 - t} \mathbb {E} [ d (x _ {0}, x _ {1}) ] + \frac {d}{(1 - t) ^ {2}} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ] ] ^ {\frac {1}{2}}, \\ \end{array}
$$

$$
\begin{array}{l} \mathbb {E} \left[ T _ {2} \right] = \frac {1}{1 - t} \mathbb {E} \left[ \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} \left(X _ {1}\right) \partial_ {t} \log p _ {t} \left(X _ {1} \mid x\right) \right] \\ \lesssim \frac {1}{1 - t} d \mathbb {E} [ d (x, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \frac {d}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}} \\ \lesssim \frac {d ^ {2}}{1 - t} L _ {R} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {6} ] ^ {\frac {1}{2}}, \\ \end{array}
$$

$$
\begin{array}{l} \mathbb {E} \left[ T _ {3} \right] = \frac {1}{1 - t} \mathbb {E} \left[ \partial_ {t} \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \right] \\ \lesssim \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {2} ] ^ {\frac {1}{2}} \frac {d}{(1 - t) ^ {2}} L _ {R} ^ {3} \mathbb {E} [ d (x _ {1}, x _ {0}) ^ {2} s _ {K _ {\min }} (d (x _ {0}, x _ {1})) ^ {1 2} ] ^ {\frac {1}{2}}, \\ \end{array}
$$

$$
\begin{array}{l} \mathbb {E} \left[ T _ {4} \right] = \frac {1}{1 - t} \mathbb {E} \left[ \left\langle \operatorname {g r a d} _ {x} \log p _ {t} \left(X _ {1} \mid x\right), \operatorname {L o g} _ {x} \left(X _ {1}\right) \right\rangle \partial_ {t} \log p _ {t} \left(X _ {1} \mid x\right) \right] \\ \lesssim \frac {1}{1 - t} \left(\frac {d ^ {3}}{(1 - t) ^ {3}} L _ {R} ^ {3} \mathbb {E} \left[ s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {9} \right]\right) ^ {\frac {1}{3}} \mathbb {E} \left[ d \left(x, x _ {1}\right) ^ {3} \right] ^ {\frac {1}{3}} \left(\frac {d ^ {3}}{(1 - t) ^ {3}} L _ {R} ^ {3} \mathbb {E} \left[ d \left(x _ {0}, x _ {1}\right) ^ {3} s _ {K _ {\min }} \left(d \left(x _ {0}, x _ {1}\right)\right) ^ {9} \right]\right) ^ {\frac {1}{3}} \\ \end{array}
$$

$$
\lesssim \frac {d ^ {2}}{(1 - t) ^ {2}} L _ {R} ^ {2} \mathbb {E} [ s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {9} ] ^ {\frac {1}{3}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {3} ] ^ {\frac {1}{3}} \mathbb {E} [ d (x _ {0}, x _ {1}) ^ {3} s _ {K _ {\min}} (d (x _ {0}, x _ {1})) ^ {9} ] ^ {\frac {1}{3}}.
$$

Higher order bounds follow exactly the same procedure.

# E.3 Auxiliary Bounds on Derivatives

Recall that we are using the following notation

$$
\Psi_ {t, x _ {1}} (x) = \mathrm {E x p} _ {x _ {1}} \left(\frac {1}{1 - t} \mathrm {L o g} _ {x _ {1}} (x)\right).
$$

Lemma E.7 (Controlling derivatives of $\log p_0$ ). Let $M$ be a Hadamard manifold. Fix $\beta > 0$ , $m = 2$ , and $z \in M$ , and define

$$
p _ {0} (x) \propto \exp \left(- \beta d (x, z) ^ {m}\right).
$$

Fix $t \in [0,1)$ , $x_1 \in M$ , and $x \in M$ . Define $r := d(\Psi_{t,x_1}(x), z)$ , so that $r$ represents the radial distance between $x_0$ and $z$ . Then the following bounds hold:

$$
\begin{array}{l} \left\| \operatorname {g r a d} _ {x} \log p _ {0} \Psi_ {t, x _ {1}} (x) \right\| \leq 2 \beta r \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}, \\ \left| \partial_ {t} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \right| \leq 2 \beta r \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{(1 - t) ^ {2}} \left\| \operatorname {L o g} _ {x _ {1}} (x) \right\|, \\ \end{array}
$$

$$
\begin{array}{l} \| \nabla_ {x} ^ {2} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \| _ {\mathrm {o p}} \leq \Big (\bigg \| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \bigg \| _ {\mathrm {o p}} \frac {1}{1 - t} \bigg \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \bigg \| _ {\mathrm {o p}} \Big) ^ {2} \\ \left(2 \beta + 2 \beta r \| \nabla^ {2} r \| _ {\mathrm {o p}} \Big | _ {\Psi_ {t, x _ {1}} (x)}\right) \\ + \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| \left(\frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}\right) ^ {2} 2 \beta r \\ + \left\| (d \mathrm {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \mathrm {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| \nabla (d \mathrm {L o g} _ {x _ {1}}) _ {x} \right\| 2 \beta r, \\ \end{array}
$$

$$
\begin{array}{l} \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \right\| \leq \left(\left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\mathrm {o p}}\right) \\ \times \left(2 \beta + 2 \beta r \| \nabla^ {2} r \| _ {\mathrm {o p}} \Big | _ {\Psi_ {t, x _ {1}} (x)}\right) \\ \times \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{(1 - t) ^ {2}} \left\| \operatorname {L o g} _ {x _ {1}} (x) \right\| \\ + \left[ \frac {1}{(1 - t) ^ {2}} \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}} \right. \\ + \frac {1}{(1 - t) ^ {3}} \left\| \operatorname {L o g} _ {x _ {1}} (x) \right\| \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}} \Biggr ] 2 \beta r. \\ \end{array}
$$

where

$$
\| \nabla^ {2} r \| _ {\mathrm {o p}} \Big | _ {\Psi_ {t, x _ {1}} (x)} \leq \frac {s _ {K _ {\mathrm {m i n}}} ^ {\prime} (r)}{s _ {K _ {\mathrm {m i n}}} (r)} = \sqrt {- K _ {\mathrm {m i n}}} \coth (r \sqrt {- K _ {\mathrm {m i n}}}).
$$

and note that $r \mapsto r \cosh(r)$ has no singularity at $r = 0$ .

Proof. We start with deriving bounds for $\| \operatorname{grad} \log p_0(\Psi_{t,x_1}(x))\|$ and $\| \nabla^2 \log p_0(\Psi_{t,x_1}(x))\|_{\mathrm{op}}$ . Since $\log p_0(y) = -\beta d(y,z)^m + \mathrm{const}$ , and $\| \operatorname{grad} d(\cdot, z)\| = 1$ , we have

$$
\left\| \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \right\| = 2 \beta r.
$$

Moreover, notice that

$$
\nabla^ {2} (d (y, z) ^ {m}) = 2 d (y, z) \nabla^ {2} d (y, z) + 2 \operatorname {g r a d} d (y, z) \otimes \operatorname {g r a d} d (y, z).
$$

The above identity, together with $\| \operatorname{grad} d(y,z) \otimes \operatorname{grad} d(y,z)\|_{\mathrm{op}} = 1$ , yields

$$
\left. \left\| \nabla^ {2} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \right\| _ {\mathrm {o p}} \leq 2 \beta + 2 \beta r \left\| \nabla^ {2} r \right\| _ {\mathrm {o p}} \right| _ {\Psi_ {t, x _ {1}} (x)}.
$$

We next derive the first (spatial) derivative of $\Psi_{t,x_1}$ . Using the chain rule,

$$
(d \Psi_ {t, x _ {1}}) _ {x} [ u ] = (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \left[ \frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u ] \right], \qquad \forall u \in T _ {x} M.
$$

Hence

$$
\left\| \left(d \Psi_ {t, x _ {1}}\right) _ {x} \right\| _ {\mathrm {o p}} \leq \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\mathrm {o p}}. \tag {26}
$$

For any $u \in T_xM$ , the chain rule gives the identity

$$
\left\langle \operatorname {g r a d} _ {x} \log p _ {0} (\Psi_ {t, x _ {1}} (x)), u \right\rangle = \left\langle \operatorname {g r a d} \log p _ {0} (\Psi_ {t, x _ {1}} (x)), (d \Psi_ {t, x _ {1}}) _ {x} [ u ] \right\rangle .
$$

Therefore, by Cauchy-Schwarz with supremum over $\| u\| = 1$ , yields

$$
\begin{array}{l} \left| \langle \operatorname {g r a d} _ {x} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right), u \rangle \right| \leq \| \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| \| \left(d \Psi_ {t, x _ {1}}\right) _ {x} [ u ] \| \\ \leq \left\| \operatorname {g r a d} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \right\| \left\| (d \Psi_ {t, x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}. \\ \end{array}
$$

Substituting $\| \operatorname{grad} \log p_0(\Psi_{t,x_1}(x)) \| = 2\beta r$ and using (26), we obtain

$$
\begin{array}{l} \left\| \operatorname {g r a d} _ {x} \log p _ {0} \left(\operatorname {E x p} _ {x _ {1}} \left(\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)\right)\right) \right\| \\ \leq 2 \beta r \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}. \\ \end{array}
$$

Now we work on the first time derivative. Recall $\Psi_{t,x_1}(x) = \mathrm{Exp}_{x_1}\left(\frac{1}{1 - t}\mathrm{Log}_{x_1}(x)\right)$ . By chain rule,

$$
\partial_ {t} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) = \left\langle \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right), \partial_ {t} \Psi_ {t, x _ {1}} (x) \right\rangle ,
$$

where $\partial_t\Psi_{t,x_1}(x) = (d\mathrm{Exp}_{x_1})_{\frac{1}{1 - t}\mathrm{Log}_{x_1}(x)}\Bigl [\frac{1}{(1 - t)^2}\mathrm{Log}_{x_1}(x)\Bigr ]$ . By Cauchy-Schwarz,

$$
\begin{array}{l} \left| \partial_ {t} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \right| \leq \| \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| \| \partial_ {t} \Psi_ {t, x _ {1}} (x) \| \\ \leq \| \operatorname {g r a d} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \| \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \\ \leq 2 \beta r \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{(1 - t) ^ {2}} \left\| \operatorname {L o g} _ {x _ {1}} (x) \right\|, \\ \end{array}
$$

where recall $\| \operatorname{grad} \log p_0(\Psi_{t,x_1}(x))\| = 2\beta r$

Now we compute the Hessian. For any $u, w \in T_xM$ , using chain rule, we obtain

$$
\begin{array}{l} \nabla_ {x} ^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) [ u, w ] = \nabla^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \left[ \left(\Psi_ {t, x _ {1}}\right) _ {x} [ u ], \left(\Psi_ {t, x _ {1}}\right) _ {x} [ w ] \right] \\ + \left\langle \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right), \nabla_ {u} \left(\left(\Psi_ {t, x _ {1}}\right) _ {x} [ w ]\right) \right\rangle . \\ \end{array}
$$

By Cauchy-Schwarz and taking the supremum over $\| u \| = \| w \| = 1$ , we obtain

$$
\begin{array}{l} \| \nabla_ {x} ^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| _ {\text {o p}} = \sup  _ {\| u \| = \| w \| = 1} \left| \nabla_ {x} ^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) [ u, w ] \right| \\ \leq \sup  _ {\| u \| = \| w \| = 1} \| \nabla^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| _ {\text {o p}} \| \left(\Psi_ {t, x _ {1}}\right) _ {x} [ u ] \| \| \left(\Psi_ {t, x _ {1}}\right) _ {x} [ w ] \| \\ + \| \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| \left\| \nabla_ {u} \left(\left(\Psi_ {t, x _ {1}}\right) _ {x} [ w ]\right) \right\| \\ \leq \| \nabla^ {2} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \| _ {\mathrm {o p}} \| (\Psi_ {t, x _ {1}}) _ {x} \| _ {\mathrm {o p}} ^ {2} + \| \operatorname {g r a d} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \| \| \nabla (\Psi_ {t, x _ {1}}) _ {x} \|. \\ \end{array}
$$

It remains to bound $\| \nabla (\Psi_{t,x_1})_x\|$ . Recall that

$$
(\Psi_ {t, x _ {1}}) _ {x} [ w ] = (d \operatorname {E x p} _ {x _ {1}}) \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x) \Big [ \frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ w ] \Big ].
$$

Recall the Leibniz rule with $v = \frac{1}{1 - t}\operatorname{Log}_{x_1}(x)$ being a $x$ -dependent tangent vector at $T_{x_1}M$ .

$$
\begin{array}{l} \nabla_ {u} \big ((\Psi_ {t, x _ {1}}) _ {x} [ w ] \big) = \nabla_ {u} \Big ((d \operatorname {E x p} _ {x _ {1}}) _ {v} \left[ \frac {1}{1 - t} (d \log_ {x _ {1}}) _ {x} [ w ] \right] \Big) \\ = \left(\nabla_ {\nabla_ {u} v} (d \operatorname {E x p} _ {x _ {1}})\right) _ {v} \Big [ \frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ w ] \Big ] + \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {v} \Big [ \frac {1}{1 - t} \nabla_ {u} \big ((d \operatorname {L o g} _ {x _ {1}}) _ {x} [ w ] \big) \Big ]. \\ \end{array}
$$

where note that $v$ depends on $x$ , so using chain rule,

$$
\begin{array}{l} \nabla_ {u} ((d \operatorname {E x p} _ {x _ {1}}) _ {v}) = \nabla_ {u} ((d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)}) \\ = \left(\nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)}\right) \left(\nabla_ {u} \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)\right) \\ = \left(\nabla_ {\nabla_ {u}} \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x) \left(d \operatorname {E x p} _ {x _ {1}}\right)\right) \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x). \\ \end{array}
$$

Notice that for $v = \frac{1}{1 - t}\operatorname{Log}_{x_1}(x)$ , its first derivative is a directional derivative. We have

$$
\nabla_ {u} v = \frac {1}{1 - t} \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} [ u ], \qquad \text {a n d} \qquad \nabla_ {u} \bigl (\left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} [ w ] \bigr) = \nabla (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u, w ].
$$

Taking norms and applying the definitions of the operator norms gives

$$
\begin{array}{l} \left\| \nabla_ {u} \big ((\Psi_ {t, x _ {1}}) _ {x} [ w ] \big) \right\| \leq \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {v} \right\| \left\| \nabla_ {u} v \right\| \left\| \frac {1}{1 - t} (d \log_ {x _ {1}}) _ {x} [ w ] \right\| \\ + \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {v} \right\| _ {\text {o p}} \frac {1}{1 - t} \| \nabla \left(d \log_ {x _ {1}}\right) _ {x} [ u, w ] \| \\ = \left\| \nabla \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {v} \right\| \left\| \frac {1}{1 - t} \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} [ u ] \right\| \left\| \frac {1}{1 - t} \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} [ w ] \right\| \\ + \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {v} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| \nabla (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u, w ] \right\|. \\ \end{array}
$$

Taking supremum over $\| u \| = \| w \| = 1$ , we obtain

$$
\left\| \nabla \bigl ((d \Psi_ {t, x _ {1}}) _ {x} \bigr) \right\| \leq \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {v} \right\| \left(\frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}\right) ^ {2} + \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {v} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| \nabla (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\|.
$$

Finally using the fact that

$$
\begin{array}{l} \left\| \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \right\| = 2 \beta r, \\ \| \nabla^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| _ {\text {o p}} \leq 2 \beta + 2 \beta r \| \nabla^ {2} r \| _ {\text {o p}} \big | _ {\Psi_ {t, x _ {1}} (x)}, \\ \end{array}
$$

and using (26), we have

$$
\begin{array}{l} \| \nabla_ {x} ^ {2} \log p _ {0} (\Psi_ {t, x _ {1}} (x)) \| _ {\mathrm {o p}} \\ \leq \| \nabla^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| _ {\text {o p}} \| \left(\Psi_ {t, x _ {1}}\right) _ {x} \| _ {\text {o p}} ^ {2} + \| \text {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| \| \nabla \left(\Psi_ {t, x _ {1}}\right) _ {x} \| \\ \leq \left(\left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\text {o p}} \frac {1}{1 - t} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\text {o p}}\right) ^ {2} \left(2 \beta + 2 \beta r \| \nabla^ {2} r \| _ {\text {o p}} \Big | _ {\Psi_ {t, x _ {1}} (x)}\right) \\ + \left\| \nabla \left(d \operatorname {E x p} _ {x _ {1}}\right) \frac {1}{1 - t} \log_ {x _ {1}} (x) \right\| \left(\frac {1}{1 - t} \| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \| _ {\mathrm {o p}}\right) ^ {2} 2 \beta r \\ + \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\text {o p}} \frac {1}{1 - t} \| \nabla \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \| 2 \beta r. \\ \end{array}
$$

It remains to consider the mixed derivative term. For any $u \in T_xM$ , recall we have

$$
\left\langle \operatorname {g r a d} _ {x} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right), u \right\rangle = \left\langle \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right), \left(\Psi_ {t, x _ {1}}\right) _ {x} [ u ] \right\rangle .
$$

Differentiate both sides in $t$ (with $x_{1}, x, u$ fixed):

$$
\begin{array}{l} \left\langle \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right), u \right\rangle = \left\langle \nabla^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \left[ \partial_ {t} \Psi_ {t, x _ {1}} (x) \right], \left(\Psi_ {t, x _ {1}}\right) _ {x} [ u ] \right\rangle \\ + \left\langle \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right), \partial_ {t} \left(\left(\Psi_ {t, x _ {1}}\right) _ {x} [ u ]\right) \right\rangle . \\ \end{array}
$$

By Cauchy-Schwarz,

$$
\begin{array}{l} \left| \left\langle \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right), u \right\rangle \right| \leq \| \nabla^ {2} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| _ {\mathrm {o p}} \| \partial_ {t} \Psi_ {t, x _ {1}} (x) \| \| \left(\Psi_ {t, x _ {1}}\right) _ {x} \| _ {\mathrm {o p}} \| u \| \\ + \| \operatorname {g r a d} \log p _ {0} \left(\Psi_ {t, x _ {1}} (x)\right) \| \left\| \partial_ {t} \left(\left(\Psi_ {t, x _ {1}}\right) _ {x} [ u ]\right) \right\|. \\ \end{array}
$$

We already have $\| \partial_t\Psi_{t,x_1}(x)\|$ and $\| (\Psi_{t,x_1})_x\|_{\mathrm{op}}$ from previous steps.

It remains to bound $\| \partial_t((\Psi_{t,x_1})_x[u])\|$ . Recall for any $u\in T_xM$

$$
\left(\Psi_ {t, x _ {1}}\right) _ {x} [ u ] = \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {v} \left[ \frac {1}{1 - t} \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} [ u ] \right], \quad v = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x).
$$

Fix $x_1, x, u$ and differentiate with respect to $t$ . Since $x$ is fixed, the tensor $(d\operatorname{Log}_{x_1})_x[u]$ does not depend on $t$ ; only the scalar factor $\frac{1}{1 - t}$ and the point $v$ depend on $t$ . By the Leibniz rule (product rule for a $t$ -dependent linear map applied to a $t$ -dependent vector),

$$
\partial_ {t} \big ((\Psi_ {t, x _ {1}}) _ {x} [ u ] \big) = \partial_ {t} \Big ((d \operatorname {E x p} _ {x _ {1}}) _ {v} \Big) \Big [ \frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u ] \Big ] + (d \operatorname {E x p} _ {x _ {1}}) _ {v} \Big [ \partial_ {t} \Big (\frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u ] \Big) \Big ].
$$

For the first term, $(d\mathrm{Exp}_{x_1})_v$ depends on $t$ only through $v(t)$ , hence the chain rule gives

$$
\partial_ {t} \Big ((d \operatorname {E x p} _ {x _ {1}}) _ {v} \Big) = \Big (\nabla (d \operatorname {E x p} _ {x _ {1}}) _ {v} \Big) (\partial_ {t} v) = \Big (\nabla_ {\partial_ {t} v} (d \operatorname {E x p} _ {x _ {1}}) \Big) _ {v}.
$$

For the second term, since $(d\log_{x_1})_x[u]$ is $t$ -independent,

$$
\partial_ {t} \Big (\frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u ] \Big) = \frac {1}{(1 - t) ^ {2}} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u ].
$$

Combining these identities yields the formula

$$
\partial_ {t} \big ((\Psi_ {t, x _ {1}}) _ {x} [ u ] \big) = \Big (\nabla_ {\partial_ {t} v} (d \operatorname {E x p} _ {x _ {1}}) \Big) _ {v} \Big [ \frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u ] \Big ] + (d \operatorname {E x p} _ {x _ {1}}) _ {v} \Big [ \frac {1}{(1 - t) ^ {2}} (d \operatorname {L o g} _ {x _ {1}}) _ {x} [ u ] \Big ].
$$

Noting $\partial_t v = \frac{1}{(1 - t)^2}\operatorname{Log}_{x_1}(x)$ , we take norms and obtain (for $\| u\| = 1$ )

$$
\begin{array}{l} \left\| \partial_ {t} \big ((\Psi_ {t, x _ {1}}) _ {x} [ u ] \big) \right\| \\ \leq \left\| \nabla \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {v} \right\| \| \partial_ {t} v \| \left\| \frac {1}{1 - t} \left(d \log_ {x _ {1}}\right) _ {x} [ u ] \right\| \\ + \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {v} \right\| _ {\mathrm {o p}} \frac {1}{(1 - t) ^ {2}} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}} \| u \| \\ = \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {v} \right\| \frac {1}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}} \\ + \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {v} \right\| _ {\mathrm {o p}} \frac {1}{(1 - t) ^ {2}} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}} \\ = \frac {1}{(1 - t) ^ {3}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \left\| \nabla \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {v} \right\| \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\mathrm {o p}} \\ + \frac {1}{(1 - t) ^ {2}} \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {v} \right\| _ {\mathrm {o p}} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}. \\ \end{array}
$$

Substituting the expressions for $\| \operatorname{grad} \log p_0(\Psi_{t,x_1}(x))\|$ and $\| \nabla^2 \log p_0(\Psi_{t,x_1}(x))\|_{\mathrm{op}}$ , we get

$$
\begin{array}{l} \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log p _ {0} \Big (\operatorname {E x p} _ {x _ {1}} \big (\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x) \big) \Big) \right\| \\ \leq \left(\left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \frac {1}{1 - t} \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}}\right) \\ \times \left(2 \beta + 2 \beta r \| \nabla^ {2} r \| _ {\mathrm {o p}} \Big | _ {\Psi_ {t, x _ {1}} (x)}\right) \\ \times \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\text {o p}} \frac {1}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \\ + \left[ \frac {1}{(1 - t) ^ {2}} \left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| _ {\mathrm {o p}} \left\| \left(d \operatorname {L o g} _ {x _ {1}}\right) _ {x} \right\| _ {\mathrm {o p}} \right. \\ + \frac {1}{(1 - t) ^ {3}} \left\| \operatorname {L o g} _ {x _ {1}} (x) \right\| \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| _ {\mathrm {o p}} \Biggr ] 2 \beta r. \\ \end{array}
$$

Finally, we remark that when $K_{\mathrm{min}} < 0$ , the Hessian comparison theorem gives

$$
\| \nabla^ {2} r \| _ {\mathrm {o p}} \Big | _ {\Psi_ {t, x _ {1}} (x)} \leq \frac {s _ {K _ {\mathrm {m i n}}} ^ {\prime} (r)}{s _ {K _ {\mathrm {m i n}}} (r)} = \sqrt {- K _ {\mathrm {m i n}}} \coth (r \sqrt {- K _ {\mathrm {m i n}}}).
$$

Lemma E.8 (Controlling derivatives of $J_{t}$ -terms). Assume $M$ is a Hadamard manifold. Fix $x_{1} \in M$ , $x \in M$ , and $t \in (0,1)$ . Recall

$$
\begin{array}{l} J _ {t} (x \mid x _ {1}) = (1 - t) ^ {- d} \frac {\left| \det (d \mathrm {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \mathrm {L o g} _ {x _ {1}} (x)} \right|}{\left| \det (d \mathrm {E x p} _ {x _ {1}}) _ {\mathrm {L o g} _ {x _ {1}} (x)} \right|}, \\ \log J _ {t} (x \mid x _ {1}) = - d \log (1 - t) + \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} - \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)}. \\ \end{array}
$$

Then the following pointwise bounds hold.

$$
\| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \leq d \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left(\frac {1}{1 - t} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| + \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right),
$$

$$
\begin{array}{l} \| \nabla_ {x} ^ {2} \log J _ {t} (x \mid x _ {1}) \| _ {\mathrm {o p}} \leq d \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| ^ {2} \left[ \frac {1}{(1 - t) ^ {2}} \left(\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} \right. \right. \\ \left. + \left\| \nabla^ {2} \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\|\right) \\ \left. + \left(\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right) \right] \\ + d \| \nabla (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left(\frac {1}{1 - t} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| + \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right), \\ \end{array}
$$

$$
| \partial_ {t} \log J _ {t} (x \mid x _ {1}) | \leq \frac {d}{1 - t} + \frac {d}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \|,
$$

$$
\begin{array}{l} \| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \leq \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left[ \frac {d}{(1 - t) ^ {2}} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t}} \operatorname {L o g} _ {x _ {1}} (x) \| \right. \\ + \frac {d}{(1 - t) ^ {3}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \\ \left. \left(\| \nabla \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| \nabla^ {2} \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \|\right) \right]. \\ \end{array}
$$

Proof. We repeatedly use Lemma E.16 with $A(\cdot)$ chosen to be $\xi \mapsto (d\mathrm{Exp}_{x_1})_\xi$ , and the chain rule through $\operatorname{Log}_{x_1}$ .

We first estimate the gradient. From

$$
\log J _ {t} (x \mid x _ {1}) = - d \log (1 - t) + \log \det (d \mathrm {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \mathrm {L o g} _ {x _ {1}} (x)} - \log \det (d \mathrm {E x p} _ {x _ {1}}) _ {\mathrm {L o g} _ {x _ {1}} (x)},
$$

the constant $-d\log (1 - t)$ has zero $x$ -gradient, hence

$$
\operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) = \operatorname {g r a d} _ {x} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} - \operatorname {g r a d} _ {x} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)}.
$$

Consider the first term. Differentiating the map $x \mapsto \frac{1}{1 - t} \log_{x_1}(x)$ yields a factor $\frac{1}{1 - t} (d \log_{x_1})_x$ . Thus,

$$
\begin{array}{l} \left\| \operatorname {g r a d} _ {x} \log \det  \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| \\ \leq \frac {1}{1 - t} \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left\| \operatorname {g r a d} _ {\xi} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| \Bigg | _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)}. \\ \end{array}
$$

Now apply Lemma E.16 (specifically, the gradient bound in (33)) at $A(\xi) = (d\mathrm{Exp}_{x_1})_\xi$ to get

$$
\left\| \operatorname {g r a d} _ {\xi} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| \leq d \| (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} ^ {- 1} \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \|.
$$

Combining the above, we obtain

$$
\left\| \operatorname {g r a d} _ {x} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\|
$$

$$
\leq \frac {d}{1 - t} \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \|.
$$

The same argument (without the factor $\frac{1}{1 - t}$ ) yields

$$
\big \| \operatorname {g r a d} _ {x} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \big \| \leq d \big \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \big \| \big \| (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \big \| \big \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \big \|.
$$

Finally, apply the triangle inequality, we get

$$
\begin{array}{l} \| \operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) \| \leq d \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left(\frac {1}{1 - t} \| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right. \\ \left. + \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \right\| \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \right\|\right). \\ \end{array}
$$

Now we estimate the Hessian. Write $f(x) \coloneqq \log \det(d\mathrm{Exp}_{x_1})_{\frac{1}{1 - t}\mathrm{Log}_{x_1}(x)}$ . Taking second derivative (with product rule) we have

$$
\begin{array}{l} \| \nabla_ {x} ^ {2} f (x) \| _ {\mathrm {o p}} \leq \left\| \nabla_ {\xi} ^ {2} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| _ {\mathrm {o p}} \Bigg | _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \cdot \left\| \frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| ^ {2} \\ + \left\| \operatorname {g r a d} _ {\xi} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| \Bigg | _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \cdot \left\| \nabla \Big (\frac {1}{1 - t} (d \operatorname {L o g} _ {x _ {1}}) _ {x} \Big) \right\|. \\ \end{array}
$$

Thus we have (here $\nabla_{\xi}^{2}$ represent taking derivative w.r.t. $\xi$ )

$$
\begin{array}{l} \left\| \nabla_ {x} ^ {2} \log J _ {t} (x \mid x _ {1}) \right\| _ {\mathrm {o p}} \\ \leq \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| ^ {2} \left(\frac {1}{(1 - t) ^ {2}} \left\| \nabla_ {\xi} ^ {2} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| _ {\mathrm {o p}} \Bigg | _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} + \left\| \nabla_ {\xi} ^ {2} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| _ {\mathrm {o p}} \Bigg | _ {\xi = \operatorname {L o g} _ {x _ {1}} (x)}\right) \\ + \left\| \nabla (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\|\left( \right.\frac {1}{1 - t} \left\| \operatorname {g r a d} _ {\xi} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\|\left. \right| _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} + \left\| \operatorname {g r a d} _ {\xi} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| \Bigg | _ {\xi = \operatorname {L o g} _ {x _ {1}} (x)}\left. \right) \\ \leq d \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| ^ {2} \left[ \frac {1}{(1 - t) ^ {2}} \left(\left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t}} \operatorname {L o g} _ {x _ {1}} (x) \right\| ^ {2} \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t}} \operatorname {L o g} _ {x _ {1}} (x) \right\| ^ {2} \right. \right. \\ \left. + \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \right\| \left\| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\|\right) \\ + \left(\| (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \| ^ {2} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \| \| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right) \Biggr ] \\ + d \| \nabla (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left(\frac {1}{1 - t} \| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right. \\ \left. + \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \right\| \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \right\|\right), \\ \end{array}
$$

where in the first inequality we used triangle inequality, and in the second inequality we applied Lemma E.16.

For time derivative, since $x$ is fixed and only $\frac{1}{1 - t}$ depends on $t$ ,

$$
\partial_ {t} \log J _ {t} (x \mid x _ {1}) = \frac {d}{1 - t} + \partial_ {t} \Big (\log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \Big).
$$

By the chain rule,

$$
\partial_ {t} \Big (\log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \Big) = D \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \Big | _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \Big [ \partial_ {t} \Big (\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x) \Big) \Big ].
$$

But $\partial_t\bigl (\frac{1}{1 - t}\operatorname {Log}_{x_1}(x)\bigr) = \frac{1}{(1 - t)^2}\operatorname {Log}_{x_1}(x),$ hence

$$
\left| \partial_ {t} \Big (\log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \Big) \right| \leq \frac {1}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \left\| \operatorname {g r a d} _ {\xi} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| \Bigg | _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)}.
$$

Apply Lemma E.16 (gradient bound (33)) at $\xi = \frac{1}{1 - t}\operatorname{Log}_{x_1}(x)$ , we obtain

$$
| \partial_ {t} \log J _ {t} (x | x _ {1}) | \leq \frac {d}{1 - t} + \frac {d}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \|.
$$

For mixed derivative, recall

$$
\operatorname {g r a d} _ {x} \log J _ {t} (x \mid x _ {1}) = \operatorname {g r a d} _ {x} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} - \operatorname {g r a d} _ {x} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)}.
$$

Only the first term depends on $t$ . Differentiate the first term: there are two contributions, one from differentiating the prefactor $\frac{1}{1 - t}$ and one from differentiating $\operatorname{grad}_{\xi} \log \det(d \operatorname{Exp}_{x_1})_{\xi}$ at $\xi = \frac{1}{1 - t} \operatorname{Log}_{x_1}(x)$ . This yields

$$
\begin{array}{l} \| \partial_ {t} \operatorname {g r a d} _ {x} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \\ \leq \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left[ \frac {1}{(1 - t) ^ {2}} \left\| \operatorname {g r a d} _ {\xi} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| \right| _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \\ \left. + \frac {1}{1 - t} \left\| \partial_ {t} \left(\operatorname {g r a d} _ {\xi} \log \det  (d \operatorname {E x p} _ {x _ {1}}) _ {\xi}\right) \right\| \right| _ {\xi = \frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \biggr ]. \\ \end{array}
$$

Next, note that

$$
\partial_ {t} \left(\operatorname {g r a d} _ {\xi} \log \det  \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\xi}\right) = \nabla_ {\xi} ^ {2} \log \det  \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\xi} [ \partial_ {t} \xi ]
$$

with $\partial_t\xi = \frac{1}{(1 - t)^2}\operatorname {Log}_{x_1}(x)$ . Hence

$$
\left\| \partial_ {t} \Big (\operatorname {g r a d} _ {\xi} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \Big) \right\| \leq \frac {1}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \left\| \nabla_ {\xi} ^ {2} \log \det (d \operatorname {E x p} _ {x _ {1}}) _ {\xi} \right\| _ {\mathrm {o p}}.
$$

By Lemma E.16, we obtain

$$
\begin{array}{l} \left\| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} \left(x \mid x _ {1}\right) \right\| \\ \leq \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left[ \frac {1}{(1 - t) ^ {2}} d \| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \right. \\ \end{array}
$$

$$
\begin{array}{l} + \frac {1}{(1 - t) ^ {3}} \| \operatorname {L o g} _ {x _ {1}} (x) \| d \Big (\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t}} ^ {- 1} \operatorname {L o g} _ {x _ {1}} (x) \| ^ {2} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t}} \operatorname {L o g} _ {x _ {1}} (x) \| ^ {2} \\ \left. \left. + \left\| (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \right\| \left\| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\|\right) \right]. \\ \end{array}
$$

Finally, by Lezcano-Casado (2020, Theorem 3.12) with $r = \frac{\|\operatorname{Log}_{x_1}(x)\|}{1 - t}$ , and noting that on $\mathrm{SPD}(n)$ sectional curvature is upper bounded by zero, we have

$$
\left\| \left(d \operatorname {E x p} _ {x _ {1}}\right) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} ^ {- 1} \right\| \leq 1.
$$

Hence we get

$$
\| \operatorname {g r a d} _ {x} \log J _ {t} (x | x _ {1}) \| \leq d \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left(\frac {1}{1 - t} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| + \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right),
$$

$$
\begin{array}{l} \left\| \nabla_ {x} ^ {2} \log J _ {t} (x \mid x _ {1}) \right\| _ {\mathrm {o p}} \leq d \left\| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| ^ {2} \\ \left[ \frac {1}{(1 - t) ^ {2}} \Big (\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \right) \\ + \left(\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \|\right) \Bigg ] \\ + d \left\| \nabla (d \operatorname {L o g} _ {x _ {1}}) _ {x} \right\| \left(\frac {1}{1 - t} \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \right\| + \left\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\operatorname {L o g} _ {x _ {1}} (x)} \right\|\right), \\ \end{array}
$$

$$
| \partial_ {t} \log J _ {t} (x \mid x _ {1}) | \leq \frac {d}{1 - t} + \frac {d}{(1 - t) ^ {2}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \|,
$$

$$
\begin{array}{l} \| \partial_ {t} \operatorname {g r a d} _ {x} \log J _ {t} (x | x _ {1}) \| \leq \| (d \operatorname {L o g} _ {x _ {1}}) _ {x} \| \left[ \frac {d}{(1 - t) ^ {2}} \| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| \right. \\ + \frac {d}{(1 - t) ^ {3}} \| \operatorname {L o g} _ {x _ {1}} (x) \| \\ \left. \left(\| \nabla (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \| ^ {2} + \| \nabla^ {2} (d \operatorname {E x p} _ {x _ {1}}) _ {\frac {1}{1 - t} \operatorname {L o g} _ {x _ {1}} (x)} \|\right) \right], \\ \end{array}
$$

completing the proof.

# E.4 Bounding $\left\| \left(\nabla^{2}d\operatorname{Exp}_{p}\right)_{rv}\right\|_{\mathrm{op}}$

In this section, we bound the third derivative of Exp. We first recall some notation in Lezcano-Casado (2020), which allows us to write the third derivative as some ODE. Then we apply some comparison theorem to derive the upper bound. We remark that on a symmetric space, the (covariant) derivative of the curvature tensor is identically zero, see for example (Lee, 2018, Theorem 10.19). The techniques in this section works for non-symmetric spaces, but as we are working on $\mathrm{SPD}(n)$ , we assume $M$ is a symmetric space, which would simplify our computation.

Recall that $\nabla$ denotes the (Levi-Civita) connection on $TM$ over $M$ . Let $\nabla^{\mathrm{flat}}$ be the flat connection on the vector space $T_{p}M$ . Set $\mathrm{Exp}_{p}: U \subset T_{p}M \to M$ on a normal neighborhood of $p$ .

We first introduce pullback connection. Instead of differentiating along a vector field on $M$ , we can also differentiate along a vector field $X$ on $T_{p}M$ . Define the corresponding connection as

$$
\big (\nabla_ {X} ^ {\mathrm {p u l l b a c k}} Y \big) (u) = \nabla_ {(d \operatorname {E x p} _ {p}) _ {u} (X (u))} Y,
$$

In other words, given $u \in T_pM$ , and we have $q \coloneqq \mathrm{Exp}_p(u)$ . Then differentiate along $X$ in the tangent space via the pullback connection, evaluated at $u \in T_pM$ , is equivalent to differentiate along $d\mathrm{Exp}_p(X)$ (which can be viewed as a vector field on $M$ ) evaluated at $q$ .

Recall the pullback bundle $\mathrm{Exp}_p^* (TM)$ is a vector bundle over the base $T_{p}M$ . Concretely,

$$
\operatorname {E x p} _ {p} ^ {*} (T M) := \{(u, v): u \in T _ {p} M, v \in T M \mathrm {w i t h b a s e p o i n t} \operatorname {E x p} _ {p} (u) \}.
$$

For example, given an element of the tensor product space $(\alpha, (u, v)) \in T_p^* M \otimes \mathrm{Exp}_p^*(TM)$ , we have $(\alpha, (u, v))(w) = \alpha(w)v$ , where $\alpha \in T_p^* M$ is a covector, so that $\alpha(w) \in \mathbb{R}$ .

Let $\{e_i\}$ be an orthonormal basis for $T_{p}M$ , and $\{e^i\}$ be the corresponding basis in the cotangent space $T_{p}^{*}M$ . By definition,

$$
\big (\sum_ {i} e ^ {i} \otimes (u, (d \operatorname {E x p} _ {p}) _ {u} [ e _ {i} ]) \big) (w) := \sum_ {i} e ^ {i} (w) (d \operatorname {E x p} _ {p}) _ {u} [ e _ {i} ],
$$

and by linearity

$$
\sum_ {i} e ^ {i} (w) (d \operatorname {E x p} _ {p}) _ {u} [ e _ {i} ] = (d \operatorname {E x p} _ {p}) _ {u} [ \sum_ {i} e ^ {i} (w) e _ {i} ] = (d \operatorname {E x p} _ {p}) _ {u} (w).
$$

Thus we see that $d\operatorname{Exp}_p$ can be viewed as an element of the tensor product space:

$$
(d \operatorname {E x p} _ {p}) _ {u} \sum_ {i} e ^ {i} \otimes (u, (d \operatorname {E x p} _ {p}) _ {u} [ e _ {i} ]) \in T _ {p} ^ {*} M \otimes \operatorname {E x p} _ {p} ^ {*} (T M).
$$

We equip $T_{p}^{*}M$ with the connection induced by $\nabla^{\mathrm{flat}}$ and $\mathrm{Exp}_p^* (TM)$ with $\nabla^{\mathrm{pullback}}$ . These induce a connection on the tensor product bundle, denoted by $\nabla^{\mathrm{induced}}$ , characterized by the Leibniz rule. Now consider $\overline{W}_1, \overline{W}_2$ being vector fields in the tangent space $T_{p}M$ , and $d\mathrm{Exp}_p(\overline{W}_2)$ can be viewed as a section, i.e., $d\mathrm{Exp}_p(\overline{W}_2): u \mapsto (d\mathrm{Exp}_p)_u(\overline{W}_2(u))$ . We differentiate

$$
\begin{array}{l} \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} (d \operatorname {E x p} _ {p} (\overline {{W}} _ {2})) = \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} (\sum_ {i} e ^ {i} (\overline {{W _ {2}}}) (d \operatorname {E x p} _ {p}) [ e _ {i} ]) \\ = \sum_ {i} \overline {{W}} _ {1} e ^ {i} (\overline {{W _ {2}}}) (d \operatorname {E x p} _ {p}) [ e _ {i} ] + \sum_ {i} e ^ {i} (\overline {{W _ {2}}}) \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} (d \operatorname {E x p} _ {p}) [ e _ {i} ]. \\ \end{array}
$$

where we emphasize that $(d\mathrm{Exp}_p)[e_i]$ is a function of $u$ , similar as before: $(d\mathrm{Exp}_p)[e_i]:u\mapsto (d\mathrm{Exp}_p)_u[e_i]$ .

By linearity of $(d\mathrm{Exp}_p)$ , and definition of flat connection, we have

$$
\sum_ {i} \overline {{W}} _ {1} e ^ {i} (\overline {{W _ {2}}}) (d \mathrm {E x p} _ {p}) [ e _ {i} ] = (d \mathrm {E x p} _ {p}) [ \sum_ {i} \overline {{W}} _ {1} e ^ {i} (\overline {{W _ {2}}}) e _ {i} ] = (d \mathrm {E x p} _ {p}) [ \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {f l a t}} \overline {{W}} _ {2} ].
$$

On the other hand, since $e^i$ are constants, we know $\nabla_{\overline{W}_1}^{\mathrm{flat}}e^i = 0$ , so that

$$
e ^ {i} \otimes \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} (d \mathrm {E x p} _ {p}) [ e _ {i} ] = e ^ {i} \otimes \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} (d \mathrm {E x p} _ {p}) [ e _ {i} ] + \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {f l a t}} e ^ {i} \otimes (d \mathrm {E x p} _ {p}) [ e _ {i} ]
$$

$$
= \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {i n d u c e d}} (e ^ {i} \otimes (d \operatorname {E x p} _ {p}) [ e _ {i} ]),
$$

hence

$$
\begin{array}{l} \sum_ {i} e ^ {i} (\overline {{W}} _ {2}) \otimes \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} ((d \operatorname {E x p} _ {p}) [ e _ {i} ]) = \Big (\sum_ {i} e ^ {i} \otimes \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} ((d \operatorname {E x p} _ {p}) [ e _ {i} ]) \Big) (\overline {{W}} _ {2}) \\ = \Big (\sum_ {i} \nabla_ {\overline {{W}} _ {1}} ^ {\text {i n d u c e d}} \left(e ^ {i} \otimes \left(d \operatorname {E x p} _ {p}\right) [ e _ {i} ]\right)\left. \right) (\overline {{W}} _ {2}) = \sum_ {i} \Big (\nabla_ {\overline {{W}} _ {1}} ^ {\text {i n d u c e d}} \left(e ^ {i} \otimes \left(d \operatorname {E x p} _ {p}\right) [ e _ {i} ]\right)\Big) (\overline {{W}} _ {2}) \\ = (\nabla_ {\overline {{W}} _ {1}} ^ {\text {i n d u c e d}} (\sum_ {i} e ^ {i} \otimes (d \operatorname {E x p} _ {p}) [ e _ {i} ])) (\overline {{W}} _ {2}) = (\nabla_ {\overline {{W}} _ {1}} ^ {\text {i n d u c e d}} d \operatorname {E x p} _ {p}) (\overline {{W}} _ {2}). \\ \end{array}
$$

Substitute into the previous expression, we obtain

$$
\begin{array}{l} \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} (d \operatorname {E x p} _ {p} (\overline {{W}} _ {2})) \\ = \sum_ {i} \overline {{W}} _ {1} e ^ {i} (\overline {{W _ {2}}}) (d \operatorname {E x p} _ {p}) [ e _ {i} ] + \sum_ {i} e ^ {i} (\overline {{W _ {2}}}) \nabla_ {\overline {{W}} _ {1}} ^ {\mathrm {p u l l b a c k}} (d \operatorname {E x p} _ {p}) [ e _ {i} ] \\ = (d \operatorname {E x p} _ {p}) [ \nabla_ {\overline {{W}} _ {1}} ^ {\text {f l a t}} \overline {{W}} _ {2} ] + \nabla_ {\overline {{W}} _ {1}} ^ {\text {i n d u c e d}} (d \operatorname {E x p} _ {p}) (\overline {{W}} _ {2}) \\ \end{array}
$$

Thus, for vector fields $\overline{W}_1, \overline{W}_2$ on $U \subset T_pM$ we have

$$
\nabla_ {\overline {{W}} _ {1}} ^ {\text {p u l l b a c k}} \left(d \operatorname {E x p} _ {p} \left(\overline {{W}} _ {2}\right)\right) = \left(\nabla_ {\overline {{W}} _ {1}} ^ {\text {i n d u c e d}} d \operatorname {E x p} _ {p}\right) \left(\overline {{W}} _ {2}\right) + d \operatorname {E x p} _ {p} \left(\nabla_ {\overline {{W}} _ {1}} ^ {\text {f l a t}} \overline {{W}} _ {2}\right). \tag {27}
$$

Define $c(t, s_1, s_2, s_3) = \mathrm{Exp}_p(t(v + s_1w_1 + s_2w_2 + s_3w_3))$ , and $\gamma(t) = \mathrm{Exp}_p(tv)$ . We briefly recall what Lezcano-Casado (2020) did, to control the second derivative of Exp map. Define $J_1(t) = (d\mathrm{Exp}_p)_{tv}(tw_1)$ to be the Jacobi field along $\gamma$ with initial condition $w_1$ . We can define the extension of $J_1$ in the $w_2$ -direction by $\widetilde{J}_1(t,s) \coloneqq (d\mathrm{Exp}_p)_{t(v + sw_2)}(tw_1)$ , where note that $\widetilde{J}_1(t,0) = J_1(t)$ . For fixed $t$ , the tangent space vector field $u \mapsto tw_1$ is constant on $T_pM$ , hence

$$
\nabla_ {t w _ {2}} ^ {\text {f l a t}} \left(t w _ {1}\right) = 0. \tag {28}
$$

Applying (27) with $\overline{W}_1 \equiv tw_2$ and $\overline{W}_2 \equiv tw_1$ , and evaluated at $t(v + sw_2)$ , we have

$$
\left(\nabla_ {t w _ {2}} ^ {\mathrm {p u l l b a c k}} \widetilde {J} _ {1} (t, s)\right) (t (v + s w _ {2})) = \left(\nabla_ {t w _ {2}} ^ {\mathrm {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {t (v + s w _ {2})} (t w _ {1}) + (d \operatorname {E x p} _ {p}) _ {t (v + s w _ {2})} \big (\nabla_ {t w _ {2}} ^ {\mathrm {f l a t}} (t w _ {1}) \big).
$$

By (28) the last term vanishes. Using the fact $\left(\nabla_X^{\mathrm{pullback}}Y\right)(u) = \nabla_{(d\operatorname{Exp}_p)_u(X(u))}Y$ with $X = tw_2$ , $Y = \widetilde{J}_1$ , $u = tv$ , we have (restricted to $s = 0$ )

$$
\left(\nabla_ {t w _ {2}} ^ {\mathrm {p u l l b a c k}} \widetilde {J} _ {1}\right) (t v) = \nabla_ {(d \operatorname {E x p} _ {p}) _ {t v} (t w _ {2})} \widetilde {J} _ {1}.
$$

Together, with the previously defined notation $J_{2} = (d\mathrm{Exp}_{p})_{tv}(tw_{2})$ , we have

$$
\nabla_ {J _ {2}} J _ {1} = \nabla_ {J _ {2}} \widetilde {J} _ {1} \big | _ {s = 0} = \nabla_ {t w _ {2}} ^ {\mathrm {p u l b a c k}} \widetilde {J} _ {1} \big | _ {s = 0} = \left(\nabla^ {\mathrm {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {t v} (t w _ {1}, t w _ {2}).
$$

We therefore define the second-order variation field along $\gamma$ by

$$
K _ {1 2} (t) := \left(\nabla^ {\mathrm {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {t v} (t w _ {1}, t w _ {2}) = \nabla_ {J _ {2}} J _ {1}.
$$

Then (Lezcano-Casado, 2020, Proposition 4.1) shows that $K_{12}$ satisfies

$$
\ddot {K} _ {1 2} + R \left(K _ {1 2}, \dot {\gamma}\right) \dot {\gamma} + Y _ {1 2} = 0, \quad K _ {1 2} (0) = 0, \dot {K} _ {1 2} (0) = 0, \tag {29}
$$

with $Y_{12}$ given explicitly therein. Using the same technique, we can define

$$
K _ {1 3} (t) := \left(\nabla^ {\mathrm {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {t v} (t w _ {1}, t w _ {3}) = \nabla_ {J _ {3}} J _ {1}, K _ {2 3} (t) := \left(\nabla^ {\mathrm {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {t v} (t w _ {2}, t w _ {3}) = \nabla_ {J _ {3}} J _ {2},
$$

satisfying the corresponding ODE as (29).

Now we study the third derivative $L_{123} = \left((\nabla^{\mathrm{induced}})^2 d\mathrm{Exp}_p\right)(tw_1, tw_2, tw_3)$ . Define $J_i(t)$ to be the Jacobi field along $\gamma$ with initial condition $w_i$ for $i = 2, 3$ , in the same way as we did for $J_1$ . Extend $K_{12}(t) = \left(\nabla^{\mathrm{induced}}d\mathrm{Exp}_p\right)_{tv}(tw_1, tw_2) = \nabla_{J_2}J_1$ off $\gamma$ by

$$
\widetilde {K} _ {1 2} (t, s _ {3}) := \left(\nabla^ {\mathrm {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {t (v + s _ {3} w _ {3})} (t w _ {1}, t w _ {2}),
$$

so that $\widetilde{K}_{12}(t,0) = K_{12}(t)$ . We then define the third-order variation field along $\gamma$ by

$$
L _ {1 2 3} (t) := \nabla_ {J _ {3}} K _ {1 2} (t) := \left. \nabla_ {J _ {3}} \widetilde {K} _ {1 2} (t, s _ {3}) \right| _ {s _ {3} = 0}. \tag {30}
$$

Apply $\nabla_{\overline{W}_3}^{\mathrm{pullback}}$ to the first-order Leibniz rule (27). For vector fields $\overline{W}_1, \overline{W}_2, \overline{W}_3$ on $T_pM$ we obtain, at any $u \in T_pM$ ,

$$
\begin{array}{l} \left(\nabla_ {\overline {{W}} _ {3}} ^ {\text {p u l l b a c k}} \nabla_ {\overline {{W}} _ {1}} ^ {\text {p u l l b a c k}} (d \operatorname {E x p} _ {p} (\overline {{W}} _ {2}))\right) (u) = \left((\nabla_ {\overline {{W}} _ {3}} ^ {\text {i n d u c e d}} \nabla_ {\overline {{W}} _ {1}} ^ {\text {i n d u c e d}} d \operatorname {E x p} _ {p}) _ {u}\right) (\overline {{W}} _ {2} (u)) \\ + \left(\nabla_ {\overline {{W}} _ {1}} ^ {\text {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {u} \left((\nabla_ {\overline {{W}} _ {3}} ^ {\text {f l a t}} \overline {{W}} _ {2}) (u)\right) \\ + \left(\nabla_ {\overline {{W}} _ {3}} ^ {\text {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {u} \left(\left(\nabla_ {\overline {{W}} _ {1}} ^ {\text {f l a t}} \overline {{W}} _ {2}\right) (u)\right) \\ + \left(d \operatorname {E x p} _ {p}\right) _ {u} \left(\left(\nabla_ {\overline {{W}} _ {3}} ^ {\text {f l a t}} \nabla_ {\overline {{W}} _ {1}} ^ {\text {f l a t}} \overline {{W}} _ {2}\right) (u)\right). \tag {31} \\ \end{array}
$$

Now specialize (31) to the constant vector fields $\overline{W}_1 \equiv tw_2$ , $\overline{W}_2 \equiv tw_1$ , $\overline{W}_3 \equiv tw_3$ . Since $\nabla_{tw_i}^{\mathrm{flat}}(tw_j) = 0$ for all $i,j$ , the last three terms in (31) vanish. Evaluating at $u = tv$ yields

$$
L _ {1 2 3} (t) = \left(\nabla_ {t w _ {3}} ^ {\text {p u l l b a c k}} \widetilde {K} _ {1 2}\right) (t v) = \left(\left(\nabla_ {t w _ {3}} ^ {\text {i n d u c e d}} \nabla_ {t w _ {2}} ^ {\text {i n d u c e d}} d \operatorname {E x p} _ {p}\right) _ {t v}\right) (t w _ {1}),
$$

where note that $(d\operatorname{Exp}_p)_{tv}(tw_3) = J_3(t)$ .

By definition of the second covariant derivative tensor $(\nabla^{\mathrm{induced}})^2 d\mathrm{Exp}_p$ , this is precisely

$$
L _ {1 2 3} (t) = \left(\left(\nabla^ {\text {i n d u c e d}}\right) ^ {2} d \operatorname {E x p} _ {p}\right) _ {t v} \left(t w _ {1}, t w _ {2}, t w _ {3}\right). \tag {32}
$$

Throughout this section, we consider covariant derivative along $J_{i}$ , for example $\nabla_{J_3}J_2$ , as abbreviation of $\nabla_{J_3}\tilde{J}_2$ . Here, the $\tilde{\cdot}$ represent the corresponding extension along suitable direction, as constructed above.

Lemma E.9. For $L_{123}$ defined above, we have

$$
\ddot {L} _ {1 2 3} + R (L _ {1 2 3}, \dot {\gamma}) \dot {\gamma} + Y _ {1 2 3} = 0, \qquad L _ {1 2 3} (0) = 0, \dot {L} _ {1 2 3} (0) = 0.
$$

When $M$ is a symmetric space,

$$
\begin{array}{l} Y _ {1 2 3} = R (\dot {J} _ {3}, \dot {\gamma}) K _ {1 2} + 2 R (J _ {3}, \dot {\gamma}) \dot {K} _ {1 2} + R (K _ {1 2}, \dot {J} _ {3}) \dot {\gamma} + R (K _ {1 2}, \dot {\gamma}) \dot {J} _ {3} \\ + 2 R \left(\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}\right) \dot {J} _ {2} + 2 R \left(J _ {1}, \dot {J} _ {3}\right) \dot {J} _ {2} + 2 R \left(J _ {1}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {J} _ {2} \\ + 2 R \left(\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}\right) \dot {J} _ {1} + 2 R \left(J _ {2}, \dot {J} _ {3}\right) \dot {J} _ {1} + 2 R \left(J _ {2}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {J} _ {1}. \\ \end{array}
$$

Proof. Now recall the following ODE is staisified by $K$ (Lezcano-Casado, 2020, Proposition 4.1.).

$$
\ddot {K} _ {1 2} + R \left(K _ {1 2}, \dot {\gamma}\right) \dot {\gamma} + Y _ {1 2} = 0.
$$

By differentiating the ODE (note that the vector field to which we take covariant derivative, is viewed as the corresponding extension, i.e., $\tilde{K}_{12}$ for $K_{12}$ , grad $r$ for $\dot{\gamma}$ and $\nabla_{\mathrm{grad}~r}\nabla_{\mathrm{grad}~r}\tilde{K}_{12}$ for $\ddot{K}_{12}$ ), we obtain

$$
\nabla_ {J _ {3}} \ddot {K} _ {1 2} + \nabla_ {J _ {3}} R (K _ {1 2}, \dot {\gamma}) \dot {\gamma} + \nabla_ {J _ {3}} Y _ {1 2} = 0,
$$

We first compute $\nabla_{J_3}\ddot{K}_{12}$ . Recall $\dot{X} \coloneqq \nabla_{\dot{\gamma}}X$ and $\ddot{X} \coloneqq \nabla_{\dot{\gamma}}\nabla_{\dot{\gamma}}X$ . Let $L_{123} \coloneqq \nabla_{J_3}K_{12}$ . We compute $\nabla_{J_3}\ddot{K}_{12}$ step by step.

Recall by definition of curvature tensor

$$
\nabla_ {J _ {3}} \nabla_ {\dot {\gamma}} X = \nabla_ {\dot {\gamma}} \nabla_ {J _ {3}} X + \nabla_ {[ J _ {3}, \dot {\gamma} ]} X + R (J _ {3}, \dot {\gamma}) X,
$$

and the fact that $[J_3,\dot{\gamma} ] = 0$ (for the same reason as in Lezcano-Casado (2020, Proposition 4.1)), we have

$$
\begin{array}{l} \nabla_ {J _ {3}} \ddot {K} _ {1 2} = \nabla_ {J _ {3}} \nabla_ {\dot {\gamma}} \dot {K} _ {1 2} = \nabla_ {\dot {\gamma}} \nabla_ {J _ {3}} \dot {K} _ {1 2} + R (J _ {3}, \dot {\gamma}) \dot {K} _ {1 2} \\ = \nabla_ {\dot {\gamma}} \nabla_ {J _ {3}} \nabla_ {\dot {\gamma}} K _ {1 2} + R (J _ {3}, \dot {\gamma}) \dot {K} _ {1 2} \\ = \nabla_ {\dot {\gamma}} (\nabla_ {\dot {\gamma}} \nabla_ {J _ {3}} K _ {1 2} + R (J _ {3}, \dot {\gamma}) K _ {1 2}) + R (J _ {3}, \dot {\gamma}) \dot {K} _ {1 2} = \nabla_ {\dot {\gamma}} \nabla_ {\dot {\gamma}} L _ {1 2 3} + \nabla_ {\dot {\gamma}} (R (J _ {3}, \dot {\gamma}) K _ {1 2}) + R (J _ {3}, \dot {\gamma}) \dot {K} _ {1 2}. \\ \end{array}
$$

Notice that (by Leibniz rule)

$$
\begin{array}{l} \nabla_ {\dot {\gamma}} \left(R \left(J _ {3}, \dot {\gamma}\right) K _ {1 2}\right) = \left(\nabla_ {\dot {\gamma}} R\right) \left(J _ {3}, \dot {\gamma}\right) K _ {1 2} + R \left(\nabla_ {\dot {\gamma}} J _ {3}, \dot {\gamma}\right) K _ {1 2} + R \left(J _ {3}, \nabla_ {\dot {\gamma}} \dot {\gamma}\right) K _ {1 2} + R \left(J _ {3}, \dot {\gamma}\right) \nabla_ {\dot {\gamma}} K _ {1 2} \\ = (\nabla_ {\dot {\gamma}} R) \left(J _ {3}, \dot {\gamma}\right) K _ {1 2} + R \left(\dot {J} _ {3}, \dot {\gamma}\right) K _ {1 2} + R \left(J _ {3}, \dot {\gamma}\right) \dot {K} _ {1 2}. \\ \end{array}
$$

Hence we have

$$
\nabla_ {J _ {3}} \ddot {K} _ {1 2} = \dddot {L} _ {1 2 3} + (\nabla_ {\dot {\gamma}} R) (J _ {3}, \dot {\gamma}) K _ {1 2} + R (\dot {J} _ {3}, \dot {\gamma}) K _ {1 2} + 2 R (J _ {3}, \dot {\gamma}) \dot {K} _ {1 2}.
$$

Now we compute $\nabla_{J_3}\big(R(K_{12},\dot{\gamma})\dot{\gamma}\big)$ . Note that $\nabla_{J_3}\dot{\gamma} = \nabla_{\dot{\gamma}}J_3 = \dot{J}_3$ , by Leibniz rule,

$$
\begin{array}{l} \nabla_ {J _ {3}} \left(R (K _ {1 2}, \dot {\gamma}) \dot {\gamma}\right) = (\nabla_ {J _ {3}} R) (K _ {1 2}, \dot {\gamma}) \dot {\gamma} + R (\nabla_ {J _ {3}} K _ {1 2}, \dot {\gamma}) \dot {\gamma} + R (K _ {1 2}, \nabla_ {J _ {3}} \dot {\gamma}) \dot {\gamma} + R (K _ {1 2}, \dot {\gamma}) \nabla_ {J _ {3}} \dot {\gamma} \\ = (\nabla_ {J _ {3}} R) (K _ {1 2}, \dot {\gamma}) \dot {\gamma} + R (L _ {1 2 3}, \dot {\gamma}) \dot {\gamma} + R (K _ {1 2}, \dot {J} _ {3}) \dot {\gamma} + R (K _ {1 2}, \dot {\gamma}) \dot {J} _ {3}. \\ \end{array}
$$

Recall

$$
Y := 2 R (J _ {1}, \dot {\gamma}) \dot {J} _ {2} + 2 R (J _ {2}, \dot {\gamma}) \dot {J} _ {1} + (\nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) J _ {1} + (\nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {\gamma}.
$$

Also recall $[J_3,\dot{\gamma} ] = 0$ and $\nabla_{J_3}\dot{\gamma} = \nabla_{\dot{\gamma}}J_3 = \dot{J}_3$ . Then, by the Leibniz rule for tensor fields, we have

$$
\begin{array}{l} \nabla_ {J _ {3}} Y = 2 \nabla_ {J _ {3}} \left(R \left(J _ {1}, \dot {\gamma}\right) \dot {J} _ {2}\right) + 2 \nabla_ {J _ {3}} \left(R \left(J _ {2}, \dot {\gamma}\right) \dot {J} _ {1}\right) \\ + \nabla_ {J _ {3}} \Big ((\nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) J _ {1} \Big) + \nabla_ {J _ {3}} \Big ((\nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {\gamma} \Big), \\ \end{array}
$$

where each term expands as follows. For the first term,

$$
\begin{array}{l} \nabla_ {J _ {3}} \left(R (J _ {1}, \dot {\gamma}) \dot {J} _ {2}\right) = (\nabla_ {J _ {3}} R) (J _ {1}, \dot {\gamma}) \dot {J} _ {2} + R (\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}) \dot {J} _ {2} + R (J _ {1}, \nabla_ {J _ {3}} \dot {\gamma}) \dot {J} _ {2} + R (J _ {1}, \dot {\gamma}) \nabla_ {J _ {3}} \dot {J} _ {2} \\ = (\nabla_ {J _ {3}} R) (J _ {1}, \dot {\gamma}) \dot {J} _ {2} + R (\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}) \dot {J} _ {2} + R (J _ {1}, \dot {J} _ {3}) \dot {J} _ {2} + R (J _ {1}, \dot {\gamma}) \nabla_ {J _ {3}} \dot {J} _ {2}. \\ \end{array}
$$

For the second term,

$$
\begin{array}{l} \nabla_ {J _ {3}} \big (R (J _ {2}, \dot {\gamma}) \dot {J} _ {1} \big) = (\nabla_ {J _ {3}} R) (J _ {2}, \dot {\gamma}) \dot {J} _ {1} + R (\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}) \dot {J} _ {1} + R (J _ {2}, \nabla_ {J _ {3}} \dot {\gamma}) \dot {J} _ {1} + R (J _ {2}, \dot {\gamma}) \nabla_ {J _ {3}} \dot {J} _ {1} \\ = (\nabla_ {J _ {3}} R) (J _ {2}, \dot {\gamma}) \dot {J} _ {1} + R (\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}) \dot {J} _ {1} + R (J _ {2}, \dot {J} _ {3}) \dot {J} _ {1} + R (J _ {2}, \dot {\gamma}) \nabla_ {J _ {3}} \dot {J} _ {1}. \\ \end{array}
$$

For the third term,

$$
\begin{array}{l} \nabla_ {J _ {3}} \Bigl ((\nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) J _ {1} \Bigr) = (\nabla_ {J _ {3}} \nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) J _ {1} + (\nabla_ {\dot {\gamma}} R) (\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}) J _ {1} \\ + (\nabla_ {\dot {\gamma}} R) \left(J _ {2}, \nabla_ {J _ {3}} \dot {\gamma}\right) J _ {1} + (\nabla_ {\dot {\gamma}} R) \left(J _ {2}, \dot {\gamma}\right) \nabla_ {J _ {3}} J _ {1} \\ = (\nabla_ {J _ {3}} \nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) J _ {1} + (\nabla_ {\dot {\gamma}} R) (\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}) J _ {1} \\ + (\nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {J} _ {3}) J _ {1} + (\nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) \nabla_ {J _ {3}} J _ {1}. \\ \end{array}
$$

For the last term,

$$
\begin{array}{l} \nabla_ {J _ {3}} \Big ((\nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {\gamma} \Big) = (\nabla_ {J _ {3}} \nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {\gamma} + (\nabla_ {J _ {2}} R) (\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}) \dot {\gamma} \\ + \left(\nabla_ {J _ {2}} R\right) \left(J _ {1}, \nabla_ {J _ {3}} \dot {\gamma}\right) \dot {\gamma} + \left(\nabla_ {J _ {2}} R\right) \left(J _ {1}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {\gamma} \\ = (\nabla_ {J _ {3}} \nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {\gamma} + (\nabla_ {J _ {2}} R) (\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}) \dot {\gamma} \\ + (\nabla_ {J _ {2}} R) (J _ {1}, \dot {J} _ {3}) \dot {\gamma} + (\nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {J} _ {3}. \\ \end{array}
$$

Plug in the expressions, we have

$$
\ddot {L} _ {1 2 3} + R \left(L _ {1 2 3}, \dot {\gamma}\right) \dot {\gamma} + Y _ {1 2 3} = 0,
$$

where

$$
\begin{array}{l} Y _ {1 2 3} = (\nabla_ {\dot {\gamma}} R) (J _ {3}, \dot {\gamma}) K _ {1 2} + (\nabla_ {J _ {3}} R) (K _ {1 2}, \dot {\gamma}) \dot {\gamma} + R (\dot {J} _ {3}, \dot {\gamma}) K _ {1 2} + 2 R (J _ {3}, \dot {\gamma}) \dot {K} _ {1 2} \\ + R \left(K _ {1 2}, \dot {J} _ {3}\right) \dot {\gamma} + R \left(K _ {1 2}, \dot {\gamma}\right) \dot {J} _ {3} \\ + 2 \left(\nabla_ {J _ {3}} R\right) \left(J _ {1}, \dot {\gamma}\right) \dot {J} _ {2} + 2 R \left(\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}\right) \dot {J} _ {2} + 2 R \left(J _ {1}, \dot {J} _ {3}\right) \dot {J} _ {2} + 2 R \left(J _ {1}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {J} _ {2} \\ + 2 \left(\nabla_ {J _ {3}} R\right) \left(J _ {2}, \dot {\gamma}\right) \dot {J} _ {1} + 2 R \left(\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}\right) \dot {J} _ {1} + 2 R \left(J _ {2}, \dot {J} _ {3}\right) \dot {J} _ {1} + 2 R \left(J _ {2}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {J} _ {1} \\ + (\nabla_ {J _ {3}} \nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) J _ {1} + (\nabla_ {\dot {\gamma}} R) (\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}) J _ {1} + (\nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {J} _ {3}) J _ {1} + (\nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) \nabla_ {J _ {3}} J _ {1} \\ + (\nabla_ {J _ {3}} \nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {\gamma} + (\nabla_ {J _ {2}} R) (\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}) \dot {\gamma} + (\nabla_ {J _ {2}} R) (J _ {1}, \dot {J} _ {3}) \dot {\gamma} + (\nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {J} _ {3}. \\ \end{array}
$$

On a symmetric space,

$$
\begin{array}{l} Y _ {1 2 3} = R \left(\dot {J} _ {3}, \dot {\gamma}\right) K _ {1 2} + 2 R \left(J _ {3}, \dot {\gamma}\right) \dot {K} _ {1 2} + R \left(K _ {1 2}, \dot {J} _ {3}\right) \dot {\gamma} + R \left(K _ {1 2}, \dot {\gamma}\right) \dot {J} _ {3} \\ + 2 R \left(\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}\right) \dot {J} _ {2} + 2 R \left(J _ {1}, \dot {J} _ {3}\right) \dot {J} _ {2} + 2 R \left(J _ {1}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {J} _ {2} \\ + 2 R \left(\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}\right) \dot {J} _ {1} + 2 R \left(J _ {2}, \dot {J} _ {3}\right) \dot {J} _ {1} + 2 R \left(J _ {2}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {J} _ {1}. \\ \end{array}
$$

![](images/d541b914375bb76e9096872cf189b9fc70a0506b3828faf585feeb71a70eef28.jpg)

Now we can apply comparison theory (Lezcano-Casado, 2020, Proposition 4.9) to control $\| L\|$ .

Lemma E.10. Let $(M,g)$ be a Riemannian symmetric space, i.e. $\nabla R\equiv 0$ . Fix a unit-speed geodesic $\gamma :[0,r]\to M$ with $\| \dot{\gamma}\| \equiv 1$ . Under Assumption 1, we have

$$
\| L (t) \| \leq \frac {7 L _ {R} ^ {2}}{3} s _ {K _ {\min}} (s) ^ {5} + 1 6 L _ {R} ^ {3} t ^ {2} s _ {K _ {\min}} (t) ^ {5} + 2 0 L _ {R} ^ {2} t s _ {K _ {\min}} (t) ^ {4}.
$$

Consequently,

$$
\begin{array}{l} \left\| \left(\left(\nabla\right) ^ {2} d \operatorname {E x p} _ {p}\right) _ {r v} \right\| _ {\mathrm {o p}} = \sup  _ {\left\| w _ {1} \right\|, \left\| w _ {2} \right\|, \left\| w _ {3} \right\| \leq 1} \left\| \left(\left(\nabla^ {\text {i n d u c e d}}\right) ^ {2} d \operatorname {E x p} _ {p}\right) _ {r v} \left(w _ {1}, w _ {2}, w _ {3}\right) \right\| \\ = \sup_{\| w_{1}\| ,\| w_{2}\| ,\| w_{3}\| \leq 1}\frac{1}{r^{3}}\| L_{123}(r)\| \leq \frac{7L_{R}^{2}}{3r^{3}} s_{K_{\min}}(r)^{5} + 16L_{R}^{3}\frac{1}{r} s_{K_{\min}}(r)^{5} + 20L_{R}^{2}\frac{1}{r^{2}} s_{K_{\min}}(r)^{4}. \\ \end{array}
$$

Proof. Recall

$$
\begin{array}{l} Y _ {1 2 3} = R \left(\dot {J} _ {3}, \dot {\gamma}\right) K _ {1 2} + 2 R \left(J _ {3}, \dot {\gamma}\right) \dot {K} _ {1 2} + R \left(K _ {1 2}, \dot {J} _ {3}\right) \dot {\gamma} + R \left(K _ {1 2}, \dot {\gamma}\right) \dot {J} _ {3} \\ + 2 R \left(\nabla_ {J _ {3}} J _ {1}, \dot {\gamma}\right) \dot {J} _ {2} + 2 R \left(J _ {1}, \dot {J} _ {3}\right) \dot {J} _ {2} + 2 R \left(J _ {1}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {J} _ {2} \\ + 2 R \left(\nabla_ {J _ {3}} J _ {2}, \dot {\gamma}\right) \dot {J} _ {1} + 2 R \left(J _ {2}, \dot {J} _ {3}\right) \dot {J} _ {1} + 2 R \left(J _ {2}, \dot {\gamma}\right) \nabla_ {J _ {3}} \dot {J} _ {1}. \\ \end{array}
$$

By definition of $K_{13}, K_{23}$ , we have $\nabla_{J_3} J_1 = K_{13}$ and $\nabla_{J_3} J_2 = K_{23}$ . Next we express $\nabla_{J_3} \dot{J}_i$ in terms of $\dot{K}_{i3}$ and curvature. By definition of $R$ and $[J_3, \dot{\gamma}] = 0$ ,

$$
\begin{array}{l} \nabla_ {J _ {3}} \dot {J} _ {i} = \nabla_ {J _ {3}} \nabla_ {\dot {\gamma}} J _ {i} = \nabla_ {\dot {\gamma}} \nabla_ {J _ {3}} J _ {i} + R (J _ {3}, \dot {\gamma}) J _ {i} \\ = \dot {K} _ {i 3} + R \left(J _ {3}, \dot {\gamma}\right) J _ {i}. \\ \end{array}
$$

Therefore

$$
2 R (J _ {1}, \dot {\gamma}) \nabla_ {J _ {3}} \dot {J} _ {2} = 2 R (J _ {1}, \dot {\gamma}) \dot {K} _ {2 3} + 2 R (J _ {1}, \dot {\gamma}) \big (R (J _ {3}, \dot {\gamma}) J _ {2} \big),
$$

$$
2 R (J _ {2}, \dot {\gamma}) \nabla_ {J _ {3}} \dot {J} _ {1} = 2 R (J _ {2}, \dot {\gamma}) \dot {K} _ {1 3} + 2 R (J _ {2}, \dot {\gamma}) \big (R (J _ {3}, \dot {\gamma}) J _ {1} \big).
$$

Substituting these and using $R(x,y)z \leq L_R\| x\| \| y\| \| z\|$ , we have

$$
\begin{array}{l} \| Y _ {1 2 3} \| \leq 3 L _ {R} \| K _ {1 2} \| \| \dot {J} _ {3} \| + 2 L _ {R} \| J _ {3} \| \| \dot {K} _ {1 2} \| + 2 L _ {R} \| K _ {1 3} \| \| \dot {J} _ {2} \| + 2 L _ {R} \| K _ {2 3} \| \| \dot {J} _ {1} \| \\ + 2 L _ {R} \| J _ {1} \| \| \dot {K} _ {2 3} \| + 2 L _ {R} \| J _ {2} \| \| \dot {K} _ {1 3} \| + 2 L _ {R} \| J _ {1} \| \| \dot {J} _ {2} \| \| \dot {J} _ {3} \| + 2 L _ {R} \| J _ {2} \| \| \dot {J} _ {1} \| \| \dot {J} _ {3} \| \\ + 4 L _ {R} ^ {2} \| J _ {1} \| \| J _ {2} \| \| J _ {3} \| \\ \leq 7 L _ {R} \| K \| \| \dot {J} \| + 6 L _ {R} \| J \| \| \dot {K} \| + 4 L _ {R} \| J \| \| \dot {J} \| ^ {2} + 4 L _ {R} ^ {2} \| J \| ^ {3}. \\ \end{array}
$$

Using Lemma E.11, (Lezcano-Casado, 2020, Theorem 3.12, Theorem 4.11) we have

$$
\| K (t) \| \leq \frac {1 6}{3} s _ {K _ {\min }} (t / 2) ^ {2} L _ {R} s _ {K _ {\min }} (t),
$$

$$
\| \dot {K} (t) \| \leq L _ {R} ^ {2} \frac {1 6}{3} t s _ {K _ {\min }} (t) ^ {3} + 2 L _ {R} s _ {K _ {\min }} (t) ^ {2},
$$

$$
\| J (t) \| \leq s _ {K _ {\min }} (t),
$$

$$
\| \tilde {J} (t) \| \leq s _ {K _ {\min }} ^ {\prime} (t),
$$

hence we can bound

$$
\begin{array}{l} \| Y _ {1 2 3} \| \leq 7 L _ {R} \frac {1 6}{3} s _ {K _ {\min }} (t / 2) ^ {2} L _ {R} s _ {K _ {\min }} (t) s _ {K _ {\min }} ^ {\prime} (t) + 6 L _ {R} s _ {K _ {\min }} (t) \left(L _ {R} ^ {2} \frac {1 6}{3} t s _ {K _ {\min }} (t) ^ {3} + 2 L _ {R} s _ {K _ {\min }} (t) ^ {2}\right) \\ + 4 L _ {R} s _ {K _ {\min}} (t) \left(s _ {K _ {\min}} ^ {\prime} (t)\right) ^ {2} + 4 L _ {R} ^ {2} \left(s _ {K _ {\min}} (t)\right) ^ {3} \\ \leq \frac {1 1 2 L _ {R} ^ {2}}{3} s _ {K _ {\min }} (t / 2) ^ {2} s _ {K _ {\min }} (t) s _ {K _ {\min }} ^ {\prime} (t) + 3 2 L _ {R} ^ {3} t s _ {K _ {\min }} (t) ^ {4} + 2 0 L _ {R} ^ {2} s _ {K _ {\min }} (t) ^ {3} \\ \leq \frac {2 8 L _ {R} ^ {2}}{3} s _ {K _ {\min}} (t) ^ {3} s _ {K _ {\min}} ^ {\prime} (t) + 3 2 L _ {R} ^ {3} t s _ {K _ {\min}} (t) ^ {4} + 2 0 L _ {R} ^ {2} s _ {K _ {\min}} (t) ^ {3}. \\ \end{array}
$$

We apply (Lezcano-Casado, 2020, Proposition 4.9). Consider ODE

$$
\rho^ {\prime \prime} (t) + K _ {\mathrm {m i n}} \rho (t) = \eta (t).
$$

Define $y(t) = s_{K_{\min}}(t)$ . Note that $y$ solves $y''(t) + K_{\min}y(t) = 0$ . Then the function $\rho(t) = \int_0^t y(t - s)\eta(s)ds$ satisfies $\rho''(t) + K_{\min}\rho(t) = \eta(t)$ . We apply this to each part of the bound on $Y_{123}$ :

$$
\begin{array}{l} \int_ {0} ^ {t} s _ {K _ {\min}} (t - s) \frac {2 8 L _ {R} ^ {2}}{3} s _ {K _ {\min}} (s) ^ {3} s _ {K _ {\min}} ^ {\prime} (s) d s \leq \frac {7 L _ {R} ^ {2}}{3} s _ {K _ {\min}} (t) \int_ {0} ^ {t} 4 s _ {K _ {\min}} (s) ^ {3} s _ {K _ {\min}} ^ {\prime} (s) d s = \frac {7 L _ {R} ^ {2}}{3} s _ {K _ {\min}} (s) ^ {5}, \\ \int_ {0} ^ {t} s _ {K _ {\min}} (t - s) 3 2 L _ {R} ^ {3} s _ {K _ {\min}} (s) ^ {4} s d s \leq 3 2 L _ {R} ^ {3} s _ {K _ {\min}} (t) \int_ {0} ^ {t} s _ {K _ {\min}} (s) ^ {4} s d s \\ \leq 3 2 L _ {R} ^ {3} s _ {K _ {\mathrm {m i n}}} (t) ^ {5} \int_ {0} ^ {t} s d s = 1 6 L _ {R} ^ {3} t ^ {2} s _ {K _ {\mathrm {m i n}}} (t) ^ {5}, \\ \int_ {0} ^ {t} s _ {K _ {\mathrm {m i n}}} (t - s) 2 0 L _ {R} ^ {2} s _ {K _ {\mathrm {m i n}}} (s) ^ {3} d s \leq 2 0 L _ {R} ^ {2} t s _ {K _ {\mathrm {m i n}}} (t) ^ {4}. \\ \end{array}
$$

Hence we can use the following $\tilde{\rho}$ as upper bound for $\rho$ :

$$
\rho (t) \leq \tilde {\rho} (t) := \frac {7 L _ {R} ^ {2}}{3} s _ {K _ {\min}} (s) ^ {5} + 1 6 L _ {R} ^ {3} t ^ {2} s _ {K _ {\min}} (t) ^ {5} + 2 0 L _ {R} ^ {2} t s _ {K _ {\min}} (t) ^ {4}.
$$

In other words,

$$
\| L (t) \| \leq \frac {7 L _ {R} ^ {2}}{3} s _ {K _ {\min}} (s) ^ {5} + 1 6 L _ {R} ^ {3} t ^ {2} s _ {K _ {\min}} (t) ^ {5} + 2 0 L _ {R} ^ {2} t s _ {K _ {\min}} (t) ^ {4}.
$$

Lemma E.11. When $M$ is a symmetric space, we have

$$
\| \dot {K} (t) \| \leq L _ {R} ^ {2} \frac {1 6}{3} t s _ {K _ {\min }} (t) ^ {3} + 2 L _ {R} s _ {K _ {\min }} (t) ^ {2}.
$$

Proof.

Since $K$ solves $\ddot{K} + R(K, \dot{\gamma})\dot{\gamma} + Y = 0$ , we have

$$
\ddot {K} = - R (K, \dot {\gamma}) \dot {\gamma} - Y.
$$

Integrate over $[0,t]$ , we obtain

$$
\dot {K} (t) - \dot {K} (0) = \int_ {0} ^ {t} \ddot {K} (s) d s = \int_ {0} ^ {t} - R (K, \dot {\gamma}) \dot {\gamma} (s) - Y (s) d s.
$$

Using $\| \dot{\gamma} \| = 1$ and $\dot{K}(0) = 0$ , we obtain

$$
\| \dot {K} (t) \| = \| \int_ {0} ^ {t} \ddot {K} (s) d s \| \leq \int_ {0} ^ {t} \| R (K, \dot {\gamma}) \dot {\gamma} (s) \| + \| Y (s) \| d s \leq \int_ {0} ^ {t} L _ {R} \| K (s) \| + \| Y (s) \| d s.
$$

It suffices to obtain bound for $\| Y\|$ and $\| K\|$ . Recall

$$
Y := 2 R (J _ {1}, \dot {\gamma}) \dot {J} _ {2} + 2 R (J _ {2}, \dot {\gamma}) \dot {J} _ {1} + (\nabla_ {\dot {\gamma}} R) (J _ {2}, \dot {\gamma}) J _ {1} + (\nabla_ {J _ {2}} R) (J _ {1}, \dot {\gamma}) \dot {\gamma},
$$

and that for a symmetric space, we have Recall

$$
Y = 2 R (J _ {1}, \dot {\gamma}) \dot {J} _ {2} + 2 R (J _ {2}, \dot {\gamma}) \dot {J} _ {1}.
$$

Hence

$$
\| Y (s) \| \leq 2 L _ {R} (\| J _ {1} \| \| \dot {J} _ {2} \| + \| \dot {J} _ {1} \| \| J _ {2} \|) \leq 4 L _ {R} s _ {K _ {\min}} ^ {\prime} (s) s _ {K _ {\min}} (s) = 2 L _ {R} s _ {K _ {\min}} (2 s),
$$

where by Lezcano-Casado (2020, Theorem 3.12) we have for unit tangent vector $v$ ,

$$
\| d (\mathrm {E x p} _ {p}) _ {r v} (r w) \| \leq \max  \{1, \frac {s _ {K _ {\min}} (r)}{r} \} r \| w \|,
$$

so that $\| J(s)\| \leq s_{K_{\min}}(s)$ . Also, Lezcano-Casado (2020, Theorem 3.11) gives

$$
\| \operatorname {H e s s} r \| \leq \frac {s _ {K _ {\operatorname* {m i n}}} ^ {\prime} (r)}{s _ {K _ {\operatorname* {m i n}}} (r)},
$$

so that $\| \dot{J} (s)\| \leq \| J\| \| \mathrm{Hess}r\| \leq \frac{s_{K_{\min}}'(s)}{s_{K_{\min}}(s)} s_{K_{\min}}(s)\leq s_{K_{\min}}'(s).$

Furthermore, Lezcano-Casado (2020, Theorem 4.11) implies (with $w$ replaced by $r w$ )

$$
K (s) \leq \frac {1 6}{3} s _ {K _ {\min}} (s / 2) ^ {2} L _ {R} s _ {K _ {\min}} (s).
$$

Hence, we have

$$
\| \dot {K} (t) \| \leq \int_ {0} ^ {t} L _ {R} \left(\frac {1 6}{3} s _ {K _ {\min }} (s / 2) ^ {2} L _ {R} s _ {K _ {\min }} (s)\right) + 2 \left(L _ {R} s _ {K _ {\min }} (2 s)\right) d s.
$$

Note that in our case, $s_{K_{\min}}(t) = \frac{\sinh(\sqrt{|K_{\min}|}t)}{\sqrt{|K_{\min}|}}$ , so we have $s_{K_{\min}}(s / 2) \leq s_{K_{\min}}(s)$ .

For the first term, we have

$$
\begin{array}{l} \int_ {0} ^ {t} L _ {R} \left(\frac {1 6}{3} s _ {K _ {\mathrm {m i n}}} (s / 2) ^ {2} L _ {R} s _ {K _ {\mathrm {m i n}}} (s)\right) d s \leq L _ {R} ^ {2} \frac {1 6}{3} \int_ {0} ^ {t} s _ {K _ {\mathrm {m i n}}} (s) ^ {3} d s \leq L _ {R} ^ {2} \frac {1 6}{3} \int_ {0} ^ {t} s _ {K _ {\mathrm {m i n}}} (t) ^ {3} d s \\ = L _ {R} ^ {2} \frac {1 6}{3} t s _ {K _ {\mathrm {m i n}}} (t) ^ {3}. \\ \end{array}
$$

For the second term,

$$
\int_ {0} ^ {t} 2 (L _ {R} s _ {K _ {\mathrm {m i n}}} (2 s)) d s \leq 2 L _ {R} s _ {K _ {\mathrm {m i n}}} (t) ^ {2}.
$$

Put together, we obtain

$$
\| \dot {K} (t) \| \leq L _ {R} ^ {2} \frac {1 6}{3} t s _ {K _ {\min }} (t) ^ {3} + 2 L _ {R} s _ {K _ {\min }} (t) ^ {2}.
$$

# E.5 Bounds involving Riemannian Log

Here, we obtain bounds on $\| (d\operatorname{Log}_x)_y\|$ , $\| (\nabla (d\operatorname{Log}_x))_y\|$ , $\| \nabla_x\operatorname{Log}_x(y)\|_{\mathrm{op}}$ , $\| \nabla_x\operatorname{Log}_x(y)\|_{\mathrm{op}}^2$ , $|\operatorname{div}_x\operatorname{Log}_x(y)|$ and $|\operatorname{div}_x\operatorname{Log}_x(y)|^2$ . We also obtain a bound $\| \operatorname{grad}\operatorname{div}_x\operatorname{Log}_x(y)\|$ when the manifold is SPD $(n)$ . In this section, for different differential operators $d$ and $\nabla$ , note that $\nabla \operatorname{Log}_x(x_1)$ is covariant derivative (viewing $\operatorname{Log}_x(x_1)$ as a vector field, with $x_1$ being fixed. On the other hand, $d\operatorname{Log}_{x_1}$ is considering fixed base point.

Before presenting our results, we also recall some facts. Let $M$ be a Hadamard manifold of dimension $d$ . Fix $x \in M$ and let $y \in M$ , $y \neq x$ . Then:

(i) $\| \operatorname{Log}_x(y)\| = d(x,y)$ .   
(ii) $\operatorname{grad}_x\left(\frac{1}{2} d(x,y)^2\right) = -\operatorname{Log}_x(y)$ .   
(iii) $\operatorname{div}_x\operatorname{Log}_x(y) = -\Delta_x\left(\frac{1}{2} d(x,y)^2\right)$ .

Lemma E.12 (Bounds for $d\operatorname{Log}_x$ and $\nabla(d\operatorname{Log}_x)$ ). Let $M$ be a Hadamard manifold of dimension $d$ . Fix $x \in M$ . Then, we have

$$
\begin{array}{l} \left\| \left(d \operatorname {L o g} _ {x}\right) _ {y} \right\| \leq 1, \\ \left\| \left(\nabla (d \operatorname {L o g} _ {x})\right) _ {y} \right\| \leq \left\| \left(\nabla (d \operatorname {E x p} _ {x})\right) _ {\operatorname {L o g} _ {x} (y)} \right\|. \\ \end{array}
$$

Proof. On a Hadamard manifold, $\mathrm{Exp}_x: T_xM \to M$ is a global diffeomorphism, hence $\mathrm{Log}_x = \mathrm{Exp}_x^{-1}$ is smooth on $M$ . Let $u = \mathrm{Log}_x(y)$ . Then $\mathrm{Exp}_x(u) = y$ and the inverse function theorem gives

$$
(d \operatorname {L o g} _ {x}) _ {y} = \left((d \operatorname {E x p} _ {x}) _ {u}\right) ^ {- 1} = \left((d \operatorname {E x p} _ {x}) _ {\operatorname {L o g} _ {x} (y)}\right) ^ {- 1}.
$$

Take norm on both sides and recall $\left\| \left((d\mathrm{Exp}_x)_{\mathrm{Log}_x(y)}\right)^{-1}\right\| \leq 1$ , we get the first bound.

Now we differentiate the identity

$$
\left(d \operatorname {E x p} _ {x}\right) _ {\operatorname {L o g} _ {x} (\cdot)} \circ \left(d \operatorname {L o g} _ {x}\right). = I d _ {T. M}
$$

covariantly at $y$ in the direction $w_{1}\in T_{y}M$ , and then apply the resulting operator to $w_{2}\in T_{y}M$ . Using Leibniz rule and that $\nabla (Id) = 0$ , we get

$$
\left(\nabla (d \operatorname {E x p} _ {x})\right) _ {\operatorname {L o g} _ {x} (y)} \Big [ (d \operatorname {L o g} _ {x}) _ {y} w _ {1}, (d \operatorname {L o g} _ {x}) _ {y} w _ {2} \Big ] + (d \operatorname {E x p} _ {x}) _ {\operatorname {L o g} _ {x} (y)} \Big (\left(\nabla (d \operatorname {L o g} _ {x})\right) _ {y} [ w _ {1}, w _ {2} ] \Big) = 0.
$$

Re-arrange the terms, we get

$$
\begin{array}{l} \left(\nabla (d \operatorname {L o g} _ {x})\right) _ {y} [ w _ {1}, w _ {2} ] \\ = - \left((d \operatorname {E x p} _ {x}) _ {\operatorname {L o g} _ {x} (y)}\right) ^ {- 1} \Big (\left(\nabla (d \operatorname {E x p} _ {x})\right) _ {\operatorname {L o g} _ {x} (y)} \Big [ \left((d \operatorname {E x p} _ {x}) _ {\operatorname {L o g} _ {x} (y)}\right) ^ {- 1} w _ {1}, \left((d \operatorname {E x p} _ {x}) _ {\operatorname {L o g} _ {x} (y)}\right) ^ {- 1} w _ {2} \Big ] \Big). \\ \end{array}
$$

Take norms, and recalling that $\| \bigl ((d\mathrm{Exp}_x)_{\mathrm{Log}_x(y)}\bigr)^{-1}\| \leq 1$ , we obtain

$$
\left\| \left(\nabla (d \operatorname {L o g} _ {x})\right) _ {y} \right\| \leq \left\| \left(\nabla (d \operatorname {E x p} _ {x})\right) _ {\operatorname {L o g} _ {x} (y)} \right\|.
$$

□

Lemma E.13 (Bounds for $\| \nabla_x\mathrm{Log}_x(y)\|$ ). Let $M$ be a Hadamard manifold of dimension $d$ with sectional curvature bounded below by $K_{\min}\leq 0$ . Fix $x\in M$ and $y\in M$ , $y\neq x$ . Then

$$
\| \nabla_ {x} \operatorname {L o g} _ {x} (y) \| _ {\mathrm {o p}} \leq 1 + d (x, y) \frac {s _ {K _ {\min}} ^ {\prime} (d (x , y))}{s _ {K _ {\min}} (d (x , y))},
$$

$$
\left\| \nabla_ {x} \operatorname {L o g} _ {x} (y) \right\| _ {\mathrm {o p}} ^ {2} \leq 2 + 2 d (x, y) ^ {2} \left(\frac {s _ {K _ {\min}} ^ {\prime} (d (x , y))}{s _ {K _ {\min}} (d (x , y))}\right) ^ {2}.
$$

Proof. Let $r(\cdot) \coloneqq d(\cdot, y)$ , so $r(x) = d(x, y)$ . Since $r \operatorname{grad}_x r = -\operatorname{Log}_x(y)$ (since $\operatorname{grad}_x \left( \frac{1}{2} r^2 \right) = r \operatorname{grad}_x r$ ), we have

$$
\operatorname {L o g} _ {x} (y) = - r (x) \operatorname {g r a d} _ {x} r (x).
$$

Differentiate covariantly in $x$ , we obtain

$$
\nabla_ {x} \operatorname {L o g} _ {x} (y) = - \nabla_ {x} \big (r (x) \operatorname {g r a d} _ {x} r (x) \big) = - \big (\nabla_ {x} r (x) \big) \otimes \operatorname {g r a d} _ {x} r (x) - r (x) \nabla_ {x} \operatorname {g r a d} _ {x} r (x).
$$

Taking operator norms and using $\| \operatorname{grad}_x r(x) \| = 1$ gives

$$
\| \nabla_ {x} \operatorname {L o g} _ {x} (y) \| _ {\mathrm {o p}} \leq \| \operatorname {g r a d} _ {x} r (x) \| ^ {2} + r (x) \| \nabla \operatorname {g r a d} _ {x} r (x) \| _ {\mathrm {o p}} = 1 + d (x, y) \| \nabla \operatorname {g r a d} _ {x} r (x) \| _ {\mathrm {o p}}.
$$

By Hessian comparison under $\operatorname{Sec} \geq K_{\min}$ , we have

$$
\| \nabla \operatorname {g r a d} _ {x} r (x) \| _ {\mathrm {o p}} \leq \frac {s _ {K _ {\min }} ^ {\prime} (d (x , y))}{s _ {K _ {\min }} (d (x , y))}.
$$

Combining the above estimates yields the first inequality. The squared bound follows from $(a + b)^2 \leq 2a^2 + 2b^2$ with $a = 1$ and $b = d(x, y) \frac{s_{K_{\min}}'(d(x, y))}{s_{K_{\min}}(d(x, y))}$ .

Lemma E.14 (Bounds for $\mathrm{div}_x\mathrm{Log}_x(y)$ and $|\mathrm{div}_x\mathrm{Log}_x(y)|^2$ ). Let $M$ be a Hadamard manifold of dimension $d$ with sectional curvature bounded below by $K_{\min} \leq 0$ . Fix $x \in M$ and $y \in M$ , $y \neq x$ . Then

$$
\left| \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (y) \right| \leq 1 + (d - 1) d (x, y) \frac {s _ {K _ {\min}} ^ {\prime} (d (x , y))}{s _ {K _ {\min}} (d (x , y))},
$$

$$
| \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (y) | ^ {2} \leq 2 + 2 (d - 1) ^ {2} d (x, y) ^ {2} \Big (\frac {s _ {K _ {\operatorname* {m i n}}} ^ {\prime} (d (x , y))}{s _ {K _ {\operatorname* {m i n}}} (d (x , y))} \Big) ^ {2}.
$$

Proof. Let $r(\cdot) \coloneqq d(\cdot, y)$ . Then we have $\operatorname{div}_x \operatorname{Log}_x(y) = -\Delta_x \left( \frac{1}{2} r(x)^2 \right)$ . Using the product rule for Laplacian, we have $\Delta \left( \frac{1}{2} r^2 \right) = \langle \operatorname{grad} r, \operatorname{grad} r \rangle + r\Delta r = 1 + r\Delta r$ . For the upper bound, Laplacian comparison theorem under Sec $\geq K_{\min}$ gives

$$
\Delta r \leq (d - 1) \frac {s _ {K _ {\operatorname* {m i n}}} ^ {\prime} (d (x , y))}{s _ {K _ {\operatorname* {m i n}}} (d (x , y))}.
$$

Substitute into $|\operatorname{div}_x \operatorname{Log}_x(y)| = \Delta_x\left(\frac{1}{2} r^2\right)$ we obtain

$$
| \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (y) | \leq 1 + (d - 1) d (x, y) \frac {s _ {K _ {\min}} ^ {\prime} (d (x , y))}{s _ {K _ {\min}} (d (x , y))}.
$$

Finally, using $(a + b)^2 \leq 2a^2 + 2b^2$ with $a = 1$ and $b = (d - 1)d(x,y)\frac{s_{K_{\min}}'(d(x,y))}{s_{K_{\min}}(d(x,y))}$ gives the desired results.

Moreover, on $\operatorname{SPD}(n)$ , we have the following results.

Lemma E.15 (grad div Log bound on $\operatorname{SPD}(n)$ ). Let $\operatorname{SPD}(n)$ be the manifold of real symmetric positive-definite matrices endowed with the affine-invariant Riemannian metric

$$
\langle U, V \rangle_ {P} := \operatorname {T r} \left(P ^ {- 1} U P ^ {- 1} V\right), \qquad U, V \in T _ {P} \operatorname {S P D} (n) = \operatorname {S y m} (n).
$$

Fix $y\in \mathrm{SPD}(n)$ and define

$$
r (x) := d (x, y), \qquad f (x) := d (x, y) ^ {2} = r (x) ^ {2}, \qquad d := \dim (\operatorname {S P D} (n)) = \frac {n (n + 1)}{2}.
$$

Then we have

$$
\left\| \operatorname {g r a d} \operatorname {d i v} \operatorname {L o g} \right\| \leq \frac {\sqrt {2} d}{2} \left(2 \left(1 + r \frac {s _ {K _ {\operatorname* {m i n}}} ^ {\prime} (r)}{s _ {K _ {\operatorname* {m i n}}} (r)}\right)\right) ^ {\frac {3}{2}}.
$$

Proof. We first show that $\mathrm{SPD}(n)$ is a totally geodesic submanifold of $PD(n,\mathbb{C})$ under the affine-invariant metric. Let $\mathrm{PD}(n,\mathbb{C})$ denote the manifold of complex Hermitian positive-definite matrices endowed with the same affine-invariant metric $\langle U,V\rangle_P = \operatorname {Tr}(P^{-1}UP^{-1}V)$ . Define a smooth isometry by

$$
\sigma : \mathrm {P D} (n, \mathbb {C}) \rightarrow \mathrm {P D} (n, \mathbb {C}), \quad \sigma (P) := \overline {{P}}.
$$

Notice that $\sigma$ is an isometry because for any $P\in \mathrm{PD}(n,\mathbb{C})$ and $U,V\in \mathrm{Herm}(n)$

$$
\langle d \sigma_ {P} [ U ], d \sigma_ {P} [ V ] \rangle_ {\sigma (P)} = \mathrm {T r} \left(\overline {{P}} ^ {- 1} \overline {{U}} \overline {{P}} ^ {- 1} \overline {{V}}\right) = \overline {{\mathrm {T r} \left(P ^ {- 1} U P ^ {- 1} V\right)}} = \mathrm {T r} \left(P ^ {- 1} U P ^ {- 1} V\right) = \langle U, V \rangle_ {P},
$$

where we used that $\operatorname{Tr}(P^{-1}UP^{-1}V) \in \mathbb{R}$ for Hermitian $P, U, V$ . Thus we see that the fixed-point set of $\sigma$ is exactly $\operatorname{SPD}(n)$ . According to Kobayashi (1972, Theorem 5.1) we have that the fixed-point set of an isometry is a (embedded) totally geodesic submanifold. Hence $\operatorname{SPD}(n)$ is totally geodesic in $\operatorname{PD}(n, \mathbb{C})$ .

Let $F(P) \coloneqq d_{\mathrm{PD}(n,\mathbb{C})}(P,y)^2$ be the squared distance to $y \in \mathrm{SPD}(n) \subset PD(n,\mathbb{C})$ , considered as a function on $PD(n,\mathbb{C})$ . By Hirai et al. (2023, Theorem 1.4), $F$ is 2-self-concordant on $\mathrm{PD}(n,\mathbb{C})$ : we have that for all $P \in \mathrm{PD}(n,\mathbb{C})$ and $u,v,w \in T_P \mathrm{PD}(n,\mathbb{C})$ ,

$$
| (\nabla^ {3} F) _ {P} (u, v, w) | \leq \sqrt {2} \sqrt {(\nabla^ {2} F) _ {P} (u , u)} \sqrt {(\nabla^ {2} F) _ {P} (v , v)} \sqrt {(\nabla^ {2} F) _ {P} (w , w)}.
$$

Now restrict $F$ to the totally geodesic submanifold $\operatorname{SPD}(n)$ . By definition, for a totally geodesic submanifold, the second fundamental form vanishes, and Gauss formula (Lee, 2018, Theorem 8.2) implies that the connection $\nabla$ on $\operatorname{SPD}(n)$ is induced by that of $\operatorname{PD}(n,\mathbb{C})$ . Moreover, the geodesic distance function on $\operatorname{SPD}(n)$ is induced by that on $\operatorname{PD}(n,\mathbb{C})$ , so we know self-concordance of distance squared also holds on $\operatorname{SPD}(n)$ .

Now we make use of the self-concordance property to bound $\| \operatorname{grad} \operatorname{div} \operatorname{Log} \|$ . Let $f(x) = d_{\mathrm{SPD}}(x, y)^2$ and note that on the Hadamard manifold $\mathrm{SPD}(n)$ ,

$$
\| \operatorname {g r a d} _ {x} \operatorname {d i v} _ {x} \operatorname {L o g} _ {x} (y) \| = \frac {1}{2} \| \operatorname {g r a d} _ {x} \Delta_ {x} f (x) \|.
$$

Let $\{e_i\}_{i=1}^d$ be an orthonormal basis of $T_x \mathrm{SPD}(n)$ . Such an orthonormal basis can be extended to a neighborhood of $x$ , and we obtain an orthonormal frame: $\nabla e_i|_x = 0, \forall i$ (Lee, 2018, Exercise 5-21). Thus we can differentiate $\Delta f$ as follows. For any unit $w \in T_x \mathrm{SPD}(n)$

$$
\langle \mathrm {g r a d} \Delta f, w \rangle = \sum_ {i = 1} ^ {d} (\nabla^ {3} f) (w, e _ {i}, e _ {i}) + 2 \nabla^ {2} f (\nabla_ {w} e _ {i}, e _ {i}) = \sum_ {i = 1} ^ {d} (\nabla^ {3} f) (w, e _ {i}, e _ {i}).
$$

By self-concordance, we have $|(\nabla^3 f)(w, e_i, e_i)| \leq \sqrt{2} \sqrt{(\nabla^2 f)(w, w)} (\nabla^2 f)(e_i, e_i)$ . Therefore

$$
\| \operatorname {g r a d} \operatorname {d i v} \operatorname {L o g} \| \leq \frac {\sqrt {2} d}{2} \sqrt {\| \nabla^ {2} f \| _ {\mathrm {o p}} ^ {3}}.
$$

Writing $f = r^2$ , we have

$$
\nabla^ {2} f = 2 d r \otimes d r + 2 r \nabla^ {2} r, \qquad \Delta f = 2 + 2 r \Delta r,
$$

using $\| \operatorname{grad} r \| = 1$ . Under $\operatorname{Sec} \geq K_{\min}$ , Hessian comparison gives $\| \nabla^2 r \|_{\mathrm{op}} \leq \frac{s_{K_{\min}}'(r)}{s_{K_{\min}}(r)}$ , hence

$$
\| \nabla^ {2} f \| _ {\mathrm {o p}} \leq 2 + 2 r \| \nabla^ {2} r \| _ {\mathrm {o p}} \leq 2 \Big (1 + r \frac {s _ {K _ {\mathrm {m i n}}} ^ {\prime} (r)}{s _ {K _ {\mathrm {m i n}}} (r)} \Big).
$$

Substituting this in the previous estimate yields

$$
\| \operatorname {g r a d} \operatorname {d i v} \operatorname {L o g} \| \leq \frac {\sqrt {2} d}{2} \left(2 \Big (1 + r \frac {s _ {K _ {\operatorname* {m i n}}} ^ {\prime} (r)}{s _ {K _ {\operatorname* {m i n}}} (r)} \Big)\right) ^ {1. 5}.
$$

![](images/d9ede5e58d80d454339fd86ebab37375dd161eade055114e8dc59d0a27a646a5.jpg)

# E.6 Auxiliary results

Given a matrix $A(x)$ , the directional derivative in $v$ can be computed through

$$
D \log \det  (A (x)) [ v ] = \operatorname {t r} \left(A ^ {- 1} D A (x) [ v ]\right).
$$

Hence

$$
\| \nabla \log \det (A(x)) \| _ {\mathrm {o p}} = \sup  _ {\| v \| = 1} | \operatorname {t r} \left(A ^ {- 1} D A (x) [ v ]\right) | \leq d \| A ^ {- 1} \| \times \| D A (x) \| _ {\mathrm {o p}}.
$$

Furthermore, using the product rule, and noting that $DA^{-1}(x) = -A^{-1}(x)DA(x)A^{-1}(x)$ , we obtain

$$
\begin{array}{l} D ^ {2} \log \det  (A (x)) [ v, v ] \\ = \operatorname {t r} \left(D A ^ {- 1} (x) [ v ] D A (x) [ v ]\right) + \operatorname {t r} \left(A ^ {- 1} (x) D ^ {2} A (x) [ v, v ]\right) \\ = - \operatorname {t r} (A ^ {- 1} (x) D A (x) [ v ] A ^ {- 1} (x) D A (x) [ v ]) + \operatorname {t r} (A ^ {- 1} (x) D ^ {2} A (x) [ v, v ]). \\ \end{array}
$$

Hence, we have

$$
\| \nabla^ {2} \log \det (A (x)) \| _ {o p} \leq d \| A ^ {- 1} (x) \| ^ {2} \times \| \nabla A (x) \| ^ {2} + d \| A ^ {- 1} (x) \| \times \| \nabla^ {2} A (x) \|.
$$

This is summarized as the following result, and is used in Lemma E.8.

Lemma E.16 (Derivatives of log det). Let $A(x)$ be a smooth family of invertible linear maps on a $d$ -dimensional inner product space. Then for any unit vector $v$ ,

$$
D \log \det  (A (x)) [ v ] = \operatorname {t r} \left(A (x) ^ {- 1} D A (x) [ v ]\right).
$$

Consequently,

$$
\left\| \nabla \log \det  (A (x)) \right\| = \sup  _ {\| v \| = 1} \left| \operatorname {t r} \left(A (x) ^ {- 1} D A (x) [ v ]\right) \right| \leq d \| A (x) ^ {- 1} \| \| \nabla A (x) \|, \tag {33}
$$

$$
\left\| \nabla^ {2} \log \det  (A (x)) \right\| _ {\mathrm {o p}} \leq d \| A (x) ^ {- 1} \| ^ {2} \| \nabla A (x) \| ^ {2} + d \| A (x) ^ {- 1} \| \| \nabla^ {2} A (x) \|. \tag {34}
$$