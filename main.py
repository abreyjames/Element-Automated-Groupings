"""This module contains the function's business logic.

Use the automation_context module to wrap your function in an Automate context helper.
"""

from pydantic import Field, SecretStr
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)
from specklepy.objects.geometry import Base

from computations.beam_categories import Line, Node, classify_line_orientation
from flatten import flatten_base
from project.project import Project


class FunctionInputs(AutomateBase):
    """These are function author-defined values.

    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    # TODO: Add the inputs to the automate function here
    # results_model_name: str = Field(
    #     ...,
    #     title="Branch name of the results model to send the classified data too.",
    # )

    # TODO: Add the inputs to the automate function here
    test_input_name: str = Field(
        ...,
        title="Test Input",
    )

    # TODO: remove... An example of how to use secret values.
    whisper_message: SecretStr = Field(title="This is a secret message")
    forbidden_speckle_type: str = Field(
        title="Forbidden speckle type",
        description=(
            "If a object has the following speckle_type,"
            " it will be marked with an error."
        ),
    )


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    # Step 1: get input of the submodel to send the results too
    # EG. Analytical to Geometric Coordination
    commit = automate_context.receive_version()
    model_element = commit["@Model"]

    elements = getattr(model_element, "elements", None)

    if not elements:
        raise Exception
        # show the user if there are any elements

    # There could be surfaces too!!! using the speckle type to filter between surfaces and 1D
    for element in elements:
        baseLine = element.baseLine

        start_node = Node(baseLine.start.id, baseLine.start.x,
                          baseLine.start.y, baseLine.start.z)
        end_node = Node(baseLine.end.id, baseLine.end.x,
                        baseLine.end.y, baseLine.end.z)
        line = Line(baseLine.id, start_node, end_node)

        classification = classify_line_orientation(line)
        print(classification)

        element["classification"] = classification

        # Get the shape
        section_name = element.property.name

        # run mesh function for the shape

        # Return the mesh to the speckle data

        # override the element.displayValue with mesh value (don't worry about colour)

    speckle_results_model = Project(automate_context.speckle_client,
                                    automate_context.automation_run_data.project_id,
                                    # function_inputs.results_model)
                                    "sap/classified_results")
    speckle_results_model.get_results_model()

    commit_object = Base()
    commit_object["elements"] = elements

    speckle_results_model.send_results_model(commit_object)


def automate_function_without_inputs(automate_context: AutomationContext) -> None:
    """A function example without inputs.

    If your function does not need any input variables,
     besides what the automation context provides,
     the inputs argument can be omitted.
    """
    pass


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference; do not invoke it!

    # Pass in the function reference with the inputs schema to the executor.
    execute_automate_function(automate_function, FunctionInputs)

    # If the function has no arguments, the executor can handle it like so
    # execute_automate_function(automate_function_without_inputs)
