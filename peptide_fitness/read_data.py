import os 
import csv
from typing import Tuple, List

DATA_FILE = "DataSetforAssignment.xlsx-Sheet2023.csv"

def read_data(path=DATA_FILE) -> Tuple[List[str], List[float]]:
    sequences, responses = [], []
    data_path = os.path.join("data", path)
    with open(data_path, 'r') as f:
        fitness_reader = csv.DictReader(f, delimiter=",")
        for line in fitness_reader:
            sequences.append([a for a in line["Variants"]])
            responses.append(float(line["Fitness"]))

    return sequences, responses
