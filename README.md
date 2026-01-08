# Lanchonete App – Pedidos

Este repositório contém o microsserviço **Pedidos** do projeto **Good Burguer**, desenvolvido como parte do **Tech Challenge – Fase 4** da pós-graduação **FIAP POS TECH (SOAT)**.

O serviço é responsável pelo gerenciamento do ciclo de vida dos pedidos, desde a criação até o acompanhamento de status, seguindo princípios de **Arquitetura Limpa**, **DDD** e **DevSecOps**.

---

## 🧱 Arquitetura

O projeto segue uma abordagem baseada em **Clean Architecture / Hexagonal**, com clara separação de responsabilidades:

- **API (FastAPI)** – Exposição dos endpoints REST
- **Controllers** – Orquestração das requisições
- **Use Cases** – Regras de negócio
- **Entities** – Modelos de domínio
- **Gateways / DAO** – Acesso a dados
- **Infrastructure** – Banco de dados, FastAPI e integrações externas

Estrutura resumida:

```
app/
 ├── api
 ├── controllers
 ├── use_cases
 ├── entities
 ├── gateways
 ├── dao
 ├── infrastructure
 ├── models
 └── main.py
tests/
 ├── unit
 └── integration
```

---

## 🧪 Testes

O projeto possui testes **unitários** e **de integração**, executados com `pytest`.

A cobertura de testes é gerada automaticamente durante o CI, produzindo o arquivo:

```
coverage.xml
```

Esse relatório é utilizado pelo **SonarCloud** para cálculo de coverage.

---

## 🔍 Qualidade de Código (SonarCloud)

A análise estática e de qualidade é realizada com **SonarCloud**, utilizando as configurações definidas no arquivo:

```
sonar-project.properties
```

Não há duplicação de configuração no pipeline: o workflow utiliza exclusivamente este arquivo como fonte de verdade.

---

## 🚀 CI/CD

O pipeline de CI/CD é executado via **GitHub Actions**, contemplando:

### CI
- Instalação de dependências
- Execução dos testes (`pytest`)
- Geração do `coverage.xml`
- Análise de qualidade no SonarCloud

### CD
- Build da imagem Docker
- Push para o **Amazon ECR**
- Deploy no **Amazon EKS**
- Configuração via manifests Kubernetes (`k8s/`)

---

## ☁️ Infraestrutura

- **AWS EKS** – Orquestração de containers
- **AWS ECR** – Registro de imagens
- **MongoDB Atlas** – Persistência de dados
- **Secrets** – Gerenciados via Kubernetes Secrets

As configurações sensíveis (ex: URI do MongoDB) **não ficam no código**, sendo injetadas via variáveis de ambiente.

---

## 📦 Execução Local

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

---

## 📌 Observações Importantes

- Projeto estruturado para fins acadêmicos e demonstrativos
- Enfase em boas práticas de arquitetura, testes e automação
- Parte integrante do ecossistema **Good Burguer**

---

## 👨‍💻 Autor

The Code Crafters  
Pós-graduação em Arquitetura de Sistemas – FIAP  
