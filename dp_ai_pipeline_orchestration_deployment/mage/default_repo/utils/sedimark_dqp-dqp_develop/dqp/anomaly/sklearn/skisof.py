##Copyright 2023 NUID UCD. All Rights Reserved.


from sklearn.ensemble import IsolationForest



class skisof(IsolationForest):


    def __init__(self,**params):
         super().__init__(**params)




    def fit(self,X,y=None):
        
        super().fit(X)
        self.decision_scores_=-self.score_samples(X)
        return self
