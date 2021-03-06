# """
# This script contains the function generated by cvxopt package.
# 1 The Logistic function is to solve the logistic lasso (L1) regression problem with only feature and labels (No comparison included).
# 2 The Log_Log is to solve logistic lasso (L1) regression with Bradley Terry comparison model.
# 3 The SVM_Log function is to solve SVM for absolute labels and Logistic regression for comparison labels.


from cvxopt import solvers, matrix, spdiag, log, exp, div, spmatrix
import numpy as np
import cvxopt.modeling as cvm
import sys
from sklearn.linear_model import LogisticRegression
def Logistic(absDataOrigin,absLabels, lamda,alpha=1):
    # This function uses both absolute label data and comparison data to train the logistic regression model.
    # Equation: min_{beta, const} sum(logisticLoss(absData))+lamda*norm(beta,1)

    # Parameter:
    # ------------
    # absDataOrigin : N by d numpy matrix where N the number of absolute label data and d is the dimension of data
    # abslabels : (N,) numpy array, +1 means positive label and -1 represents negative labels
    # lamda : weight on L1 penalty. Large lamda would have more zeros in beta.

    # Return:
    # ------------
    # beta : the logistic regression model parameter
    # const : the logistic regression global constant.

    absN,d = np.shape(absDataOrigin)
    absData = np.concatenate((np.array(absDataOrigin),np.ones([absN,1])),axis = 1)
#   A : y_i * x_i since y_i is a scalar
    A = np.multiply(absLabels.T, absData.T).T #absData must be in N, d matrix, and absLabels must be in (N,1) or (N,) matrix
    A = matrix(A)
    def F(x=None, z=None):
        # beta without constant x[:d], constant x[d], t = x[d+1:]
        if x is None: return 2 * d, matrix(0.0,(2*d+1,1)) # m = 2 *d is the number of constraints
        e = A*x[:d+1] # 0 - d contains the constant
        w = exp(e)
        f = matrix(0.0,(2*d+1,1))
        f[0] = alpha*(-sum(e) + sum(log(1+w))) + lamda * sum(x[d+1::])# from d+1 withou the constant
        f[1:d+1] = x[:d] - x[d+1:] # beta - t < 0
        f[d+1:] = -x[:d] - x[d+1:] # -beta - t <0
        Df = matrix(0.0,(2*d+1,2*d+1))
        # Df[0,:d+1] = (matrix(A.T * (div(w,1+w)-1.0))).T
        Df[0, :d + 1] = alpha*(matrix(A.T * (div(w, 1 + w) - 1.0))).T
        Df[0,d+1:] = lamda
        Df[1:d+1,0:d] = spdiag(matrix(1.0,(d,1)))
        Df[d+1:, 0:d] = spdiag(matrix(-1.0,(d,1)))
        Df[1:d+1,d+1:] = spdiag(matrix(-1.0,(d,1)))
        Df[d+1:,d+1:] = spdiag(matrix(-1.0,(d,1)))
        if z is None: return f ,Df
        H = matrix(0.0,(2*d+1,2*d+1))
        H[0:d+1,0:d+1] =  alpha*(A.T *spdiag(div(w, (1 + w) ** 2)) * A)
        return f, Df, z[0]*H
    solvers.options['show_progress'] = False
    sol = solvers.cp(F)
    beta, const = sol['x'][0:d], sol['x'][d]
    return beta, const








def Log_Log(absDataOrigin,absLabels,cmpDataOrigin,cmpLabels, absWeight, lamda):
# This function uses both absolute label data and comparison data to train the logistic regression model.
# The comparison data and label must be included.
# Equation: min_{beta, const} alpha*sum(logisticLoss(absData))+(1-alpha)*sum(logisticLoss(cmpData))+lamda*norm(beta,1)

# Parameter:
# ------------
# absDataOrigin : N by d numpy matrix where N the number of absolute label data and d is the dimension of data
# abslabels : (N,) numpy array, +1 means positive label and -1 represents negative labels
# cmpDataOrigin : N by d numpy matrix where N the number of comparion label data and d is the dimension of data
# cmpLabels : (N,) numpy array, +1 means positive label and -1 represents negative labels
# absWeight : the Weight on absolute label data. And (1-absWeight) would be the weight on comparison data.
# lamda : weight on L1 penalty. Large lamda would have more zeros in beta.
# normalizeWeight : binary value. 1 describes the normalize factor on  the absWeight and cmpWeight by its number of data.
#                   0 shows no normalied factor happen.

# Return:
# ------------
# beta : the logistic regression model parameter
# const : the logistic regression global constant.

    absN,d = np.shape(absDataOrigin)
    cmpN,_ = np.shape(cmpDataOrigin)
    cmpWeight = 1.0 - absWeight
    if cmpWeight == 1:
        mdl = LogisticRegression(penalty='l1', C=1. / lamda)
        mdl.fit(cmpDataOrigin, cmpLabels)
        beta = mdl.coef_.T
        const = mdl.intercept_
        return beta, const
    elif absWeight == 1:
        mdl = LogisticRegression(penalty='l1', C=1. / lamda)
        mdl.fit(absDataOrigin, absLabels)
        beta = mdl.coef_.T
        const = mdl.intercept_
        return beta, const
    else:
        absData = np.concatenate((np.array(absDataOrigin),np.ones([absN,1])),axis = 1)
        cmpData = np.concatenate((np.array(cmpDataOrigin),np.ones([cmpN,1])),axis=1)
        #   A : y_i * x_i since y_i is a scalar
        absA = np.multiply(absLabels, absData.T).T # absData must be in N, d matrix, and absLabels must be in (N,1) or (N,) matrix
        absA = matrix(absA)
        cmpA = np.multiply(cmpLabels, cmpData.T).T # absData must be in N, d matrix, and absLabels must be in (N,1) or (N,) matrix
        cmpA = matrix(cmpA)
        def F(x=None, z=None):
            # beta without constant x[:d], constant x[d], t = x[d+1:]
            if x is None: return 2 * d, matrix(0.0,(2*d+1,1)) # m = 2 *d is the number of constraints
            absE = absA*x[:d+1] # 0 - d contains the constant
            absW = exp(absE)
            cmpE = cmpA*x[:d+1]
            cmpW = exp(cmpE)
            f = matrix(0.0,(2*d+1,1))
            f[0] = absWeight*(-sum(absE) + sum(log(1+absW))) + cmpWeight*(-sum(cmpE) + sum(log(1+cmpW))) + lamda * sum(x[d+1:])# from d+1 withou the constant
            f[1:d+1] = x[:d] - x[d+1:] # beta - t < 0
            f[d+1:] = -x[:d] - x[d+1:] # -beta - t <0
            Df = matrix(0.0,(2*d+1,2*d+1))
            Df[0,:d+1] = absWeight*(matrix(absA.T * (div(absW,1+absW)-1.0))).T + cmpWeight*(matrix(cmpA.T * (div(cmpW,1+cmpW)-1.0))).T
            Df[0,d+1:] = lamda
            Df[1:d+1,0:d] = spdiag(matrix(1.0,(d,1)))
            Df[d+1:, 0:d] = spdiag(matrix(-1.0,(d,1)))
            Df[1:d+1,d+1:] = spdiag(matrix(-1.0,(d,1)))
            Df[d+1:,d+1:] = spdiag(matrix(-1.0,(d,1)))
            if z is None: return f ,Df
            H = matrix(0.0,(2*d+1,2*d+1))
            H[0:d+1,0:d+1] = absWeight*(absA.T *spdiag(div(absW, (1 + absW) ** 2)) * absA) + cmpWeight*(cmpA.T *spdiag(div(cmpW, (1 +cmpW) ** 2)) * cmpA)
            return f, Df, z[0]*H
        solvers.options['show_progress'] = False
        sol = solvers.cp(F)
        beta, const = sol['x'][0:d], sol['x'][d]
        return beta, const

def SVM_Log(absDataOrigin,absLabels,cmpDataOrigin,cmpLabels, absWeight, lamda,cmpIgnore=False):
# This function uses both absolute label data to train the SVM primal model and comparison data is using Bradley-Terry model.
# The comparison data and label must be included.
# Equation:

# Parameter:
# ------------
# absDataOrigin : N by d numpy matrix where N the number of absolute label data and d is the dimension of data
# abslabels : (N,) numpy array, +1 means positive label and -1 represents negative labels
# cmpDataOrigin : N by d numpy matrix where N the number of comparion label data and d is the dimension of data
# cmpLabels : (N,) numpy array, +1 means positive label and -1 represents negative labels
# absWeight : the Weight on absolute label data. And (1-absWeight) would be the weight on comparison data.
# lamda : weight on L1 penalty. Large lamda would have more zeros in beta.
# cmpIgnore : boolean variable. If True, the function will completely ignore the comparison data and labels. Please let them be None when input. And absWeight will be 1.

# Return:
# ------------
# beta : the SVM model parameter
# const : the SVM global constant.
    if cmpIgnore is True:
        # This component is currently wrong. Guess it is not satisfied the CVXOPT assumptions.
        absWeight = 1
        absN, d = np.shape(absDataOrigin)
        absData = np.concatenate((np.array(absDataOrigin), np.ones([absN, 1])), axis=1)
        # y_i times x_i and y_i is a scalar number
        absA = np.multiply(absLabels,absData.T).T  # absData must be in N, d matrix, and absLabels must be in (N,1) or (N,) matrix
        absA = matrix(absA)
        def F(x=None, z=None):
            # The cvxopt matrix slicing does not include the last number.
            # x[0:d] is beta; x[d] is const; x[d+1:2*d+1] is t ; x[2*d+1:] is zeta
            if x is None: return 2 * d + 2*absN, matrix(0.0, (2*d+1+absN, 1))
            absS = absA * x[:d + 1]  # 0 - d contains the constant. Absolute label scores.
            f = matrix(0.0,(2*d+1+2*absN,1))
            f[0] = absWeight*sum(x[2*d+1:]) + lamda * sum(x[d+1:2*d+1])
            f[1: d + 1] = x[:d] - x[d+1:2*d+1]  # beta - t <= 0
            f[d + 1: 2*d+1] = -x[:d] - x[d+1:2*d+1]  # -beta - t <= 0
            f[2*d+1:2*d+1+absN] = -absS-x[2*d+1:]+1 # -y_i(beta.T*x_i)-zeta_i+1 <=0
            f[2*d+1+absN:] = -x[2*d+1:]
            Df = matrix(0.0, (2*d+1+2*absN, 2*d+1+absN))
            Df[0, d+1 : 2*d+1] = lamda
            Df[0, 2*d+1:] = absWeight
            Df[1 : d+1, 0:d] = spdiag(matrix(1.0, (d, 1)))
            Df[d+1: 2*d+1, 0:d] = spdiag(matrix(-1.0, (d, 1)))
            Df[1 : d+1, d+1 : 2*d+1] = spdiag(matrix(-1.0, (d, 1)))
            Df[d+1 : 2*d+1, d+1 : 2*d+1] = spdiag(matrix(-1.0, (d, 1)))
            Df[2*d+1:2*d+1+absN, 0:d+1] = -absA
            Df[2*d+1:2*d+1+absN , 2*d+1:] = spdiag(matrix(-1.0,(absN,1)))
            Df[2*d+1+absN:,2*d+1:] = spdiag(matrix(-1.0,(absN,1)))
            if z is None: return f, Df
            H = matrix(0.0, (2*d+1+absN, 2*d+1+absN))
            return f, Df, z[0] * H
        solvers.options['show_progress'] = False
        sol = solvers.cp(F)
        beta, const = sol['x'][0:d], sol['x'][d]
        return beta, const
    else:
        if absWeight>1.0 or absWeight<0.0: sys.exit('The absWeight must be in [0.0, 1.0]')
        cmpWeight = 1.0 - absWeight
        absN, d = np.shape(absDataOrigin)
        cmpN, _ = np.shape(cmpDataOrigin)
        absData = np.concatenate((np.array(absDataOrigin), np.ones([absN, 1])), axis=1)
        cmpData = np.concatenate((np.array(cmpDataOrigin), np.ones([cmpN, 1])), axis=1)
        # y_i times x_i and y_i is a scalar number
        absA = np.multiply(absLabels,absData.T).T  # absData must be in N, d matrix, and absLabels must be in (N,1) or (N,) matrix
        absA = matrix(absA)
        cmpA = np.multiply(cmpLabels,cmpData.T).T  # absData must be in N, d matrix, and absLabels must be in (N,1) or (N,) matrix
        cmpA = matrix(cmpA)
        def F(x=None, z=None):
            # The cvxopt matrix slicing does not include the last number.
            # x[0:d] is beta; x[d] is const; x[d+1:2*d+1] is t ; x[2*d+1:] is zeta
            if x is None: return 2 * d + 2*absN, matrix(0.0, (2*d+1+absN, 1))
            absS = absA * x[:d + 1]  # 0 - d contains the constant. Absolute label scores.
            cmpE = cmpA * x[:d + 1]
            cmpW = exp(cmpE)
            f = matrix(0.0,(2*d+1+2*absN,1))
            f[0] = absWeight*sum(x[2*d+1:])+ cmpWeight*(-sum(cmpE) + sum(log(1+cmpW))) + lamda * sum(x[d+1:2*d+1])
            f[1: d + 1] = x[:d] - x[d+1:2*d+1]  # beta - t <= 0
            f[d + 1: 2*d+1] = -x[:d] - x[d+1:2*d+1]  # -beta - t <= 0
            f[2*d+1:2*d+1+absN] = -absS-x[2*d+1:]+1 # -y_i(beta.T*x_i)-zeta_i+1 <=0
            f[2*d+1+absN:] = -x[2*d+1:]
            Df = matrix(0.0, (2*d+1+2*absN, 2*d+1+absN))
            Df[0, 0:d+1] =  cmpWeight * (matrix(cmpA.T * (div(cmpW, 1 + cmpW) - 1.0))).T
            Df[0, d+1 : 2*d+1] = lamda
            Df[0, 2*d+1:] = absWeight
            Df[1 : d+1, 0:d] = spdiag(matrix(1.0, (d, 1)))
            Df[d+1: 2*d+1, 0:d] = spdiag(matrix(-1.0, (d, 1)))
            Df[1 : d+1, d+1 : 2*d+1] = spdiag(matrix(-1.0, (d, 1)))
            Df[d+1 : 2*d+1, d+1 : 2*d+1] = spdiag(matrix(-1.0, (d, 1)))
            Df[2*d+1:2*d+1+absN, 0:d+1] = -absA
            Df[2*d+1:2*d+1+absN , 2*d+1:] = spdiag(matrix(-1.0,(absN,1)))
            Df[2*d+1+absN:,2*d+1:] = spdiag(matrix(-1.0,(absN,1)))
            if z is None: return f, Df
            H = matrix(0.0, (2*d+1+absN, 2*d+1+absN))
            H[0:d + 1, 0:d + 1] =  cmpWeight * (cmpA.T * spdiag(div(cmpW, (1 + cmpW) ** 2)) * cmpA)
            return f, Df, z[0] * H
        solvers.options['show_progress'] = False
        sol = solvers.cp(F)
        beta, const = sol['x'][0:d], sol['x'][d]
        return beta, const


