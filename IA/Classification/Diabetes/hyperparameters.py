# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

# pylint: disable=C0301

################################################################################

""" hyperparameters """

################################################################################

from    hyperopt            import hp
from    hyperopt.pyll       import scope

################################################################################

space_lrc   = { "C"                     : hp.uniform("C", 0.01, 0.1),
                "max_iter"              : hp.randint("max_iter", 1000),
                "cases"                 : hp.choice("cases", [ ("case_1", { "solver"    : "lbfgs",
                                                                            "penalty"   : hp.choice("p1", [ None, "l2" ]) }),
                                                               ("case_2", { "solver"    : "liblinear",
                                                                            "penalty"   : hp.choice("p2", [ "l1", "l2" ]) }),
                                                               ("case_3", { "solver"    : "saga",
                                                                            "penalty"   : hp.choice("p3", [ None, "l1", "l2" ]) }) ]),
                "tol"                   : hp.uniform("tol", 0.0001, 0.01) }

space_svm   = { "C"                     : hp.uniform("C", 0.01, 0.1),
                "class_weight"          : hp.choice("class_weight", [ None, "balanced" ]),
                "degree"                : scope.int(hp.quniform("degree", 3, 6, 1)),
                "gamma"                 : hp.choice("gamma", [ "auto", "scale" ]),
                "kernel"                : hp.choice("kernel", [ "linear", "poly", "rbf" ]) }

space_knn   = { "algorithm"             : hp.choice("algorithm", [ "ball_tree", "brute", "kd_tree" ]),
                "metric"                : hp.choice("metric", [ "euclidean", "manhattan", "minkowski" ]),
                "n_neighbors"           : scope.int(hp.quniform("n_neighbors", 16, 32, 2)),
                "weights"               : hp.choice("weights", [ "uniform" ]) }

space_dst   = { "criterion"             : hp.choice("criterion", [ "entropy", "gini" ]),
                "max_depth"             : scope.int(hp.quniform("max_depth", 8, 32, 1)),
                "max_features"          : scope.int(hp.quniform("max_features", 2, 8, 1)),
                "min_samples_leaf"      : scope.int(hp.quniform("min_samples_leaf", 2, 20, 1)),
                "min_samples_split"     : scope.int(hp.quniform("min_samples_split", 2, 40, 1)) }

space_rfc   = { "criterion"             : hp.choice("criterion", [ "entropy", "gini" ]),
                "max_depth"             : scope.int(hp.quniform("max_depth", 8, 32, 1)),
                "max_features"          : scope.int(hp.quniform("max_features", 2, 8, 1)),
                "min_samples_leaf"      : scope.int(hp.quniform("min_samples_leaf", 2, 20, 2)),
                "min_samples_split"     : scope.int(hp.quniform("min_samples_split", 2, 40, 1)),
                "n_estimators"          : scope.int(hp.quniform("n_estimators", 10, 50, 1)) }

space_xgb   = { "max_depth"             : scope.int(hp.quniform("max_depth", 8, 32, 1)),
                "min_child_weight"      : hp.uniform("min_child_weight", 1, 20),
                "subsample"             : hp.uniform("subsample", 0, 1),
                "colsample_bytree"      : hp.uniform("colsample_bytree", 0.5, 1),
                "eta"                   : hp.uniform("eta", 0.001, 1.0),
                "n_estimators"          : scope.int(hp.quniform("n_estimators", 10, 50, 1)),
                "gamma"                 : hp.quniform("gamma", 1, 10, 0.1) }

################################################################################
