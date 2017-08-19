from sklearn.svm import SVR
import numpy as np
n_samples, n_features = 10, 5
#np.random.seed(0)
y = np.random.randn(n_samples)
print type(y)
X = np.random.randn(n_samples, n_features)
clf = SVR(C=1.0, epsilon=0.2)
clf.fit(X, y)

print X
print y

print clf.predict(np.random.randn(n_features))
print clf.predict(np.random.randn(n_features))
