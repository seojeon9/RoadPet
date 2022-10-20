from infra.jdbc import DataWarehouse, save_data
from infra.spark_session import get_spark_session


class SigunguTrasformer:

    @classmethod
    def transform(cls):
        # DW에서 시도/시군구 코드 받아오기
        sido = '6110000'
        sigungu = '3220000'
        path = '/road_pet/shelter/shelter/shelter_' + sigungu + '.json'
        shelter_json = get_spark_session().read.option(
            "multiline", "true").json(path, encoding='UTF-8').first()

        shelter_df = get_spark_session().createDataFrame(
            shelter_json['response']['body']['items']['item'])

        # DW의 테이블에 맞게 가공
        # save_data(DataWarehouse, sigungu_df, 'ACTORS')
