from __future__ import absolute_import, print_function

__all__ = ["distance_based_on_molecular_formula"]


def distance_based_on_molecular_formula(metabolite1, metabolite2, normalize=True):
    """Calculate the distance of two metabolites bases on the molecular formula

    Parameters
    ----------
    metabolite1 : Metabolite
        The first metabolite.
    metabolite2 : Metabolite
        The second metabolite.
    normalize : bool, optional
        If the distance should be normalized by the total number of elements in both metabolites (defaults to True).

    Returns
    -------
    float
        The distance between metabolite1 and metabolite2.

    """
    if len(metabolite1.elements) == 0 or len(metabolite2.elements) == 0:
        raise ValueError(
            "Cannot calculate distance between metabolites %s and %s"
            % (metabolite1, metabolite2)
        )
    elements = set(
        list(metabolite1.elements.keys()) + list(metabolite2.elements.keys())
    )
    distance = 0.0
    for element in elements:
        distance += abs(
            metabolite1.elements.get(element, 0) - metabolite2.elements.get(element, 0)
        )
    if normalize:
        return distance / sum(
            list(metabolite1.elements.values()) + list(metabolite2.elements.values())
        )
    else:
        return distance
