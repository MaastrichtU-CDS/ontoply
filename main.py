# -*- coding: utf-8 -*-

import os
from owlready2 import *
from src.sub_ontology import SubOntology


if __name__ == '__main__':
    # Load NCIT ontology
    cwd = os.getcwd()
    path = os.path.join(cwd, 'ontologies')
    onto_path.append(path)
    ncit = get_ontology('ncit.owl')
    ncit.load()

    # Create sub-ontology
    subonto_iri = 'http://test.org/onto.owl'
    subonto = SubOntology(ontology=ncit, subonto_iri=subonto_iri)

    # Extract concept from main ontology and add to sub-ontology
    concept_label = 'Marital Status'
    subonto.add_concept(concept_label)

    # Save sub-ontology extracted
    output_file = os.path.join(path, 'subonto.owl')
    output_format = 'rdfxml'
    subonto.save(output_file, output_format)
