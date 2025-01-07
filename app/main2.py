import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.login import Login
from app.investments import Investment
from app.portfolio import Portfolio
from app.ativo import Ativo
from app.data import Data

Login.createLogin("Gustavo","manezinhoLindinhu")
user = "Gustavo"
password = "manezinhoLindinhu"
newPassword = "coxinha123"
Login.updateUserLogin(user,password,newPassword)
login2 = Login.logging(user, newPassword)
userPortfolio = Portfolio(Investment.getUserInvestment(user))
aaplInfo = Ativo(ativo = "BTC",custodia = "Rico", codigo = "AAPL", quantidade = 5.5, data = "2025-01-03", valor = 89)
print(userPortfolio.getPortfolio())
userPortfolio.addAtivoPortfolio(aaplInfo)
print(userPortfolio.getPortfolio())
Investment.updateUserInvestment(user,userPortfolio)