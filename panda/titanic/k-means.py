import random
from patsy import dmatrices
import pandas as pd
import numpy as np


def fixup_with_median(population, column):
    median_ages = np.zeros((2, 3))
    sex = ['male', 'female']

    for i in range(0, 2):
        for j in range(0, 3):
            median_ages[i, j] = population[(population['Sex'] == sex[i]) & \
                                           (population['Pclass'] == j + 1)][column].dropna().median()

    for i in range(0, 2):
        for j in range(0, 3):
            population.loc[
                (population.Age.isnull()) & (population.Sex == sex[i]) & (population.Pclass == j + 1), column] = \
                median_ages[i, j]


def distance(a, b, columns):
    d = 0
    for c in columns:
        d += abs(a[c] - b[c])
    return d / len(columns)


def to_terminal(group, target_column):
    outcomes = group[target_column].value_counts()
    max = outcomes.keys()[0]
    return max


def find_best(points, row):
    bd = None
    bg = None
    for i in range(len(points)):
        p = points.iloc[i]
        d = distance(p, row, columns)
        if bd is None or d < bd:
            bd = d
            bg = i
    return bg, points.iloc[bg]

def kmeans(population, columns, k):
    points = population.sample(k)
    groups = {}
    pgroups = {}
    g = {}
    pg = {}
    changed = True

    for i in range(len(points)):
        pgroups[i] = None
        pg[i] = []

    while changed:
        changed = False

        for i in range(len(points)):
            groups[i] = []
            g[i] = []

        for r in range(len(population)):
            row = population.iloc[r]
            bg, _ = find_best(points, row)
            groups[bg].append(row)
            g[bg].append(row.name)

        for i in range(len(points)):
            df = pd.DataFrame(groups[i])
            points[i] = df.mean()
            for c in df.columns:
                if c not in columns:
                    points[i][c] = to_terminal(df, c)

        for i in range(len(points)):
            if len(pg[i]) != len(g[i]):
                changed = True
            elif ''.join(map(str,sorted(pg[i]))) != ''.join(map(str,sorted(g[i]))):
                changed = True
            pg[i] = list(g[i])
            pgroups[i] = pd.DataFrame(groups[i])
            print('group %d has size: %d' % (i, len(groups[i])))

    return points, pgroups.values()


def gini_index_for_group(population, group, target_column):
    if len(group) == 0:
        return 0

    group_size = len(group)
    population_size = len(population)
    weight = group_size / population_size
    values = group[target_column].unique()
    index = 0

    for v in values:
        proportion = len(group[group[target_column] == v]) / group_size
        index += proportion * proportion

    return (1 - index) * weight


def gini_index(population, groups, target_column):
    index = 0
    for g in groups:
        index += gini_index_for_group(population, g, target_column)
    return index


def gmeans(population, columns, max = 10):
    best = None
    best_pts = None

    for k in range(2, max+1):
        pts, grp = kmeans(population, columns, k)
        print(pts)
        #print(grp)
        gindex = gini_index(population, grp, 'Survived')
        if best is None or gindex < best:
            best = gindex
            best_pts = pts

    return best_pts

df = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

# Cleanup training data
fixup_with_median(df, 'Age')
df = df.drop(['Ticket', 'Cabin'], axis=1)
formula = 'Survived ~ C(Pclass) + C(Sex) + Age + SibSp + Parch + C(Embarked)'
y, x = dmatrices(formula, data=df, return_type='dataframe')
z = x.join(y)
z = z.drop('Intercept', axis=1)

# Cleanup test data
fixup_with_median(test_data, 'Age')
test_data['Survived'] = 2
formula_test = 'Survived ~ PassengerId + C(Pclass) + C(Sex) + Age + SibSp + Parch + C(Embarked)'
_, t = dmatrices(formula_test, data=test_data, return_type='dataframe')

columns = z.columns.drop('Survived')
pts = gmeans(z, columns)


t['Survived'] = t.apply(lambda x: find_best(pts, x)[1].Survived, axis=1)
t[['PassengerId', 'Survived']].to_clipboard(sep=',', index=False)