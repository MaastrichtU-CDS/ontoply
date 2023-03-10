# -*- coding: utf-8 -*-

import types
from owlready2 import *


class SubOntology:
    """ Extract subsets from ontologies
    """
    def __init__(self, ontology: Ontology, subonto_iri: str) -> None:
        """ Initialising class

        Parameters
        ----------
        ontology : owlready2 ontology
            Original ontology loaded with owlready2
        subonto_iri : str
            Namespace for sub-ontology
        """
        self.ontology = ontology
        self.subonto_iri = subonto_iri
        self.subonto = get_ontology(subonto_iri)  # Create empty ontology

    def _add_parents(self, concept: ThingClass) -> None:
        """ Add parent classes of desired concept to sub-ontology

        Parameters
        ----------
        concept : owlready2 entity
        """

        # Get parent classes in order, reverse array to start with root class,
        # and remove unnecessary classes (object, Thing and itself)
        parents = list(concept.mro())[::-1][2:-1]

        # Loop through parent classes to add them
        with self.subonto:
            if len(parents) > 0:
                for i, parent in enumerate(parents):
                    parent_class = Thing if i == 0 else \
                        self.subonto[parents[i-1].name]
                    types.new_class(parent.name, (parent_class,))
                    self.subonto[parent.name].label = parent.label[0]

    def _add_class(self, concept: ThingClass, parents: bool = True) -> None:
        """ Add desired concept to sub-ontology

        Parameters
        ----------
        concept : owlready2 entity
        parents : bool
            Whether parent classes were added to chain, default to True
        """
        if parents:
            parent_class = list(concept.mro())[1]  # First item is the concept
        else:
            parent_class = Thing
        with self.subonto:
            types.new_class(concept.name, (parent_class,))
            self.subonto[concept.name].label = concept.label[0]

    def _add_children(self, concept: ThingClass) -> None:
        """ Add children classes of desired concept to sub-ontology

        Parameters
        ----------
        concept : owlready2 entity
            Parent concept
        """
        self.children = list(concept.subclasses())
        with self.subonto:
            if len(self.children) > 0:
                for child in self.children:
                    types.new_class(child.name, (self.subonto[concept.name],))
                    self.subonto[child.name].label = child.label[0]

    def add_concept(
            self, concept_label: str,
            parents: bool = True, children: bool = True
    ) -> None:
        """ Run steps to add a concept to sub-ontology, which includes adding
        the concept itself, its parent classes, and its children classes

        Parameters
        ----------
        concept_label : str
            Human-readable label for the concept
        parents : bool
            Whether to add parent classes, default to True
        children : bool
            Whether to add children classes, default to True
        """

        # Get concept entity searching by its label
        concept = self.ontology.search(label=concept_label)[0]

        # Runs steps to add concept
        if parents:
            self._add_parents(concept)
        self._add_class(concept, parents)
        if children:
            self._add_children(concept)

    def add_concepts_list(
            self, concepts_list: list,
            parents: bool = True, children: bool = True
    ) -> None:
        """ Loop through list with concepts and add one-by-one

        Parameters
        ----------
        concepts_list : list
            List with human-readable labels for concepts
        parents : bool
            Whether to add parent classes, default to True
        children : bool
            Whether to add children classes, default to True
        """
        for concept in concepts_list:
            self.add_concept(concept, parents, children)

    def save(self, output_file: str, output_format: str) -> None:
        """ Save sub-ontology to a file

        Parameters
        ----------
        output_file : str
            Name and path of output file
        output_format : str
            Format of output file
        """
        self.subonto.save(file=output_file, format=output_format)

        # Changing namespace of sub-ontology forcefully in the output
        # TODO: should be possible to achieve this before saving?
        new_iri = self.ontology.base_iri[:-1]  # Removing # sign from IRI end
        with open(output_file, 'r') as file:
            content = file.read()
            content = content.replace(self.subonto_iri, new_iri)
        with open(output_file, 'w') as file:
            file.write(content)
