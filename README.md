# Descrição do Projeto
Este repositório contém uma implementação simples de blockchain em Python, que utiliza a API do Google Drive como camada de armazenamento distribuído. Cada bloco da cadeia é salvo como um arquivo na sua conta do Drive, permitindo simular vários clientes (nós) interagindo entre si por meio de operações de upload/download de arquivos.
📦 Funcionalidades

    Criação de Blocos: Geração de blocos com timestamp, hash do bloco anterior e dados transacionais (não inseridos), hash do bloco e nonce.

    Validação de Cadeia: Verificação da integridade da blockchain através da conferência de hashes.

    Armazenamento Distribuído: Uso do Google Drive para armazenar e sincronizar blocos entre clientes.

    Simulação de Clientes: Execução de múltiplas instâncias do nó (cliente) em threads ou processos para testar consenso básico.

### 🛠️ Tecnologias

    Python 3.8+

    Google Drive API v3

    Bibliotecas Python:

        google-auth

        google-api-python-client

### 🚀 Pré-requisitos

    Conta Google com acesso ao Drive.

    Projeto habilitado no Google Cloud Console com credenciais OAuth 2.0.

    Python 3.8 ou superior instalado.

    virtualenv (recomendado) ou similar.

### ⚙️ Instalação
- Clone este repositório

- Crie e ative um ambiente virtual
  
      python3 -m virtualenv venv
      source venv/bin/activate  # Linux/Mac
      venv\Scripts\activate     # Windows


- Instale dependências:
  
      pip install -r requirements.txt


### 🔧 Configuração da Google Drive API

    Acesse o Google Cloud Console.

    Crie um novo projeto e habilite a Google Drive API.

    Na seção "Credenciais", crie um OAuth Client ID do tipo Aplicativo de Desktop.

    Faça o download do arquivo credentials.json e coloque-o na raiz do projeto.

    Execute pela primeira vez para gerar o token de acesso:

    python main.py

    Isso criará um arquivo token.json com seu consentimento.

### ▶️ Uso
    O projeto está configurado para rodar em forma de experimentos, ou seja, uma quatidade fixa de threads (clientes) gerando um quantidade fixa de arquivos cada. Você pode modificar para as threads rodarem de forma inderteminada modificando o Main.py

Para executar:
    python main.py

### 📉Análise

  Fizemos alguns testes de análise de colisões. Nessas investigações, alteramos a dificuldade do Proof of Work e obtivemos dados úteis para testar diferentes níveis de dificuldade. Quando maior a dificuldade, menor o número de colisões; em contrapartida, o tempo para gerar um bloco aumenta exponencialmente.

Para a análise, contamos com 20 threads, cada uma gerando dois arquivos. Ao final do experimento, foram criados 40 arquivos. Cada cliente monitora a blockchain enquanto minera um bloco e, se detectar que outro nó já validou o mesmo bloco primeiro, desiste da mineração. Assim, quanto maior a dificuldade do Proof of Work, mais tempo leva para gerar o bloco, aumentando a probabilidade de desistência e reduzindo o número de colisões.
![image](https://github.com/user-attachments/assets/d3e09a5c-9aa4-4cfe-92b8-4bbba70c4c6a)

#### Interpretação do gráfico:
  Interpretação do gráfico
- A dificuldade representa o número de zeros exigidos no início do hash para que o bloco seja considerado válido.
- A média de colisões é calculada com base em três experimentos por nível de dificuldade e indica quantos blocos inválidos foram gerados.

A média de colisões revela o volume de esforço computacional desperdiçado na geração de blocos inválidos. Na dificuldade 3, obtivemos em média apenas 12 blocos válidos, enquanto na dificuldade 6 alcançamos 36 blocos válidos. É importante notar que o tempo para gerar os blocos aumenta exponencialmente à medida que elevamos a dificuldade.


### 🤝 Contribuidores

    Pedro Vinicius - @PedroVinici

    Caio Victor - @CaioVFA

    Gabriel Alves - @kpzinnm

