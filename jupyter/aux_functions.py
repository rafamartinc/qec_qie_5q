from sympy import symbols, expand as expand_2
from sympy.core.expr import Expr
from itertools import combinations


def copy_list(list_to_copy: list) -> list:
    """
    Create a copy of a list, so that both copies contain the same values, but none of them
    are modified if elements are included to or excluded from the other list.
    """
    return list_to_copy[:]


def copy_dictionary(dictionary: dict) -> dict:
    """
    Create a copy of a dictionary, so that both copies contain the same values, but none of
    them are modified if elements are included to or excluded from the other dictionary.
    """
    result = {}
    for key in dictionary:
        result[key] = dictionary[key]
    return result


def get_all_monomials(a_s: Expr, b_s: Expr, c_s: Expr, d_s: Expr,
                      valid_variables: list) -> list:
    """
    Function used to get all monomials within a[s], b[s], c[s] and d[s], for a fixed 0 ≤ s < 16.
    The result is given as a list of monomials, being each monomial expressed as a list itself,
    with the variables of V that participate in it, and will be later used to try possible values
    for V_s. Only those variables included in 'valid_variables' will be considered.
    
    :param a_s: Expression of a[s] for a given 0 ≤ s < 16, such as 'A_0*A_1*A_2*A_3*A_4 +
        A_0*B_1*B_4*C_2*C_3 + ... + A_4*C_0*C_3*D_1*D_2', with a total of 16 monomials.
        
    :param b_s: Expression of b[s] for a given 0 ≤ s < 16, in the same shape as a_s.
    
    :param c_s: Expression of c[s] for a given 0 ≤ s < 16, in the same shape as a_s.
    
    :param d_s: Expression of d[s] for a given 0 ≤ s < 16, in the same shape as a_s.
    
    :param valid_variables: List of variables that may participate in V_s, such as [B_0, B_1, ...,
        B_4, C_0, ..., C_4, D_0, ..., D_4]. This allows the programmer to exclude numeric factors,
        as well as A_u variables when considering 0 < s < 16.
        
    :result: List of monomials, in which each monomial is a list of up to 5 variables (if A_u's
        are excluded, monomials with less than 5 variables may be found). E.g.: [
            [[B_0, B_4, C_3], [B_3, C_2, C_4, D_0], ..., [B_0, B_2, C_4, D_1, D_3]]
        ]
    """
    result = []
    
    # Iterate over the 4 polynomials.
    polynomials = [a_s, b_s, c_s, d_s]
    polynomial_index = 0
    while polynomial_index < len(polynomials):
        polynomial = polynomials[polynomial_index]
        
        # Iterate over the 16 monomials.
        monomials = expand_2(polynomial).args
        monomial_index = 0
        while monomial_index < len(monomials):
            monomial = monomials[monomial_index]
            
            # Gather the variables from this monomial, from those that are valid for V_s.
            variables = [var for var in monomial.args if var in valid_variables]
            result.append(variables)
            
            monomial_index += 1 

        polynomial_index += 1
    
    return result


def get_all_odd_combinations_of_variables(variables: list) -> list:
    """
    Given a list of up to 5 variables, this function will return all the ways to pick an odd number
    of variables from the list. Should the list contain less than 5 variables, the function will
    work nevertheless. For example, if the list [B_1, C_2, C_4, D_3] is given, the ways to pick just
    one variable are [(B_1,), (C_2,), (C_4,), (D_3,)], the ways to pick 3 variables are [(B_1, C_2, C_4),
    (B_1, C_2, D_3), (B_1, C_4, D_3), (C_2, C_4, D_3)], and the ways to pick 5 variables are [] (none).
    
    :param variables: List of variables to consider (e.g.: [A_0, A_3, C_2, C_4, D_1])
    
    :result: List of ways (as tuples) of picking an odd number of variables from the list given as
        input, such as [(B_1,), (C_2,), (C_4,), (D_3,), (B_1, C_2, C_4), ..., (C_2, C_4, D_3)]
    """
    
    options_1 = list(combinations(variables, 1))
    options_2 = list(combinations(variables, 3))
    options_3 = list(combinations(variables, 5))
    
    return options_1 + options_2 + options_3


def is_valid_modification_of_V_s(included_variables: list, excluded_variables: list, V_s: dict) -> bool:
    """
    When considering an update to a set V_u under construction, by including a set of variables
    that must be included in the final form of V_s, and a set of variables that must not be
    included, this function helps determine wether that is compatible with the contents of V_s that
    have already been established before. For example, if we want to include the variable B_0 in
    V_s but that variable was already flagged for exclusion when considering a previous monomial,
    this function will return False.
    
    :param included_variables: List of variables we would like to include in V_s, such as [B_0, C_2].
    
    :param excluded_variables: List of variables we would not want to put in V_s, because that will
        may no longer change the sign of a previously seen monomial. E.g.: [D_1].
        
    :param V_s: Configuration of V_s so far, stating which variables will be included in the final set,
        and which ones can not be included, according to the monomials already considered. It takes
        the shape of a dictionary with the variables as keys, and a boolean value for each key,
        indicating whether that variable is included or not. Missing variables have not been
        considered yet. E.g.: {B_0: True, B_2: False, C_0: False, C_1: False, C_2: False}.
        
    :result: True if V_s can be modified as suggested, False otherwise.
    """
    
    result = True
    
    i = 0
    while result and i < len(included_variables):
        variable = included_variables[i]
        if variable in V_s and V_s[variable] is False:
            result = False
        i += 1
        
    i = 0
    while result and i < len(excluded_variables):
        variable = excluded_variables[i]
        if variable in V_s and V_s[variable] is True:
            result = False
        i += 1
        
    return result


def apply_changes_to_V_s(included_variables: list, excluded_variables: list, V_s: dict) -> dict:
    """
    Apply an update to a set V_u under construction, by including a set of variables that must be
    included in the final form of V_s, and marking for exclusion a set of variables that must not be
    included. This function should only be executed if 'is_valid_modification_of_V_s' stated that
    the modification is valid.
    
    :param included_variables: List of variables we would like to include in V_s, such as [B_0, C_2].
    
    :param excluded_variables: List of variables we would not want to put in V_s, because that will
        may no longer change the sign of a previously seen monomial. E.g.: [D_1].
        
    :param V_s: Configuration of V_s so far, stating which variables will be included in the final set,
        and which ones can not be included, according to the monomials already considered. It takes
        the shape of a dictionary with the variables as keys, and a boolean value for each key,
        indicating whether that variable is included or not. Missing variables have not been
        considered yet. E.g.: {B_0: True, B_2: False, C_0: False, C_1: False, C_2: False}.
        
    :result: Updated configuration of V_s.
    """
    
    new_V_s = copy_dictionary(V_s)
    
    for variable in included_variables:    
        new_V_s[variable] = True    
    for variable in excluded_variables:    
        new_V_s[variable] = False
    
    return new_V_s


def search_configurations_recursively(s: int, V_s: dict, monomials: list, result: list,
                                      get_all_combinations: bool) -> None:
    """
    This function will try to go through all the monomials given (recursively, each call to this
    function will consider one monomial), to build a set V_s of variables from V that ensures
    that all monomials' signs are flipped if we change the sign of all the variables from V_s.

    :param s: Value of 's'.
    
    :param V_s: Configuration of V_s so far, stating which variables will be included in the final set,
        and which ones can not be included, according to the monomials already considered. It takes
        the shape of a dictionary with the variables as keys, and a boolean value for each key,
        indicating whether that variable is included or not. Missing variables have not been
        considered yet. E.g.: {B_0: True, B_2: False, C_0: False, C_1: False, C_2: False}.
        
    :param monomials: List of monomials, in which each monomial is a list of up to 5 variables (if
        A_u's are excluded, monomials with less than 5 variables may be found). E.g.: [
            [[B_0, B_4, C_3], [B_3, C_2, C_4, D_0], ..., [B_0, B_2, C_4, D_1, D_3]]
        ]
        
    :param result: List that will end up containing all the valid forms of V_s that have been found
        across all executions of this functions.
        
    :param get_all_combinations: Configuration parameter that indicates whether all valid forms of V_s
        should be found (True), or if just one is enough (False).
    """
    
    # Get one monomial and consider all ways to pick an odd number of variables from it.
    monomials = copy_list(monomials)
    monomial = monomials.pop()
    options = get_all_odd_combinations_of_variables(monomial)
    
    # For each way to pick an odd number of variables, keep only those that are compatible with the
    # existing contents of V_s so far.
    for included_variables in options:
        excluded_variables = [var for var in monomial if var not in included_variables]
        
        if is_valid_modification_of_V_s(included_variables, excluded_variables, V_s):
            
            new_V_s = apply_changes_to_V_s(included_variables, excluded_variables, V_s)
            
            # Check if a solution has been found. Otherwise, keep running.
            
            if len(monomials) == 0:
                # Done, configuration found.
                V = [str(key) for key in new_V_s.keys() if new_V_s[key]]
                V.sort()
                
                print('   Valid V_' + str(s) + ' found:', V)
                result.append(V)
                
            elif len(result) == 0 or get_all_combinations:
                # Continue with the next monomial.
                search_configurations_recursively(s, new_V_s, monomials, result, get_all_combinations)
