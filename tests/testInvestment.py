import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.investments import Investment
from app.portfolio import Portfolio
from app.ativo import Ativo

class TestInvestment:
    path = os.path.join(os.getcwd(), "dbTest", "testInvesment.json")

    @staticmethod
    def setup():
        # Cria o diretório e arquivo JSON para teste, se necessário
        os.makedirs(os.path.dirname(TestInvestment.path), exist_ok=True)
        with open(TestInvestment.path, "w") as f:
            f.write("{}")  # Inicializa com um JSON vazio

    @staticmethod
    def teardown():
        pass
        # Remove o arquivo de teste após os testes
        # if os.path.exists(TestInvestment.path):
        #     os.remove(TestInvestment.path)

    @staticmethod
    def testInvestmentCreation():
        user = "GAP"

        Investment.createInvestment(user, TestInvestment.path)

        allUsers = Investment.getAllInvestments(TestInvestment.path)
        assert user in allUsers, "Portfolio nao foi criado"

    @staticmethod
    def testInvestmentAddAtivoMultipleTimes():
        user = "GAP"
        Investment.createInvestment(user, TestInvestment.path)

        userPortfolio = Portfolio(Investment.getUserInvestment(user,TestInvestment.path))
        first = Ativo(ativo = "Apple",custodia = "Rico", codigo = "AAPL", quantidade = 3.5, data = "2025-01-01", valor = 85)
        userPortfolio.addAtivoPortfolio(first)
        second = Ativo(ativo = "Apple",custodia = "Rico", codigo = "AAPL", quantidade = 5.5, data = "2025-01-03", valor = 89)
        userPortfolio.addAtivoPortfolio(second)
        Investment.updateUserInvestment(user,userPortfolio,TestInvestment.path)
        newUserPortfolio = Portfolio(Investment.getUserInvestment(user,TestInvestment.path))
        apple = newUserPortfolio.getAtivo("Apple","Rico")
        assert apple.getQuantidade() == 9, "Erro na contagem de acoes adquiridas"
        assert apple.getPrecoMedio() < 87.5, "Erro no calculo do preco medio"
         

if __name__ == "__main__":
    TestInvestment.setup()
    try:
        TestInvestment.testInvestmentCreation()
        print("Teste de criação de investimento: PASSOU")
        TestInvestment.testInvestmentAddAtivoMultipleTimes()
        print("Teste de multiplas adicoes de ativo: PASSOU")
    except AssertionError as e:
        print(f"Teste falhou: {e}")
    finally:
        TestInvestment.teardown()