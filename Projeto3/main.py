from joblib.logger import PrintTime
from numpy.lib.npyio import save
from sklearn.tree import DecisionTreeClassifier, plot_tree # árvore de decisão
from sklearn.neighbors import KNeighborsClassifier # k-NN
from sklearn.model_selection import train_test_split, cross_val_score # cross-validation
from sklearn.preprocessing import StandardScaler # normalização dos atributos
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np 
import matplotlib.pyplot as plt # gráficos
from utilsAA import * # módulo distribuido com o guião com funções auxiliares
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import silhouette_score
from sklearn.metrics import homogeneity_score, make_scorer

raw_data , classes , features ,target = load_data("C:/Users/Utilizador/Desktop/Tudo/1. Trabalhos/UNIVERSIDADE/IAA/Projeto3/heart.csv")
testRaw_data , testFeatures = load_data("C:/Users/Utilizador/Desktop/Tudo/1. Trabalhos/UNIVERSIDADE/IAA/Projeto3/test.csv",testdata=True)

#remover o identificador de pessoa
raw_data = raw_data[:,1:]
features = features[1:]
testRaw_data = testRaw_data[:,1:]
testFeatures = testFeatures[1:]


# codificar atributo Age
raw_data[:,1] = encode_feature(raw_data[:,1])
testRaw_data[:,1] = encode_feature(testRaw_data[:,1]) 
# codificar atributo FastingBS
raw_data[:,5] = encode_feature(raw_data[:,5])
testRaw_data[:,5] = encode_feature(testRaw_data[:,5])
# codificar atributo RestingECG
raw_data[:,6] = encode_feature(raw_data[:,6])
testRaw_data[:,6] = encode_feature(testRaw_data[:,6]) 
# codificar atributo ExerciseAngina
raw_data[:,8] = encode_feature(raw_data[:,8])
testRaw_data[:,8] = encode_feature(testRaw_data[:,8]) 
# codificar atributo ChestPainType
raw_data, features = one_hot_encode_feature(raw_data, 2, features)
testRaw_data, testFeatures = one_hot_encode_feature(testRaw_data, 2, testFeatures)
# codificar atributo ST_slope
raw_data, features = one_hot_encode_feature(raw_data, 9, features)
testRaw_data, testFeatures = one_hot_encode_feature(testRaw_data, 9, testFeatures)

#X_train, X_test, y_train, y_test = train_test_split(raw_data, classes, random_state=50)

#DecisionTreeClassifier
#dtc = DecisionTreeClassifier()
#dtc_parameters={    'criterion' : ["gini", "entropy"],
#                'max_depth': (1,100),
#                'min_samples_leaf': (0,1000),
#                'min_samples_leaf' : (1,1000),
#                'min_weight_fraction_leaf' : (0.0,0.5,0.1)}
#
#grid_search_dtc = GridSearchCV(
#    estimator=dtc,
#    param_grid=dtc_parameters,
#    scoring = 'accuracy',
#    cv=200
#)
#
#grid_search_dtc.fit(X_train, y_train)
#
#y_pred_dtc = grid_search_dtc.predict(X_test)
#print("Com os parametros: ", grid_search_dtc.best_params_)
#print("A arvore de decisão obteve a accuracy: ", grid_search_dtc.best_score_)

#Perceptron
#perceptron = Perceptron(eta0 = 0.9, random_state=1)
#perceptron_parameters = {   'alpha': (0.01,5,0.01),
#                            'max_iter': [10000],
#                            'eta0' :[0.0001, 0.001, 0.01, 0.1, 1.0,10],
#                            'l1_ratio' : (0.01,1,0.01),
#                        }
#
#f1_scorer = make_scorer(f1_score, pos_label="Heart disease") #Normal
#Perceptron_search = GridSearchCV(
#    estimator=perceptron,
#    param_grid=perceptron_parameters,
#    scoring = f1_scorer,
#    cv=200
#)
#
#Perceptron_search.fit(X_train, y_train)
#
#y_pred_Perceptron1 =Perceptron_search.predict(X_test)
#print(Perceptron_search.best_params_ )
#print('Best Score - Perceptron:', Perceptron_search.best_score_ )

#MLPClassifier
#mlp = Pipeline([('classifier' , MLPClassifier())])
#mlp_parameters = [{ 'classifier' : [MLPClassifier()],
#                    'classifier__activation' : ['identity', 'logistic', 'tanh', 'relu'],
#                    'classifier__solver' : ['adam'],
#                    'classifier__learning_rate_init': [0.0001],
#                    'classifier__max_iter': [10000],
#                    'classifier__hidden_layer_sizes': [(x,y,z) for x in range(1,100,5) for y in range(1,100,5) for z in range(1,100,5)],
#                    'classifier__alpha': [0.0001, 0.001, 0.005],
#                    'classifier__early_stopping': [True, False]},
#                    {'classifier' : [RandomForestClassifier()],
#                    'classifier__n_estimators' : list(range(10,100,10)),
#                    'classifier__max_features' : list(range(1,len(features)))}
#]
#
#mlp_search = GridSearchCV(
#    estimator=mlp, 
#    param_grid=mlp_parameters,
#    n_jobs=-1, 
#    refit=True, 
#    verbose=0, 
#    return_train_score=False
#    )
#
#mlp_search.fit(raw_data, classes)
#
#y_pred_mlp1 =mlp_search.predict(testRaw_data)
#save_data("final",y_pred_mlp1)
#print(mlp_search.best_params_ )
#print('Best Score - MLPClassifier:', mlp_search.best_score_ )

#Neighbors
#knn = KNeighborsClassifier(algorithm='auto')
#knn_parameters = {  'n_neighbors': (1,300, 1),
#                    'leaf_size': (200,1000,1),
#                    'p': (1,100),
#                    'weights': ('uniform', 'distance'),
#                    'metric': ('minkowski',
#                    'chebyshev'),
#                    "p" : (1,5),
#                    'algorithm' : ('auto', 'ball_tree', 'kd_tree', 'brute')
#                    }
#
#knn_search = GridSearchCV(
#    estimator=knn,
#    param_grid=knn_parameters,
#    scoring = 'accuracy',
#    n_jobs = -1,
#    cv = 200
#)
#
#knn_search.fit(X_train, y_train)
#
#y_pred_KNN1 =knn_search.predict(X_test)
#print(knn_search.best_params_ )
#print('Best Score - KNeighborsClassifier:', knn_search.best_score_ )


#Logistic regression
#logReg = Pipeline([('classifier' , RandomForestClassifier())])
#logReg_parameters =[{   'classifier' : [LogisticRegression()],
#                        'classifier__penalty' : ['l1', 'l2'],
#                        'classifier__C' : np.logspace(-16, 16, 20),
#                        'classifier__solver' : ['liblinear']},
#                        {'classifier' : [RandomForestClassifier()],
#                        'classifier__n_estimators' : list(range(10,100,10)),
#                        'classifier__max_features' : list(range(1,len(features)))}
#]
#
#logReg_search = GridSearchCV(
#    estimator = logReg,
#    param_grid = logReg_parameters,
#    cv = 10,
#    verbose=False,
#    n_jobs=-1)
#
#logReg_search.fit(X_train, y_train)
#
#y_pred_logReg1 =logReg_search.predict(X_test)
#print(logReg_search.best_params_ )
#print('Best Score - LogisticRegression:', logReg_search.best_score_ )

#Naive Bayes
#gnb = GaussianNB()
#gnb_parameters = {
#    'var_smoothing': np.logspace(0,-15, num=100)
#}
#gnb_search = GridSearchCV(
#    estimator=gnb,
#    param_grid=gnb_parameters,
#    verbose=0,
#    cv=10,
#    n_jobs=-1)
#
#gnb_search.fit(raw_data,classes)
#
#y_pred_GNB = gnb_search.predict(testRaw_data)
#save_data("final",y_pred_GNB)
#print(gnb_search.best_params_ )
#print('Best Score - Naive Bayes:', gnb_search.best_score_ )

gnb = GaussianNB(var_smoothing=1.4174741629268048e-05)
gnb.fit(raw_data,classes)
y_pred_GNB = gnb.predict(testRaw_data)
save_data("final.csv",y_pred_GNB)

#SGDclassifier
#SgdC = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
#SgdC_parameters = {
#    'loss' : ['hinge', 'log', 'modified_huber','squared_hinge', 'perceptron'],
#    'alpha': [1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3], # learning rate
#    'max_iter': [100000], # number of epochs
#    'penalty': ['l2'],
#    'n_jobs': [-1]
#}
#
#SgdC_search = GridSearchCV(
#    estimator = SgdC, 
#    param_grid = SgdC_parameters, 
#    scoring='accuracy', 
#    cv=200)
#
#SgdC_search.fit(X_train,y_train)
#
#print(SgdC_search.best_params_ )
#print('Best Score - SGDclassifier:', SgdC_search.best_score_ )

#Kmeans
#KM = KMeans()
#KM_parameters = {'n_clusters': [2, 3, 5, 7] }
#rs = np.random.RandomState(1389057)
#cvalue = StratifiedKFold(4, shuffle=True, random_state=rs)
#
#scorer = make_scorer(f1_score, pos_label="Heart disease") #Normal
#
#
#KM_search = GridSearchCV(
#    estimator = KM,
#    param_grid = KM_parameters,
#    scoring = scorer,
#    cv= cvalue
#)
#
#KM_search.fit(X_train,y_train)
#
#print(KM_search.best_params_ )
#print('Best Score - Kmeans:', KM_search.best_score_ )

#plt.show()