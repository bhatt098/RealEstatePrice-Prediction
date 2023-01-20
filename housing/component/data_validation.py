from housing.entity.config_entity import*
from housing.entity.artifact_entity import*
from housing.exception import*
import os,sys
import json
import pandas as pd

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab



class DataValidation:


    def __init__(self,data_validation_config=DataValidationConfig,data_ingestion_artifact=DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys)



    def is_data_drift_found(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df= pd.read_csv(self.data_ingestion_artifact.test_file_path)

            profile.calculate(train_df,test_df)
            report = json.loads(profile.json())
            report_file_path=self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            # return report

            # now for HTML Page
            dashboard = Dashboard(tabs=[DataDriftTab()])
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)


        except Exception as e:
            raise HousingException(e,sys)   


    
    def initiate_data_validation(self)->DataValidationArtifact :
        try:
            # self.is_train_test_file_exists()
            # self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed successully."
            )
            # logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

        
