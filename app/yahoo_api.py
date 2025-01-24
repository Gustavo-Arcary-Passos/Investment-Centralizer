import yfinance as yf
from datetime import datetime, timedelta

class Info:
    def __init__(self,codigo):
        self.ticker = yf.Ticker(codigo)
        self.current_value = self.getValue()

    def getTicker(self):
        return self.ticker
    
    def getCurrentValue(self):
        return self.current_value

    def getValue(self, data = None):
        if data is None:
            historico1dia = self.ticker.history(period="1d")
        else:
            data_obj = datetime.strptime(data, "%Y-%m-%d")
            data_fim = (data_obj + timedelta(days=1)).strftime("%Y-%m-%d")
            historico1dia = self.ticker.history(start=data, end=data_fim)

        if historico1dia.empty:
            print(f"Nenhum dado encontrado para {data}.")
            return None
        
        return historico1dia['Close'].iloc[-1]
    
    def getCurrency(self):
        return self.ticker.info['currency']