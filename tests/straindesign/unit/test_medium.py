from collections import OrderedDict

from cameobrs import load_model
from straindesign.medium import associate_flux_env, load_medium
from tests.straindesign.main_test import Main_test


class TestMedium(Main_test):
    def test_load_medium(self):
        medium = load_medium(self.medium_butanol_csv)
        theorical_medium = OrderedDict(
            {"EX_glc__D_e": (-10.0, 10.0), "EX_o2_e": (-5.0, 5.0)}
        )
        self.assertEqual(medium, theorical_medium)

    def test_associate_flux_env(self):
        medium = load_medium(self.medium_butanol_csv)
        model = load_model(self.model_ecoli)
        self.assertEqual(
            model.reactions.get_by_id("EX_glc__D_e").bounds, (-8.0, 999999.0)
        )
        associate_flux_env(
            model=model,
            envcond=medium,
        )
        self.assertEqual(model.reactions.get_by_id("EX_glc__D_e").bounds, (-10.0, 10.0))
        self.assertEqual(model.reactions.get_by_id("EX_o2_e").bounds, (-5.0, 5.0))

    def test_format(self):
        medium_csv = load_medium(self.medium_butanol_csv)
        medium_tsv = load_medium(self.medium_butanol_tsv)
        self.assertEqual(medium_csv, medium_tsv)
