import pandas as pd
import argparse
parser = argparse.ArgumentParser(description="Converts csv files to json files.")
parser.add_argument("--input", "-i", help="Input CSV")
parser.add_argument("--output", "-o",help="Output JSON")
args = parser.parse_args()
csv_file = pd.DataFrame(pd.read_csv(args.input, sep = ",", header = 0, index_col = False))
csv_file.to_json(args.output, orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)