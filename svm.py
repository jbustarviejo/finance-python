
diabetes = datasets.load_diabetes()
for clf in (svm.NuSVR(kernel='linear', nu=.4, C=1.0),
            svm.NuSVR(kernel='linear', nu=.4, C=10.),
            svm.SVR(kernel='linear', C=10.),
            svm.LinearSVR(C=10.),
            svm.LinearSVR(C=10.),
            ):
    clf.fit(diabetes.data, diabetes.target)
    assert_greater(clf.score(diabetes.data, diabetes.target), 0.02)

# non-regression test; previously, BaseLibSVM would check that
# len(np.unique(y)) < 2, which must only be done for SVC
svm.SVR().fit(diabetes.data, np.ones(len(diabetes.data)))
svm.LinearSVR().fit(diabetes.data, np.ones(len(diabetes.data)))
