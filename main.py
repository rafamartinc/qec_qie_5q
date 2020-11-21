#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function
from sympy import symbols, Symbol, Matrix, I, pprint, diff
from sympy.core.expr import Expr
from sympy.physics.quantum import Dagger
from sympy.physics.quantum.tensorproduct import TensorProduct


def main():
    num_qubits = 5

    L0 = Symbol('00000') - Symbol('00011') + Symbol('00101') - Symbol('00110') + \
         Symbol('01001') + Symbol('01010') - Symbol('01100') - Symbol('01111') - \
         Symbol('10001') + Symbol('10010') + Symbol('10100') - Symbol('10111') - \
         Symbol('11000') - Symbol('11011') - Symbol('11101') - Symbol('11110')

    L1 = - Symbol('00001') - Symbol('00010') - Symbol('00100') - Symbol('00111') - \
         Symbol('01000') + Symbol('01011') + Symbol('01101') - Symbol('01110') - \
         Symbol('10000') - Symbol('10011') + Symbol('10101') + Symbol('10110') - \
         Symbol('11001') + Symbol('11010') - Symbol('11100') + Symbol('11111')

    print('L0:', L0)
    print('L1:', L1)
    print()

    X = Matrix([[0, 1], [1, 0]])
    Y = Matrix([[0, -I], [I, 0]])
    Z = Matrix([[1, 0], [0, -1]])
    print('X:', X)
    print('Y:', Y)
    print('Z:', Z)
    print()

    B_c = []  # Computational basis: [ 00000, 00001, ..., 11111 ].
    for i in range(2 ** num_qubits):
        B_c.append(get_computational_basis_string_state(i, num_qubits))
    print('B_c:', B_c)
    print()

    B = [L0, L1]
    for operator in [X, Y, Z]:
        for u in range(num_qubits):
            for generator in [L0, L1]:
                B.append(
                    apply_1qubit_operation(operator, u, generator, num_qubits)
                )
    print('B:', B)
    print()

    # Now we will determine M: v{B} -> v{B_c}.

    # First way of calculating M: putting the vectors from B, expressed in tearms of B_c, as columns.
    M = Matrix([
        [
            B[columna].coeff(get_computational_basis_string_state(fila, num_qubits))
            for columna in range(2 ** num_qubits)
        ] for fila in range(2 ** num_qubits)
    ])

    # Second way of calculating M: using derivatives.
    M2 = Matrix([
        [
            diff(B[j], B_c[i]) for j in range(2 ** num_qubits)
        ] for i in range(2 ** num_qubits)
    ])

    assert 0 == sum(M - M2)
    for i in range(2 ** num_qubits):
        state_B_vector = M * get_computational_basis_vector_state(i, num_qubits)
        state_B_c_expression = transform_vector_state_to_expression_state(state_B_vector, num_qubits)
        assert state_B_c_expression == B[i]

    print('M == M1 == M2: \n')
    pprint(M)
    print()

    A = symbols('A0:%d' % num_qubits)  # Define A_0 through A_4.
    B = symbols('B0:%d' % num_qubits)  # Define A_0 through A_4.
    C = symbols('C0:%d' % num_qubits)  # Define A_0 through A_4.
    D = symbols('D0:%d' % num_qubits)  # Define A_0 through A_4.

    W_u = []
    for u in range(num_qubits):  # Define W_0 through W_4.
        W_u.append(Matrix([
            [A[u] + I * B[u], -C[u] + I * D[u]],
            [C[u] + I * D[u], A[u] - I * B[u]]
        ]))
        print('W[%d]:' % u, W_u[u])
    print()

    W = TensorProduct(W_u[0], W_u[1], W_u[2], W_u[3], W_u[4])
    print('Shape of W:', W.shape)
    print()

    W_B = Dagger(M) * W * M
    print('Shape of W_B:', W.shape)
    print()


def apply_1qubit_operation(operation: Matrix, target_qubit: int, initial_state: Expr, num_qubits: int) -> Expr:
    final_state = 0

    for i in range(2 ** num_qubits):
        index = get_computational_basis_string_state(i, num_qubits)

        alpha = initial_state.coeff(index)
        state_0, state_1 = get_basis_states_one_bit_apart(index, target_qubit)

        initial_qubit_state = Matrix([[1], [0]]) if index.name[target_qubit] == '0' else Matrix([[0], [1]])
        final_qubit_state = operation * initial_qubit_state

        final_state += alpha * (final_qubit_state[0] * state_0 + final_qubit_state[1] * state_1)

    return final_state


def get_computational_basis_string_state(i: int, num_qubits: int) -> Symbol:
    binary_string = str(bin(i)[2:])
    binary_string = ''.join(['0' for _ in range(num_qubits - len(binary_string))]) + binary_string
    return Symbol(binary_string)


def get_computational_basis_vector_state(i: int, num_qubits: int) -> Matrix:
    return Matrix([
        [
            1 if i == j else 0
        ] for j in range(2 ** num_qubits)
    ])


def get_basis_states_one_bit_apart(reference_state: Symbol, target_qubit: int) -> tuple:
    reference_state = reference_state.name

    return Symbol(reference_state[:target_qubit] + '0' + reference_state[target_qubit + 1:]), \
           Symbol(reference_state[:target_qubit] + '1' + reference_state[target_qubit + 1:])


def transform_expression_state_to_vector_state(state: Expr, num_qubits: int) -> Matrix:

    return Matrix([
        [
            state.coeff(get_computational_basis_string_state(i, num_qubits))
        ] for i in range(2 ** num_qubits)
    ])


def transform_vector_state_to_expression_state(state: Matrix, num_qubits: int) -> Expr:

    result = 0

    for j in range(state.shape[0]):
        binary_string = get_computational_basis_string_state(j, num_qubits)
        result += state[j, 0] * binary_string

    return result


if __name__ == '__main__':
    main()
