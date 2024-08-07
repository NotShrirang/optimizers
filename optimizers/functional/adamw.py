"""
Functional implementation of the AdamW optimizer.
"""

import numpy as np


def adamw(
        params,
        grads,
        learning_rate,
        state,
        beta1=0.9,
        beta2=0.999,
        epsilon=1e-8,
        t=1,
        weight_decay=0.01,
    ) -> tuple[list, dict]:
    """
    AdamW optimizer.

    Args:
    params (np.ndarray): List of parameter arrays to update.
    grads (np.ndarray): List of gradient arrays corresponding to the parameters.
    learning_rate (float): Learning rate for the optimizer.
    state (dict): Dictionary to store the state of the optimizer (m and v).
    beta1 (float): Exponential decay rate for the first moment estimates.
    beta2 (float): Exponential decay rate for the second moment estimates.
    epsilon (float): Small constant to prevent division by zero.
    t (int): Time step (iteration number).
    weight_decay (float): Weight decay factor.

    Returns:
    tuple of list and dict: Updated parameters and state of the optimizer.
        updated_params (list): List of updated parameter arrays.
        state (dict): Updated state of the optimizer.
    """

    if state is None:
        state = {
            "m": [np.zeros_like(p) for p in params],
            "v": [np.zeros_like(p) for p in params],
        }

    m = state["m"]
    v = state["v"]

    updated_params = []
    for i, (param, grad) in enumerate(zip(params, grads)):
        m[i] = beta1 * m[i] + (1 - beta1) * grad
        v[i] = beta2 * v[i] + (1 - beta2) * (grad ** 2)

        m_hat = m[i] / (1 - beta1**t)
        v_hat = v[i] / (1 - beta2**t)

        param_update = (
            learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)
            + learning_rate * weight_decay * param
        )
        updated_param = param - param_update

        updated_params.append(updated_param)

    state["m"] = m
    state["v"] = v

    return updated_params, state
