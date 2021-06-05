from sqlalchemy import Column, String, VARCHAR, INTEGER, FLOAT, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AsammModel(Base):
    __tablename__ = "asamm"
    __table_args__ = {"schema": "tesc3"}

    coil_id = Column(VARCHAR(25), nullable=False, primary_key=True)
    prediction_model_result = Column(FLOAT, nullable=True)
    technology_error_number = Column(INTEGER)
    technology_error_description = Column(String(2000), nullable=True)
    data_error_number = Column(INTEGER)
    data_error_description = Column(String(2000), nullable=True)
    model_name = Column(VARCHAR(40), primary_key=True)
    model_description = Column(String(2000), nullable=True)
    work_model_result_description = Column(String(2000), nullable=True)
    work_model_result_status = Column(INTEGER)
    steel_grade = Column(VARCHAR(25))
    min_prediction_value = Column(FLOAT)
    max_prediction_value = Column(FLOAT)
    control_unit = Column(INTEGER)
    prediction_datetime = Column(TIMESTAMP)
    attestation_status = Column(INTEGER)
    attestation_description = Column(String(2000), nullable=True)
    real_test_value = Column(FLOAT)
    rewrite_count = Column(INTEGER)

    def __repr__(self):
        return f"<asamm {self.coil_id}-{self.model_name}>"


if __name__ == '__main__':
    print(AsammModel.__dict__)