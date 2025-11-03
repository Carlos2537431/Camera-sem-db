# Monitoramento de Veículos Roubados

Este projeto é um sistema de monitoramento de veículos roubados que utiliza câmeras em ruas para identificar veículos e notificar imediatamente as autoridades através da nuvem. O sistema integra com a API Monuv, Detecta e Alerta Brasil para fornecer alertas em tempo real sobre veículos roubados.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
monitoramento-veiculos-roubados
├── src
│   ├── main.py                     # Ponto de entrada da aplicação
│   ├── api                         # Módulo da API
│   │   ├── routes                  # Rotas da API
│   │   ├── deps.py                 # Dependências comuns
│   ├── core                        # Configurações e logging
│   ├── services                    # Lógica de negócios e integrações
│   ├── workers                     # Tarefas em segundo plano
│   └── types                       # Modelos de dados
├── configs                         # Configurações da aplicação
├── tests                           # Testes automatizados
├── scripts                         # Scripts auxiliares
├── .env.example                    # Exemplo de variáveis de ambiente
├── requirements.txt                # Dependências do projeto
├── pyproject.toml                  # Configurações do projeto
├── Dockerfile                      # Instruções para construção da imagem Docker
└── README.md                       # Documentação do projeto
```

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd monitoramento-veiculos-roubados
   ```

2. Crie um ambiente virtual e ative-o:
   ```
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate     # Para Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente copiando o arquivo `.env.example` para `.env` e ajustando conforme necessário.

## Uso

Para iniciar a aplicação, execute o seguinte comando:
```
python src/main.py
```

A aplicação estará disponível em `http://localhost:8000`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar problemas.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.