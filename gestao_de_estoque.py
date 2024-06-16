import sqlite3

class Gestao:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        self.criar_tabela_estoque()
        
    def criar_tabela_estoque(self):
        cursor = self.conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS estoque (
                           id INTEGER PRIMARY KEY,
                           produto TEXT,
                           quantidade INTEGER
                       )
                       ''')
        self.conn.commit()
        
    def adicionar_produto(self, produto, quantidade):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO estoque (produto, quantidade) VALUES (?, ?)", (produto, quantidade))
        self.conn.commit()
        
    def remover_produto(self, produto, quantidade):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT quantidade FROM estoque WHERE produto=?", (produto,)
        )
        resultado = cursor.fetchone()
        if resultado: 
            estoque_atual = resultado[0]
            if estoque_atual >= quantidade:
                cursor.execute("UPDATE estoque SET quantidade=? WHERE produto=?",
                               (estoque_atual - quantidade, produto))
                self.conn.commit()
            else: 
                print(f"Quantidade insuficiente de {produto} em estoque.")
        else:
            print(f"{produto} não encontrado em estoque.")
                
    def consulta_estoque(self, produto):
        cursor = self.conn.cursor()
        cursor.execute("SELECT quantidade FROM estoque WHERE produto=?", (produto,))
        resultado = cursor.fetchone()
        if resultado: 
            return resultado[0]
        else: 
            return 0 
            
    def listar_produtos(self): 
        cursor = self.conn.cursor()
        cursor.execute("SELECT produto FROM estoque")
        produtos = cursor.fetchall()
        return [produto[0] for produto in produtos]
        

sistema = Gestao("estoque.db")


while True:
    print("\nOpções:")
    print("1. Adicionar produto")
    print("2. Remover produto")
    print("3. Consultar estoque de um produto")
    print("4. Listar todos os produtos")
    print("5. Sair")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        nome_produto = input("Nome do produto: ")
        quantidade_produto = int(input("Quantidade: "))
        sistema.adicionar_produto(nome_produto, quantidade_produto)
        print(f"Produto {nome_produto} adicionado com sucesso!")
        
    elif opcao == "2":
        nome_produto = input("Nome do produto: ")
        quantidade_produto = int(input("Quantidade: "))
        sistema.remover_produto(nome_produto, quantidade_produto)
        
    elif opcao == "3":
        nome_produto = input("Nome do produto: ")
        quantidade = sistema.consulta_estoque(nome_produto)
        print(f"Estoque de {nome_produto}: {quantidade}")
        
    elif opcao == "4":
        produtos = sistema.listar_produtos()
        print("Produtos em estoque:")
        for produto in produtos:
            print(produto)
            
    elif opcao == "5":
        break
        
    else:
        print("Opção inválida. Tente novamente.")
