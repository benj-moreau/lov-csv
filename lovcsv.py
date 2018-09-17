import csv
import argparse

from hdt import HDTDocument

OWL_CLASS = "http://www.w3.org/2002/07/owl#Class"
RDF_CLASS = "http://www.w3.org/2000/01/rdf-schema#Class"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
LABEL = "http://www.w3.org/2000/01/rdf-schema#label"
COMMENT = "http://www.w3.org/2000/01/rdf-schema#comment"
OCCURENCIES = "http://purl.org/vocommons/voaf#occurrencesInDatasets"
REUSED = "http://purl.org/vocommons/voaf#reusedByDatasets"
SUB_CLASSES = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
EQUIVALENT_CLASSES = "http://www.w3.org/2002/07/owl#equivalentClass"
DEFINED_BY = "http://www.w3.org/2000/01/rdf-schema#isDefinedBy"

OWL_PROPERTY = "http://www.w3.org/2002/07/owl#ObjectProperty"
RDF_PROPERTY = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
DOMAIN = "http://www.w3.org/2000/01/rdf-schema#domain"
RANGE = "http://www.w3.org/2000/01/rdf-schema#range"
SUB_PROPERTY = "http://www.w3.org/2000/01/rdf-schema#subPropertyOf"
EQUIVALENT_PROPERTY = "http://www.w3.org/2000/01/rdf-schema#subPropertyOf"

try:
    LOV = HDTDocument("lov_hdt/lov.hdt")
except RuntimeError:
    raise RuntimeError("LOV dump not found: Put lov dump into lov_hdt/ folder")


def generate_classes_dataset():
    with open('lov_csv/lov_classes.csv', 'w') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['uri', 'label', 'description', 'language', 'occurencies_in_datasets', 'reused_by_datasets', 'sub_classes', 'equivalent_classes', 'defined_by'])
        (classe_triples, cardinality) = LOV.search_triples("", RDF_TYPE, OWL_CLASS)
        (classe_triples2, cardinality2) = LOV.search_triples("", RDF_TYPE, RDF_CLASS)
        hdt_iterators = [classe_triples, classe_triples2]
        already_added_uri = []
        for hdt_iterator in hdt_iterators:
            for classe_triple in hdt_iterator:
                uri_classe = classe_triple[0].encode('utf-8')
                if 'http' in uri_classe and uri_classe not in already_added_uri:
                    already_added_uri.append(uri_classe)
                    sub_classes = []
                    equivalent_classes = []
                    (sub_triples, cardinality) = LOV.search_triples(uri_classe, SUB_CLASSES, "")
                    for sub_triple in sub_triples:
                        if 'http' in sub_triple[2]:
                            sub_classes.append(sub_triple[2].encode('utf-8'))
                    if sub_classes:
                        sub_classes = str(sub_classes)
                    else:
                        sub_classes = ''
                    (equi_triples, cardinality) = LOV.search_triples(uri_classe, EQUIVALENT_CLASSES, "")
                    for equi_triple in equi_triples:
                        if 'http' in equi_triple[2]:
                            equivalent_classes.append(equi_triple[2].encode('utf-8'))
                    if equivalent_classes:
                        equivalent_classes = str(equivalent_classes)
                    else:
                        equivalent_classes = ''
                    (defined_triples, cardinality) = LOV.search_triples(uri_classe, DEFINED_BY, "")
                    defined_by = ''
                    for defined_triple in defined_triples:
                        defined_by = defined_triple[2].replace('"', '').encode('utf-8')
                    (occurences_triples, cardinality) = LOV.search_triples(uri_classe, OCCURENCIES, "")
                    if cardinality > 0:
                        occurencies = int(occurences_triples.next()[2].split('^^')[0].replace('"', ''))
                    else:
                        occurencies = 0
                    (reused_triples, cardinality) = LOV.search_triples(uri_classe, REUSED, "")
                    if cardinality > 0:
                        reused = int(reused_triples.next()[2].split('^^')[0].replace('"', ''))
                    else:
                        reused = 0
                    labels_and_descriptions = {}
                    (label_triples, cardinality) = LOV.search_triples(uri_classe, LABEL, "")
                    for label_triple in label_triples:
                        label, language = split_string_lang(label_triple[2])
                        if language not in labels_and_descriptions:
                            labels_and_descriptions[language] = {}
                        labels_and_descriptions[language]['label'] = label
                    (description_triples, cardinality) = LOV.search_triples(uri_classe, COMMENT, "")
                    for description_triple in description_triples:
                        description, language = split_string_lang(description_triple[2])
                        if language not in labels_and_descriptions:
                            labels_and_descriptions[language] = {}
                        labels_and_descriptions[language]['description'] = description
                    if labels_and_descriptions:
                        for language, value in labels_and_descriptions.iteritems():
                            if 'label' not in value:
                                label = ''
                            else:
                                label = value['label']
                            if 'description' not in value:
                                description = ''
                            else:
                                description = value['description']
                            writer.writerow([uri_classe, label, description, language, occurencies, reused, sub_classes, equivalent_classes, defined_by])
                    else:
                        writer.writerow([uri_classe, '', '', 'undefined', occurencies, reused, sub_classes, equivalent_classes, defined_by])


def generate_properties_dataset():
    with open('lov_csv/lov_properties.csv', 'w') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['uri', 'label', 'description', 'language', 'occurencies_in_datasets', 'reused_by_datasets', 'domain', 'range', 'sub_properties', 'equivalent_properties', 'defined_by'])
        (property_triples, cardinality) = LOV.search_triples("", RDF_TYPE, OWL_PROPERTY)
        (property_triples2, cardinality2) = LOV.search_triples("", RDF_TYPE, RDF_PROPERTY)
        hdt_iterators = [property_triples, property_triples2]
        already_added_uri = []
        for hdt_iterator in hdt_iterators:
            for property_triple in hdt_iterator:
                uri_property = property_triple[0].encode('utf-8')
                if 'http' in uri_property and uri_property not in already_added_uri:
                    already_added_uri.append(uri_property)
                    sub_properties = []
                    equivalent_properties = []
                    (sub_triples, cardinality) = LOV.search_triples(uri_property, SUB_PROPERTY, "")
                    for sub_triple in sub_triples:
                        if 'http' in sub_triple[2]:
                            sub_properties.append(sub_triple[2].encode('utf-8'))
                    if sub_properties:
                        sub_properties = str(sub_properties)
                    else:
                        sub_properties = ''
                    (equi_triples, cardinality) = LOV.search_triples(uri_property, EQUIVALENT_PROPERTY, "")
                    for equi_triple in equi_triples:
                        if 'http' in equi_triple[2]:
                            equivalent_properties.append(equi_triple[2].encode('utf-8'))
                    if equivalent_properties:
                        equivalent_properties = str(equivalent_properties)
                    else:
                        equivalent_properties = ''
                    (defined_triples, cardinality) = LOV.search_triples(uri_property, DEFINED_BY, "")
                    defined_by = ''
                    for defined_triple in defined_triples:
                        defined_by = defined_triple[2].replace('"', '').encode('utf-8')
                    (domain_triples, cardinality) = LOV.search_triples(uri_property, DOMAIN, "")
                    domain = ''
                    for domain_triple in domain_triples:
                        domain = domain_triple[2].replace('"', '').encode('utf-8')
                    (range_triples, cardinality) = LOV.search_triples(uri_property, RANGE, "")
                    p_range = ''
                    for range_triple in range_triples:
                        p_range = range_triple[2].replace('"', '').encode('utf-8')
                    (occurences_triples, cardinality) = LOV.search_triples(uri_property, OCCURENCIES, "")
                    if cardinality > 0:
                        occurencies = int(occurences_triples.next()[2].split('^^')[0].replace('"', ''))
                    else:
                        occurencies = 0
                    (reused_triples, cardinality) = LOV.search_triples(uri_property, REUSED, "")
                    if cardinality > 0:
                        reused = int(reused_triples.next()[2].split('^^')[0].replace('"', ''))
                    else:
                        reused = 0
                    labels_and_descriptions = {}
                    (label_triples, cardinality) = LOV.search_triples(uri_property, LABEL, "")
                    for label_triple in label_triples:
                        label, language = split_string_lang(label_triple[2])
                        if language not in labels_and_descriptions:
                            labels_and_descriptions[language] = {}
                        labels_and_descriptions[language]['label'] = label
                    (description_triples, cardinality) = LOV.search_triples(uri_property, COMMENT, "")
                    for description_triple in description_triples:
                        description, language = split_string_lang(description_triple[2])
                        if language not in labels_and_descriptions:
                            labels_and_descriptions[language] = {}
                        labels_and_descriptions[language]['description'] = description
                    if labels_and_descriptions:
                        for language, value in labels_and_descriptions.iteritems():
                            if 'label' not in value:
                                label = ''
                            else:
                                label = value['label']
                            if 'description' not in value:
                                description = ''
                            else:
                                description = value['description']
                            writer.writerow([uri_property, label, description, language, occurencies, reused, domain, p_range, sub_properties, equivalent_properties, defined_by])
                    else:
                        writer.writerow([uri_property, '', '', 'undefined', occurencies, reused, domain, p_range, sub_properties, equivalent_properties, defined_by])


def split_string_lang(obj):
    splitted_obj = obj.replace('"', '').split('@')
    string = splitted_obj[0].encode('utf-8')
    language = 'undefined'
    if len(splitted_obj) > 1:
        language = splitted_obj[1].encode('utf-8')
    return string, language


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
