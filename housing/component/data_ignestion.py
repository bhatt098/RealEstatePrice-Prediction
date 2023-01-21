from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.constant import*

from housing.exception import*
import tarfile
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import train_test_split
import zipfile
import re
import shutil
from zipfile import ZipFile
import pandas as pd


import os,sys

class DataIngestion:

    def __init__(self, data_ingestion_config=DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config 
        except Exception as e:
            raise HousingException(e,sys)

   
    def download_housing_data(self):
        try:
            download_url=self.data_ingestion_config.dataset_download_url
            tgz_download_dir=self.data_ingestion_config.tgz_download_dir
            os.makedirs(tgz_download_dir,exist_ok=True)

            housing_file_name = os.path.basename(download_url)
            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)
            regex = re.compile(
                 r'^(?:http|ftp)s?://' # http:// or https://
                 r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                 r'localhost|' #localhost...
                 r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                 r'(?::\d+)?' # optional port
                 r'(?:/?|[/?]\S+)$', re.IGNORECASE)

            # print(re.match(regex, "http://www.example.com") is not None) # True
            # print(re.match(regex, "example.com") is not None)  

            if(re.match(regex, download_url) is not None):
                urllib.request.urlretrieve(download_url, tgz_file_path)

            else:
                download_url=os.path.join(ROOT_DIR,download_url)
                shutil.copy(download_url,tgz_download_dir )

            return tgz_file_path

        except Exception as e:
            raise HousingException(e,sys)



    def extract_tgz_file(self,tgz_file_path):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            download_url=self.data_ingestion_config.dataset_download_url

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)
            with ZipFile(tgz_file_path, 'r') as housing_tgz_file_obj:
                housing_tgz_file_obj.printdir()
                print('Extracting all the files now...')
                housing_tgz_file_obj.extractall(path=raw_data_dir)
            
        except Exception as e:
            raise HousingException(e,sys)




    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            # shutil.copy(download_url,tgz_download_dir )

            raw_data_dir = self.data_ingestion_config.raw_data_dir
            test_file=os.listdir(raw_data_dir)[0]
            train_file=os.listdir(raw_data_dir)[0] 
            test_df=os.path.join(raw_data_dir,test_file)
            train_df=os.path.join(raw_data_dir,train_file)

            test_data=pd.read_csv(test_df)
            train_data=pd.read_csv(train_df)
            # df=pd.concat([train_data,test_data])

            # train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, train_file)
            # test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, test_file)

            # os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
            # train_data.to_csv(train_file_path,index=False)
    
            # # if X_train in not None:
            # os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
            # test_data.to_csv(test_file_path,index=False)

            file_name=os.listdir(raw_data_dir)[0]   #will modify as per requirements
            print('filename')
            print(file_name)
            file_name=os.listdir(raw_data_dir)[0]
            housing_file_path=os.path.join(raw_data_dir,file_name)
            df=pd.read_csv(housing_file_path)
            # print(df)
            df.drop(['No'], axis=1,inplace=True)
            # print("columns after drop")
            # print(df.columns)
            X=df.iloc[:,:-1]   #independent
            # print(X)
            y=df.iloc[:,-1]    #dependent
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)
            # if X_train in not None:
            # print(X_train)
            # print(X_test)
            train_data=pd.concat([X_train,y_train],axis=1)
            test_data=pd.concat([X_test,y_test],axis=1)
            os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
            train_data.to_csv(train_file_path,index=False)
    
            # if X_train in not None:
            os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
            test_data.to_csv(test_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                    test_file_path=test_file_path,
                                    is_ingested=True,
                                    message=f"Data ingestion completed successfully."
                                    )
            return data_ingestion_artifact


        except Exception as e:
            raise HousingException(e,sys)



    def ingested_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path =  self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(e,sys) from e
        




    




