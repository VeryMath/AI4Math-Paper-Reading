# Mirror Flow Matching with Heavy-Tailed Priors for Generative Modeling on Convex Domains

Yunrui Guan<sup>1</sup>, Krishnakumar Balasubramanian<sup>2</sup>, and Shiqian Ma<sup>1</sup>

<sup>1</sup>Department of Computational Applied Mathematics and Operations Research, Rice University.

$^{2}$ Department of Statistics, University of California, Davis.

$^{1}\{\mathrm{yg83, sqma}\}$ @rice.edu

2{kbala} @ucdavis.edu

# Abstract

We study generative modeling on convex domains using flow matching and mirror maps, and identify two fundamental challenges. First, standard log-barrier mirror maps induce heavy-tailed dual distributions, leading to ill-posed dynamics. Second, coupling with Gaussian priors performs poorly when matching heavy-tailed targets. To address these issues, we propose Mirror Flow Matching based on a regularized mirror map that controls dual tail behavior and guarantees finite moments, together with coupling to a Student- $t$ prior that aligns with heavy-tailed targets and stabilizes training. We provide theoretical guarantees, including spatial Lipschitzness and temporal regularity of the velocity field, Wasserstein convergence rates for flow matching with Student- $t$ priors and primal-space guarantees for constrained generation, under $\varepsilon$ -accurate learned velocity fields. Empirically, our method outperforms baselines in synthetic convex-domain simulations and achieves competitive sample quality on real-world constrained generative tasks.

# 1 Introduction

Flow matching (Lipman et al., 2023; Liu et al., 2023c; Albergo et al., 2023; Albergo and Vanden-Eijnden, 2023; Tong et al., 2024; Chen and Lipman, 2024) has emerged as a powerful framework for generative modeling, unifying score-based diffusion and optimal transport approaches under a single perspective. The central idea in flow matching is to construct a continuous-time deterministic flow that transports a simple prior distribution (e.g., Gaussian) to a complex target distribution, by learning its velocity field. Formally, given random variables $X_0 \sim \pi_0$ and $X_1 \sim \pi_1$ , both supported on $\mathbb{R}^d$ , we seek a time-dependent vector field $v: \mathbb{R}^d \times [0,1] \to \mathbb{R}^d$ such that the solution of the ODE $dX_t = v(X_t, t) dt$ , with $X_0 \sim \pi_0$ , satisfies $X_1 \sim \pi_1$ . A simple construction is based on straight-line interpolation $X_t = (1 - t)X_0 + tX_1$ , which yields the conditional velocity field $v^*(x,t) = \mathbb{E}[X_1 - X_0 \mid X_t = x]$ . This vector field $v^*$ minimizes the regression loss $\min_v \mathbb{E}[|v(X_t,t) - \frac{d}{dt} X_t|^2]$ , making it the optimal velocity field for the interpolation path. Since computing $v^*$ exactly is intractable, modern flow-matching methods approximate $v$ with a neural network and simulate the ODE numerically. This pathwise formulation leads to scalable training objectives, principled continuous-time generative processes, and improved sample quality.

Constrained Flow Matching. In many applications, the target is supported on constrained domains like polytope, simplex, or positive semidefinite matrices, rather than the full Euclidean space. Examples include molecular generation, where atoms and bonds must satisfy physical stability constraints (Fishman et al., 2023b), preference alignment (Kim et al., 2024), policy optimization and physical constraints for

robotics (Zhang et al., 2025; Utkarsh et al., 2025) and watermarked content generation (Liu et al., 2023a). Standard flow-based methods fail in this setting: projecting unconstrained samples back onto the domain distorts the distribution. Several strategies address this challenge including reflection-based methods (Lou and Ermon, 2023; Fishman et al., 2023a; Xie et al., 2024; Christopher et al., 2024) that keep trajectories inside the domain using boundary normals; mirror-map diffusion models (Liu et al., 2023a; Feng et al., 2025) that transform constrained problems into unconstrained ones using mirror-maps; gauge-map approaches (Li et al., 2025) that enforce feasibility via reflections; and distance-penalty methods (Huan et al., 2025; Khalafi et al., 2024) that penalize distance to the constraint set, at notable computational cost. Despite this progress, no framework yet ensures constraint satisfaction while providing convergence rates for flow matching.

In this work, we focus on the development of mirror flow matching, where the velocity field is adapted to the geometry of the constraint set. Formally, let $\mathcal{K} = \{\phi_i(x) < 0, \phi : \mathbb{R}^d \to \mathbb{R}, i = 1, \dots, m\}$ , where $\phi_i$ are smooth convex functions, be a closed convex set, and suppose the target distribution $\pi_1$ is supported on $\mathcal{K}$ . Our approach is based on constructing a mirror map $\nabla \Psi : \mathcal{K} \to \mathbb{R}^d$ , where $\Psi : \mathcal{K} \to \mathbb{R}$ is a strictly convex, differentiable potential. The mirror map transports points from the constrained primal space $\mathcal{K}$ to an unconstrained dual space. In this dual space, one can perform standard (unconstrained) flow matching, i.e., define $Z_t = \nabla \Psi(X_t)$ , and evolve it via $dZ_t = v^D(Z_t, t) dt$ with $Z_0 = \nabla \Psi(X_0)$ , where $v^D$ is a velocity field learned by minimizing the unconstrained flow matching objective. The primal trajectory is then recovered by mapping back using the inverse mirror map $X_t = (\nabla \Psi)^{-1}(Z_t)$ . This mirror-descent-based formulation ensures that the entire trajectory $\{X_t\}_{t \in [0,1]}$ remains in $\mathcal{K}$ while leveraging the flexibility of unconstrained flow matching in the dual space. Thus, mirror flow matching combines geometry-aware sampling with scalable learning, broadening the applicability of flow models to structured domains that naturally arise in the aforementioned application areas.

# 1.1 Challenges and Solutions

Methodological Challenges. Extending flow matching to constrained domains via mirror maps introduces key challenges. First, the transformed target distribution in the dual space may have heavy tails, causing standard mirror maps (e.g., log-barrier) to violate moment conditions required for well-posed flow ODEs (Figure 1, red dots). We address this with a regularized mirror map that controls heavy tails and ensures finite $p$ -th moments for all $p \geq 1$ (Figure 1, blue dots), stabilizing training. Second, Gaussian priors often mismatch the heavy-tailed dual distributions; we instead adopt a Student- $t$ prior, improving alignment, sample quality, and stability. Together, these modifications overcome limitations of standard log-barrier and Gaussian priors, yielding high-fidelity constrained generative modeling. A visual illustration is provided in Appendix Section A.

Theoretical Challenges. In addition to the methodological issues above, theoretical analysis of mirror flow matching poses challenges. Rigorous error bounds for the sampling stage require the velocity field $v(x,t)$ to be Lipschitz in $x$ (Benton et al., 2024; Bansal et al., 2024; Zhou and Liu, 2025; Gao et al., 2024), while ODE discretization error further requires Lipschitz continuity in both $x$ and $t$ (Bansal et al., 2024; Zhou and Liu, 2025). However, the dual velocity field $v^{D}(z,t)$ is generally not Lipschitz over $t \in [0,1]$ . Partial progress includes spatial Lipschitzness on $t \in [0,T] \subsetneq [0,1]$ under bounded $\pi_1$ (Benton et al., 2024; Zhou and Liu, 2025) or Gaussian-like $\pi_1$ (Gao et al., 2024). In general, unbounded $\pi_1$ can induce polynomial growth in $\| \nabla_x v(x,t) \|$ as $\| x \|$ grows and singularities near $t = 1$ , motivating early stopping. Recent work (Cordero-Encinar et al., 2025) leverages Log-Sobolev inequalities to establish spatial Lipschitzness, though $t$ -Lipschitzness is not addressed. We overcome this challenge by using t-distribution as priors. While such priors have been explored empirically (for example, (Pandey et al., 2025, Appendix B)), our motivation comes from addressing the above theoretical challenge.

Contributions. In this work, we introduce flow matching with a Student- $t$ prior (see Section 3) and provide new theoretical guarantees establishing both spatial Lipschitzness and temporal regularity (see

Proposition 6). This result enables us to obtain explicit error bounds under substantially more general target distributions (see Theorem 7) in the dual Euclidean space under the assumption that the learned velocity fields approximates the true dynamics up to $\varepsilon$ -accuracy. Finally in Theorem 9 we further prove primal-space guarantees for constrained dynamics.

# 2 Ingredients for Designing Mirror Flow Matching

# 2.1 Ingredient 1: The Mirror map

Before introducing our proposed mirror map, we first explain why the classical log-barrier is not suitable in our setting. The main issue arises from our first identified challenge: ensuring the existence of moments. As the following general result shows, if the log-barrier transformation induces heavy tails, then even low-order moments (e.g., the second moment) may fail to exist.

Lemma 1. Let $Y$ be a random variable in $\mathbb{R}^d$ with law $P$ . Then, (i) if $P(\|Y\| \geq R) \geq C / R^p$ for some constant $C > 0$ , then $\mathbb{E}[\|Y\|^p]$ does not exist, and (ii) if $P(\|Y\| \geq R) \leq C / R^\beta$ with $\beta > p$ , then $\mathbb{E}[\|Y\|^p]$ is finite.

In addition to controlling tails, we would also like the geometry induced by the mirror map to have a desirable metric property: the metric in the dual space should be stronger than that in the primal space. Formally, we require

$$
\| x - y \| \leq L _ {\Psi} \| \nabla \Psi (x) - \nabla \Psi (y) \|, \quad \forall x, y \in \mathcal {K}, \tag {2.1}
$$

for some constant $L_{\Psi} > 0$ . To see why this is important, we first recall some definitions of $p$ -Wasserstein distance in primal space and dual space. Let $\nu, \mu$ be two probability measures on $\mathcal{K}$ . Then we have:

$$
W _ {p} (\nu , \mu) ^ {p} = \inf  _ {\gamma \in \Gamma (\nu , \mu)} \mathbb {E} _ {\gamma} [ \| x - y \| ^ {p} ],
$$

$$
W _ {p, \Psi} (\nu , \mu) ^ {p} = \inf _ {\gamma \in \Gamma (\nu , \mu)} \mathbb {E} _ {\gamma} [ \| \nabla \Psi (x) - \nabla \Psi (y) \| ^ {p} ],
$$

where $\gamma \in \Gamma(\nu, \mu)$ means $\gamma$ is a coupling of $\nu, \mu$ . The first one is just the Wasserstein distance for $\mathcal{K}$ under Euclidean distance, and the second one is actually the Wasserstein distance in the dual space. To see this, let $\nu', \mu'$ denote the distribution of $\nu, \mu$ in dual space, i.e., $\nu' = (\nabla \Psi)_{\#} \nu$ and $\mu' = (\nabla \Psi)_{\#} \mu$ . Then we have $W_{2,\Psi}(\mu, \nu) = W_2(\mu', \nu')$ . We remark that $W_{2,\Psi}$ was used to analyze the convergence of mirror Langevin algorithm (e.g., see Li et al. (2022)).

In general, an upper bound for $W_{2,\Psi}(\nu, \mu)$ doesn't directly imply an error bound for $W_{2}(\nu, \mu)$ in the primal space. But under inequality (2.1), Wasserstein distances in the primal space can be controlled by those in the dual space:

![](images/011b3700e788e298b9f723f17d83b6d4b605fd2e249bad4778a68973ef66aadb.jpg)  
Figure 1: Dual space distribution comparison between the log barrier and our mirror map $(\kappa = 0.5)$ . The primal distribution is a truncated Gaussian mixture within a polytope (see Appendix A). The log barrier yields a heavy-tailed distribution, while our mirror map produces a much lighter tail.

$$
W _ {2} (\nu , \mu) ^ {2} = \inf _ {\gamma \in \Gamma (\nu , \mu)} \mathbb {E} _ {\gamma} [ \| x - y \| ^ {2} ] \leq \inf _ {\gamma \in \Gamma (\nu , \mu)} \mathbb {E} _ {\gamma} [ L _ {\Psi} ^ {2} \| \nabla \Psi (x) - \nabla \Psi (y) \| ^ {2} ] = L _ {\Psi} ^ {2} W _ {2, \Psi} (\nu , \mu) ^ {2}.
$$

Inequality (2.1) is equivalent to $\nabla \Psi^{*}$ being $L_{\Psi}$ -Lipschitz. Since $\nabla^2\Psi$ and $\nabla^2\Psi^*$ are inverses of each other, this condition is in turn equivalent to $\Psi$ being strongly convex. However, classical mirror maps are generally

only strictly convex, not strongly convex. As a result, $L_{\Psi}$ can be arbitrarily large in certain domains; for instance, even for simple 2D polytopes with three facets ( $d = 2, m = 3$ ), the constant $L_{\Psi}$ may blow up (see Example 10 in the Appendix).

These observations suggest that we need to design a new mirror map that balances tail behavior and convexity. In particular, the desired mirror map should satisfy the following goals:

1. Transform the constrained distribution into an unconstrained distribution on $\mathbb{R}^d$ .   
2. Ensure that key moments (e.g., the second moment) of the transformed distribution exist.   
3. Be strongly convex, so that convergence guarantees in the dual Euclidean metric can be transferred to guarantees in the primal Euclidean metric.

Motivated by the mirror-map framework of Vural et al. (2022), we propose in Proposition 2 a modified log-barrier that achieves these properties.

Proposition 2. Let $\mathcal{K} = \{\phi_i(x) < 0, \forall i \in [m]\}$ , where $\phi_i$ are smooth convex functions with bounded gradient. Let $\Psi(x) = -\frac{1}{1-\kappa} \sum_{i=1}^{m} (-\phi_i(x))^{1-\kappa} + \frac{1}{2} \|x\|^2$ . Then we have $W_2(\nu, \mu) \leq W_{2,\Psi}(\nu, \mu)$ . Denote $\mathcal{K}_{\delta} = \{x \in \mathcal{K}: -\phi_i(x) \geq \delta\}$ . Let $X$ be a random variable on $\mathcal{K}$ whose law is denoted as $P$ . Assume there exists positive constants $C_{\mathcal{K}}, \beta, \delta_0$ s.t. for all $0 < \delta < \delta_0$ it holds that $P(\mathcal{K} \backslash \mathcal{K}_{\delta}) \leq C_{\mathcal{K}} \delta^{\beta}$ . Then there exists some constant $C$ s.t. in the dual space $\mathbb{R}^d$ , for all $R \geq C' / \delta_0^\kappa$ (here $C'$ is some constant that depends on $\mathcal{K}$ , $P(\| \nabla \Psi(X) \| \geq R) \leq C / R^{\beta/\kappa}$ ). By choosing $\kappa < \beta/p$ , we can guarantee $\mathbb{E}[\| \nabla \Psi(X) \|^p]$ exists.

Specific examples (including $L_{2}$ ball and polytopes) are discussed in Appendix Section B. We verify that the boundary-measure condition $P(\mathcal{K} \setminus \mathcal{K}_{\delta}) \leq C_{\mathcal{K}} \delta^{\beta}$ is natural in typical cases.

Example 3 (Uniform distribution on the cube). Let $\mathcal{K} = [-1,1]^d$ and let $P$ be the uniform distribution on $\mathcal{K}$ . Define the $\delta$ -interior as $\mathcal{K}_{\delta} = \{x \in \mathcal{K} : d(x, \partial \mathcal{K}) \geq \delta\}$ . Then the boundary layer has probability mass $P(\mathcal{K} \setminus \mathcal{K}_{\delta}) = \frac{2^d - (2 - 2\delta)^d}{2^d} = 1 - (1 - \delta)^d$ . Using the first-order expansion $(1 - \delta)^d \approx 1 - d\delta$ , we obtain $P(\mathcal{K} \setminus \mathcal{K}_{\delta}) \approx d\delta$ . Hence the condition $P(\mathcal{K} \setminus \mathcal{K}_{\delta}) \leq C_{\mathcal{K}}\delta^{\beta}$ holds with $\beta = 1$ and $C_{\mathcal{K}} = d$ . This shows the assumption is mild and satisfied by standard convex bodies such as the cube under uniform measure.

# 2.2 Ingredient 2: The Prior Distribution

For flow matching, let the target distribution be denoted by $X_{1} \sim \pi_{1}$ with density $p$ , and let the initial distribution (prior) be $X_{0} \sim \pi_{0}$ . The evolution between $\pi_{0}$ and $\pi_{1}$ is described by a time-dependent vector field, where $v(x,t)$ denotes the true vector field. Considering straight-line interpolation, by definition, the velocity field at a point $(x,t)$ is the conditional expectation of the instantaneous displacement along this interpolation: $v(x,t) = \mathbb{E}[X_1 - X_0 \mid X_t = x]$ . To make this expression explicit (Karras et al., 2022; Wan et al., 2025), note that the interpolation relation $X_{t} = (1 - t)X_{0} + tX_{1}$ can be inverted to obtain $X_{0} = \frac{1}{1 - t}\big(X_{t} - tX_{1}\big)$ . Substituting this into the displacement $X_{1} - X_{0}$ yields $X_{1} - X_{0} = -\frac{1}{1 - t} X_{t} + \frac{1}{1 - t} X_{1}$ . Taking conditional expectation given $X_{t} = x$ , we obtain the closed-form expression for the true velocity field:

$$
v (x, t) = \mathbb {E} \left[ - \frac {1}{1 - t} X _ {t} + \frac {1}{1 - t} X _ {1} \Bigg | X _ {t} = x \right] = - \frac {1}{1 - t} x + \frac {1}{1 - t} \mathbb {E} [ X _ {1} \mid X _ {t} = x ].
$$

Thus, the vector field $v(x,t)$ consists of two interpretable terms: a deterministic contraction term $-\frac{1}{1 - t} x$ that pulls $x$ toward the origin, and a prediction term $\frac{1}{1 - t}\mathbb{E}[X_1\mid X_t = x]$ that directs the flow toward the target distribution $\pi_{1}$ .

A crucial modeling choice in flow matching is the prior distribution. The choice of the prior distribution affects this conditional expectation $\mathbb{E}[X_1\mid X_t = x]$ significantly. While Gaussian priors are the standard

choice in unconstrained generative modeling, they are poorly suited when the target distribution exhibits heavy tails. The following example illustrates this pathology. Denote standard Student t distribution as $t_{d,\nu}(x) = C_{\nu,d}\left(1 + \frac{1}{\nu}\| x\|^2\right)^{-\frac{\nu + d}{2}}$ .

Example 4. Consider the one-dimensional target density $X_{1} \sim p(x) \propto (1 + \frac{1}{2} x^{2})^{-\frac{3}{2}}$ . Suppose we use a Gaussian prior $X_{0} \sim \mathcal{N}(0,1)$ . Then the conditional distribution of $X_{1}$ given an interpolated point $X_{t} = x$ , is given by

$$
p (X _ {1} | X _ {t} = x) \propto g (x _ {1}) := \exp \left(- \frac {(t x _ {1} - x) ^ {2}}{2 (1 - t) ^ {2}}\right) \left(\frac {1}{1 + \frac {1}{2} x _ {1} ^ {2}}\right) ^ {\frac {3}{2}}.
$$

This conditional distribution develops two modes: one near $x_{1} = 0$ and another near $x_{1} \approx x / t$ . Although the $t \to 0$ limit will not cause a singularity (Wan et al., 2025), we emphasize that for large values of $\| x \|$ , the vector field would scales as $\exp(x^{2})$ for some small values of $t$ , implying that the true velocity field $v(x, t)$ can blow up super-exponentially in $x$ . Furthermore, as discussed in Wan et al. (2025); Zhou and Liu (2025), singularities exist as $t \to 1$ . By contrast, if we replace the Gaussian prior with a heavy-tailed Student- $t$ prior (e.g., with $\nu = 1$ ), the conditional density becomes

$$
p (X _ {1} | X _ {t} = x) \propto g (x _ {1}) = \left(1 + \left\| \frac {x - t x _ {1}}{1 - t} \right\| ^ {2}\right) ^ {- 1} \left(\frac {1}{1 + \frac {1}{2} x _ {1} ^ {2}}\right) ^ {\frac {3}{2}},
$$

for which the dominant mode remains near $x_{1} = 0$ even as $x$ being large, over $t \in [0,T] \subsetneq [0,1]$ . In this case, the conditional expectation does not explode with $x$ , and the resulting velocity field remains controlled. See Appendix Section C for a visualization.

This example highlights a key principle: when the target distribution is heavier-tailed than the prior, the conditional distribution is likely to have a mode that is dominant near $\frac{x}{t}$ for some values of $t$ . Then the induced velocity field can diverge at large $\| x \|$ , producing ill-posed dynamics and complicating error analysis. In particular, such blow-ups directly cause the Lipschitz constant of $v(x, t)$ to diverge as $\| x \| \to \infty$ , necessitating additional assumptions on the tail of data distribution (e.g., bounded support) (Benton et al., 2024; Bansal et al., 2024; Gao et al., 2024; Zhou and Liu, 2025). Choosing a Student- $t$ prior prevents these blow-ups by making the data distribution to dominate the tail behavior of the conditional distribution, suppressing the mode near $x / t$ . In this way, the mode near zero will be dominant, ensuring controlled velocity fields, finite-moment guarantees of the interpolation conditional distribution, and stability in both theoretical analysis and practical training.

# 3 Mirror Flow Matching

Recall from Section 2 that we discussed choices of mirror maps for closed convex sets of the form $\mathcal{K} = \{x\in$ $\mathbb{R}^d:\phi_i(x) < 0,\forall i\in [m]\}$ . In mirror flow matching, both the prior $\pi_0$ and the target $\pi_{1}$ are required to be supported on $\mathcal{K}$ . The objective is to learn a continuous-time flow $X_{t}$ defined by the ODE $\frac{d}{dt} X_t = v^P (X_t,t)$ with $X_0\sim \pi_0(x)$ that transports $\pi_0$ to $\pi_{1}$ over the interval $t\in [0,1]$ .

Mirror flow matching achieves this transport by interpolating in a transformed (mirror) space. Given a mirror map $\nabla \Psi$ , we map $x \in \mathcal{K}$ into the dual space via $z = \nabla \Psi(x)$ . As shown in Li et al. (2022), the dual Euclidean space $(\mathbb{R}^d, I_d)$ is isometric to the primal space equipped with the squared Hessian metric $(\mathcal{K}, (\nabla^2 \Psi)^2)$ . We denote these metrics as $g^P = (\nabla^2 \Psi)^2$ and $g^D = I_d$ . The procedure is then as follows: (1.) Map primal data to dual space: $z = \nabla \Psi(x)$ . (2.) Perform flow matching in the dual space using straight-line interpolation $Z_t = (1 - t) Z_0 + t Z_1$ . (3.) After generating samples $\hat{z}$ in the dual space, map them back to primal space using the inverse mirror map $\hat{x} = \nabla \Psi^*(\hat{z})$ . In particular, interpolation in primal space is defined

![](images/b8cc9772779f5b9cc034ec3b18d0fc58640814403eb89569b2a503050f848abd.jpg)  
(a) Primal space trajectory

![](images/31204978f51a71cca0f75dba4b34f17b0842d4ad29aac238e88142b3515d01a0.jpg)  
(b) Dual space trajectory   
Figure 2: Visualization of interpolations in primal and dual spaces - Straight line interpolation in the dual space (Figure (b)) corresponds to curved "geodesic" interpolation in primal space Figure (a)).

as $X_{t} = \nabla \Psi^{*}(Z_{t})$ , which can be interpreted as the geodesic interpolation between $X_{0}$ and $X_{1}$ under the squared Hessian metric. See Figure 2 for an illustrative trajectory visualization in both the primal and dual spaces.

Relation between dual and primal velocity fields. Consider a dual-space flow $Z_{t}$ defined by vector field $v^{D}$ . By direct differentiation, the corresponding primal velocity field is

$$
v ^ {P} \left(X _ {t}, t\right) := \frac {d}{d t} X _ {t} = \nabla^ {2} \Psi^ {*} \left(Z _ {t}\right) \left(\frac {d}{d t} Z _ {t}\right) = \nabla^ {2} \Psi^ {*} \left(Z _ {t}\right) v ^ {D} \left(Z _ {t}, t\right). \tag {3.1}
$$

The flow matching objective in the dual space is

$$
\min  _ {v} \mathbb {E} _ {t, Z _ {0}, Z _ {1}} \left[ \| v ^ {D} \left(Z _ {t}, t\right) - \frac {d}{d t} Z _ {t} \| _ {g ^ {D}} ^ {2} \right], \quad Z _ {t} = (1 - t) Z _ {0} + t Z _ {1}, \tag {3.2}
$$

whose solution is known to be the conditional expectation $v^{D}(z,t) = \mathbb{E}\left[\frac{d}{dt} Z_{t} \mid Z_{t} = z\right]$ (Liu et al., 2023b). The following proposition establishes the equivalence between primal and dual formulations.

Proposition 5. Learning a vector field in the dual Euclidean space $(\mathbb{R}^d, I_d)$ is equivalent to learning a vector field in the primal space $(\mathcal{K}, (\nabla^2 \Psi)^2)$ . Specifically,

$$
\min _ {v} \mathbb {E} \Big [ \| v ^ {P} (X _ {t}, t) - \frac {d}{d t} X _ {t} \| _ {g ^ {P}} ^ {2} \Big ] a n d \min _ {v} \mathbb {E} \Big [ \| v ^ {D} (Z _ {t}, t) - \frac {d}{d t} Z _ {t} \| _ {g ^ {D}} ^ {2} \Big ]
$$

are equivalent, with the correspondence $v^{D}(z,t) = \nabla^{2}\Psi (x)v^{P}(x,t)$ . Moreover, the primal flow matching objective is solved by $v^{P}(x,t) = \mathbb{E}\big[\frac{d}{dt} X_{t}\big|X_{t} = x\big]$ .

This result shows that training in the dual space with straight-line interpolation is equivalent to training in the primal space with geodesic interpolation under the squared Hessian metric. From an algorithmic standpoint, this equivalence is highly convenient: we can train the dual-space vector field $v^{D}$ , which is simpler due to its Euclidean geometry, and recover the primal vector field $v^{P}$ by the transformation in (3.1). Thus, the difficult geometry of $\mathcal{K}$ is automatically handled by the mirror map, while optimization is carried out in an unconstrained Euclidean space.

The algorithmic procedure for mirror flow matching is summarized in Algorithm 1. This pipeline leverages the simplicity of Euclidean training in dual space, while ensuring that the generated samples respect the original convex constraints in primal space. Here, $h$ denotes the step size (in sampling stage) and $T < 1$ denotes the terminal time if early stopping is adopted.

Algorithm 1 Mirror Flow matching with Student t distribution

1: Map data distribution from $\mathcal{K}$ to $\mathbb{R}^d$ using $\nabla \Psi$ , obtain samples for $Z_{1}$ .   
2: Learn a vector field $\hat{v}^D(z,t)$ with prior $\pi_0(x) \sim t_{d,\nu}$ via $\min_{\hat{v}^D} \mathbb{E}_{t,Z_0 \sim \pi_0^D,Z_1 \sim \pi_1^D}\left[\|\hat{v}^D(Z_t,t) - (Z_1 - Z_0)\|^2\right]$ where $Z_t = tZ_1 + (1 - t)Z_0$ .   
3: Choose step size $h$ for Euler discretization s.t. $\frac{1}{h}$ is integer. Choose $T \in (0, 1)$ as early stopping time, satisfying $\frac{T}{h} \in \mathbb{Z}$ .   
4: Perform Euler discretization to sample from $\pi_1^D$ with constant step size $h$ , up to time $T$ :   
5: Generate $\overline{z}_0\sim \pi_0^D$   
6: for $k = 0$ to $\frac{T}{h} - 1$ do   
7: $\overline{z}_{h(k + 1)} = \overline{z}_{hk} + h\hat{v} (\overline{z}_k,hk)$   
8: end for   
9: Denote the obtained sample by $\overline{z}_T\sim \hat{\pi}_T^D$   
10: Map samples $\overline{z}_T$ back to $\mathcal{K}$ using $\nabla \Psi^{*}$ to obtain $\overline{x}_T$ .

# 4 Theoretical Results

In this section, we provide a theoretical analysis of error bounds for flow matching. A key component of our analysis is the accuracy of the neural network used to approximate the target velocity field. We adopt the following assumption, which is standard in the literature on flow-based generative modeling (see, e.g., Benton et al. (2024); Bansal et al. (2024); Li et al. (2025)) as well as in the study of diffusion models (see, e.g., Chen et al. (2023); Li et al. (2024)). Theoretical justification for this assumption can be found in Wang et al. (2024); Zhou and Liu (2025), where the authors establish that such an $\varepsilon$ -level approximation error can be achieved by a neural network under suitable training conditions.

Assumption 1. (Neural Network Estimation Error) Let $v(x,t)$ denote the true velocity field and $\hat{v}(x,t)$ its neural network approximation. We assume that the approximation error is bounded in mean square, i.e., $\mathbb{E}\big[\| v(x,t) - \hat{v}(x,t)\|^2\big] \leq \varepsilon^2$ .

Intuitively, Assumption 1 states that the learned velocity field $\hat{v}$ is close to the true velocity field $v$ in an average sense across both space and time. The parameter $\varepsilon$ therefore quantifies the quality of the neural network approximation: smaller $\varepsilon$ implies a more accurate approximation, which directly translates into higher fidelity of the generated samples.

# 4.1 Guarantees for Euclidean Flow Matching with t-Distribution Priors

In this subsection, we provide an error analysis for flow matching in Euclidean space when the prior distribution is chosen to be a Student- $t$ distribution (henceforth referred to as $t$ -Flow). Our analysis applies to the general framework of flow matching with straight-line interpolation, and is not restricted to the mirror flow matching setup. To maintain notation consistency, we denote random variables as $Z \in \mathbb{R}^d$ with density $\pi_1^D$ . We begin by introducing the assumptions required.

Assumption 2 (Finite Moments). Let $Z_0$ denote the prior (chosen as Student-t) random variable and $Z_1$ denote the target random variable, both supported on $\mathbb{R}^d$ . We assume that they have finite second moments, i.e., $\mathbb{E}[\| Z_0\|^2] < \infty$ , $\mathbb{E}[\| Z_1\|^2] < \infty$ , which is necessary for well-definedness.

Assumption 3 (Polynomial Tail Bound). Let $\pi_1^D(x)$ denote the probability density function of the data distribution supported on $\mathbb{R}^d$ . It is assumed to satisfy: (1) For $\|x\| \geq 1$ , we have $\pi_1^D(x) \leq \frac{C}{\|\bar{x}\|^{\alpha}}$ , and (2) For $\|x\| < 1$ , we have $\pi_1^D(x) \leq C_u$ .

The above assumption allows the target distribution to be heavy-tailed, covering a wide range of realistic distributions. We next establish Lipschitz guarantees for the true vector field, showing that under Assumption 3, the velocity field induced by t-Flow is both spatially Lipschitz and admits a controlled temporal derivative, which is crucial for bounding the discretization error in Theorem 7.

Proposition 6. Let $v^{D}$ be the minimizer of the $t$ -Flow objective (Equation 3.2). Under Assumption 3 with $\alpha \geq 2d + \nu + 2$ , there exist constants $B_{1}, B_{2}$ such that, for all $t \in [0, T]$ :

1. (Spatial Lipschitzness) The vector field $v^{D}(z,t)$ is $L_{1}$ -Lipschitz in $z$ , with $L_{1} \coloneqq \frac{d + \nu}{(1 - T)^{2}} B_{1}$ .   
2. (Temporal Regularity) The time derivative of the velocity field is bounded as

$$
\left\| \frac {\partial}{\partial t} v (z, t) \right\| \leq \frac {1}{(1 - T) ^ {2}} \| z \| + \frac {1}{(1 - T) ^ {2}} B _ {1} + \frac {1}{1 - T} \frac {\nu + d}{\nu} \frac {3 \sqrt {\nu}}{2 (1 - T) ^ {2}} \bigl (B _ {2} + 3 B _ {1} ^ {2} \bigr).
$$

The proof is deferred to Appendix F.1. To the best of our knowledge, the only prior work that controlled the temporal Lipschitzness of the vector field in order to bound discretization error is Zhou and Liu (2025). However, their analysis required the data distribution to have bounded support, whereas our result only assumes a polynomial tail bound. For spatial Lipschitzness, existing results either imposed stronger conditions on the data distribution (Zhou and Liu, 2025; Benton et al., 2024; Gao et al., 2024) or studied different problem settings (Cordero-Encinar et al., 2025). We can now quantify the discretization error of t-Flow.

Theorem 7 (Discretization Error of t-Flow). Consider t-Flow in Euclidean space. Let $\pi_1^D$ denote the data distribution supported on $\mathbb{R}^d$ , and $\hat{\pi}_T^D$ be the law of generated sample $\overline{z}_T$ obtained by Euler discretization with constant step size $h$ , up to time $T$ (see line 9 of Algorithm 1). Under Assumption 3 with $\alpha \geq 2d + \nu + 2$ , Assumption 2, and Assumption 1, there exists a constant $D_3$ , depending polynomially on $\frac{1}{1 - T}$ , $d$ , $\nu$ , and on $B_1, B_2, \mathbb{E}[\|Z_1\|^2], \mathbb{E}[\|Z_0\|^2]$ , such that

$$
W _ {2} (\pi_ {1} ^ {D}, \hat {\pi} _ {T} ^ {D}) \leq \frac {e ^ {6 L _ {1}}}{L _ {1}} \sqrt {h ^ {2} D _ {3} + \varepsilon^ {2}} + (1 - T) \sqrt {2 \big (\mathbb {E} [ \| Z _ {1} \| ^ {2} ] + \mathbb {E} [ \| Z _ {0} \| ^ {2} ] \big)}.
$$

The proof is provided in Appendix F.2. The error bound consists of two terms. The first term captures the discretization error (from Euler steps of size $h$ ) and the neural network approximation error (measured by $\varepsilon$ ). Both vanish as $h \to 0$ and $\varepsilon \to 0$ . The second term corresponds to early stopping error, which decreases to zero as $T \to 1$ . Thus, by taking $T$ close to 1 and ensuring accurate vector field approximation with sufficiently small step size, we can guarantee high-quality samples.

We now compare our result with recent related works. Bansal et al. (2024) did not analyze the Lipschitz properties of the velocity field, but instead imposed them as assumptions. Zhou and Liu (2025) established both spatial and temporal Lipschitzness and further analyzed neural network approximation, but required the data distribution to have bounded support. We note that the exponential dependence on the spatial Lipschitz constant $L_{1}$ arises due to non-convexity, and also appears in existing analyses (Bansal et al., 2024; Zhou and Liu, 2025). It is plausible that this exponential dependency could be improved to polynomial dependence by following the probabilistic coupling strategy in Chen et al. (2023), though the resulting algorithm is not purely deterministic.

# 4.2 Primal Space Guarantee for Mirror Flow Matching

We next obtain the following primal space guarantee. First note that the primal space $(\mathcal{K}, g^{P})$ and the dual space $(\mathbb{R}^d, g^D)$ are isometric. Hence, we have the following result.

Lemma 8. If the vector field $v^{D}$ is $L_{1}$ Lipschitz in the dual space $(\mathbb{R}^d, g^D)$ , it is $L_{1}$ Lipschitz in the primal space $(\mathcal{K}, g^{P})$ (under the squared Hessian metric).

To relate Assumption 3 with the distribution in primal space, we impose the following condition.

Assumption 4. (Primal Space Probability Density Function). Denote $\pi_{Euc}^{P}(x)$ as the probability density function for $\pi_1^P$ in the primal space, under Euclidean metric. Assume that $\pi_{Euc}^{P}(x)$ is smooth and that there exists a small constant $\delta_0$ such that $\sup_{x\in \mathcal{K}\backslash \mathcal{K}_{\delta}}\pi_{Euc}^{P}(x)\leq C_{pdf}\delta^{\gamma},\forall \delta \leq \delta_{0}$

Theorem 9. Let $\hat{\pi}_T^P$ be the law of output samples generated by Algorithm 1 (i.e., the law of $\overline{x}_T$ in Line 10). Under Assumption 1 and 4, with $\kappa \leq \frac{\gamma}{2d + \nu + 2}$ , and we further require $\kappa < \frac{\beta}{2}$ , there exists constant $L_1, D_3$ and $M := \sqrt{2\left(\mathbb{E}[\|Z_1\|^2] + \mathbb{E}[\|Z_0\|^2]\right)}$ such that

$$
W _ {2} (\pi_ {1} ^ {P}, \hat {\pi} _ {T} ^ {P}) \leq \frac {e ^ {6 L _ {1}}}{L _ {1}} \sqrt {h ^ {2} D _ {3} + \varepsilon^ {2}} + (1 - T) M.
$$

The proof is provided in Appendix F.3 and essentially follows by Proposition 2 and Theorem 7.

# 5 Experiments

We demonstrate the effectiveness of our approach by performing numerical simulation (see section 5.1) and real world data experiments on AFHQv2 dataset (see section 5.2). The numerical simulation is performed on a personal laptop using a CPU. The real world data experiments were performed on a single A100 GPU.

# 5.1 Numerical simulation

We build on the experimental setup of Li et al. (2025) and conduct numerical simulations on two representative constrained generative modeling tasks. The first task is a 10-dimensional polytope problem, defined as $\{x\in \mathbb{R}^{10}:a_i^\top x < b_i,i = 1,2,\ldots ,30\}$ , with constraints loaded from a pre-specified data file from Li et al. (2025). The target distribution is a uniform mixture of Gaussians, where the means are partly sampled at random and partly human-designed to stress-test the model (e.g., $(-3, - 3,3,3,\dots , - 3)\in \mathbb{R}^{10})$ , and covariances are fixed to $0.4I_{10}$ . The second task is a 6-dimensional $L_{2}$ ball problem, defined as $\{x\in \mathbb{R}^6:\| x\| ^2 < 144\}$ , with target distributions generated in the same manner as in the polytope case.

We implemented our method with $\kappa = 0.3$ and used a $t$ -Flow prior with $\nu = 10$ . As shown in Table 1 and Table 2, our approach consistently outperforms both Gauge Flow Matching (Li et al., 2025) and Reflected Flow Matching (RFM) (Xie et al., 2024). Across both tasks, our method achieves lower KL divergence and smaller Maximum Mean Discrepancy (MMD) values, while simultaneously guaranteeing sample feasibility. For the $L_{2}$ ball case, Gauge Flow Matching is omitted since it coincides with Reflected Flow Matching.

These experiments highlight the advantages of our method. By jointly choosing mirror maps and priors based on careful analysis, our approach achieves superior performance on numerical benchmarks while preserving feasibility by construction. The ability to obtain tighter divergence metrics under strict feasibility underscores its promise for high-dimensional constrained generative modeling, demonstrating robustness across geometries (polytope vs. $L_{2}$ ball) and scalability to practical domains where constraints are central.

# 5.2 Real-data application: Watermarked image generation

Following Liu et al. (2023a), we evaluate our method on the task of $64 \times 64$ watermarked image generation using the AFHQv2 dataset. We begin by generating parameters $(a_i, b_i, c_i)$ , which serve as user-specific private keys. These parameters define a polytope $\mathcal{K} = \{x : c_i < a_i^\top x < b_i\}$ , where an image can be vectorized and checked for feasibility: an image lying inside $\mathcal{K}$ is verifiably generated by the model. During training, we first watermark the AFHQv2 images by projecting them (with added noise) onto the polytope,

Table 1: Performance comparison with 10-dimensional polytope constraints. Results are based on an average of 10 runs. MMD values are scaled by $10^{-3}$ .   

<table><tr><td>Method</td><td>MMD ↓</td><td>KL Divergence ↓</td><td>Feasibility</td></tr><tr><td>Mirror t-Flow</td><td>5.552 ± 0.116</td><td>0.339 ± 0.021</td><td>100%</td></tr><tr><td>Mirror G-Flow</td><td>5.774 ± 0.110</td><td>0.379 ± 0.028</td><td>100%</td></tr><tr><td>Gauge Vanilla (Li et al., 2025)</td><td>7.490 ± 0.068</td><td>0.813 ± 0.020</td><td>90.653 ± 0.284%</td></tr><tr><td>Gauge Reflect (Li et al., 2025)</td><td>7.527 ± 0.072</td><td>0.860 ± 0.020</td><td>100%</td></tr><tr><td>RFM (Xie et al., 2024)</td><td>5.868 ± 0.173</td><td>0.360 ± 0.030</td><td>98.259 ± 0.123%</td></tr></table>

Table 2: Performance comparison on 6-dimensional $L_{2}$ ball constraints. Results are based on an average of 10 runs. Performance metrics are scaled by $10^{-2}$ .   

<table><tr><td>Method</td><td>MMD ↓</td><td>KL Divergence ↓</td><td>Feasibility</td></tr><tr><td>Mirror t-Flow</td><td>1.153 ± 0.028</td><td>6.944 ± 1.111</td><td>100%</td></tr><tr><td>Mirror G-Flow</td><td>1.221 ± 0.035</td><td>9.644 ± 1.174</td><td>100%</td></tr><tr><td>RFM (Xie et al., 2024)</td><td>1.393 ± 0.039</td><td>14.827 ± 1.108</td><td>100%</td></tr></table>

thereby producing a watermarked dataset. We then use these watermarked images as training data and compare the performance of Mirror Diffusion Models (MDM) (Liu et al., 2023a) with our proposed Mirror $t$ -Flow approach.

A crucial component is the initialization used for the models. We first train both methods with random neural network initialization under a limited training budget (24 hours). We set the mirror map parameter as $\kappa = 0.1$ for our method, with random initialization. We first report the CMMD metric (Jayasumana et al., 2024). CMMD combines CLIP embedding with Maximum Mean Discrepancy metric and is considered more reliable than FID for evaluating generative models. With 10,000 generated images, our approach achieves a CMMD score of 0.177, which is competitive with the MDM baseline (Liu et al., 2023a), calculated to be 0.152. Nevertheless, as shown in Figure 3(a), our method already produces visually high-quality samples within a limited training budget, demonstrating strong potential for further improvements with better initializations.

Towards that, in Table 3 we next report results when the models are initialized at EDM (Karras et al., 2022) checkpoint for AFHQv2 dataset; the corresponding sample images are displayed in in Figure 3(b). We note that in this case, our method achieves superior CMMD and FID scores, requiring a smaller amount of training time. Finally, we remark that if we initialize at the checkpoint for a flow matching model from Lee et al. (2024), the FID (50k) can achieve 3.14 after 1.5 hours of training. This value is similar to 3.05 reported in Liu et al. (2023a), while fully executing their scheduled number of iterations could result in an estimated training time up to several hundred hours in our experimental setup.

Table 3: Performance comparison on watermarked image generation on the AFHQ2 dataset. Both implementations are initialized at EDM (Karras et al., 2022) checkpoint. For MDM, we use the code from Liu et al. (2023a). For flow matching, we apply the training framework from Lee et al. (2024).   

<table><tr><td>Method</td><td>FID (50k)↓</td><td>CMMD</td><td>training time</td></tr><tr><td>Mirror Flow (κ = 0.05)</td><td>4.27</td><td>0.023</td><td>3 hours</td></tr><tr><td>Mirrod Diffusion Model (Liu et al., 2023a)</td><td>7.29</td><td>0.170</td><td>13 hours</td></tr></table>

![](images/7f964d645a3333609ae784dd75e2ebc26c5b3e4a7d79c85f546556d8b8dc27ed.jpg)

![](images/fe412bef33a84b85df422113f897e52246a6e92bb1aef5f04d75e05ddba1fc5a.jpg)

![](images/b056d71f3f9cd4c5a870a6df23fb56d6c6cdbd3de6fe098c449fc2f4f8cacf51.jpg)

![](images/6021ddcf34ea31b93a93d9a0d0d6b6b451fd81fbb284de468f287e5ae1d9cb3a.jpg)

![](images/cde71301a7129973426b8a829f21736e1f2c91808b76faad063453b8ef02c272.jpg)

![](images/43a2ba81786293d67711b9fd8d484c966dddbd21e5938cb6e566b06310dff46a.jpg)

![](images/f8401d1a39d7a36d9bd49d191c2eb438c52187653fbb80514e85efd745500c66.jpg)

![](images/7b3d627c0a7ccfa1fdaa8ba5c5cd0d070ec60b660d20ba39edd0b97c5e20f6f5.jpg)  
(a) With random initialization

![](images/1b5df42b29c13e3a78b4e01a245b3329a45f8382789e527853ab475008633b05.jpg)

![](images/8bc20660905160e79ab7a327cd0621ea85feb3a76a31a6ebca78fa9c73ce8bfa.jpg)

![](images/5afb8cd04f254655d0db837485c269730bd011274165d157dc241a3dd6b40907.jpg)

![](images/a701654ada36da92b095d1c67709be629a2aeffd79a7102ac2707ba2e63185de.jpg)

![](images/910c1417071eee56a8fabaffd03ba9a2335fee4e3701c8ec9035979c85fe97f6.jpg)

![](images/3919a38407c242be2beddd858f6eb3dec047e755b98800313b78bfdbfb9c49d0.jpg)

![](images/67eb34c7102981ff8b8223125591d96a9d1a5d34293b20679ef6bcfde88f4e89.jpg)

![](images/0514627e852e591d9c2384384557113a81213ef6b188175ced21aaffc167c954.jpg)  
(b) With EDM checkpoint initialization   
Figure 3: Samples of generated watermarked images from the AFHQv2 $64 \times 64$ dataset. Constraint satisfaction were checked with built-in functions of Liu et al. (2023a).

# 6 Conclusion

We introduced $t$ -Flow, a flow-matching framework with Student- $t$ priors, and established rigorous guarantees on both spatial Lipschitzness and temporal regularity of the underlying velocity field. Our analysis yielded the first error bounds for flow matching under polynomial tail assumptions, thereby extending prior results beyond bounded-support assumptions. We further demonstrated that $t$ -Flow provides robust sample quality in practice, particularly in scenarios where Gaussian priors fail to capture heavy-tailed structures. Beyond technical guarantees, our results emphasize that successful generative modeling on complex domains requires a careful co-design of mirror maps and priors, rather than defaulting to standard choices. This perspective opens up several promising avenues. One direction is exploring adaptive choices of degrees of freedom in the $t$ -prior could yield even more flexibility, enabling flows that automatically adapt to local tail behavior of the data. Another is extending $t$ -Flow to constrained domains with non-convex geometry, potentially leveraging landing techniques. On the theory front, improving the exponential dependence on Lipschitz constants, for example via probabilistic couplings or randomized flow strategies is interesting. Finally integrating $t$ -Flow with hybrid diffusion-flow architectures and energy-based models offers yet another exciting path, combining the complementary strengths of these paradigms.

# Acknowledgments

Krishnakumar Balasubramanian was supported in part by NSF grant DMS-2413426. Shiqian Ma was supported in part by NSF grants CCF-2311275 and ECCS-2326591, and ONR grant N00014-24-1-2705.

# References

M. S. Albergo and E. Vanden-Eijnden. Building normalizing flows with stochastic interpolants. In The Eleventh International Conference on Learning Representations, 2023. URL https://openreview.net/forum?id=1i7qeBbCR1t.   
M. S. Albergo, N. M. Boffi, and E. Vanden-Eijnden. Stochastic interpolants: A unifying framework for flows and diffusions. arXiv preprint arXiv:2303.08797, 2023.   
V. Bansal, S. Roy, P. Sarkar, and A. Rinaldo. On the wasserstein convergence and straightness of rectified flow. arXiv preprint arXiv:2410.14949, 2024.   
J. Benton, G. Deligiannidis, and A. Doucet. Error bounds for flow matching methods. Transactions on Machine Learning Research, 2024. ISSN 2835-8856. URL https://openreview.net/forum?id=uqQPyWFDhY.   
R. T. Q. Chen and Y. Lipman. Flow matching on general geometries. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=g7ohD1TITL.   
S. Chen, S. Chewi, H. Lee, Y. Li, J. Lu, and A. Salim. The probability flow ode is provably fast. Advances in Neural Information Processing Systems, 36:68552-68575, 2023.   
J. K. Christopher, S. Baek, and N. Fioretto. Constrained synthesis with projected diffusion models. Advances in Neural Information Processing Systems, 37:89307-89333, 2024.   
P. Cordero-Encinar, O. D. Akyildiz, and A. B. Duncan. Non-asymptotic analysis of diffusion annealed Langevin monte carlo for generative modelling. arXiv preprint arXiv:2502.09306, 2025.   
B. Feng, R. Baptista, and K. Bouman. Neural approximate mirror maps for constrained diffusion models. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=vgZDcUetWS.   
N. Fishman, L. Klarner, V. D. Bortoli, E. Mathieu, and M. J. Hutchinson. Diffusion models for constrained domains. Transactions on Machine Learning Research, 2023a. ISSN 2835-8856. URL https://openreview.net/forum?id= xuWTFQ4VGO. Expert Certification.   
N. Fishman, L. Klarner, E. Mathieu, M. Hutchinson, and V. De Bortoli. Metropolis sampling for constrained diffusion models. Advances in Neural Information Processing Systems, 36:62296-62331, 2023b.   
Y. Gao, J. Huang, and Y. Jiao. Gaussian interpolation flows. Journal of Machine Learning Research, 25(253): 1-52, 2024.   
Z. Huan, J. Boerma, L.-P. Liu, and S. Aeron. Efficient constraint-aware flow matching via randomized exploration. arXiv preprint arXiv:2508.13316, 2025.   
T. Hytönen, J. Van Neerven, M. Veraar, and L. Weis. Analysis in Banach spaces, volume 1. Springer, 2016.   
S. Jayasumana, S. Ramalingam, A. Veit, D. Glasner, A. Chakrabarti, and S. Kumar. Rethinking fid: Towards a better evaluation metric for image generation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 9307-9315, 2024.   
T. Karras, M. Aittala, T. Aila, and S. Laine. Elucidating the design space of diffusion-based generative models. Advances in neural information processing systems, 35:26565-26577, 2022.

S. Khalafi, D. Ding, and A. Ribeiro. Constrained diffusion models via dual training. Advances in Neural Information Processing Systems, 37:26543-26576, 2024.   
M. Kim, Y. Lee, S. Kang, J. Oh, S. Chong, and S.-Y. Yun. Preference alignment with flow matching. Advances in Neural Information Processing Systems, 37:35140-35164, 2024.   
S. Lee, Z. Lin, and G. Fanti. Improving the training of rectified flows. Advances in neural information processing systems, 37:63082-63109, 2024.   
G. Li, Y. Wei, Y. Chen, and Y. Chi. Towards non-asymptotic convergence for diffusion-based generative models. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=4VGEeER6W9.   
R. Li, M. Tao, S. S. Vempala, and A. Wibisono. The mirror langevin algorithm converges with vanishing bias. In International Conference on Algorithmic Learning Theory, pages 718-742. PMLR, 2022.   
X. Li, E. Liang, and M. Chen. Gauge flow matching for efficient constrained generative modeling over general convex set. In ICLR 2025 Workshop on Deep Generative Model in Machine Learning: Theory, Principle and Efficacy, 2025.   
Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. In The Eleventh International Conference on Learning Representations, 2023. URL https://openreview.net/forum?id=PqvMRDCJT9t.   
G.-H. Liu, T. Chen, E. Theodorou, and M. Tao. Mirror diffusion models for constrained and watermarked generation. Advances in Neural Information Processing Systems, 36:42898-42917, 2023a.   
X. Liu, C. Gong, and qiang liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. In The Eleventh International Conference on Learning Representations, 2023b. URL https://openreview.net/forum?id=XVjTT1nw5z.   
X. Liu, C. Gong, and qiang liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. In The Eleventh International Conference on Learning Representations, 2023c. URL https://openreview.net/forum?id=XVjTT1nw5z.   
A. Lou and S. Ermon. Reflected diffusion models. In International Conference on Machine Learning, pages 22675-22701. PMLR, 2023.   
K. Pandey, J. Pathak, Y. Xu, S. Mandt, M. Pritchard, A. Vahdat, and M. Mardani. Heavy-tailed diffusion models. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=toz1OEN4qp.   
A. Tong, K. Fatras, N. Malkin, G. Huguet, Y. Zhang, J. Rector-Brooks, G. Wolf, and Y. Bengio. Improving and generalizing flow-based generative models with minibatch optimal transport. Transactions on Machine Learning Research, 2024. ISSN 2835-8856. URL https://openreview.net/forum?id=CD9Snc73AW. Expert Certification.   
U. Utkarsh, P. Cai, A. Edelman, R. Gomez-Bombarelli, and C. V. Rackauckas. Physics-constrained flow matching: Sampling generative models with hard constraints. arXiv preprint arXiv:2506.04171, 2025.   
N. M. Vural, L. Yu, K. Balasubramanian, S. Volgushev, and M. A. Erdogdu. Mirror descent strikes again: Optimal stochastic convex optimization under infinite noise variance. In Conference on Learning Theory, pages 65-102. PMLR, 2022.

Z. Wan, Q. Wang, G. Mishne, and Y. Wang. Elucidating flow matching ODE dynamics via data geometry and denoisers. In *Forty-second International Conference on Machine Learning*, 2025. URL https://openreview.net/forum?id=f5czhqYK3H.   
Y. Wang, Y. He, and M. Tao. Evaluating the design space of diffusion-based generative models. Advances in Neural Information Processing Systems, 37:19307-19352, 2024.   
T. Xie, Y. Zhu, L. Yu, T. Yang, Z. Cheng, S. Zhang, X. Zhang, and C. Zhang. Reflected flow matching. In *Forty-first International Conference on Machine Learning*, 2024. URL https://openreview.net/forum?id=Sf5KYznS2G.   
Q. Zhang, Z. Liu, H. Fan, G. Liu, B. Zeng, and S. Liu. Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pages 14754-14762, 2025.   
Z. Zhou and W. Liu. An error analysis of flow matching for deep generative modeling. In *Forty-second International Conference on Machine Learning*, 2025. URL https://openreview.net/forum?id=vES22INUKm.

# A Visual Illustration of Methodological Challenges

We illustrate the benefits of our approach in Figure 4. The constraint set is a polytope $\mathcal{K} = \{x\in \mathbb{R}^2:Ax < b\}$ with

$$
A ^ {\top} = \left( \begin{array}{c c c c c} 1 & - 1 & 1 & - 5 & - 1 / 3 \\ 1 & - 1 & - 1 & 1 & 1 \end{array} \right), \qquad b ^ {\top} = \left( \begin{array}{c c c c c} 1 0 & 3 0 & 1 & 9 0 & 5 \end{array} \right).
$$

The target $\pi_1$ is a mixture of three Gaussians, truncated to $\mathcal{K}$ : $\mathcal{N}([ -10, 0]^T, \mathrm{diag}(8, 2))$ with weight 0.6, $\mathcal{N}([-15, -10]^T, \mathrm{diag}(1, 1))$ with weight 0.2, and $\mathcal{N}([3, 3]^T, \mathrm{diag}(0.5, 0.25))$ with weight 0.2. We compare G-flow (Gaussian prior) and t-flow (Student- $t$ prior) under both the log-barrier mirror map and our proposed regularized map (Figures 4(b)-4(e)), alongside samples from the true target (Figure 4(a)). Vector fields were parameterized by neural networks and simulated via Euler discretization ( $h = 0.1$ ) with early stopping. As shown in Figure 4, our approach achieves robust mode recovery and faithful constrained sampling, consistently outperforming Gaussian-based flow methods.

# B Examples verifying Proposition 2

Proposition 2 can be specialized to several classical examples of convex sets.

1. $L_{2}$ ball. Consider the closed Euclidean ball $\mathcal{K} = \{x\in \mathbb{R}^d:\| x\| \leq R\}$ . Define the mirror potential $\Psi (x) = -\frac{1}{1 - \kappa}\big(R^2 -\| x\|^2\big)^{1 - \kappa} + \frac{1}{2}\| x\|^2$ . In this case the barrier function is $\phi (x) = \| x\| ^2 -R^2$ , which is clearly smooth and convex. Moreover, its gradient is bounded on $\mathcal{K}$ , satisfying the required assumptions.   
2. Polytope. Let $\mathcal{K} = \{x\in \mathbb{R}^d:a_i^T x\leq b_i,\forall i\in [m]\}$ be a polytope defined by $m$ linear inequalities. Define the potential $\Psi (x) = -\sum_{i = 1}^{m}\frac{1}{1 - \kappa}\bigl {(}b_i - a_i^T x\bigr)^{1 - \kappa} + \frac{1}{2}\sum_{j = 1}^{d}x_j^2.$ Here the barrier functions are $\phi_i(x) = a_i^T x - b_i$ . Each $\phi_{i}$ is affine (hence smooth and convex), with Hessian $\nabla^2\phi_i(x) = 0$ , and its gradient is bounded uniformly. Thus the conditions are again satisfied.

![](images/6e8df23f8493fd08923178e949662540b6b85471c0dfc6104bef95fb1c0168f0.jpg)  
(a) Ground truth

![](images/eb8edac8d82625fc01a616b6f036068981a59e12a6a1c77d76c2ff5ad83af110.jpg)  
(b) G-flow Log Barrier

![](images/e22c05e3e711cacb54eab8d278223aff8dfd6c27537e2d2b1d98f84f99a1197a.jpg)  
(c) t-flow Log Barrier

![](images/ed6f858c3d2d8f087a0cd9220e8200a7919e1dadb09a4513e77dc64e51ed3845.jpg)  
(d) G-flow proposed mirror map

![](images/1d1e2ee69ac0db882637bfc19e36dce61fd444c5e07035989f0cd0ce905a01fe.jpg)  
(e) T-flow proposed mirror map   
Figure 4: Figure 4(a) shows the ground-truth reference distribution. Figures 4(b) and 4(c) illustrate that the log-barrier method performs poorly (both with G or t-flow), while Figure 4(d) demonstrates that G-flow (with our mirror map) fails to capture the mode centered near $(-10,0)$ . In contrast, Figure 4(e) shows that t-flow with our mirror map covers the target distribution better. All results are obtained with discretization step size $h = 0.1$ . See also Figure 5 for a zoomed-in illustration near the boundary.

# C Visual Illustration corresponding Section 2.2

We illustrate the blow-up phenomenon discussed in Section 2.2. In Figure 6(a), 6(b), 6(c) we illustrate the $t \to 0$ limit, blows-up for small $t$ , and $t \to 1$ limit respectively, for the G-flow. The corresponding Figure 6(d), 6(e), 6(f) for the t-flow is more benign.

# D Proofs for Section 2

Proof. [Proof of Lemma 1] Recall that for any one dimensional random variable $X$ , we have

$$
\int_ {0} ^ {\infty} P (X \geq t) d t = \int_ {0} ^ {\infty} \mathbb {E} [ \mathbb {1} _ {X \geq t} ] d t = \mathbb {E} [ \int_ {0} ^ {\infty} \mathbb {1} _ {X \geq t} d t ] = \mathbb {E} [ \int_ {0} ^ {X} d t ] = \mathbb {E} [ X ].
$$

# 1. First claim.

Assume $P(\| Y \| \geq R) \geq \frac{C}{R^p}$ . Hence we know (where $s := t^{1/p}$ , so that $dt = ps^{p-1} ds$ )

$$
\begin{array}{l} \mathbb {E} [ \| Y \| ^ {p} ] = \int_ {0} ^ {\infty} P (\| Y \| ^ {p} \geq t) d t = \int_ {0} ^ {\infty} P (\| Y \| \geq t ^ {1 / p}) d t = \int_ {0} ^ {\infty} P (\| Y \| \geq s) p s ^ {p - 1} d s \\ \geq \int_ {0} ^ {\infty} \frac {C}{s ^ {p}} p s ^ {p - 1} d s = \int_ {0} ^ {\infty} C p s ^ {- 1} d s. \\ \end{array}
$$

The integral does not converge.

![](images/9c6e856b486fd24019b5ef370aaa4a295dddd5b50771f193137c128880cb2dd0.jpg)  
(a) Ground truth

![](images/5115dbcec74a01b53c53360a2a46afffdfe9a19fbf0eceda844273ad9987664a.jpg)  
(b) G-flow proposed mirror map

![](images/34137b9b3913131cf40556141c1928eebc8e46fb94451ca02f3ffa6d356759a2.jpg)  
(c) t-flow proposed mirror map   
Figure 5: We generate a total of 10,000 samples, but for visualization we only display those lying in the boundary region $x \in [-14, -12]$ , $y \in [0,2]$ . Figure 5(a) shows the ground-truth reference distribution. Figures 5(b) and 5(c) demonstrate that, near the boundary, t-flow provides a closer approximation to the ground truth than G-flow.

# 2. Second claim.

Assume $P(\| Y\| \geq R)\leq \frac{C}{R^{\beta}}$

$$
\begin{array}{l} \mathbb {E} [ \| Y \| ^ {p} ] = \int_ {0} ^ {\infty} P (\| Y \| ^ {p} \geq t) d t = \int_ {0} ^ {\infty} P (\| Y \| \geq t ^ {1 / p}) d t = \int_ {0} ^ {\infty} P (\| Y \| \geq s) p s ^ {p - 1} d s \\ \leq \int_ {0} ^ {\infty} \frac {C}{s ^ {\beta}} p s ^ {p - 1} d s = \int_ {0} ^ {\infty} C p s ^ {p - 1 - \beta} d s. \\ \end{array}
$$

The integral converges iff $p - 1 - \beta < -1$ , i.e., $\beta > p$ .

![](images/ae390a5f51a5e90b58b87debf86cbeae91e4da4cd24ada871f7d67755ffc95d3.jpg)

Example 10. Let $\mathcal{K} \subseteq \mathbb{R}^2$ be a triangle defined by the following inequalities:

$$
\begin{array}{l} 1 0 0 x _ {1} + 0. 0 1 x _ {2} \leq 1, \\ 1 0 0 x _ {1} - 0. 0 1 x _ {2} \leq 1, \\ - x _ {1} \leq 0. \\ \end{array}
$$

Recall that for each constraint $a_i^T x \leq b_i$ we can define $\psi_i(x) = -\log (b_i - a_i^T x)$ . Then the log-barrier is $\psi(x) = \sum_i \psi_i(x)$ . Take derivative, we obtain $\nabla \psi(x) = \sum_i \frac{1}{b_i - a_i^T x} a_i$ .

$$
\begin{array}{l} \nabla \psi (k _ {1}, k _ {2}) = \sum_ {i} \frac {1}{b _ {i} - a _ {i} ^ {T} x} a _ {i} = \frac {1}{1 - 1 0 0 k _ {1} - 0 . 0 1 k _ {2}} \left[ \begin{array}{c} 1 0 0 \\ 0. 0 1 \end{array} \right] + \frac {1}{1 - 1 0 0 k _ {1} + 0 . 0 1 k _ {2}} \left[ \begin{array}{c} 1 0 0 \\ - 0. 0 1 \end{array} \right] + \frac {1}{k _ {1}} \left[ \begin{array}{c} - 1 \\ 0 \end{array} \right] \\ = \left[ \begin{array}{c} 1 0 0 (\frac {2 - 2 0 0 k _ {1}}{(1 - 1 0 0 k _ {1} - 0 . 0 1 k _ {2}) (1 - 1 0 0 k _ {1} + 0 . 0 1 k _ {2})}) - \frac {1}{k _ {1}} \\ 0. 0 1 (\frac {0 . 0 2 k _ {2}}{(1 - 1 0 0 k _ {1} - 0 . 0 1 k _ {2}) (1 - 1 0 0 k _ {1} + 0 . 0 1 k _ {2})}) \end{array} \right]. \\ \end{array}
$$

Consider two points $(k_{1}, k_{2})$ , $(k_{1}, -k_{2}) \in \mathbb{R}^{2}$ in the dual space:

$$
\| \nabla \psi (k _ {1}, k _ {2}) - \nabla \psi (k _ {1}, - k _ {2}) \| = \left\| \left[ 0. 0 1 (\frac {0}{(1 - 1 0 0 k _ {1} - 0 . 0 1 k _ {2}) (1 - 1 0 0 k _ {1} + 0 . 0 1 k _ {2})}) \right] \right\|.
$$

![](images/1073643c6c7cb4a46dc2e86fff27f882fe49d30a5e11943d1b660267d7d20f05.jpg)  
$g(x_{1})\propto \exp \left(-\frac{(t_{x_{1}} - x)^{2}}{2(1 - d)^{2}}\right)\cdot \left(\frac{1}{1 + \frac{1}{2}x^{2}}\right)^{\frac{3}{2}},t = 0.02,x = 5$   
(a) G Prior: $t \to 0$

![](images/46390c051df98bc2626013bc845039b4adf4a2d528159ca474a32e9a8c6e9dd6.jpg)  
$g(x_{1})\propto \exp \left(-\frac{(tx_{1} - x)^{2}}{2(1 - d)^{2}}\right)\cdot \left(\frac{1}{1 + \frac{1}{2}x_{1}^{2}}\right)^{\frac{3}{2}},t = 0.05,x = 5$   
(b) G Prior: small $t$

![](images/1843ccdedbe81d27f5a8f508358368326179937dcdd50bce088a5966c1abf1e3.jpg)  
$g(x_{1})\propto \exp \left(-\frac{(tx_{1} - x)^{2}}{2(1 - t)^{2}}\right)\cdot \left(\frac{1}{1 + \frac{1}{2}x_{1}^{2}}\right)^{\frac{3}{2}},t = 0.9,x = 10000$   
(c) G Prior: large $t$ , large $x$

![](images/f87bb929793c43d7319b3b245dd0ef25fab8571485a746dabf22f8842af8a169.jpg)  
$g(x_{1})\propto \frac{1}{1 + (\frac{\xi - \xi_{0}}{\xi})^{2}}\cdot (\frac{1}{1 + |x|^{2}})^{\frac{3}{2}},t = 0.02,x = 5$   
(d) t Prior: $t\to 0$

![](images/4c3c04e4b640bf5ba23019c8350a67bedc829b60844d6ca035c2800c1f0c9f4c.jpg)  
$g(x_{1})\propto \frac{1}{1 + (\frac{x - x_{0}}{x})^{2}}\cdot \left(\frac{1}{1 + \frac{1}{x}x^{2}}\right)^{3},t = 0.05,x = 5$   
(e) t Prior: small $t$

![](images/fd7c27a71bf3e238d1a80516ee2524032db190a72bf253ec9988e786a6e222ef.jpg)  
$g(x_{1})\propto \frac{1}{1 + (\frac{c - c_{0}^{2}}{c_{0}^{2}})^{2}}\cdot \left(\frac{1}{1 + \frac{1}{2}x_{1}^{2}}\right)^{\frac{3}{2}},t = 0.9,x = 10000$   
(f) t Prior: large $t$ , large $x$   
Figure 6: Illustration for Example 4. (i) Figures 6(a) and 6(d) demonstrate that in the limit $t \to 0$ , the distribution remains well-behaved and does not blow up. (ii) Figure 6(b) shows that for sufficiently large values of $x$ (here we choose a moderately large $x$ for readability), there exists a small value of $t$ such that the flow with a Gaussian prior diverges. (iii) Figure 6(e) illustrates that such divergence does not occur when using a Student- $t$ prior. (iv) Finally, Figures 6(c) and 6(f) show that as $t$ approaches 1, the Gaussian-prior flow becomes unstable, whereas the Student- $t$ prior remains stable.

Hence

$$
\begin{array}{l} \frac {\| \nabla \psi (k _ {1} , k _ {2}) - \nabla \psi (k _ {1} , - k _ {2}) \|}{\| (k _ {1} , k _ {2}) ^ {T} - (k _ {1} , - k _ {2}) ^ {T} \|} \\ = \frac {0 . 0 1 \left(\frac {0 . 0 4 k _ {2}}{\left(1 - 1 0 0 k _ {1} - 0 . 0 1 k _ {2}\right) \left(1 - 1 0 0 k _ {1} + 0 . 0 1 k _ {2}\right)}\right)}{2 k _ {2}} = 2 \times 1 0 ^ {- 4} \frac {1}{\left(1 - 1 0 0 k _ {1} - 0 . 0 1 k _ {2}\right) \left(1 - 1 0 0 k _ {1} + 0 . 0 1 k _ {2}\right)}. \\ \end{array}
$$

When $(k_{1},k_{2})\to 0$ , we have $\frac{\|\nabla\psi(k_1,k_2) - \nabla\psi(k_1, - k_2)\|}{\|(k_1,k_2)^T - (k_1, - k_2)^T\|}\to 2\times 10^{-4}.$

The above example shows that, there are cases when the polytope is "ill-shaped", and leading to a very large $L_{\psi}$ .

Proof. [Proof of Proposition 2] We have

$$
\nabla \Psi (x) = \sum_ {i = 1} ^ {m} (- \phi_ {i} (x)) ^ {- \kappa} \nabla \phi_ {i} (x) + x,
$$

$$
\nabla^ {2} \Psi (x) = \kappa \sum_ {i = 1} ^ {m} (- \phi_ {i} (x)) ^ {- \kappa - 1} \nabla \phi_ {i} (x) \nabla \phi_ {i} (x) ^ {T} + \sum_ {i = 1} ^ {m} (- \phi_ {i} (x)) ^ {- \kappa} \nabla^ {2} \phi_ {i} (x) + I.
$$

Note that $\nabla^2\phi_i(x)\succeq 0$ due to convexity of $\phi_{i}$ . So we have $\nabla^2\Psi (x)\succeq I$ . It follows that

$$
W _ {2} (\nu , \mu) \leq W _ {2, \Psi} (\nu , \mu).
$$

Furthermore, $\nabla \Psi (x) = \sum_{i = 1}^{m}(-\phi_{i}(x))^{-\kappa}\nabla \phi_{i}(x) + x$ so we know

$$
\| \nabla \Psi (x) \| \leq \| x \| + \sum_ {i = 1} ^ {m} \| (- \phi_ {i} (x)) ^ {- \kappa} \nabla \phi_ {i} (x) \| \leq \| x \| + \sum_ {i = 1} ^ {m} \frac {1}{\delta^ {\kappa}} \| \nabla \phi_ {i} (x) \|.
$$

Since we assumed $\phi_i(x)$ are of bounded gradient, we know $\| \nabla \Psi (x)\| = \frac{C'}{\delta^{\kappa}}$ for some $C^\prime$ . Denote

$$
R _ {\delta , \kappa} = \frac {C ^ {\prime}}{\delta^ {\kappa}} \geq \sup  _ {x \in \mathcal {K} _ {\delta}} \| \nabla \Psi (x) \|.
$$

Hence we know, $R_{\delta,\kappa}$ is such that $\{x \in \mathbb{R}^d : \|x\| \leq R_{\delta,\kappa}\} \supseteq \nabla \Psi(\mathcal{K}_{\delta})$ . It follows that

$$
P (\| \nabla \Psi (X) \| \geq R _ {\delta , \kappa}) \leq P (\mathcal {K} \backslash \mathcal {K} _ {\delta}) \leq C _ {\mathcal {K}} \delta^ {\beta} = \frac {C}{R _ {\delta , \kappa} ^ {\beta / \kappa}}.
$$

where note that $\frac{C}{R_{\delta,\kappa}^{\beta/\kappa}} = \frac{C}{\left(\frac{C'}{\delta^{\kappa}}\right)^{\beta/\kappa}} = C_{\mathcal{K}}\delta^{\beta}$ .

# E Proofs for section 3

We first provide some definitions related to conditional expectation in an abstract vector space. We follow the notation in Hytönen et al. (2016). Let $(S, \mathcal{A})$ be a measurable space, and $X$ a Banach space. $L^p(S; X)$ denote the linear space of all $\mu$ -measurable functions from $S$ to $X$ , with $\int_S \|f\|^p d\mu < \infty$ . When $\mathcal{F}$ is a sub- $\sigma$ -algebra of $\mathcal{A}$ , $L^p(S; \mathcal{F}; X)$ represent the $L_p$ space w.r.t. $(S, \mathcal{F}, \mu|_{\mathcal{F}})$ .

Definition 11. (Hytönen et al., 2016, Theorem 2.6.23 and Proposition 2.6.31)

If $\mu$ is $\sigma$ -finite on the sub-algebra $\mathcal{F}$ , then every $f \in L^{1}(S;X)$ admits a unique conditional expectation with respect to $\mathcal{F}$ . It satisfies

$$
\int_ {F} \mathbb {E} [ f | \mathcal {F} ] d \mu = \int_ {F} f d \mu , \forall F \in \mathcal {F}.
$$

Furthermore, let $g \in L^0(S; \mathcal{F}; X_1)$ , and that $f \in L^1(S; X_2)$ be $\sigma$ -integrable over $\mathcal{F}$ . Let $\beta : X_1 \times X_2 \to Y$ be a bounded bi-linear map. Then $\beta(g, f) \in L^0(S; Y)$ is $\sigma$ -integrable over $\mathcal{F}$ , and we have

$$
\mathbb {E} [ \beta (g, f) | \mathcal {F} ] = \beta (g, \mathbb {E} [ f | \mathcal {F} ]) \quad a. s.
$$

Proof. [Proof of Proposition 5] In primal space, the corresponding interpolation would be

$$
\frac {d}{d t} X _ {t} = \frac {d}{d t} \nabla \psi^ {*} (Z _ {t}) = \nabla^ {2} \psi^ {*} (Z _ {t}) \frac {d}{d t} Z _ {t}.
$$

Recall that the two minimization problems are:

$$
\underset {v} {\min} \mathbb {E} \left[ \| v ^ {P} (X _ {t}, t) - \frac {d}{d t} X _ {t} \| _ {g ^ {P}} ^ {2} \right] \quad \mathrm {a n d} \quad \underset {v} {\min} \mathbb {E} \left[ \| v ^ {D} (Z _ {t}, t) - \frac {d}{d t} Z _ {t} \| _ {g ^ {D}} ^ {2} \right]
$$

respectively.

Recall that $\nabla^2\psi$ evaluated at $x$ is the inverse of $\nabla^2\psi^*$ evaluated at $z = \nabla \psi (x)$ , i.e., $\nabla^2\psi (x) = (\nabla^2\psi^* (\nabla \psi (x)))^{-1}$ . Hence we obtain $\nabla^2\psi (x)\circ \nabla^2\psi^* (z)\frac{d}{dt} Z_t = \frac{d}{dt} Z_t$ . Condition on $X_{t} = x$ , we have

$$
\begin{array}{l} \left\| v ^ {P} \left(X _ {t}, t\right) - \frac {d}{d t} X _ {t} \right\| _ {g ^ {P}} ^ {2} = g ^ {P} \left(v ^ {P} \left(X _ {t}, t\right) - \frac {d}{d t} X _ {t}, v ^ {P} \left(X _ {t}, t\right) - \frac {d}{d t} X _ {t}\right) \\ = (\nabla^ {2} \psi (x)) ^ {2} \left(v ^ {P} \left(X _ {t}, t\right) - \nabla^ {2} \psi^ {*} \left(Z _ {t}\right) \frac {d}{d t} Z _ {t}, v ^ {P} \left(X _ {t}, t\right) - \nabla^ {2} \psi^ {*} \left(Z _ {t}\right) \frac {d}{d t} Z _ {t}\right) \\ = g ^ {D} \left(\nabla^ {2} \psi (x) v ^ {P} (x, t) - \frac {d}{d t} Z _ {t}, \nabla^ {2} \psi (x) v ^ {P} (x, t) - \frac {d}{d t} Z _ {t}\right) = \| \nabla^ {2} \psi (x) v ^ {P} (x, t) - \frac {d}{d t} Z _ {t} \| _ {g ^ {D}} ^ {2}. \\ \end{array}
$$

Hence we get $\| v^{P}(x,t) - \frac{d}{dt} X_{t}\|_{g^{P}}^{2} = \| \nabla^{2}\psi (x)v^{P}(x,t) - \frac{d}{dt} Z_{t}\|_{g^{D}}^{2}$ or equivalently $\| v^{D}(z,t) - \frac{d}{dt} Z_t\| _g^2 = \| \nabla^2\psi^* (z)v^D (z,t) - \frac{d}{dt} X_t\| _g^2$ . So we get

$$
v ^ {D} (z, t) = \nabla^ {2} \psi (x) v ^ {P} (x, t), \quad v ^ {P} (x, t) = \nabla^ {2} \psi^ {*} (z) v ^ {D} (z, t).
$$

The equivalence follows from the change of variable formula.

Now we show the last claim. Now consider $\mathcal{G}$ to be the sigma algebra corresponding to $X_{t} = x$ . Note that each tangent space $T_{x}M$ is a Hilbert space, with Riemannian metric $g$ . Then for any $Y$ (that is measurable in $\mathcal{G}$ ), we have

$$
\begin{array}{l} \mathbb {E} [ \| \frac {d}{d t} X _ {t} - Y \| _ {g (x)} ^ {2} ] = \mathbb {E} [ \| \frac {d}{d t} X _ {t} - \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ] + \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ] - Y \| _ {g (x)} ^ {2} ] \\ = \mathbb {E} [ \| \frac {d}{d t} X _ {t} - \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ] \| _ {g (x)} ^ {2} ] + \mathbb {E} [ \| \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ] - Y \| _ {g (x)} ^ {2} ] \\ + 2 \mathbb {E} [ \left\langle \frac {d}{d t} X _ {t} - \mathbb {E} \left[ \frac {d}{d t} X _ {t} \right| X _ {t} = x \right], \mathbb {E} \left[ \frac {d}{d t} X _ {t} \mid X _ {t} = x \right] - Y \rangle ]. \\ \end{array}
$$

Since $f \coloneqq \mathbb{E}\left[\frac{d}{dt} X_t|X_t = x\right] - Y$ is measurable in $\mathcal{G}$ , we have

$$
\begin{array}{l} \mathbb {E} [ \langle \frac {d}{d t} X _ {t} - \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ], f \rangle ] = \mathbb {E} [ \langle \frac {d}{d t} X _ {t}, f \rangle ] - \mathbb {E} [ \langle \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ], f \rangle ] \\ = \mathbb {E} [ \langle \frac {d}{d t} X _ {t}, f \rangle ] - \langle \mathbb {E} [ \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ] ], f \rangle = 0. \\ \end{array}
$$

where the last equality is by tower property (Hytönen et al., 2016, Proposition 2.6.33).

Hence we get

$$
\begin{array}{l} \mathbb {E} [ \| \frac {d}{d t} X _ {t} - Y \| _ {g (x)} ^ {2} ] = \mathbb {E} [ \| \frac {d}{d t} X _ {t} - \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ] \| _ {g (x)} ^ {2} ] + \mathbb {E} [ \| \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ] - Y \| _ {g (x)} ^ {2} ] \\ \geq \mathbb {E} [ \| \frac {d}{d t} X _ {t} - \mathbb {E} [ \frac {d}{d t} X _ {t} | X _ {t} = x ] \| _ {g (x)} ^ {2} ], \forall Y \in \mathcal {G}. \\ \end{array}
$$

It follows that among all $Y$ being measurable in $\mathcal{G}$ , the choice $Y = \mathbb{E}[\frac{d}{dt} X_t|X_t = x]$ minimizes the problem. Hence $v^{P}(x,t) = \mathbb{E}[\frac{d}{dt} X_{t}|X_{t} = x]$ .

# F Proofs for Section 4

We start with several intermediate results. Define $p_{t,x}(z_1) = \frac{(1 + \frac{1}{\nu}\| \frac{x - tz_1}{1 - t} \|^2)^{-\frac{\nu + d}{2}} p(z_1)}{\int_{\mathbb{R}^d} (1 + \frac{1}{\nu}\| \frac{x - tz}{1 - t} \|^2)^{-\frac{\nu + d}{2}} p(z) dz}$ . Throughout this section, to make the notation compatible with $p_{t,x}(z_1)$ , we use $p$ to denote the probability density function of the data distribution, supported on Euclidean space.

Proposition 12. Under Assumption 3 with $\alpha \geq 2d + \nu + 2$ , there exists a constant $B$ that doesn't depend on $t, x$ s.t. for all $t \in [0, T]$ ,

$$
\mathbb {E} _ {p _ {t, x} (z _ {1})} [ \| z _ {1} \| ^ {2} ] \leq \frac {B}{(1 - T) ^ {\nu + d}}.
$$

In other words, we have that, for all $T \in (0,1)$ , there exists $B_{1}, B_{2}$ independent of $x$ , so that

$$
\sup _ {t \in [ 0, T ]} \mathbb {E} _ {p _ {t, x}} [ \| z _ {1} \| ] \leq B _ {1}, \forall x,
$$

$$
\sup  _ {t \in [ 0, T ]} \mathbb {E} _ {p _ {t, x}} [ \| z _ {1} \| ^ {2} ] \leq B _ {2}, \forall x.
$$

# Proof. [Proof of Proposition 12]

To derive the desired upper bound, we aim to upper bound $p_{t,x}(z_1)$ . We first derive a lower bound on the normalizing constant:

$$
\begin{array}{l} \int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z _ {1}) d z _ {1} \\ = \int_ {\mathbb {R} ^ {d}} (\frac {(\frac {1 - t}{t}) ^ {2}}{(\frac {1 - t}{t}) ^ {2} + \frac {1}{\nu} \| \frac {x}{t} - z _ {1} \| ^ {2}}) ^ {\frac {\nu + d}{2}} p (z _ {1}) d z _ {1} \geq \int_ {\| z _ {1} \| \leq R} (\frac {(\frac {1 - t}{t}) ^ {2}}{(\frac {1 - t}{t}) ^ {2} + \frac {1}{\nu} \| \frac {x}{t} - z _ {1} \| ^ {2}}) ^ {\frac {\nu + d}{2}} p (z _ {1}) d z _ {1} \\ \geq \left(\frac {\left(\frac {1 - t}{t}\right) ^ {2}}{\left(\frac {1 - t}{t}\right) ^ {2} + \frac {1}{\nu} \left(\frac {\| x \|}{t} + R\right) ^ {2}}\right) ^ {\frac {\nu + d}{2}} \left(1 - \frac {C ^ {\prime}}{R ^ {\beta}}\right) \geq \left(\frac {\left(\frac {1 - t}{t}\right) ^ {2}}{\left(\frac {1 - t}{t}\right) ^ {2} + \frac {1}{\nu} \frac {2 \| x \| ^ {2}}{t ^ {2}}}\right) ^ {\frac {\nu + d}{2}} \frac {1}{2} \\ = \frac {1}{2} \left(\frac {(1 - t) ^ {2}}{(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}}\right) ^ {\frac {\nu + d}{2}}. \\ \end{array}
$$

We will split $\mathbb{R}^d$ into different regions, and derive upper bounds of $p_{t,x}(z_1)$ for each of them.

1. Region 1 $\| \frac{x}{t} - z_1 \| \leq \frac{\|x\|}{2t}$ .

$$
\begin{array}{l} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z _ {1}) \\ = \frac {1}{\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {\frac {\nu + d}{2}}} p (z _ {1}) \leq \frac {1}{\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {\frac {\nu + d}{2}}} (\frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}) ^ {\frac {\nu + d}{2}} \\ = \big (\frac {1}{(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2})} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}} \big) ^ {\frac {\nu + d}{2}} = \big (\frac {(\frac {1 - t}{t}) ^ {2}}{((\frac {1 - t}{t}) ^ {2} + \frac {1}{\nu} \| \frac {x}{t} - z _ {1} \| ^ {2})} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}} \big) ^ {\frac {\nu + d}{2}} \\ \leq \left(\frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}\right) ^ {\frac {\nu + d}{2}}. \\ \end{array}
$$

Hence

$$
\begin{array}{l} p _ {t, x} (z _ {1}) = \frac {(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z) d z} \leq 2 (\frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}) ^ {\frac {\nu + d}{2}} (\frac {(1 - t) ^ {2}}{(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}}) ^ {- \frac {\nu + d}{2}} \\ = 2 (\frac {(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}}{(1 - t) ^ {2}} \frac {C _ {\nu + d} ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| _ {\nu + d} ^ {\frac {2 \alpha}{\nu + d}}}) ^ {\frac {\nu + d}{2}}. \\ \end{array}
$$

When $\| \frac{x}{t} - z_1 \| \leq \frac{\|x\|}{2t}$ ,

$$
\begin{array}{l} \int_ {B _ {x} (R)} \| z _ {1} \| ^ {2} p _ {t, x} (z _ {1}) d z _ {1} \leq 2 \int_ {B _ {\frac {x}{t}} (R = \frac {\| x \|}{2 t})} \| z _ {1} \| ^ {2} (\frac {(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}}{(1 - t) ^ {2}} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}) ^ {\frac {\nu + d}{2}} d z _ {1} \\ \leq 2 \mathrm {V o l} (B _ {\frac {x}{t}} (R = \frac {\| x \|}{2 t})) \sup _ {B _ {\frac {x}{t}} (R = \frac {\| x \|}{2 t})} \| z _ {1} \| ^ {2} (\frac {(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}}{(1 - t) ^ {2}} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}) ^ {\frac {\nu + d}{2}} \\ \leq 2 C _ {B} (\frac {\| x \|}{t}) ^ {d} \sup _ {B _ {\frac {x}{t}} (R = \frac {\| x \|}{2 t})} (\frac {\frac {3}{\nu} \| x \| ^ {2}}{(1 - T) ^ {2}} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha - 4}{\nu + d}}}) ^ {\frac {\nu + d}{2}} \\ \leq 2 C _ {B} \| x \| ^ {d} \frac {1}{t ^ {d}} \sup _ {B _ {\frac {x}{t}} (R = \frac {\| x \|}{2 t})} \left(\frac {\frac {3}{\nu}}{(1 - T) ^ {2} \| x \| ^ {- 2}} \frac {C ^ {\frac {2}{\nu + d}}}{\| \frac {x}{2 t} \| ^ {\frac {2 \alpha - 4}{\nu + d}}}\right) ^ {\frac {\nu + d}{2}} \\ \leq 2 C _ {B} \| x \| ^ {d} \frac {1}{t ^ {d}} \left(\frac {\frac {3}{\nu} C ^ {\frac {2}{\nu + d}} (2 t) ^ {\frac {2 \alpha - 4}{\nu + d}}}{(1 - T) ^ {2} \| x \| ^ {\frac {2 \alpha - 4 - 2 \nu - 2 d}{\nu + d}}}\right) ^ {\frac {\nu + d}{2}} \\ = \| x \| ^ {2 d + \nu + 2 - \alpha} t ^ {\alpha - 2 - d} \frac {1}{(1 - T) ^ {\nu + d}} \left(2 C _ {B} 2 ^ {\alpha - 2} C \left(\frac {3}{\nu}\right) ^ {\frac {\nu + d}{2}}\right), \\ \end{array}
$$

where observe that $\frac{2\alpha - 4}{\nu + d} - 2 = \frac{2\alpha - 4 - 2\nu - 2d}{\nu + d}$ and

$$
\| x \| ^ {d} \left(\frac {1}{\| x \| ^ {\frac {2 \alpha - 4 - 2 \nu - 2 d}{\nu + d}}}\right) ^ {\frac {\nu + d}{2}} = \| x \| ^ {d} \| x \| ^ {- \frac {2 \alpha - 4 - 2 \nu - 2 d}{\nu + d} \frac {\nu + d}{2}} = \| x \| ^ {d - (\alpha - 2 - \nu - d)} = \| x \| ^ {2 d + \nu + 2 - \alpha}.
$$

To control the second moment so that it doesn't explode with $\| x\|$ , we need $\alpha \geq 2d + \nu +2$

2. Region 2 $\| \frac{x}{t} - z_1 \| \geq \frac{1}{2t} \| x \|$ and $\| z_1 \| \geq 1$

For this case, we can have a sharper upper bound on $p_{t,x}(z_1)$ .

$$
\begin{array}{l} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z _ {1}) \\ = \frac {1}{\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {\frac {\nu + d}{2}}} p (z _ {1}) \leq \frac {1}{\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {\frac {\nu + d}{2}}} \left(\frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}\right) ^ {\frac {\nu + d}{2}} \\ = (\frac {1}{(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2})} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}) ^ {\frac {\nu + d}{2}} = (\frac {(\frac {1 - t}{t}) ^ {2}}{((\frac {1 - t}{t}) ^ {2} + \frac {1}{\nu} \| \frac {x}{t} - z _ {1} \| ^ {2})} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}) ^ {\frac {\nu + d}{2}} \\ \leq \bigl (\frac {(\frac {1 - t}{t}) ^ {2}}{((\frac {1 - t}{t}) ^ {2} + \frac {1}{4 t ^ {2} \nu} \| x \| ^ {2})} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}} \bigr) ^ {\frac {\nu + d}{2}} = \bigl (\frac {(1 - t) ^ {2}}{((1 - t) ^ {2} + \frac {1}{4 \nu} \| x \| ^ {2})} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}} \bigr) ^ {\frac {\nu + d}{2}}. \\ \end{array}
$$

Hence

$$
\begin{array}{l} p _ {t, x} (z _ {1}) = \frac {\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z} \\ \leq 2 \left(\frac {(1 - t) ^ {2}}{\left((1 - t) ^ {2} + \frac {1}{4 \nu} \| x \| ^ {2}\right)} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}}\right) ^ {\frac {\nu + d}{2}} \left(\frac {(1 - t) ^ {2}}{(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}}\right) ^ {- \frac {\nu + d}{2}} \\ \end{array}
$$

$$
= 2 \big (\frac {(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}}{(1 - t) ^ {2} + \frac {1}{4 \nu} \| x \| ^ {2}} \frac {C ^ {\frac {2}{\nu + d}}}{\| z _ {1} \| ^ {\frac {2 \alpha}{\nu + d}}} \big) ^ {\frac {\nu + d}{2}}.
$$

We see that for $\| \frac{x}{t} - z_1 \| \geq \frac{1}{2t} \| x \|$ , $p_{t,x}(z_1)$ has a polynomial tail bound that doesn't depend on $x, t$ . Thus $\int_{\| \frac{x}{t} - z_1 \| \geq \frac{1}{2t} \| x \|$ and $\| z_1 \| \geq 1 \| z_1 \|^2 p_{t,x}(z_1) dz_1$ can be bounded by some constant that doesn't depend on $x, t$ :

$$
\int_ {\| \frac {x}{t} - z _ {1} \| \geq \frac {1}{2 t} \| x \| \text {a n d} \| z _ {1} \| \geq 1} \| z _ {1} \| ^ {2} p _ {t, x} (z _ {1}) d z _ {1} \leq C ^ {\prime} \int_ {\| z _ {1} \| \geq 1} \frac {1}{\| z _ {1} \| ^ {\alpha - 2}} d z _ {1}.
$$

The convergence of the integral is equivalent to the convergence of $\int_{1}^{\infty}r^{d - \alpha +2}$ . When $\alpha \geq 2d + \nu +2$ , it converges.

3. Region 3 $\| \frac{x}{t} - z_1 \| \geq \frac{1}{2t} \| x \|$ and $\| z_1 \| \leq 1$

$$
\begin{array}{l} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z _ {1}) \\ = \frac {1}{\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {\frac {\nu + d}{2}}} p (z _ {1}) \leq \frac {1}{\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {\frac {\nu + d}{2}}} \left(C _ {u} ^ {\frac {2}{\nu + d}}\right) ^ {\frac {\nu + d}{2}} \\ = (\frac {1}{(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2})} C _ {u} ^ {\frac {2}{\nu + d}}) ^ {\frac {\nu + d}{2}} = (\frac {(\frac {1 - t}{t}) ^ {2}}{((\frac {1 - t}{t}) ^ {2} + \frac {1}{\nu} \| \frac {x}{t} - z _ {1} \| ^ {2})} C _ {u} ^ {\frac {2}{\nu + d}}) ^ {\frac {\nu + d}{2}} \\ \leq \left(\frac {(\frac {1 - t}{t}) ^ {2}}{((\frac {1 - t}{t}) ^ {2} + \frac {1}{4 t ^ {2} \nu} \| x \| ^ {2})} C _ {u} ^ {\frac {2}{\nu + d}}\right) ^ {\frac {\nu + d}{2}} = \left(\frac {(1 - t) ^ {2}}{((1 - t) ^ {2} + \frac {1}{4 \nu} \| x \| ^ {2})} C _ {u} ^ {\frac {2}{\nu + d}}\right) ^ {\frac {\nu + d}{2}}. \\ \end{array}
$$

Hence

$$
\begin{array}{l} p _ {t, x} (z _ {1}) = \frac {\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z} \\ \leq 2 \big (\frac {(1 - t) ^ {2}}{((1 - t) ^ {2} + \frac {1}{4 \nu} \| x \| ^ {2})} C _ {u} ^ {\frac {2}{\nu + d}} \big) ^ {\frac {\nu + d}{2}} \big (\frac {(1 - t) ^ {2}}{(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}} \big) ^ {- \frac {\nu + d}{2}} \\ = 2 \left(\frac {(1 - t) ^ {2} + \frac {2}{\nu} \| x \| ^ {2}}{(1 - t) ^ {2} + \frac {1}{4 \nu} \| x \| ^ {2}} C _ {u} ^ {\frac {2}{\nu + d}}\right) ^ {\frac {\nu + d}{2}}. \\ \end{array}
$$

We see that for this case, when restricting $\| z_1 \| \leq 1$ , $p_{t,x}(z_1)$ has a constant upper bound that doesn't depend on $x, t$ . Thus $\int_{\| \frac{x}{t} - z_1 \| \geq \frac{1}{2t} \| x \|$ and $\| z_1 \| \leq 1$ $\| z_1 \|^2 p_{t,x}(z_1) dz_1$ can be bounded by some constant that doesn't depend on $x, t$ .

![](images/8dc49a0d6cae74dc9f11d0977f06a36dbc9d72994c6257a3efd7f0b665afd0d7.jpg)

With the above Proposition, we can prove Lemma 13 and 14, which are the key ingredients in proving the Lipschitzness of $v$ .

Lemma 13. Under Assumption 3, we have

$$
\| \nabla_ {x} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] \| \leq \frac {\nu + d}{\nu} \frac {2 \sqrt {\nu}}{1 - t} \mathbb {E} _ {p _ {t} (z _ {1} | x)} [ \| z _ {1} \| ] \leq \frac {\nu + d}{\nu} \frac {2 \sqrt {\nu}}{1 - T} B _ {1}, \forall t \in [ 0, T ].
$$

Proof. [Proof of Lemma 13]

$$
\begin{array}{l} \nabla_ {x} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] = \nabla_ {x} \frac {\int_ {\mathbb {R} ^ {d}} z _ {1} (1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z _ {1}) d z _ {1}}{\int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z) d z} \\ = \int_ {\mathbb {R} ^ {d}} z _ {1} \nabla_ {x} \frac {\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z} d z _ {1} \\ = \int_ {\mathbb {R} ^ {d}} z _ {1} \left(\nabla_ {x} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}}\right) ^ {T} \frac {p (z _ {1}) \int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z}{\left(\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {2}} d z _ {1} \\ - \int_ {\mathbb {R} ^ {d}} z _ {1} \left(\nabla_ {x} \int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {T} \frac {(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\left(\int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {2}} d z _ {1}. \\ \end{array}
$$

Observe that

$$
\begin{array}{l} \nabla_ {x} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} \\ = - \frac {\nu + d}{2} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2} - 1} \left(\nabla_ {x} \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) \\ = - \frac {\nu + d}{2} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2} - 1} \frac {1}{\nu} \left(2 \frac {x - t z _ {1}}{1 - t}\right) \frac {1}{1 - t} \\ = - \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} \left(\frac {x - t z _ {1}}{1 - t}\right) \frac {1}{1 - t}. \\ \end{array}
$$

Hence

$$
\begin{array}{l} \nabla_ {x} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] = - \int_ {\mathbb {R} ^ {d}} z _ {1} \left((1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} (\frac {x - t z _ {1}}{1 - t}) \frac {1}{1 - t}\right) ^ {T} \\ \frac {p \left(z _ {1}\right) \int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z}{\left(\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {2}} d z _ {1} \\ + \int_ {\mathbb {R} ^ {d}} z _ {1} \left(\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}} (\frac {x - t z}{1 - t}) \frac {1}{1 - t} p (z) d z\right) ^ {T} \\ \frac {\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\left(\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {2}} d z _ {1}. \\ \end{array}
$$

Recall that we use the notation $p_{t,x}(z_1) = \frac{(1 + \frac{1}{\nu}\| \frac{x - tz_1}{1 - t} \|^2)^{-\frac{\nu + d}{2}} p(z_1)}{\int_{\mathbb{R}^d} (1 + \frac{1}{\nu}\| \frac{x - tz}{1 - t} \|^2)^{-\frac{\nu + d}{2}} p(z) dz}$ .

$$
\begin{array}{l} \nabla_ {x} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] = - \int_ {\mathbb {R} ^ {d}} z _ {1} \left(\frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} (\frac {x - t z _ {1}}{1 - t}) \frac {1}{1 - t}\right) ^ {T} p _ {t, x} (z _ {1}) d z _ {1} \\ + \int_ {\mathbb {R} ^ {d}} z _ {1} p _ {t, x} (z _ {1}) d z _ {1} \left(\int_ {\mathbb {R} ^ {d}} \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}} (\frac {x - t z}{1 - t}) \frac {1}{1 - t} p (z | x) d z\right) ^ {T}. \\ \end{array}
$$

In general, we have $\mathbb{E}[XY^T] - \mathbb{E}[X]\mathbb{E}[Y]^T = \mathbb{E}[(X - \mathbb{E}[X])(Y - \mathbb{E}[Y])^T]$ . Let $X = z_{1}$ and $Y = \frac{\nu + d}{\nu}\frac{1}{1 + \frac{1}{\nu}\|\frac{x - tz_1}{1 - t}\|^2}\left(\frac{x - tz_1}{1 - t}\right)\frac{1}{1 - t}$ . To bound $\nabla_x\mathbb{E}[Z_1|Z_t = x]$ , we consider any unit vector $v$ :

$$
\begin{array}{l} v ^ {T} \nabla_ {x} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] v = \mathbb {E} [ v ^ {T} (X - \mathbb {E} [ X ]) \cdot v ^ {T} (Y - \mathbb {E} [ Y ]) ] \leq \mathbb {E} [ \| X - \mathbb {E} [ X ] \| \cdot \| Y - \mathbb {E} [ Y ] \| ] \\ \leq \mathbb {E} [ (\| X \| + \| \mathbb {E} [ X ] \|) (\| Y \| + \| \mathbb {E} [ Y ] \|) ] \leq \mathbb {E} [ \| X \| \| Y \| ] + 3 \mathbb {E} [ \| X \| ] \mathbb {E} [ \| Y \| ]. \\ \end{array}
$$

We have

$$
\| Y \| = \frac {\nu + d}{\nu (1 - t) ^ {2}} \frac {\| x - t z _ {1} \|}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} = \frac {\nu + d}{\nu} \frac {\| x - t z _ {1} \|}{(1 - t) ^ {2} + \frac {1}{\nu} \| x - t z _ {1} \| ^ {2}}.
$$

At $(1 - t)^{2} = \frac{1}{\nu}\| x - tz_{1}\|^{2},\| Y\|$ reach maximum,

$$
\sup  _ {z _ {1}} \| Y \| = \frac {\nu + d}{\nu} \frac {\sqrt {\nu}}{2 (1 - t)}.
$$

Therefore

$$
\| \nabla_ {x} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] \| \leq \frac {\nu + d}{\nu} \frac {2 \sqrt {\nu}}{1 - t} \mathbb {E} _ {p _ {t} (z _ {1} | x)} [ \| z _ {1} \| ].
$$

![](images/f5bc3fbe12f0669c1bbb6417d81a903c4a3f0468887535c6a96de8502279bb42.jpg)

Lemma 14. Under Assumption 3 with $\alpha \geq 2d + \nu + 2$ , we have

$$
\| \frac {\partial}{\partial t} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] \| \leq \frac {\nu + d}{\nu} \frac {3 \sqrt {\nu}}{2 (1 - t) ^ {2}} \left(\mathbb {E} [ \| z _ {1} \| ^ {2} ] + 3 \mathbb {E} [ \| z _ {1} \| ] ^ {2}\right) \leq \frac {\nu + d}{\nu} \frac {3 \sqrt {\nu}}{2 (1 - T) ^ {2}} \left(B _ {2} + 3 B _ {1} ^ {2}\right), \forall t \in [ 0, T ].
$$

Proof. [Proof of Lemma 14]

$$
\begin{array}{l} \frac {\partial}{\partial t} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] = \frac {\partial}{\partial t} \frac {\int_ {\mathbb {R} ^ {d}} z _ {1} (1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z _ {1}) d z _ {1}}{\int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z) d z} \\ = \int_ {\mathbb {R} ^ {d}} z _ {1} \nabla_ {x} \frac {\left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z} d z _ {1} \\ = \int_ {\mathbb {R} ^ {d}} z _ {1} \left(\frac {\partial}{\partial t} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}}\right) \frac {p (z _ {1}) \int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z}{\left(\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {2}} d z _ {1} \\ - \int_ {\mathbb {R} ^ {d}} z _ {1} \left(\frac {\partial}{\partial t} \int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z) d z\right) \frac {(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\left(\int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {2}} d z _ {1}. \\ \end{array}
$$

Observe that

$$
\begin{array}{l} \frac {\partial}{\partial t} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} \\ = - \frac {\nu + d}{2} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2} - 1} \left(\frac {1}{\nu} \frac {\partial}{\partial t} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) \\ = - \frac {\nu + d}{2} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2} - 1} \frac {1}{\nu} \left(2 \frac {x - t z _ {1}}{1 - t}\right) ^ {T} \frac {x - z _ {1}}{(1 - t) ^ {2}} \\ \end{array}
$$

$$
= - \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} \frac {1}{(1 - t) ^ {3}} (\| x \| ^ {2} - z _ {1} ^ {T} x (1 + t) + t \| z _ {1} \| ^ {2}).
$$

Hence

$$
\nabla_ {x} \mathbb {E} [ Z _ {1} | Z _ {t} = x ]
$$

$$
= \int_ {\mathbb {R} ^ {d}} z _ {1} \left((1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} \frac {1}{(1 - t) ^ {3}} (\| x \| ^ {2} - z _ {1} ^ {T} x (1 + t) + t \| z _ {1} \| ^ {2})\right)
$$

$$
\begin{array}{l} \frac {p (z _ {1}) \int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z}{\left(\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {2}} d z _ {1} \\ \left. - \int_ {\mathbb {R} ^ {d}} z _ {1} \left(\int_ {\mathbb {R} ^ {d}} \left(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}\right) ^ {- \frac {\nu + d}{2}} \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} \frac {1}{(1 - t) ^ {3}} (\| x \| ^ {2} - z _ {1} ^ {T} x (1 + t) + t \| z _ {1} \| ^ {2}) p (z) d z\right) \right. \\ \end{array}
$$

$$
\frac {(1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z _ {1})}{\left(\int_ {\mathbb {R} ^ {d}} (1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}) ^ {- \frac {\nu + d}{2}} p (z) d z\right) ^ {2}} d z _ {1}.
$$

Define $p_{t,x}(z_1) = \frac{(1 + \frac{1}{\nu}\| \frac{x - tz_1}{1 - t} \|^2)^{-\frac{\nu + d}{2}} p(z_1)}{\int_{\mathbb{R}^d}(1 + \frac{1}{\nu}\| \frac{x - tz}{1 - t} \|^2)^{-\frac{\nu + d}{2}} p(z) dz}$ .

$$
\begin{array}{l} \frac {\partial}{\partial t} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] \\ = \int_ {\mathbb {R} ^ {d}} z _ {1} \left(\frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} \frac {1}{(1 - t) ^ {3}} \left(\| x \| ^ {2} - z _ {1} ^ {T} x (1 + t) + t \| z _ {1} \| ^ {2}\right)\right) p _ {t, x} (z _ {1}) d z _ {1} \\ - \int_ {\mathbb {R} ^ {d}} z _ {1} p _ {t, x} (z _ {1}) d z _ {1} \left(\int_ {\mathbb {R} ^ {d}} \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z}{1 - t} \| ^ {2}} \frac {1}{(1 - t) ^ {3}} (\| x \| ^ {2} - z ^ {T} x (1 + t) + t \| z \| ^ {2}) p (z | x) d z\right). \\ \end{array}
$$

Define $X = z_{1},Y = \frac{\nu + d}{\nu}\frac{1}{1 + \frac{1}{\nu}\| \frac{x - tz_{1}}{1 - t}\|^{2}}\frac{1}{(1 - t)^{3}} (\| x\|^{2} - z_{1}^{T}x(1 + t) + t\| z_{1}\|^{2})$ Note that

$$
\begin{array}{l} \| Y \| = \| \frac {\nu + d}{\nu} \frac {1}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} \frac {1}{(1 - t) ^ {3}} (x - t z _ {1}) ^ {T} (x - z _ {1}) \| \\ \leq \frac {\nu + d}{\nu (1 - t) ^ {3}} \frac {\| x - t z _ {1} \| \| x - z _ {1} \|}{1 + \frac {1}{\nu} \| \frac {x - t z _ {1}}{1 - t} \| ^ {2}} = \frac {\nu + d}{\nu} \frac {1}{1 - t} \frac {\| x - t z _ {1} \| \| x - z _ {1} \|}{(1 - t) ^ {2} + \frac {1}{\nu} \| x - t z _ {1} \| ^ {2}} \leq \frac {\nu + d}{\nu} \| z _ {1} \|. \\ \end{array}
$$

where observe that if $\| z_1 \| \leq \frac{1}{2} \| x \|$ , we have $\| x - z_1 \| \leq 2 \| x - tz_1 \|$ . Then $\| Y \| \leq \frac{\nu + d}{\nu^2} \frac{1}{1 - t}$ . If $\| z_1 \| \geq \frac{1}{2} \| x \|$ ,

$$
\| Y \| \leq \frac {\nu + d}{\nu} \frac {\sqrt {\nu}}{2 (1 - t)} \frac {1}{1 - t} \| x - z _ {1} \| \leq \frac {\nu + d}{\nu} \frac {\sqrt {\nu}}{2} \frac {1}{(1 - t) ^ {2}} (\| x \| + \| z _ {1} \|) \leq \| z _ {1} \| \frac {\nu + d}{\nu} \frac {3 \sqrt {\nu}}{2} \frac {1}{(1 - t) ^ {2}}.
$$

Recall: $\mathbb{E}[XY] - \mathbb{E}[X]\mathbb{E}[Y] = \mathbb{E}[(X - \mathbb{E}[X])(Y - \mathbb{E}[Y])]$ . Therefore

$$
\begin{array}{l} \| \frac {\partial}{\partial t} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] \| \leq \mathbb {E} [ v ^ {T} (X - \mathbb {E} [ X ]) (Y - \mathbb {E} [ Y ]) ] \leq \mathbb {E} [ \| X - \mathbb {E} [ X ] \| \cdot \| Y - \mathbb {E} [ Y ] \| ] \\ \leq \mathbb {E} [ (\| X \| + \| \mathbb {E} [ X ] \|) (\| Y \| + \| \mathbb {E} [ Y ] \|) ] \leq \mathbb {E} [ \| X \| \| Y \| ] + 3 \mathbb {E} [ \| X \| ] \mathbb {E} [ \| Y \| ] \\ \leq \frac {\nu + d}{\nu} \frac {3 \sqrt {\nu}}{2} \frac {1}{(1 - t) ^ {2}} \left(\mathbb {E} [ \| z _ {1} \| ^ {2} ] + 3 \mathbb {E} [ \| z _ {1} \| ] ^ {2}\right). \\ \end{array}
$$

The following Lemma will be used when analyzing the discretization error.

Lemma 15. Under Assumption 3 with $\alpha \geq 2d + \nu + 2$ and Assumption 2, there exists $D_3$ that depends polynomially in $\frac{1}{1 - T}$ , $d$ , $\nu$ and $B_1, B_2, \mathbb{E}[\| Z_1\|^2]$ , $\mathbb{E}[\| Z_0\|^2]$ s.t.

$$
\mathbb {E} [ \| v (Z _ {t}, t) - v (Z _ {t _ {i}}, t _ {i}) \| ^ {2} ] \leq h ^ {2} D _ {3}.
$$

Proof. [Proof of Lemma 15]

By chain rule,

$$
\frac {d}{d t} v (Z _ {t}, t) = \frac {\partial}{\partial t} v (Z _ {t}, t) + \frac {\partial}{\partial x} v (Z _ {t}, t) \circ \frac {\partial}{\partial t} Z _ {t},
$$

and therefore (note that $\frac{\partial}{\partial t} Z_t = v(Z_t, t)$ )

$$
\| \frac {d}{d t} v (Z _ {t}, t) \| \leq \| \frac {\partial}{\partial t} v (Z _ {t}, t) \| + \| \frac {\partial}{\partial x} v (Z _ {t}, t) \| \cdot \| v (Z _ {t}, t) \|.
$$

Recall

$$
\| \frac {\partial}{\partial t} v (x, t) \| \leq \frac {1}{(1 - T) ^ {2}} \| x \| + \frac {1}{(1 - T) ^ {2}} B _ {1} + \frac {1}{1 - T} \frac {\nu + d}{\nu} \frac {3 \sqrt {\nu}}{2 (1 - T) ^ {2}} \left(B _ {2} + 3 B _ {1} ^ {2}\right), \forall t \in [ 0, T ]
$$

$$
\| \nabla_ {x} v (x, t) \| \leq \frac {1}{1 - T} + \frac {\nu + d}{\nu} \frac {2 \sqrt {\nu}}{(1 - T) ^ {2}} B _ {1}, \forall t \in [ 0, T ].
$$

and

$$
\begin{array}{l} \| v (x, t) \| = \| - \frac {1}{1 - t} x + \frac {1}{1 - t} \mathbb {E} [ Z _ {1} | Z _ {t} = x ] \| \leq \frac {1}{1 - T} (\| x \| + \| \mathbb {E} [ Z _ {1} | Z _ {t} = x ] \|) \\ \leq \frac {1}{1 - T} (\| x \| + \mathbb {E} [ \| Z _ {1} \| | Z _ {t} = x ]) = \frac {1}{1 - T} (\| x \| + B _ {1}). \\ \end{array}
$$

Hence we have

$$
\begin{array}{l} \| \frac {d}{d t} v (Z _ {t}, t) \| \leq \frac {1}{(1 - T) ^ {2}} \| Z _ {t} \| + \frac {1}{(1 - T) ^ {2}} B _ {1} + \frac {1}{1 - T} \frac {\nu + d}{\nu} \frac {3 \sqrt {\nu}}{2 (1 - T) ^ {2}} \left(B _ {2} + 3 B _ {1} ^ {2}\right) \\ + \left(\frac {1}{1 - T} + \frac {\nu + d}{\nu} \frac {2 \sqrt {\nu}}{(1 - T) ^ {2}} B _ {1}\right) \cdot \frac {1}{1 - T} (\| Z _ {t} \| + B _ {1}) \forall t \in [ 0, T ]. \\ \end{array}
$$

It follows that there exists $D_{1}, D_{2}$ (that depends polynomially in $\frac{1}{1 - T}, d, \nu, B_{1}, B_{2}$ ) s.t.

$$
\| \frac {d}{d t} v (Z _ {t}, t) \| ^ {2} \leq D _ {1} \| Z _ {t} \| ^ {2} + D _ {2}, \forall t \in [ 0, T ].
$$

Recall that $\operatorname{Law}(Z_t) = \operatorname{Law}(tZ_1 + (1 - t)Z_0)$ . Hence

$$
\begin{array}{l} \mathbb {E} [ \| Z _ {t} \| ^ {2} ] = \mathbb {E} [ \| t Z _ {1} + (1 - t) Z _ {0} \| ^ {2} ] = t ^ {2} \mathbb {E} [ \| Z _ {1} \| \| ^ {2} ] + (1 - t) ^ {2} \mathbb {E} [ \| Z _ {0} \| ^ {2} ] + 2 t (1 - t) \mathbb {E} [ Z _ {0} ^ {T} Z _ {1} ] \\ \leq 2 \mathbb {E} [ \| Z _ {1} \| \| ^ {2} ] + 2 \mathbb {E} [ \| Z _ {0} \| ^ {2} ]. \\ \end{array}
$$

which implies there exists $D_{3}$ (that depends polynomially in $\frac{1}{1 - T},d,\nu ,B_1,B_2,\mathbb{E}[\| Z_1\| \| ^2 ],\mathbb{E}[\| Z_0\| \| ^2 ]$ ) s.t.

$$
\mathbb {E} [ \| \frac {d}{d t} v (Z _ {t}, t) \| ^ {2} ] \leq D _ {3}.
$$

By Jensen's inequality,

$$
\begin{array}{l} \mathbb {E} [ \| v (Z _ {t}, t) - v (Z _ {t _ {i}}, t _ {i}) \| ^ {2} ] = \mathbb {E} [ \| \int_ {t _ {i}} ^ {t} \left(\frac {d}{d s} v (Z _ {s}, s)\right) d s \| ^ {2} ] \leq (t - t _ {i}) \mathbb {E} [ \int_ {t _ {i}} ^ {t} \left\| \frac {d}{d s} v (Z _ {s}, s) \right\| ^ {2} d s ] \\ \leq h ^ {2} \mathbb {E} [ \| \frac {d}{d t} v (Z _ {t}, t) \| ^ {2} ] \leq h ^ {2} D _ {3}. \\ \end{array}
$$

![](images/25ab4c01eaa28dc8ed2c69ba44466b99050a3928c7ddf6cf3514c24fa689c7e5.jpg)

# F.1 Proof of Proposition 6

Proof. [Proof of Proposition 6] Using Lemma 13,

$$
\begin{array}{l} \left\| \nabla_ {x} v (z, t) \right\| = \| - \frac {1}{1 - t} I + \frac {1}{1 - t} \nabla_ {x} \mathbb {E} \left[ Z _ {1} \mid Z _ {t} = x \right] \| \\ \leq \frac {1}{1 - T} + \frac {\nu + d}{\nu} \frac {2 \sqrt {\nu}}{(1 - T) ^ {2}} B _ {1}, \forall t \in [ 0, T ]. \\ \end{array}
$$

Notice that

$$
\begin{array}{l} \frac {\partial}{\partial t} v (z, t) = \frac {\partial}{\partial t} \left(- \frac {1}{1 - t} z + \frac {1}{1 - t} \mathbb {E} \left[ Z _ {1} \mid Z _ {t} = z \right]\right) \\ = - \frac {1}{(1 - t) ^ {2}} z + \frac {1}{(1 - t) ^ {2}} \mathbb {E} [ Z _ {1} | Z _ {t} = z ] + \frac {1}{1 - t} \frac {\partial}{\partial t} \mathbb {E} [ Z _ {1} | Z _ {t} = z ]. \\ \end{array}
$$

Using Lemma 14, we have

$$
\| \frac {\partial}{\partial t} v (z, t) \| \leq \frac {1}{(1 - T) ^ {2}} \| z \| + \frac {1}{(1 - T) ^ {2}} B _ {1} + \frac {1}{1 - T} \frac {\nu + d}{\nu} \frac {3 \sqrt {\nu}}{2 (1 - T) ^ {2}} \left(B _ {2} + 3 B _ {1} ^ {2}\right), \forall t \in [ 0, T ].
$$

# F.2 Proof of Theorem 7

Proof. [Proof of Theorem 7] Define

$$
d Z _ {t} = v \left(Z _ {t}, t\right) d t, Z _ {0} \sim \pi_ {0},
$$

$$
d \bar {Y} _ {t} = \hat {v} (\bar {Y} _ {t _ {i}}, t _ {i}) d t, \bar {Y} _ {0} = Z _ {0}.
$$

By direct computation,

$$
\begin{array}{l} \frac {d}{d t} \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} = 2 \langle Z _ {t} - \bar {Y} _ {t}, \frac {d}{d t} Z _ {t} - \frac {d}{d t} \bar {Y} _ {t} \rangle = 2 \langle Z _ {t} - \bar {Y} _ {t}, v (Z _ {t}, t) - \hat {G} (\bar {Y} _ {t _ {i}}, t _ {i}) \rangle \\ = 2 \left\langle Z _ {t} - \bar {Y} _ {t}, v \left(Z _ {t}, t\right) - v \left(Z _ {t _ {i}}, t _ {i}\right) \right\rangle + 2 \left\langle Z _ {t} - \bar {Y} _ {t}, v \left(Z _ {t _ {i}}, t _ {i}\right) - v \left(\bar {Y} _ {t _ {i}}, t _ {i}\right) \right\rangle \\ + 2 \langle Z _ {t} - \bar {Y} _ {t}, v (\bar {Y} _ {t _ {i}}, t _ {i}) - \hat {v} (\bar {Y} _ {t _ {i}}, t _ {i}) \rangle . \\ \end{array}
$$

Using Young's inequality, we can bound the rest of the terms as follows.

1. We bound the first term. By Lemma 15,

$$
\begin{array}{l} 2 \mathbb {E} [ \langle Z _ {t} - \bar {Y} _ {t}, v (Z _ {t}, t) - v (Z _ {t _ {i}}, t) \rangle ] \\ \leq L _ {1} \mathbb {E} [ \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} ] + \frac {1}{L _ {1}} \mathbb {E} [ \| v (Z _ {t}, t) - v (Z _ {t _ {i}}, t) \| ^ {2} ] \\ \leq L _ {1} \mathbb {E} [ \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} ] + \frac {1}{L _ {1}} h ^ {2} D _ {3}. \\ \end{array}
$$

2. We bound the second term.

$$
\begin{array}{l} 2 \mathbb {E} [ \langle Z _ {t} - \bar {Y} _ {t}, v (Z _ {t _ {i}}, t _ {i}) - v (\bar {Y} _ {t _ {i}}, t _ {i}) \rangle ] \\ \leq L _ {1} \mathbb {E} [ \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} ] + \frac {1}{L _ {1}} \mathbb {E} [ \| v (Z _ {t _ {i}}, t _ {i}) - v (\bar {Y} _ {t _ {i}}, t _ {i}) \| ^ {2} ] \\ \leq L _ {1} \mathbb {E} [ \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} ] + \frac {1}{L _ {1}} L _ {1} ^ {2} \mathbb {E} [ \| Z _ {t _ {i}} - \bar {Y} _ {t _ {i}} \| ^ {2} ]. \\ \end{array}
$$

Here we used Proposition 6.

3. We bound the third term. Recall that we assumed $\mathbb{E}[\| v(x,t) - \hat{v} (x,t)\| ^2 ]\leq \varepsilon^2$ . Then

$$
\begin{array}{l} 2 \left\langle Z _ {t} - \bar {Y} _ {t}, v \left(\bar {Y} _ {t _ {i}}, t _ {i}\right) - \hat {v} \left(\bar {Y} _ {t _ {i}}, t _ {i}\right) \right\rangle \\ \leq L _ {1} \mathbb {E} [ \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} ] + \frac {1}{L _ {1}} \mathbb {E} [ \| v (\bar {Y} _ {t _ {i}}, t _ {i}) - \hat {v} (\bar {Y} _ {t _ {i}}, t _ {i}) \| ^ {2} ] \\ \leq L _ {1} \mathbb {E} [ \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} ] + \frac {1}{L _ {1}} \varepsilon^ {2}. \\ \end{array}
$$

Together,

$$
\frac {d}{d t} \mathbb {E} [ \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} ] \leq 3 L _ {1} \mathbb {E} [ \| Z _ {t} - \bar {Y} _ {t} \| ^ {2} ] + \frac {1}{L _ {1}} \left(h ^ {2} D _ {3} + L _ {1} ^ {2} \mathbb {E} [ \| Z _ {t _ {i}} - \bar {Y} _ {t _ {i}} \| ^ {2} ] + \varepsilon^ {2}\right).
$$

Define

$$
K = h ^ {2} D _ {3} + L _ {1} ^ {2} \mathbb {E} [ \| Z _ {t _ {i}} - \overline {{Y}} _ {t _ {i}} \| ^ {2} ] + \varepsilon^ {2}.
$$

Then

$$
\begin{array}{l} \mathbb {E} \left[ \left\| Z _ {t _ {i + 1}} - \bar {Y} _ {t _ {i + 1}} \right\| ^ {2} \right] \\ \leq e ^ {3 L _ {1} h} \mathbb {E} [ \| Z _ {t _ {i}} - \bar {Y} _ {t _ {i}} \| ^ {2} ] + \frac {3}{L _ {1}} \int_ {t _ {i}} ^ {t _ {i + 1}} e ^ {3 L _ {1} (t _ {i + 1} - t)} (K) d t \\ \leq e ^ {3 L _ {1} h} \mathbb {E} [ \| Z _ {t _ {i}} - \bar {Y} _ {t _ {i}} \| ^ {2} ] + \frac {e ^ {3 L _ {1} h} - 1}{L _ {1} ^ {2}} K \\ = e ^ {3 L _ {1} h} \mathbb {E} [ \| Z _ {t _ {i}} - \bar {Y} _ {t _ {i}} \| ^ {2} ] + \frac {e ^ {3 L _ {1} h} - 1}{L _ {1} ^ {2}} \left(h ^ {2} D _ {3} + \varepsilon^ {2}\right) + \left(e ^ {3 L _ {1} h} - 1\right) \mathbb {E} [ \| Z _ {t _ {i}} - \bar {Y} _ {t _ {i}} \| ^ {2} ] \\ \leq (2 e ^ {3 L _ {1} h} - 1) \mathbb {E} [ \| Z _ {t _ {i}} - \overline {{Y}} _ {t _ {i}} \| ^ {2} ] + \frac {e ^ {3 L _ {1} h} - 1}{L _ {1} ^ {2}} (h ^ {2} D _ {3} + \varepsilon^ {2}). \\ \end{array}
$$

For $A_{i + 1}\leq (2e^{3L_1h} - 1)A_i + \frac{e^{3L_1h} - 1}{L_1^2} B$ with $A_0 = 0$ , we have

$$
A _ {n} = \sum_ {i = 0} ^ {n - 1} (2 e ^ {3 L _ {1} h} - 1) ^ {i} \frac {2 e ^ {3 L _ {1} h} - 1}{L _ {1} ^ {2}} B = \frac {1 - (2 e ^ {3 L _ {1} h} - 1) ^ {n}}{1 - (2 e ^ {3 L _ {1} h} - 1)} \frac {e ^ {3 L _ {1} h} - 1}{L _ {1} ^ {2}} B \leq \frac {(2 e ^ {3 L _ {1} h} - 1) ^ {n} - 1}{2 L _ {1} ^ {2}} B.
$$

In general, for $x \in [0,1]$ we have $e^x \leq 1 + 2x$ . Hence $2e^{3L_1h} - 1 \leq e^{3L_1h} + 6L_1h \leq 1 + 12L_1h$ . And we get $(2e^{3L_1h} - 1)^n \leq (1 + 12L_1h)^n \leq (1 + \frac{12L_1}{n})^n \leq e^{12L_1}$ .

Hence

$$
\mathbb {E} \left[ \| Z _ {T} - \bar {Y} _ {T} \| ^ {2} \right] \leq \frac {e ^ {1 2 L _ {1}}}{L _ {1} ^ {2}} \left(h ^ {2} D _ {3} + \varepsilon^ {2}\right).
$$

This implies

$$
W _ {2} \left(\pi_ {T} ^ {D}, \hat {\pi} _ {T} ^ {D}\right) \leq \frac {e ^ {6 L _ {1}}}{L _ {1}} \sqrt {h ^ {2} D _ {3} + \varepsilon^ {2}}.
$$

Consequently,

$$
W _ {2} \left(\pi_ {1} ^ {D}, \hat {\pi} _ {T} ^ {D}\right) \leq \frac {e ^ {6 L _ {1}}}{L _ {1}} \sqrt {h ^ {2} D _ {3} + \varepsilon^ {2}} + (1 - T) \sqrt {2 \left(\mathbb {E} \left[ \| Z _ {1} \| ^ {2} \right] + \mathbb {E} \left[ \| Z _ {0} \| ^ {2} \right]\right)}.
$$

![](images/cd9aa2e13de423e77e46b5f8710d8a05310e89edb5341f6bcff9de37a08f67ba.jpg)

# F.3 Proof of Theorem 9

Proof. [Proof of Lemma 8] Note that we have

$$
\begin{array}{l} \| v ^ {P} (x _ {1}, t) - P _ {x _ {2}} ^ {x _ {1}} v ^ {P} (x _ {2}, t) \| _ {g ^ {P} (x _ {1})} = \| \nabla^ {2} \Psi (x _ {1}) \left(\nabla^ {2} \Psi^ {*} (z _ {1}) v ^ {D} (z _ {1}, t) - P _ {x _ {2}} ^ {x _ {1}} \nabla^ {2} \Psi^ {*} (z _ {1}) v ^ {D} (z _ {2}, t)\right) \| _ {g ^ {D} (z _ {1})} \\ = \| v ^ {D} \left(z _ {1}, t\right) - \nabla^ {2} \Psi \left(x _ {1}\right) P _ {x _ {2}} ^ {x _ {1}} \nabla^ {2} \Psi^ {*} \left(z _ {1}\right) v ^ {D} \left(z _ {2}, t\right) \| _ {g ^ {D} \left(z _ {1}\right)} \\ = \| v ^ {D} \left(z _ {1}, t\right) - \nabla^ {2} \Psi \left(x _ {1}\right) \nabla^ {2} \Psi^ {*} \left(z _ {1}\right) P _ {z _ {2}} ^ {z _ {1}} v ^ {D} \left(z _ {2}, t\right) \| _ {g ^ {D} \left(z _ {1}\right)} \\ = \left\| v ^ {D} \left(z _ {1}, t\right) - v ^ {D} \left(z _ {2}, t\right) \right\| _ {g ^ {D} \left(z _ {1}\right)}, \\ \end{array}
$$

where $P_x^y$ denotes parallel transport from $x$ to $y$ . This proves the result.

![](images/fcaa8ac56b66736b24d5696a649a695ee3a7ea29f90cae9963f4c75a9d4bbcdb.jpg)

Lemma 16. Under Assumption 4, For $\kappa \leq \frac{\gamma}{2d + \nu + 2}$ , we can guarantee Assumption 3 holds with $\alpha \geq 2d + \nu + 2$ .

Proof. Using the change of variable formula, together with the fact that the determinant of a matrix equals to the product of all its eigenvalues, we know

$$
d \pi_ {E u c} ^ {P} (x) = \sqrt {\det  \nabla^ {2} \Psi (x)} d \pi_ {H e s s} ^ {P} (x) \geq d \pi_ {H e s s} ^ {P} (x),
$$

where $\pi_{Euc}^{P}, \pi_{Hess}^{P}$ denotes the probability density function of the target distribution in primal space, under the Euclidean metric and squared Hessian metric, respectively. Furthermore, the isometric mapping from primal space to dual space guarantees that

$$
\pi_ {E u c} ^ {P} (x) \geq \pi^ {D} (z).
$$

Notice that

$$
\sup  _ {x \in \mathcal {K} _ {\delta}} \| \nabla \Psi (x) \| \leq \frac {C ^ {\prime}}{\delta^ {\kappa}}.
$$

Since we assumed $\sup_{x\in \mathcal{K}\backslash \mathcal{K}_{\delta}}\pi_{Euc}^{P}(x)\leq C_{pdf}\delta^{\gamma}$ , we have

$$
\pi^ {D} (z) \leq \pi_ {E u c} ^ {P} (x) \leq C _ {p d f} \delta^ {\gamma}, \forall z \geq \frac {C ^ {\prime}}{\delta^ {\kappa}}.
$$

Using $\delta^{\gamma} = \left(\frac{1}{\left(\frac{1}{\delta^{\kappa}}\right)}\right)^{\gamma/\kappa}$ , we conclude that there exists some $C > 0$ s.t.

$$
\pi^ {D} (z) \leq \frac {C}{\| z \| ^ {\gamma / \kappa}}, \forall z \geq 1.
$$

To guarantee $\gamma /\kappa \geq 2d + \nu +2$ , we need $\kappa \leq \frac{\gamma}{2d + \nu + 2}$

Proof. [Proof of Theorem 9] Using Lemma 16, we know Assumption 3 holds with $\alpha \geq 2d + \nu + 2$ . The result follows from applying Proposition 2 and Theorem 7.