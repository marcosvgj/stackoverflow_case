from common.dao.base import DAO
from common.kimball.fact import Fact
from common.utils.logger import logger
from model.models import CommunicationToolModel

class Entrypoint:    
    def run(self):
        dataframe = DAO.from_csv("/home/marcos/dataengineeringatame/python/src/resources/base_de_respostas_10k_amostra.csv")
        dataframe.show(10,False)
        Fact(source=dataframe,
            model=CommunicationToolModel,
            field='CommunicationTools',
            database='stackoverflow',
            table='ferramenta_comunic',
            embbebedList=False,
            sink='PostgresDAO').save()

        
        

