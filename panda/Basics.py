import random

import pandas as pd
from math import floor


def RandomName():
    firstNames = ["Mike", "Jack", "Dave", "Tim", "Tommy"]
    lastName = ["Smith", "White", "Black"]
    random.shuffle(firstNames)
    random.shuffle(lastName)

    return firstNames[0] + " " + lastName[0]

def CourseName():
    courseNames = ["Math", "French", "Biology", "Music"]

    return courseNames[floor(random.random() * len(courseNames))]

def Score():
    return floor(random.random() * 40) / 2

if __name__ == '__main__':
    Pts = pd.DataFrame([[RandomName(), CourseName(), Score()] for i in range(100)],
        columns=["Student", "Course", "Score"]
    )

    CourseAverage = Pts.groupby(['Course']).mean()
    Students = Pts.groupby(['Course', 'Student']).mean()
    Merged = pd.merge(CourseAverage.reset_index(), Students.reset_index(), on='Course')
    Merged['Pass'] = Merged['Score_x'] > Merged['Score_y']
    Pass = Merged.groupby(['Student', 'Course'])['Pass'].max()

    print(Pass)