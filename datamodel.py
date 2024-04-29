import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
class datamodel:
    def training(self):
        self.data=pd.read_csv("student_admission_dataset.csv")
        self.X=self.data[['GPA','SAT_Score','Extracurricular_Activities']]
        self.Y=self.data['Admission_Status']
        self.model=LogisticRegression()
        self.model.fit(self.X,self.Y)
        
        
    def predict(self, GPA, SAT_SCORE, EXTRACIRICULAR): # this is prediciton function
        return self.model.predict([[GPA, SAT_SCORE, EXTRACIRICULAR]])[0]
    
    
    def create(self, new_data):
        self.data = self.data.append(new_data, ignore_index=True)
        
    def read(self):
        return self.data
    
    def update(self, index, updated_data):
        self.data.loc[index] = updated_data
        
    def delete(self, index):
        self.data.drop(index, inplace=True)
    
    
# Model=datamodel()# sample class thing
# Model.exportmodel()
# print(Model.predict(4.0,1600,8))# sample Prediction