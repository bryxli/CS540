import csv
import sys
import matplotlib.pyplot as plt
import numpy as np

def q2_visualize_data(filename):
    with open(filename,'r',newline='') as file:
        data = list(csv.reader(file))
        Y,hat_beta = q3_linear_regression(data)
        xs = []
        for x in data:
            if data.index(x) > 0:
                xs.append(x[0])
        plt.plot(xs,Y)
        plt.xlabel('Year')
        plt.ylabel('Number of frozen days')
        plt.savefig('plot.jpg')
        return hat_beta

def q3_linear_regression(data):
        X = q3_a(data)
        Y = q3_b(data)
        Z = q3_c(X)
        I = q3_d(Z)
        PI = q3_e(I,X)
        hat_beta = q3_f(PI,Y)
        q4_prediction(hat_beta)
        q5_model_interpretation(hat_beta)
        q6_model_limitation(hat_beta)
        return Y,hat_beta

def q3_a(data):
    X = []
    for x in data:
        if data.index(x) > 0:
            X.append([1,int(x[0])])
    print("Q3a:")
    print(X)
    return X

def q3_b(data):
    Y = []
    for y in data:
        if data.index(y) > 0:
            Y.append(int(y[1]))
    print("Q3b:")
    print(Y)
    return Y

def q3_c(X):
    X_transpose = np.transpose(X)
    Z = np.dot(X_transpose,X)
    print("Q3c:")
    print(Z)
    return Z

def q3_d(Z):
    I = np.linalg.inv(Z)
    print("Q3d:")
    print(I)
    return I

def q3_e(I,X):
    PI = np.dot(I,np.transpose(X))
    print("Q3e:")
    print(PI)
    return PI

def q3_f(PI,Y):
    hat_beta = np.dot(PI,Y)
    print("Q3f:")
    print(hat_beta)
    return hat_beta

def predict(hat_beta, year):
    return hat_beta[0] + hat_beta[1] * year

def q4_prediction(hat_beta):
    y_test = predict(hat_beta,2021)
    print("Q4: " + str(y_test))
    return y_test

def q5_model_interpretation(hat_beta):
    if hat_beta[1] > 0:
        print('Q5a: >')
        print('Q5b: There will be more ice days in 2021-22.')
    elif hat_beta[1] < 0:
        print('Q5a: <')
        print('Q5b: There will be less ice days in 2021-22.')
    else:
        print('Q5a: =')
        print('Q5b: There will be about the same number of ice days in 2021-22.')

def q6_model_limitation(hat_beta):
    x_star = -hat_beta[0] / hat_beta[1]
    print('Q6a: ' + str(x_star))
    print('Q6b: This is a compelling prediction because it predicts that at ~2456, there will no longer be frozen days. This matches current trends with less ice days every year. Eventually, if ice days decrease every year, that number will eventually hit zero.')

if __name__=="__main__":
    q2_visualize_data(sys.argv[1])