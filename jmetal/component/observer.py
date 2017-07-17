import logging
import os

from jmetal.util.observable import Observer
from jmetal.util.solution_list_output import SolutionListOutput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicAlgorithmObserver(Observer):
    def __init__(self, frequency: float = 1.0) -> None:
        self.display_frequency = frequency

    def update(self, *args, **kwargs):
        evaluations = kwargs["evaluations"]
        population = kwargs["population"]

        if (evaluations % self.display_frequency) == 0:
            logger.info("Evaluations: " + str(evaluations) +
                        ". Best fitness: " + str(population[0].objectives) +
                        ". Worst fitness: " + str(population[len(population)-1].objectives))


class WriteFrontToFileObserver(Observer):
    def __init__(self, output_directory) -> None:
        self.counter = 0
        self.directory = output_directory

        if os.path.isdir(self.directory):
            logger.info("Directory " + self.directory + " exists. Removing contents.")
            for file in os.listdir(self.directory):
                os.remove(self.directory + "/" + file)
        else:
            logger.info("Directory " + self.directory + " does not exist. Creating it.")
            os.mkdir(self.directory)

    def update(self, *args, **kwargs):
        SolutionListOutput.print_function_values_to_file(
            self.directory + "/FUN." + str(self.counter), kwargs["population"])

        self.counter += 1


class AlgorithmObserver(Observer):
    def __init__(self, animation_speed: float, frequency: float = 1.0) -> None:
        self.animation_speed = animation_speed
        self.display_frequency = frequency

    def update(self, *args, **kwargs):
        evaluations = kwargs["evaluations"]
        population = kwargs["population"]
        computing_time = kwargs["computing time"]

        if (evaluations % self.display_frequency) == 0:
            SolutionListOutput.plot_scatter_real_time(population, evaluations, computing_time,
                                                      self.animation_speed)
