# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

""" results """

################################################################################

from joblib  import dump

################################################################################

class Results:
    """ Results class """

    def __init__(self, name):
        """ constructor """
        self.model          = { }
        self.model["name"]  = name

    ################################################################################

    def register(self, clf, evaluation):
        """ register function """
        self.model["clf"]   = clf
        self.model["hyp"]   = evaluation[0]
        self.model["cfm"]   = evaluation[1]
        self.model["clr"]   = evaluation[2]
        self.model["rep"]   = evaluation[3]

    ################################################################################

    def persist(self, name, path):
        """ persist function """
        file = path + name + ".joblib"
        dump(self.model["clf"], file)

    ################################################################################

    def write(self, name, filename):
        """ write function """
        model       = f"Model                   : {name}\n"
        params      = f"Hyperparameters         : {self.model['hyp']}\n"
        cf_matrix   = f"Confusion matrix        :\n\n{self.model['cfm']}\n\n"
        report      = f"Classification report   :\n{self.model['rep']}\n"
        delimiter   = "#" * 100 + "\n\n"
        results     = model + params + cf_matrix + report + delimiter

        with open(filename, "a+", encoding = "utf-8") as file:
            file.write(results)
            file.close()

    ################################################################################

    def __str__(self):
        """ ___str__ function """
        model       = f"Model                   : {self.model['name']}\n"
        params      = f"Hyperparameters         : {self.model['hyp']}\n"
        cf_matrix   = f"Confusion matrix        :\n\n{self.model['cfm']}\n\n"
        report      = f"Classification report   :\n{self.model['rep']}\n"
        delimiter   = "#" * 100 + "\n\n"

        return model + params + cf_matrix + report + delimiter
