from housing.exception import HousingException
from housing.entity.config_entity import*
from housing.config.configuration import*
from housing.entity.artifact_entity import*
from housing.component.data_ignestion import*
from housing.component.data_validation import*
from housing.component.data_transformation import*
from housing.component.model_trainer import*
import sys


class Pipeline:
    def __init__(self,config:Configuration=Configuration()) -> None:
        try:
            self.config=config
        except Exception as e:
            raise HousingException(e,sys)

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion=DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.ingested_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys)
    
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation=DataValidation(self.config.get_data_validation_config(),data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise HousingException(e,sys)

    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,data_transformation_artifact:DataTransformationArtifact)->DataTransformationArtifact:
        try:
            data_transformation=DataTransformation(self.config.get_data_transformation_config(),data_ingestion_artifact,data_transformation_artifact)
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise HousingException(e,sys)


    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact,data_ingestion_artifact:DataIngestionArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact,
                                         data_ignestion_artifact=data_ingestion_artifact
                                         )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise HousingException(e, sys) from e


    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact,data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact,data_ingestion_artifact)

        except Exception as e:
            raise HousingException(e,sys)        