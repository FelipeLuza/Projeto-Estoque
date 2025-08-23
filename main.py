from collections import deque
import os


# ===== CLASSES =====
class Produto:
    def __init__(self, id: int, nome: str, quantidade: int, preco: float):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self) -> str:
        return f"ID: {self.id} | Nome: {self.nome} | Quantidade: {self.quantidade} | Preço: R${self.preco:.2f}"

class Cliente:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome
        self.gasto_total = 0.0

    def __str__(self) -> str:
        return f"ID: {self.id} | Nome: {self.nome} | Total gasto: R${self.gasto_total:.2f}"


# ===== ESTRUTURAS =====
estoque = []          
clientes = []         
fila_vendas = deque() 
pilha_operacoes = []  

# IDs 
id_produto = 100
id_cliente = 200

# ===== SALVAR E CARREGAR DADOS =====

def salvar_dados():
    """Salva estoque/clientes/ids em arquivos .txt (formato simples com ;)"""
    try:
        with open("estoque.txt", "w", encoding="utf-8") as f:
            for p in estoque:
                f.write(f"{p.id};{p.nome};{p.quantidade};{p.preco}\n")
        with open("clientes.txt", "w", encoding="utf-8") as f:
            for c in clientes:
                f.write(f"{c.id};{c.nome};{c.gasto_total}\n")
        with open("ids.txt", "w", encoding="utf-8") as f:
            f.write(f"{id_produto};{id_cliente}\n")
        print("Dados salvos com sucesso!\n")
    except Exception as e:
        print(f"[AVISO] Falha ao salvar dados: {e}\n")

def carregar_dados():
    """Carrega estoque/clientes/ids se os arquivos existirem. Não quebra em erro."""
    global id_produto, id_cliente
    try:
        if os.path.exists("estoque.txt"):
            with open("estoque.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    if not linha.strip():
                        continue
                    idp, nome, qtd, preco = linha.strip().split(";")
                    estoque.append(Produto(int(idp), nome, int(qtd), float(preco)))
        if os.path.exists("clientes.txt"):
            with open("clientes.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    if not linha.strip():
                        continue
                    idc, nome, gasto = linha.strip().split(";")
                    cli = Cliente(int(idc), nome)
                    cli.gasto_total = float(gasto)
                    clientes.append(cli)
        if os.path.exists("ids.txt"):
            with open("ids.txt", "r", encoding="utf-8") as f:
                primeira = f.readline().strip()
                if primeira:
                    idp, idc = primeira.split(";")
                    id_produto, id_cliente = int(idp), int(idc)
        print("Dados carregados com sucesso!\n")
    except Exception as e:
        print(f"[AVISO] Falha ao carregar dados: {e}\n")

# ===== FUNÇÕES =====

def obter_int(msg: str) -> int:
    """Lê um inteiro do usuário sem quebrar o programa."""
    while True:
        try:
            valor = int(input(msg))
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def obter_float(msg: str) -> float:
    """Lê um float do usuário sem quebrar o programa."""
    while True:
        try:
            valor = float(input(msg))
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número (use ponto para decimais).")

def encontrar_produto_por_id(pid: int):
    return next((p for p in estoque if p.id == pid), None)

def encontrar_cliente_por_id(cid: int):
    return next((c for c in clientes if c.id == cid), None)

# ===== FUNCIONALIDADES =====

def cadastrar_produto():
    global id_produto
    nome = input("Digite o nome do produto: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return
    quantidade = obter_int("Digite a quantidade: ")
    if quantidade < 0:
        print("Quantidade não pode ser negativa.")
        return
    preco = obter_float("Digite o preço: ")
    if preco < 0:
        print("Preço não pode ser negativo.")
        return
    id_produto += 1
    p = Produto(id_produto, nome, quantidade, preco)
    estoque.append(p)
    pilha_operacoes.append(("produto", p))
    print(f"Produto cadastrado com sucesso! (ID gerado: {p.id})")


def listar_produtos():
    if not estoque:
        print("Não há produtos cadastrados.")
        return
    print("--- ESTOQUE ATUAL ---")
    for p in estoque:
        print(p)


def cadastrar_cliente():
    global id_cliente
    nome = input("Digite o nome do cliente: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return
    id_cliente += 1
    c = Cliente(id_cliente, nome)
    clientes.append(c)
    pilha_operacoes.append(("cliente", c))
    print(f"Cliente cadastrado com sucesso! (ID gerado: {c.id})")


def listar_clientes():
    if not clientes:
        print("Não há clientes cadastrados.")
        return
    print("--- LISTA DE CLIENTES ---")
    for c in clientes:
        print(c)


def realizar_venda():
    if not estoque:
        print("Estoque vazio. Não é possível realizar venda.")
        return
    if not clientes:
        print("Não há clientes cadastrados. Cadastre um cliente antes de vender.")
        return

    id_prod = obter_int("Digite o ID do produto: ")
    quantidade = obter_int("Digite a quantidade: ")
    id_cli = obter_int("Digite o ID do cliente: ")

    produto = encontrar_produto_por_id(id_prod)
    cliente = encontrar_cliente_por_id(id_cli)

    if not produto:
        print("Produto não encontrado!")
        return
    if not cliente:
        print("Cliente não encontrado!")
        return
    if quantidade <= 0:
        print("Quantidade deve ser maior que zero.")
        return
    if quantidade > produto.quantidade:
        print("Quantidade maior que o estoque disponível!")
        return

    valor_total = quantidade * produto.preco
    produto.quantidade -= quantidade
    cliente.gasto_total += valor_total

    venda = {
        'produto_id': produto.id,
        'produto': produto.nome,
        'quantidade': quantidade,
        'valor_total': valor_total,
        'cliente_id': cliente.id,
        'cliente': cliente.nome
    }

    fila_vendas.append(venda)
    pilha_operacoes.append(("venda", venda))
    print(f"Venda realizada com sucesso! (Valor total: R${valor_total:.2f})")


def ver_vendas():
    if not fila_vendas:
        print("Não há vendas registradas.")
        return
    print("--- FILA DE VENDAS ---")
    for v in list(fila_vendas):
        print(f"Produto: {v['produto']} | Quantidade: {v['quantidade']} | Valor Total: R${v['valor_total']:.2f} | Cliente: {v['cliente']}")


def desfazer_ultima_operacao():
    if not pilha_operacoes:
        print("Não há operações para desfazer.")
        return
    tipo, item = pilha_operacoes.pop()

    if tipo == 'produto':
        try:
            estoque.remove(item)
            print(f"Cadastro do produto '{item.nome}' desfeito.")
        except ValueError:
            print("[AVISO] Produto já não está no estoque.")

    elif tipo == 'cliente':
        try:
            clientes.remove(item)
            print(f"Cadastro do cliente '{item.nome}' desfeito.")
        except ValueError:
            print("[AVISO] Cliente já não está na lista.")

    elif tipo == 'venda':
        produto = encontrar_produto_por_id(item['produto_id'])
        cliente = encontrar_cliente_por_id(item['cliente_id'])
        if produto:
            produto.quantidade += item['quantidade']
        if cliente:
            cliente.gasto_total -= item['valor_total']
        if fila_vendas:
            try:
                fila_vendas.pop()
            except IndexError:
                pass
        print(f"Última venda do produto '{item['produto']}' cancelada.")


def valor_total_estoque():
    total = sum(p.quantidade * p.preco for p in estoque)
    print(f"Valor total do estoque: R${total:.2f}")


def valor_total_vendas():
    total = sum(v['valor_total'] for v in fila_vendas)
    print(f"Valor total de vendas realizadas: R${total:.2f}")


def clientes_e_gastos():
    if not clientes:
        print("Não há clientes cadastrados.")
        return
    print("--- CLIENTES E GASTOS ---")
    for c in clientes:
        print(c)

# ===== EXTRAS =====

def pesquisar_produtos():
    if not estoque:
        print("Não há produtos cadastrados.")
        return
    print("\nPesquisar produto por: 1-ID | 2-Nome")
    modo = input("Escolha (1/2): ").strip()
    if modo == '1':
        pid = obter_int("ID do produto: ")
        p = encontrar_produto_por_id(pid)
        if p:
            print(p)
        else:
            print("Produto não encontrado.")
    elif modo == '2':
        termo = input("Parte do nome (case-insensitive): ").strip().lower()
        encontrados = [p for p in estoque if termo in p.nome.lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print("Nenhum produto corresponde à pesquisa.")
    else:
        print("Opção inválida na pesquisa.")

# ===== MENU PRINCIPAL =====

def menu():
    while True:
        print("\n===== MENU ESTOQUE =====")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Cadastrar produto")
        print("4 - Listar produtos")
        print("5 - Realizar venda")
        print("6 - Ver fila de vendas")
        print("7 - Desfazer última operação")
        print("8 - Exibir valor total do estoque")
        print("9 - Exibir valor total de vendas realizadas")
        print("10 - Exibir clientes e valores totais gastos")
        print("11 - Pesquisar produtos (extra)")
        print("12 - Salvar dados agora (extra)")
        print("13 - Sair")
        escolha = input("Escolha: ").strip()

        try:
            if escolha == '1':
                cadastrar_cliente()
            elif escolha == '2':
                listar_clientes()
            elif escolha == '3':
                cadastrar_produto()
            elif escolha == '4':
                listar_produtos()
            elif escolha == '5':
                realizar_venda()
            elif escolha == '6':
                ver_vendas()
            elif escolha == '7':
                desfazer_ultima_operacao()
            elif escolha == '8':
                valor_total_estoque()
            elif escolha == '9':
                valor_total_vendas()
            elif escolha == '10':
                clientes_e_gastos()
            elif escolha == '11':
                pesquisar_produtos()
            elif escolha == '12':
                salvar_dados()
            elif escolha == '13':
                salvar_dados()
                print("Saindo do sistema... Até logo!")
                break
            else:
                print("Opção inválida! Tente novamente.")
        except Exception as e:
            print(f"[ERRO] Ocorreu um problema: {e}. A execução continuará.")

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    carregar_dados()
    menu()
