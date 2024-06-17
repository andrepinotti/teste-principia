import pandas as pd
import json
import re
from datetime import datetime
from openpyxl import load_workbook

# Dados dos clientes a serem inseridos
inserePessoa = {
    "inserePessoa": [
        {
            "id": "usp-45030275899",
            "nome": "Antônio Pereira",
            "cpf": "450.302.758-99",
            "data_nasc": "03/10/2000",
            "email": "antoniopereira@gmail.com",
            "cep": "15035-160",
            "endereco": "Guiomar Assad Callil",
            "numero": "89",
            "bairro": "Vila Itália",
            "cidade": "São José do Rio Preto",
            "uf": "SP",
            "telefone": "17999234994",
            "ra": "107593",
            "curso": "Engenharia Civil",
            "faculdade": "usp"
        },
        {
            "id": "unifesp-45030298499",
            "nome": "Luana Rogrigues",
            "cpf": "450.302.984-99",
            "data_nasc": "13/12/2002",
            "email": "antoniopereira@gmail.com",
            "cep": "01023-001",
            "endereco": "Barão de Duprat",
            "numero": "89",
            "bairro": "Centro",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone": "17998324774",
            "ra": "738945",
            "curso": "Engenharia Química",
            "faculdade": "unifesp"
        },
        {
            "id": "ifsp-12345690701",
            "nome": "Maria Souza",
            "cpf": "123.456.908-01",
            "data_nasc": "25/08/1995",
            "email": "maria.souza@ifsp.edu.br",
            "cep": "12345-678",
            "endereco": "Rua das Flores",
            "numero": "123",
            "bairro": "Jardim das Rosas",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone": "11987654321",
            "ra": "987654",
            "curso": "Engenharia de Produção",
            "faculdade": "ifsp"
        }
    ]
}

def gera_arquivo_json():
   with open("inserePessoa.json", "w", encoding="utf-8") as arquivo:
        json.dump(inserePessoa, arquivo, indent=4, ensure_ascii=False)

gera_arquivo_json()

def validar_id(estudante):
    cpf_em_numeros = re.sub(r'\D', '', estudante["cpf"])
    id_correto = f"{estudante['faculdade']}-{cpf_em_numeros}"
    return id_correto == estudante["id"]


def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    return True

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validar_telefone(telefone):
    return re.match(r"^\d{11}$", telefone) is not None

def validar_data_nascimento(data_nasc):
    try:
        data = datetime.strptime(data_nasc, "%d/%m/%Y").date()
        return (datetime.now().date() - data).days >= 18 * 365
    except ValueError:
        return False

def validar_dados(estudante):
    erros = []
    if not validar_cpf(estudante["cpf"]):
        erros.append("CPF inválido")
    if not estudante["nome"]:
        erros.append("Nome completo inválido")
    if not validar_data_nascimento(estudante["data_nasc"]):
        erros.append("Data de nascimento inválida ou menor de 18 anos")
    if not validar_email(estudante["email"]):
        erros.append("Email inválido")
    if not validar_telefone(estudante["telefone"]):
        erros.append("Telefone inválido")
    if not validar_id(estudante):
        erros.append("Id inválido")
    return erros

# Função para salvar os dados no Excel
def salvar_em_excel(estudante, erros):
    df_novo = pd.DataFrame([{
        "id": estudante["id"],
        "nome": estudante["nome"],
        "data_nascimento": estudante["data_nasc"],
        "cpf": estudante["cpf"],
        "email": estudante["email"],
        "cep": estudante["cep"],
        "endereco": estudante["endereco"],
        "numero": estudante["numero"],
        "bairro": estudante["bairro"],
        "cidade": estudante["cidade"],
        "uf": estudante["uf"],
        "telefone": estudante["telefone"],
        "ra": estudante["ra"],
        "curso": estudante["curso"],
        "faculdade": estudante["faculdade"],
        "erros": ", ".join(erros) if erros else ""
    }])



    if erros:
        arquivo_saida = "estudantes_invalidos.xlsx"
    else:
        arquivo_saida = "sistema.xlsx"

    try:
        df_existente = pd.read_excel(arquivo_saida, engine='openpyxl')
        df_combined = pd.concat([df_existente, df_novo], ignore_index=True)
    except FileNotFoundError:
        df_combined = df_novo

    with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
        df_combined.to_excel(writer, index=False)



def ler_dados_existentes():
    try:
        return pd.read_excel("dados.xlsx", engine='openpyxl')
    except FileNotFoundError:
        return pd.DataFrame()


if __name__ == "__main__":
    for cliente in inserePessoa["inserePessoa"]:
        erros = validar_dados(cliente)
        salvar_em_excel(cliente, erros)

    print("Dados processados e arquivos Excel gerados.")

    
    try:
        tabela_validos = pd.read_excel("sistema.xlsx", engine='openpyxl')
        print("Estudantes válidos:")
        print(tabela_validos)
    except FileNotFoundError:
        print("Nenhum estudante válido foi encontrado.")

    try:
        tabela_invalidos = pd.read_excel("estudantes_invalidos.xlsx", engine='openpyxl')
        print("Estudante inválidos:")
        print(tabela_invalidos)
    except FileNotFoundError:
        print("Nenhum estudante inválido foi encontrado.")
