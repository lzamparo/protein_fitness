import os
import argparse
import torch
import pyroed as pe

from typing import List
from peptide_fitness.read_data import read_data
from peptide_fitness.pyroed_design import SCHEMA, CONSTRAINTS, FEATURE_BLOCKS, GIBBS_BLOCKS

def make_outdir(run: int, suffix: str, mode: str) -> str:
    """ make the output dir and return the path """
    path = os.path.join("output", mode)
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, f"run_{run}_{suffix}.csv")


def write_output(path: str, seqs: List[str]):
    """ write the output to the approprite filename in `path` """
    with open(path, 'w') as f:
        print("order" + "," + " sequence", file=f)
        for i, s in enumerate(seqs):
            print(f"{i}, {s}", file=f)


def run(reps: int, mode: str="svi") -> None:
    """ perform number of reps for the Pyroed model """
    # read data
    sequences, responses = read_data()
    responses = torch.tensor(responses)

    for run in range(reps):
        print(f"starting {run}")
        # (Re)design the experiment dictionary 
        design = pe.encode_design(SCHEMA, sequences)
        experiment = pe.start_experiment(SCHEMA, design, responses)

        # fit model & sample top 10 predictions likely to improve scores
        design = pe.get_next_design(
            SCHEMA, CONSTRAINTS, FEATURE_BLOCKS, GIBBS_BLOCKS, experiment, design_size=10, config={"response_type": "real", "inference": mode, "mcmc_num_samples": 1000}
        )
        # write top 10 predicted outputs
        new_seqences = ["".join(s) for s in pe.decode_design(SCHEMA, design)]
        write_output(make_outdir(run, "top10", mode), new_seqences)

        # sample next top 200 predicted sequences
        design = pe.get_next_design(
            SCHEMA, CONSTRAINTS, FEATURE_BLOCKS, GIBBS_BLOCKS, experiment, design_size=200, config={"response_type": "real", "inference": mode}
        )
        # write top 10 predicted outputs
        new_seqences = ["".join(s) for s in pe.decode_design(SCHEMA, design)]
        write_output(make_outdir(run, "next200", mode), new_seqences)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--mode", type=str, default="svi")
    args = parser.parse_args()
    run(args.runs, args.mode)
        
    

