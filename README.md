## Validação e Inserção
👋 Olá, venho a partir desse read.me explicar algumas funcionalidades desse sistema.👋

Com base no formato do Json disponibilizado e nos dados da planilha dados.xlsx, foi criado uma variável nesse padrão com os dados que serão inseridos na planilha.  
Foram colocados nessa variável 3 estudantes. 
```python
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
```
Logo, será gerado um arquivo JSON que terá a informação dessa variável.
```python
def gera_arquivo_json():
   with open("inserePessoa.json", "w", encoding="utf-8") as arquivo:
        json.dump(inserePessoa, arquivo, indent=4, ensure_ascii=False)

gera_arquivo_json()
```
Além disso, fiz a função a qual será gerada a planilha e também receberá os erros que ajudarão nas funções de validações e outros tratamentos.
```python
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
```


A variável que contem os estudantes, será validada através de várias funções de validação. Entre elas, coloquei a validação de tipo de ID com o padrão de instituição-cpf, cpf, email e data de nascimento. Para as validações utilizei muito a biblioteca regex. 

```python
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

```

Com o acontecimento da validação dos estudantes, serão geradas duas planilhas. Uma planilha chamada "sistema.xlsx" que irá conter os estudantes que estão de acordo com todas as regras e uma chamada "estudantes_invalidos.xlsx" onde terão os estudantes com as informações inválidas.
Propositalmente, coloquei um dos estudantes com um padrão de validação inválido, para que seja gerado a outra tabela. Com isso, teremos de saída as seguintes mensagens: 


![Captura de tela de 2024-06-16 23-55-09](https://github.com/andrepinotti/teste-principia-/assets/115902096/408f83fb-bb8f-4197-a0c1-6c3197dbd4b8)


Por mais que falte muita coisa, me dediquei ao máximo até aqui, mesmo com falta de tempo por conta do final de semestre. Tive dificuldade de realizar alguns tópicos que não foram inseridos e outros não tive tempo, porém foquei nas partes
que eu sabia para que elas ao menos dessem certo. Obrigado por essa etapa! Espero que gostem.
