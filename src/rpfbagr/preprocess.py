import ast
import logging
import time
from typing import Dict

import pandas as pd
from Bio import Entrez
from cameo import load_model
from cobra.core.model import Model


def build_model(
    model_path: str,
    pathway_path: str,
    biomass_id: str,
    target_id: str,
    logger: logging.Logger,
):
    logger.info("Load model")

    model = load_model(model_path)
    if pathway_path:
        logger.info("Load pathway")
        pathway_model = load_model(pathway_path)
        logger.info("Merge model and pathway")
        model.merge(pathway_model, inplace=True)

    # Check if reactions are in the model
    reactions_id = [x.id for x in model.reactions]
    logger.info("Check if main objective is in the model")
    if biomass_id not in reactions_id:
        logger.error("Reaction not found in the model: %s" % (biomass_id,))
        return None
    logger.info("Check if target reaction is in the model")
    if target_id not in reactions_id:
        logger.error("Reaction not found in the model: %s" % (target_id,))
        return None

    logger.info("Set objective")
    model.objective = {
        model.reactions.get_by_id(biomass_id): 1.0,
        model.reactions.get_by_id(target_id): 0.5,
    }

    return model


def genes_annotate(
    model: Model,
    df: pd.DataFrame,
    email: str,
    logger: logging.Logger,
) -> pd.DataFrame:

    if df.empty:
        return df
    is_ncbi_error = False
    Entrez.email = email
    cache: Dict[str, str] = {}
    for ix in df.index:
        groups = df.loc[ix, "genes"]
        try:
            groups = ast.literal_eval(groups)
        except Exception:
            pass
        # Build group
        labels_groups = []
        for group in groups:
            labels = []
            for gene in group:
                model_gene = model.genes.get_by_id(gene)
                ncbi_gene = model_gene.annotation.get("ncbigene", "")
                if gene not in cache.keys():
                    label = gene
                    if ncbi_gene != "":
                        try:
                            hd = Entrez.esummary(db="gene", id=ncbi_gene)
                            rec = Entrez.read(hd, validate=False)
                            rec = rec.get("DocumentSummarySet", {})
                            rec = rec.get("DocumentSummary", [])
                            if len(rec) > 0:
                                name = rec[0].get("Name", "")
                                name = name.replace(",", "")
                                desc = rec[0].get("Description", "")
                                desc = desc.replace(",", "")
                                syn = rec[0].get("OtherAliases", "")
                                syn = syn.replace(",", "")
                                label = "%s=%s - %s" % (name, syn, desc)
                            time.sleep(2)
                        except Exception:
                            is_ncbi_error = True
                    cache[gene] = label
                labels.append(cache[gene])
            labels_groups.append("(%s)" % (",".join(labels),))
        df.at[ix, "genes_annotation"] = ",".join(labels_groups)
    if is_ncbi_error:
        logger.warning("NCBI annotation failing for some items")
    return df


def save_results(df: pd.DataFrame, path: str, sep: str = ",") -> None:
    df.to_csv(path, index=False, sep=sep)
