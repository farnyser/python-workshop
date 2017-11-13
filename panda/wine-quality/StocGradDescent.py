from math import sqrt
from patsy.highlevel import dmatrices

import pandas as pd

df = pd.read_csv('winequality-white.csv')
formula = "quality ~ density + pH + alcohol + sulphates + chlorides + Q('residual sugar') + Q('fixed acidity')" \
          " + Q('citric acid')" \
          " + Q('volatile acidity')" \
          " + Q('free sulfur dioxide')"
y, x = dmatrices(formula, data=df, return_type='dataframe')
z = x.join(y)
z = z.drop('Intercept', axis=1)
z = (z-z.min())/(z.max()-z.min())

def predict(row, columns, coefficients):
    yhat = coefficients[0]
    for i in range(len(columns)):
        yhat += coefficients[i + 1] * row[columns[i]]
    return yhat


def predict_test(row, target, columns, coefficients):
    p = predict(row, columns, coefficients)
    e = row[target]
    d = p - e
    return p, e, d


def print_prediction(r):
    p, e, d = r
    print("predicted: %f vs expected: %f (error=%f)" % (p, e, d))


def coefficients_sgd(train, target, columns, l_rate=0.01, n_epoch=50):
    coef = [0.0 for _ in range(len(columns)+1)]
    for epoch in range(n_epoch):
        sum_error = 0
        count = 0
        lr = l_rate / sqrt(sqrt(epoch+1))
        for r in range(len(train)):
            row = train.iloc[r]
            __,_,error = predict_test(row, target, columns, coef)
            sum_error += error ** 2
            count += 1
            coef[0] = coef[0] - lr * error
            for i in range(len(columns)):
                coef[i + 1] = coef[i + 1] - lr * error * row[columns[i]]
        print('>epoch=%d, lrate=%.4f, error=%.4f' % (epoch, lr, sqrt(sum_error/count)))
    return coef


columns = z.columns.drop('quality')

# hand made test
coefficients = [0.1] * (1 + len(columns))
print(coefficients)

print_prediction(predict_test(z.iloc[0], 'quality', columns, coefficients))
print_prediction(predict_test(z.iloc[1], 'quality', columns, coefficients))
print_prediction(predict_test(z.iloc[2], 'quality', columns, coefficients))

# sgd
coefficients = coefficients_sgd(z, 'quality', columns)
print(coefficients)

print_prediction(predict_test(z.iloc[0], 'quality', columns, coefficients))
print_prediction(predict_test(z.iloc[1], 'quality', columns, coefficients))
print_prediction(predict_test(z.iloc[2], 'quality', columns, coefficients))
