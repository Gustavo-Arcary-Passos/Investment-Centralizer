import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.login import Login

class TestLogin:
    path = os.path.join(os.getcwd(), "dbTest", "testLogin.json")

    @staticmethod
    def setup():
        # Cria o diretório e arquivo JSON para teste, se necessário
        os.makedirs(os.path.dirname(TestLogin.path), exist_ok=True)
        with open(TestLogin.path, "w") as f:
            f.write("{}")  # Inicializa com um JSON vazio

    @staticmethod
    def teardown():
        # Remove o arquivo de teste após os testes
        if os.path.exists(TestLogin.path):
            os.remove(TestLogin.path)

    @staticmethod
    def testUserCreation():
        user = "GustavoPassos"
        password = "Mitsubishan"

        # Criação de usuário
        result = Login.createLogin(user, password, TestLogin.path)
        assert result is True, "O usuário não foi criado com sucesso."

        # Verifica se o usuário foi adicionado corretamente ao banco
        users = Login.getAllUsers(TestLogin.path)
        assert user in users, "O usuário não está no banco de dados."
        assert users[user] == password, "A senha do usuário está incorreta."

    @staticmethod
    def testDuplicateUser():
        user = "Gustavo Arcary"
        password = "Mitsubishan"

        # Criação inicial
        Login.createLogin(user, password, TestLogin.path)

        # Tenta criar o mesmo usuário novamente
        result = Login.createLogin(user, password, TestLogin.path)
        assert result is False, "A criação duplicada de usuário foi permitida."

    @staticmethod
    def testUpdateUserLogin():
        user = "GamesEdu"
        password = "Mitsubishan"
        newPassword = "nahsibustiM"
        # Criação inicial
        Login.createLogin(user, password, TestLogin.path)

        Login.updateUserLogin(user,password,newPassword, TestLogin.path)
        passwordGet = Login.getUserDb(user,TestLogin.path)
        assert passwordGet == newPassword, "Senha do usuario foi modificada."

    @staticmethod
    def testDeleteLogin():
        user = "GAP"
        password = "NorWay"

        result = Login.createLogin(user, password, TestLogin.path)
        assert result is True, "Nao conseguiu criar o usuario"

        result = Login.deleteLogin(user, password, TestLogin.path)
        assert result is True, "Nao conseguiu deletar o usuario"
        result = Login.getUserDb(user, TestLogin.path)
        assert result is None, "Usuario nao foi encontrado."


# Executando os testes manualmente
if __name__ == "__main__":
    TestLogin.setup()
    try:
        TestLogin.testUserCreation()
        print("Teste de criação de usuário: PASSOU")
        TestLogin.testDuplicateUser()
        print("Teste de usuário duplicado: PASSOU")
        TestLogin.testUpdateUserLogin()
        print("Teste de troca de senha do usuário: PASSOU")
        TestLogin.testDeleteLogin()
        print("Teste de deletar o usuário: PASSOU")
    except AssertionError as e:
        print(f"Teste falhou: {e}")
    finally:
        TestLogin.teardown()
