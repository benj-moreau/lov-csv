import csv
import argparse

from hdt import HDTDocument

OWL_CLASS = "http://www.w3.org/2002/07/owl#Class"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

try:
    LOV = HDTDocument("lov_hdt/lov.hdt")
except RuntimeError:
    raise RuntimeError("LOV dump not found: Put lov dump into lov_hdt/ folder")


def generate_classes_dataset():
    return


def generate_properties_dataset():
    return


def main():
    parser = argparse.ArgumentParser(prog='lovcsv', description='LOV rdf to csv')
    parser.add_argument('properties_or_classes', metavar='PC', type=str, nargs='+',
                        help='select the csv dataset to generate')
    args = parser.parse_args()
    dataset = args.properties_or_classes[0]
    if dataset == "classes":
        generate_classes_dataset()
    else:
        generate_properties_dataset()


if __name__ == "__main__":
    main()
