import random
from dataclasses import dataclass
from typing import List, Optional
import click
import pandas as pd


@dataclass()
class Student:
    name: str
    index: int
    is_alive: bool
    team: Optional[int] = None


def __load_students(path: str) -> List[Student]:
    students_csv = pd.read_csv(path, keep_default_na=False)

    students = [
        Student(name, index, is_alive)
        for name, is_alive, index
        in students_csv.values
    ]

    return list(students)


def __save_students(path: str, students: List[Student]):
    students_as_dict = {
        'name': [student.name for student in students],
        'index': [student.index for student in students],
        'team': [student.team for student in students]
    }

    students_df = pd.DataFrame.from_dict(students_as_dict)
    students_df.to_csv(path)


@click.command()
@click.argument('in_csv', type=click.Path(exists=True))
@click.argument('out_csv', type=click.Path())
@click.argument('random_seed', type=click.STRING)
@click.argument('team_size', type=click.INT)
def main(in_csv: str, out_csv: str, random_seed: str, team_size: int):
    """
    Shuffle student's list and assign them to random teams.

    Parameters
    ----------
    in_csv : [type]
        Input filepath.
    out_csv : [type]
        Output filepath.
    random_seed : str
        Used to initiated shuffle.
    team_size : int
        Target team size.
    """

    students = __load_students(in_csv)
    students = [student for student in students if student.is_alive]

    random.seed(random_seed)
    random.shuffle(students)

    for i, student in enumerate(students):
        student.team = i // 4

    __save_students(out_csv, students)


if __name__ == "__main__":
    main()
