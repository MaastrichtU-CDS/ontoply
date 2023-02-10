# -*- coding: utf-8 -*-

import types
from owlready2 import *


class SubOntology:
    def __init__(self, ontology, subonto_iri):
        self.ontology = ontology
        self.subonto_iri = subonto_iri
        self.subonto = get_ontology(subonto_iri)

    def _add_parents(self, concept):
        parents = list(concept.mro())[::-1][1:-1]
        with self.subonto:
            if len(parents) > 1:
                for i, parent in enumerate(parents[1:]):
                    parent_class = Thing if i == 0 else \
                        self.subonto[parents[i].name]
                    types.new_class(parent.name, (parent_class,))
                    self.subonto[parent.name].label = parent.label[0]

    def _add_class(self, concept):
        parents = list(concept.mro())
        with self.subonto:
            parent_class = Thing if len(parents) == 2 else \
                self.subonto[parents[1].name]
            types.new_class(concept.name, (parent_class,))
            self.subonto[concept.name].label = concept.label[0]

    def _add_children(self, concept):
        self.children = list(concept.subclasses())
        with self.subonto:
            if len(self.children) > 0:
                for child in self.children:
                    types.new_class(child.name, (self.subonto[concept.name],))
                    self.subonto[child.name].label = child.label[0]

    def add_concept(self, concept_label):
        concept = self.ontology.search(label=concept_label)[0]
        self._add_parents(concept)
        self._add_class(concept)
        self._add_children(concept)

    def save(self, output_file, output_format):
        self.subonto.save(file=output_file, format=output_format)

        new_iri = self.ontology.base_iri[:-1]
        with open(output_file, 'r') as file:
            content = file.read()
            content = content.replace(self.subonto_iri, new_iri)
        with open(output_file, 'w') as file:
            file.write(content)
