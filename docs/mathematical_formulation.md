# Mathematical Formulation: $3 \times 3$ Feature Matrices & Risk Metrics

This document formalizes the mathematical transformations applied to raw time-series observations.

## 1. Discrete State Mapping

Let $x_t \in \mathbb{R}$ represent a clinical measurement recorded at timestamp $t$. We map $x_t$ into a discrete state space $S_t \in \{0, 1, 2\}$ representing Low, Normal, and High severity states:

$$
S_t =
\begin{cases}
0 & \text{if } x_t < \theta_{\text{low}} \\
1 & \text{if } \theta_{\text{low}} \le x_t \le \theta_{\text{high}} \\
2 & \text{if } x_t > \theta_{\text{high}}
\end{cases}
$$

where $\theta_{\text{low}}$ and $\theta_{\text{high}}$ are clinical thresholds defined per observation code.

---

## 2. $3 \times 3$ Transition Count & Stochastic Matrix

For a sequence of discrete states $\mathbf{S} = (S_1, S_2, \dots, S_N)$ within time window $\Delta t$, the unnormalized transition count matrix $\mathbf{C} \in \mathbb{R}^{3 \times 3}$ is computed as:

$$
C_{i,j} = \sum_{k=1}^{N-1} \mathbb{I}(S_k = i \land S_{k+1} = j)
$$

where $\mathbb{I}(\cdot)$ is the indicator function. The normalized stochastic transition matrix $\mathbf{M} \in \mathbb{R}^{3 \times 3}$ is defined row-wise:

$$
M_{i,j} = \frac{C_{i,j} + \epsilon}{\sum_{k=0}^{2} (C_{i,k} + \epsilon)}
$$

where $\epsilon = 10^{-5}$ prevents division by zero.

---

## 3. Matrix Stability Index & Escalation Score

### Stability Index (Trace Metric)

The diagonal elements of $\mathbf{M}$ represent state persistence. The stability index $I_{\text{stable}}$ is defined as:

$$
I_{\text{stable}} = \frac{1}{3} \text{Tr}(\mathbf{M}) = \frac{1}{3} \sum_{i=0}^{2} M_{i,i}
$$

### Escalation Score

The risk score $R$ capturing sudden health deterioration is driven by off-diagonal transitions towards state 2:

$$
R = w_1 \cdot M_{0,2} + w_2 \cdot M_{1,2} + w_3 \cdot M_{2,2}
$$

where $w_1 = 0.6$, $w_2 = 0.25$, and $w_3 = 0.15$.

---

## 4. Downstream Predictive Model

The flattened $3 \times 3$ matrix $\text{vec}(\mathbf{M}) \in \mathbb{R}^9$ is concatenated with the patient demographic vector $\mathbf{d} \in \mathbb{R}^d$ to form feature vector $\mathbf{z} = [\text{vec}(\mathbf{M})^T, \mathbf{d}^T]^T$. The predicted probability of decompensation $\hat{y}$ is:

$$
\hat{y} = \sigma(\mathbf{w}^T \mathbf{z} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{z} + b)}}
$$
