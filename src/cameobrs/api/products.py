"""This module provides access to supported target products."""

from __future__ import absolute_import, print_function

__all__ = ["products"]

import difflib

from pandas import DataFrame

from cameobrs.data import metanetx
from cameobrs.visualization import inchi_to_svg


class Compound(object):
    def __init__(self, inchi):
        self.InChI = inchi

    def _repr_svg_(self):
        try:
            return inchi_to_svg(self.InChI)
        except ImportError:
            return self.__repr__()

    def _repr_html_(self):
        return self._repr_svg_()


class Products(object):
    """Supported target products."""

    def __init__(self):
        self.data_frame = metanetx.chem_prop

    def search(self, query):
        """Fuzzy search of available target products.

        Parameters
        ----------
        query : str
            Compound ID, name or InChI string.

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the scored search results.
        """
        matches = self._search_by_mnx_id(query)
        if len(matches) > 0:
            return matches
        matches = self._search_by_source(query)
        if len(matches) > 0:
            return matches
        matches = self._search_by_inchi(query)
        if len(matches) > 0:
            return matches
        matches = self._search_by_name_fuzzy(query)
        if len(matches) > 0:
            return matches
        matches = self._search_by_inchi_fuzzy(query)
        if len(matches) > 0:
            return matches
        else:
            return self._empty_result()

    def _search_by_mnx_id(self, mnx_id):
        try:
            selection = self.data_frame.loc[[mnx_id]]
            selection["search_rank"] = 0
            return selection
        except KeyError:
            return self._empty_result()

    def _search_by_name_fuzzy(self, name):
        original_possibilities = self.data_frame.name.dropna()
        possibilities_mapping = {
            original_name.lower(): original_name
            for original_name in original_possibilities
        }
        matches = difflib.get_close_matches(
            name.lower(), list(possibilities_mapping.keys()), n=5, cutoff=0.8
        )
        matches = [possibilities_mapping[match] for match in matches]
        ranks = {match: i for i, match in enumerate(matches)}
        selection = DataFrame(self.data_frame[self.data_frame.name.isin(matches)])
        selection["search_rank"] = selection.name.map(ranks)
        return selection.sort_values("search_rank")

    def _search_by_source(self, source_id):
        if source_id in metanetx.all2mnx:
            mnx_id = metanetx.all2mnx[source_id]
            selection = self.data_frame.loc[[mnx_id]]
            selection["search_rank"] = 0
            return selection
        else:
            return self._empty_result()

    def _search_by_inchi(self, inchi):
        selection = self.data_frame[self.data_frame.InChI == inchi]
        selection["search_rank"] = 0
        return selection

    def _search_by_inchi_fuzzy(self, inchi):
        # TODO: use openbabel if available
        matches = difflib.get_close_matches(
            inchi, self.data_frame.InChI.dropna(), n=5, cutoff=0.8
        )
        ranks = {match: i for i, match in enumerate(matches)}
        selection = DataFrame(self.data_frame[self.data_frame.InChI.isin(matches)])
        selection["search_rank"] = selection.name.map(ranks)
        return selection.sort_values("search_rank")

    def _empty_result(self):
        return DataFrame(columns=self.data_frame.columns.tolist().append("search_rank"))


products = Products()
