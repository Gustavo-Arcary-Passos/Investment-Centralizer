from login import Login
from investments import Investment
from portfolio import Portfolio
from ativo import Ativo
from data import Data

Login.createLogin("Gustavo","manezinhoLindinhu")
user = "Gustavo"
password = "manezinhoLindinhu"
newPassword = "coxinha123"
Login.updateUserLogin(user,password,newPassword)
login2 = Login.logging(user, newPassword)
userPortfolio = Portfolio(Investment.getUserInvestment(user))
aaplInfo = Ativo(ativo = "Apple",custodia = "Rico", codigo = "AAPL", quantidade = 3.5, data = "2025-01-01", valor = 85)
print(userPortfolio.getPortfolio())
userPortfolio.addAtivoPortfolio(aaplInfo)
print(userPortfolio.getPortfolio())
Investment.updateUserInvestment(user,userPortfolio)