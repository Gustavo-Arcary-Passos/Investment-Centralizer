import yfinance as yf
from datetime import datetime, timedelta

class Info:
    def __init__(self,codigo):
        self.ticker = yf.Ticker(codigo)

    def getTicker(self):
        return self.ticker

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
    
# aapl = Info("AAPL")
# data = "2022-12-12"
# print(aapl.getValue(data))
# print(aapl.getCurrency())