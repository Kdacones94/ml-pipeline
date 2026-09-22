# Features & Model Documentation

## Feature Engineering (`src/features/`)

### $3 \times 3$ Transition Matrix Builder

- **Input**: List of `ClinicalObservationFact` domain objects for a patient encounter.

- **Transform**: Computes temporal state transitions over sliding windows.

- **Output**: `TransitionMatrix3x3` DTO containing a normalized $3 \times 3$ matrix.

### Feature Selection & Vectorization

- **Flattening**: Transforms the matrix $\mathbf{M}_{3 \times 3}$ into a 9-element floating-point vector:

  $$\text{vec}(\mathbf{M}) = [m_{0,0}, m_{0,1}, m_{0,2}, m_{1,0}, m_{1,1}, m_{1,2}, m_{2,0}, m_{2,1}, m_{2,2}]$$

- **Stability Metrics**: Trace calculation $\text{Tr}(\mathbf{M}) / 3$ measuring likelihood of patient remaining in current clinical state.

---

## Predictive Model Architecture (`src/models/`)

### Supervised Risk Trainer

- **Algorithm**: Regularized Logistic Regression / Gradient Boosting Wrapper.

- **Feature Vector Input**: 9 transition matrix features + demographic covariates (age, gender numeric encoding).

- **Target Label**: Binary indicator $y \in \{0, 1\}$ (0: Stable, 1: High Risk Deterioration).

- **Inference Payload**: Returns predicted probability distribution across classes and execution model versioning.
