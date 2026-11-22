#!/usr/bin/env python3
"""
Gene module definitions for BOLD transcriptomic validation.

Three modules map onto the three BOLD state variables:
    X  -> pro-inflammatory / ROS-generating activity
    Y  -> pro-osteogenic activity
    Z  -> metabolic fitness / oxidative-phosphorylation + M2-like program

Mouse symbols are used for GSE234451 (snRNA-seq) and GSE240390 (bulk RNA-seq).
Human orthologues are used for GSE180504 (human BMSC bulk RNA-seq).

These definitions are identical to those reported in the manuscript
(Methods, "Independent transcriptomic validation").
"""

# ---------------------------------------------------------------------------
# Mouse modules (GSE234451, GSE240390)
# ---------------------------------------------------------------------------
# NOTE (P2): MRC1, ARG1 and IL10 are canonical M2 macrophage markers (see
# M2_MARKERS below), so they contribute to both the Z score and the M2/M1
# classification. The M2-vs-M1 Z-module contrast is therefore partly
# definitional; this is acknowledged in the manuscript Limitations.
# MOUSE_MODULES_METABOLIC below provides a metabolic-only Z set
# (Tfam, Cpt1a) for a sensitivity check that excludes the M2 markers.
MOUSE_MODULES = {
    "X": ["Ncf1", "Ncf2", "Cybb", "Tnf", "Il6", "Nos2", "Fos", "Jun", "Cd86"],
    "Y": ["Yap1", "Wwtr1", "Runx2", "Sp7", "Bglap", "Alpl", "Col1a1", "Ibsp", "Spp1"],
    "Z": ["Tfam", "Cpt1a", "Mrc1", "Arg1", "Il10"],
}

# Metabolic-only Z module (excludes the M2 markers) for the sensitivity check.
MOUSE_MODULES_METABOLIC = {
    "X": MOUSE_MODULES["X"],
    "Y": MOUSE_MODULES["Y"],
    "Z": ["Tfam", "Cpt1a"],
}

# ---------------------------------------------------------------------------
# Human orthologues (GSE180504)
# ---------------------------------------------------------------------------
HUMAN_MODULES = {
    "X": ["NCF1", "NCF2", "CYBB", "TNF", "IL6", "NOS2", "FOS", "JUN", "CD86"],
    "Y": ["YAP1", "WWTR1", "RUNX2", "SP7", "BGLAP", "ALPL", "COL1A1", "IBSP", "SPP1"],
    "Z": ["TFAM", "CPT1A", "MRC1", "ARG1", "IL10"],
}

HUMAN_MODULES_METABOLIC = {
    "X": HUMAN_MODULES["X"],
    "Y": HUMAN_MODULES["Y"],
    "Z": ["TFAM", "CPT1A"],
}

# ---------------------------------------------------------------------------
# M1-like / M2-like marker sets used for macrophage sub-classification
# (GSE234451 only)
# ---------------------------------------------------------------------------
M1_MARKERS = ["Nos2", "Tnf", "Il6", "Cd86"]
M2_MARKERS = ["Mrc1", "Arg1", "Il10", "Cd163"]

# ---------------------------------------------------------------------------
# Cell-type marker sets used for cell-type partitioning (GSE234451 only)
# ---------------------------------------------------------------------------
CELLTYPE_MARKERS = {
    "Macrophage": ["Cd68", "Cd14", "Fcgr3", "Adgre1"],
    "Osteoblast": ["Runx2", "Sp7", "Bglap", "Alpl", "Col1a1"],
    "MSC": ["Prrx1", "Lepr", "Cxcl12", "Pdgfra"],
    "Endothelial": ["Pecam1", "Cdh5", "Kdr", "Vwf"],
}

# ---------------------------------------------------------------------------
# Ensembl -> symbol map for GSE240390 (mouse, GPL24247).
# The GSE240390 supplementary count matrix is indexed by Ensembl gene ID,
# so a hard-coded map is used for the 23 marker genes (18/23 are detected).
# ---------------------------------------------------------------------------
ENSEMBL_TO_SYMBOL_MOUSE = {
    # X module
    "ENSMUSG00000026864": "Ncf1",
    "ENSMUSG00000033891": "Ncf2",
    "ENSMUSG00000015337": "Cybb",
    "ENSMUSG00000024401": "Tnf",
    "ENSMUSG00000025746": "Il6",
    "ENSMUSG00000020826": "Nos2",
    "ENSMUSG00000021250": "Fos",
    "ENSMUSG00000052684": "Jun",
    "ENSMUSG00000016401": "Cd86",
    # Y module
    "ENSMUSG00000030930": "Yap1",
    "ENSMUSG00000027603": "Wwtr1",
    "ENSMUSG00000039153": "Runx2",
    "ENSMUSG00000037726": "Sp7",
    "ENSMUSG00000019731": "Bglap",
    "ENSMUSG00000028766": "Alpl",
    "ENSMUSG00000001506": "Col1a1",
    "ENSMUSG00000029305": "Ibsp",
    "ENSMUSG00000029304": "Spp1",
    # Z module
    "ENSMUSG00000003923": "Tfam",
    "ENSMUSG00000026900": "Cpt1a",
    "ENSMUSG00000026712": "Mrc1",
    "ENSMUSG00000019987": "Arg1",
    "ENSMUSG00000016529": "Il10",
}

# ---------------------------------------------------------------------------
# Sample -> time-point map for GSE234451 (6 snRNA-seq libraries)
# ---------------------------------------------------------------------------
GSE234451_SAMPLE_TIME = {
    "SC14": 0,   # uninjured periosteum
    "SC22": 3,   # day 3
    "SC17": 3,   # day 3
    "SC24": 5,   # day 5
    "SC25": 5,   # day 5
    "SC12": 7,   # day 7
}

# ---------------------------------------------------------------------------
# Sample -> (day, condition) map for GSE240390 (30 bulk RNA-seq samples)
# ---------------------------------------------------------------------------
GSE240390_SAMPLE_MAP = {
    "X1": "D5_DIO_1", "X4": "D3_DIO_1", "X5": "D3_DIO_2", "X6": "D3_DIO_3",
    "X8": "D21_DIO_1", "X9": "D21_DIO_2", "X10": "D5_Lean_1", "X12": "D5_Lean_2",
    "X13": "D5_Lean_3", "X16": "D5_DIO_2", "X18": "D5_DIO_3",
    "X19": "D7_Lean_1", "X20": "D7_Lean_2", "X23": "D7_Lean_3",
    "X24": "D7_DIO_1", "X27": "D7_DIO_2", "X28": "D7_DIO_3",
    "X29": "D3_Lean_1", "X31": "D3_Lean_2", "X32": "D3_Lean_3",
    "X49": "D14_DIO_1", "X50": "D14_DIO_2", "X53": "D14_DIO_3",
    "X54": "D10_Lean_1", "X56": "D10_Lean_2", "X57": "D10_Lean_3",
    "X59": "D10_DIO_1", "X61": "D10_DIO_2", "X62": "D10_DIO_3",
    "X70": "D21_DIO_3",
}


def parse_gse240390_sample(name):
    """'D7_DIO_2' -> (7, 'DIO', 2)."""
    day_s, cond, rep = name.split("_")
    return int(day_s[1:]), cond, int(rep)
