from dataclasses import dataclass
import trimesh
import numpy as np
from specklepy.objects.geometry import Base
from utils.colors import Color
from utils.units import Convert
from utils.mesh import trimesh_to_speckle_mesh

@dataclass
class DisplayMeshes:
    reference: 'Mesh'
    utilisation: 'Mesh'


class ElementVisualizer:
    def __init__(self, element: 'Element', units: 'ModelUnits'):
        self.element = element
        self.start_point = np.array([
            Convert.length(element.baseLine.start.x,
                           input_unit=units.length_unit),
            Convert.length(element.baseLine.start.y,
                           input_unit=units.length_unit),
            Convert.length(element.baseLine.start.z,
                           input_unit=units.length_unit)
        ])
        self.end_point = np.array([
            Convert.length(element.baseLine.end.x,
                           input_unit=units.length_unit),
            Convert.length(element.baseLine.end.y,
                           input_unit=units.length_unit),
            Convert.length(element.baseLine.end.z,
                           input_unit=units.length_unit)
        ])
        self.width = Convert.length(
            element.property.profile.width, input_unit=units.length_unit)
        self.depth = Convert.length(
            element.property.profile.depth, input_unit=units.length_unit)

    def __str__(self):
        return (f"ElementVisualizer for Element ID: {self.element.id}, Name: {self.element.name}\n"
                f"Start Point: {self.start_point}\n"
                f"End Point: {self.end_point}\n"
                f"Width: {self.width}\n"
                f"Depth: {self.depth}")
    
    def sort_line_orientation(self):
        if self.start_point[2] > self.end_point[2]:
            self.start_point, self.end_point = self.end_point, self.start_point

    def create_element_mesh(self):
        self.sort_line_orientation()
        direction = self.end_point - self.start_point
        length = np.linalg.norm(direction)

        # Create a box centered at the origin
        box = trimesh.creation.box((self.width, self.depth, length))

        # Calculate the midpoint of the column
        midpoint = (self.start_point + self.end_point) / 2

        # Calculate the rotation to align the box with the column direction
        rotation_matrix = trimesh.geometry.align_vectors([0, 0, 1], direction)

        # Apply rotation and translation to place the box at the correct position
        box.apply_transform(rotation_matrix)
        box.apply_translation(midpoint)

        return box

    def visualize(self):
        element_mesh = trimesh_to_speckle_mesh(
            self.create_element_mesh(), 0.6, Color.Highlight)
        return element_mesh

    def prepare_commit(self, attributes: dict):
        self.column.speckle_object.displayValue = self.column.display_meshes.reference
        designResults = Base()
        for key, value in attributes.items():
            designResults[key] = value
        for section, calculations_steps in self.column.design_results.calculation_log.items():
            designResults[section] = {}
            for step in calculations_steps:
                if step.unit != '':
                    designResults[section][f'{step.symbol} ({step.unit})'] = round(
                        step.value, 2)
                else:
                    designResults[section][step.symbol] = round(step.value, 2)
        designResults.displayValue = self.column.display_meshes.utilisation
        self.column.speckle_object['designResults'] = designResults
        for to_remove in ['baseLine', 'end1Node', 'end2Node', 'end1Offset', 'end2Offset', 'StiffnessModifiers', 'end1Releases', 'end2Releases']:
            delattr(self.column.speckle_object, to_remove)
        return self.column.speckle_object
