import pandas as pd
import numpy as np
from patsy import dmatrices


def fixup_with_median(population, column):
    median_ages = np.zeros((2, 3))
    sex = ['male', 'female']

    for i in range(0, 2):
        for j in range(0, 3):
            median_ages[i, j] = population[(population['Sex'] == sex[i]) & \
                                          (population['Pclass'] == j + 1)][column].dropna().median()

    for i in range(0, 2):
        for j in range(0, 3):
            population.loc[(population.Age.isnull()) & (population.Sex == sex[i]) & (population.Pclass == j + 1), column] = \
            median_ages[i, j]


def gini_index_for_group(population, group, target_column):
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


def split(population, column, value):
    left = population[population[column] < value]
    right = population[population[column] >= value]
    return left, right


def best_split(population, target_column):
    best_index = 1
    best_column = None
    best_value = None

    for column in population:
        if column == target_column:
            continue
        for i, row in population.iterrows():
            left, right = split(population, column, row[column])
            index = gini_index(population, [left, right], target_column)
            if index < best_index:
                best_column = column
                best_value = row[column]
                best_index = index

    (left, right) = split(population, best_column, best_value)
    return {'column': best_column, 'value': best_value, 'index': best_index, 'left': left, 'right': right}


def to_terminal(group, target_column):
    outcomes = group[target_column].value_counts()
    max = outcomes.keys()[0]
    return max


def node_split(node, target_column, max_depth=3, min_size=50, depth=0):
    left, right = node['left'], node['right']
    del node['left']
    del node['right']

    # check for a no split
    if not len(left) or not len(right):
        node['left'] = node['right'] = to_terminal(left + right, target_column)
        return
    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left, target_column), to_terminal(right, target_column)
        return
    # process left child
    if len(left) <= min_size:
        node['left'] = to_terminal(left, target_column)
    else:
        node['left'] = best_split(left, target_column)
        node_split(node['left'], target_column, max_depth, min_size, depth + 1)
    # process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right, target_column)
    else:
        node['right'] = best_split(right, target_column)
        node_split(node['right'], target_column, max_depth, min_size, depth + 1)


def print_tree(node, depth=0):
    if isinstance(node, dict):
        print('%s[%s < %.3f]' % (depth * ' ', (node['column']), node['value']))
        print_tree(node['left'], depth + 1)
        print_tree(node['right'], depth + 1)
    else:
        print('%s[%s]' % (depth * ' ', node))


def predict_ret(node, row, x):
    if isinstance(node[x], dict):
        return predict(node[x], row)
    else:
        return node[x]


def predict(node, row):
    if row[node['column']] < node['value']:
        return predict_ret(node, row, 'left')
    else:
        return predict_ret(node, row, 'right')


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


root = best_split(z, 'Survived')
node_split(root, 'Survived', max_depth=4)

print_tree(root)

t['Survived'] = t.apply(lambda x: predict(root, x), axis=1)

t[['PassengerId', 'Survived']].to_clipboard(sep=',', index=False)