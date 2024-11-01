import tkinter as tk
from tkinter import messagebox
import sqlite3

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT, tipo TEXT, fornecedor TEXT, quantidade INTEGER)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT, filial TEXT, ambiente TEXT)''')
    conn.commit()
    conn.close()

# Função para cadastrar um novo usuário
def cadastrar_usuario(nome, senha, filial, ambiente):
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nome, senha, filial, ambiente) VALUES (?, ?, ?, ?)', 
                   (nome, senha, filial, ambiente))
    conn.commit()
    conn.close()

# Função para autenticação de login
def login():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nome=? AND senha=? AND filial=? AND ambiente=?', 
                   (entry_nome.get(), entry_senha.get(), entry_filial.get(), entry_ambiente.get()))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        ambiente = entry_ambiente.get().lower()
        messagebox.showinfo("Login", "Login bem-sucedido!")
        login_window.destroy()
        
        if ambiente == "almoxarifado":
            abrir_menu_almoxarifado()
        else:
            messagebox.showinfo("Atualização", "Software sendo atualizado!")
    else:
        messagebox.showerror("Erro", "Credenciais inválidas.")

# Função para cadastrar um novo produto
def cadastrar_produto(descricao, tipo, fornecedor, quantidade):
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produtos (descricao, tipo, fornecedor, quantidade) VALUES (?, ?, ?, ?)', 
                   (descricao, tipo, fornecedor, quantidade))
    conn.commit()
    conn.close()
    visualizar_estoque()

# Função para visualizar o estoque
def visualizar_estoque():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()

    estoque_window = tk.Toplevel()
    estoque_window.title("Estoque")
    tk.Label(estoque_window, text="Estoque de Produtos", font=('Arial', 14, 'bold')).pack(pady=10)
    
    for produto in produtos:
        tk.Label(estoque_window, text=f"ID: {produto[0]}, Descrição: {produto[1]}, Tipo: {produto[2]}, Fornecedor: {produto[3]}, Qtd: {produto[4]}").pack()

# Função para atualizar a quantidade de um produto
def atualizar_produto(produto_id, nova_quantidade):
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE produtos SET quantidade=? WHERE id=?', (nova_quantidade, produto_id))
    conn.commit()
    conn.close()
    visualizar_estoque()

# Função para a interface de atualização de produto
def atualizar_produto_interface():
    atualizar_window = tk.Toplevel()
    atualizar_window.title("Atualizar Produto")
    tk.Label(atualizar_window, text="Atualizar Produto", font=('Arial', 14, 'bold')).pack(pady=10)
    
    tk.Label(atualizar_window, text="ID do Produto:").pack()
    produto_id_entry = tk.Entry(atualizar_window)
    produto_id_entry.pack()
    
    tk.Label(atualizar_window, text="Nova Quantidade:").pack()
    nova_quantidade_entry = tk.Entry(atualizar_window)
    nova_quantidade_entry.pack()
    
    def salvar_atualizacao():
        try:
            produto_id = int(produto_id_entry.get())
            nova_quantidade = int(nova_quantidade_entry.get())
            atualizar_produto(produto_id, nova_quantidade)
            messagebox.showinfo("Sucesso", "Quantidade atualizada com sucesso!")
            atualizar_window.destroy()
        except ValueError:
            messagebox.showerror("Erro", "ID e quantidade devem ser numéricos.")
    
    tk.Button(atualizar_window, text="Salvar", command=salvar_atualizacao).pack(pady=10)

# Função para movimentar produtos no estoque
def movimentar_produto(descricao, tipo, quantidade):
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('SELECT quantidade FROM produtos WHERE descricao=? AND tipo=?', (descricao, tipo))
    result = cursor.fetchone()
    if result:
        nova_quantidade = result[0] + quantidade if quantidade > 0 else result[0] - abs(quantidade)
        if nova_quantidade >= 0:
            cursor.execute('UPDATE produtos SET quantidade=? WHERE descricao=? AND tipo=?', 
                           (nova_quantidade, descricao, tipo))
            conn.commit()
            messagebox.showinfo("Sucesso", "Movimentação realizada! Seu produto poderá ser requisitado em alguns minutos.")
        else:
            messagebox.showerror("Erro", "Quantidade insuficiente no estoque!")
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")
    conn.close()

# Função para a interface de movimentação de produtos
def movimentar_produto_interface():
    movimentar_window = tk.Toplevel()
    movimentar_window.title("Movimentar Produto")
    tk.Label(movimentar_window, text="Movimentação de Produto", font=('Arial', 14, 'bold')).pack(pady=10)
    
    tk.Label(movimentar_window, text="Descrição do Produto:").pack()
    descricao_entry = tk.Entry(movimentar_window)
    descricao_entry.pack()
    
    tk.Label(movimentar_window, text="Tipo:").pack()
    tipo_entry = tk.Entry(movimentar_window)
    tipo_entry.pack()
    
    tk.Label(movimentar_window, text="Quantidade:").pack()
    quantidade_entry = tk.Entry(movimentar_window)
    quantidade_entry.pack()
    
    def realizar_movimentacao():
        try:
            descricao = descricao_entry.get()
            tipo = tipo_entry.get()
            quantidade = int(quantidade_entry.get())
            movimentar_produto(descricao, tipo, quantidade)
            movimentar_window.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser numérica.")
    
    tk.Button(movimentar_window, text="Movimentar", command=realizar_movimentacao).pack(pady=10)

# Função para abrir o menu do almoxarifado
def abrir_menu_almoxarifado():
    window = tk.Toplevel()
    window.title("Almoxarifado")
    tk.Label(window, text="TecCTRL - Almoxarifado - Menu Principal", font=('Arial', 16, 'bold')).pack(pady=10)
    
    tk.Button(window, text="Cadastrar Produto", command=cadastrar_produto_interface, width=20).pack(pady=5)
    tk.Button(window, text="Visualizar Estoque", command=visualizar_estoque, width=20).pack(pady=5)
    tk.Button(window, text="Movimentar Produto", command=movimentar_produto_interface, width=20).pack(pady=5)

# Configuração da janela principal para login
root = tk.Tk()
root.title("TecCTRL - Sistema de Gestão")
root.state('zoomed')  # Configura a janela para tela cheia
root.geometry("800x600")  # Define o tamanho mínimo da janela

# Cria as tabelas do banco de dados
criar_tabelas()

# Rótulo principal
label_titulo = tk.Label(root, text="TecCTRL - Sistema de Gestão", font=("Arial", 24, "bold"))
label_titulo.pack(pady=20)

# Campos de entrada para o login
tk.Label(root, text="Nome:").pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

tk.Label(root, text="Senha:").pack()
entry_senha = tk.Entry(root, show="*")
entry_senha.pack()

tk.Label(root, text="Filial:").pack()
entry_filial = tk.Entry(root)
entry_filial.pack()

tk.Label(root, text="Ambiente:").pack()
entry_ambiente = tk.Entry(root)
entry_ambiente.pack()

# Botão de login
button_login = tk.Button(root, text="Entrar", command=login)
button_login.pack(pady=20)

# Execução da janela principal
root.mainloop()