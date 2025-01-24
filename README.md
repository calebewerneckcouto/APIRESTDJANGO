# API de Agendamento - Django REST Framework

Esta é uma API REST para gerenciamento de agendamentos de serviços. A API permite que clientes agendem horários com prestadores de serviço e que prestadores visualizem e gerenciem seus próprios agendamentos. A API foi construída com Django e Django REST Framework (DRF).

## Funcionalidades

- **Criação de Agendamentos:** Clientes podem criar agendamentos para serviços.
- **Visualização de Agendamentos:** Prestadores podem visualizar seus próprios agendamentos.
- **Manipulação de Agendamentos:** Prestadores podem editar ou excluir seus agendamentos.
- **Horários Disponíveis:** A API retorna os horários disponíveis para agendamento com base na data fornecida.
- **Validação de Feriados:** A API verifica se a data de agendamento cai em um feriado (utilizando a API Brasil).

## Tecnologias Utilizadas

- **Django:** Framework web para Python.
- **Django REST Framework:** Para criação de APIs RESTful.
- **PostgreSQL:** Banco de dados relacional.
- **Python 3.x:** Linguagem de programação.
- **API Brasil:** Para verificação de feriados.

## Endpoints

### **1. Agendamentos**

- **GET** `/api/agendamentos/`
  - Retorna todos os agendamentos ou filtra por prestador com o parâmetro `username`.
  - **Parâmetros:**
    - `username`: Filtra os agendamentos por prestador.

- **POST** `/api/agendamentos/`
  - Cria um novo agendamento.
  - **Requisição:**
    ```json
    {
      "data_horario": "2022-12-25T09:00:00Z",
      "nome_cliente": "João da Silva",
      "email_cliente": "joao.silva@example.com",
      "telefone_cliente": "+5511998765432",
      "prestador": "prestador_username"
    }
    ```

- **GET** `/api/agendamentos/<id>/`
  - Retorna um agendamento específico.

- **PUT** `/api/agendamentos/<id>/`
  - Atualiza um agendamento específico.

- **DELETE** `/api/agendamentos/<id>/`
  - Exclui um agendamento específico.

### **2. Prestadores**

- **GET** `/api/prestadores/`
  - Retorna uma lista de todos os prestadores.

- **GET** `/api/prestadores/<id>/`
  - Retorna um prestador específico e seus agendamentos.

### **3. Horários Disponíveis**

- **GET** `/api/horarios/`
  - Retorna os horários disponíveis para agendamento na data fornecida.
  - **Parâmetros:**
    - `data`: Data no formato `YYYY-MM-DD`.
  - **Exemplo de resposta:**
    ```json
    [
      "2022-12-25T09:00:00Z",
      "2022-12-25T09:30:00Z",
      "2022-12-25T10:00:00Z",
      ...
    ]
    ```

## Permissões

- **Qualquer usuário autenticado** pode criar agendamentos.
- **Somente o prestador** de serviço pode visualizar, editar ou excluir os seus próprios agendamentos.

## Configuração e Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git

2. **Ative o Ambiente Virtual:**
   python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate     # Para Windows
3. **Instale as Dependencias:**
pip install -r requirements.txt


