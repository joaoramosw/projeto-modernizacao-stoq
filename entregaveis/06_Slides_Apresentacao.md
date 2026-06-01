# Estrutura de Slides para Apresentação

## Slide 1 - Título

**Evolução e Modernização de Sistema Legado**  
Estudo técnico do Stoq Retail Management System aplicado ao contexto supermercadista brasileiro  
João Victor Silva Ramos  
Docente: Sheila Tirony de Almeida Silva

## Slide 2 - Objetivo do projeto

- Analisar um sistema legado real.
- Realizar engenharia reversa.
- Diagnosticar débito técnico.
- Propor modernização e refatoração.
- Demonstrar viabilidade técnica e de negócio.

## Slide 3 - Sistema escolhido

**Stoq Retail Management System**

- ERP/PDV open source de varejo.
- Código público no GitHub.
- Origem no mercado brasileiro.
- Aplicável a supermercados, mercadinhos e lojas físicas.
- Possui PDV, estoque, vendas, compras, financeiro, fiscal e relatórios.

## Slide 4 - Por que é legado?

- Python 3.5.
- GTK/Glade/Kiwi desktop.
- Storm ORM.
- Migrações SQL/Python próprias.
- Último commit do clone: 19/04/2021.
- Classes grandes e fluxos críticos acoplados.
- Documentação parcial.

## Slide 5 - Funcionalidades atuais

- PDV e fechamento de venda.
- Cadastro de produtos.
- Estoque e inventário.
- Compras e recebimento.
- Contas a pagar/receber.
- Clientes e fornecedores.
- Fiscal brasileiro.
- Relatórios gerenciais.
- Plugins setoriais.

## Slide 6 - Arquitetura atual

Mostrar diagrama:

- Interface desktop em `stoq/gui`.
- Framework de UI em `stoq/lib/gui`.
- Domínio em `stoqlib/domain`.
- Banco em `stoqlib/database`.
- Relatórios em `stoqlib/reporting`.
- Plugins em `plugins`.
- PostgreSQL + Storm ORM.

## Slide 7 - Métricas da engenharia reversa

- 954 arquivos Python.
- 165.509 linhas Python.
- 219 arquivos `.ui`.
- 249 arquivos SQL.
- 262 patches de banco.
- 397 `FIXME`.
- 78 `TODO`.
- 117 `XXX`.
- 433 blocos duplicados aproximados.

## Slide 8 - Débito técnico principal

- Acoplamento entre UI, domínio, banco e fiscal.
- Métodos críticos com alta complexidade.
- Classes extensas: `PosApp`, `Sale`, `BoletoPDF`.
- Dependências obsoletas.
- Duplicação de regras.
- Documentação incompleta.

## Slide 9 - Evidência 1: checkout

Arquivo: `stoq/gui/pos.py`

Problema:

- `checkout()` faz validação, cria venda, controla banco, chama cupom, trata TEF, rollback e eventos.

Proposta:

- Extrair `CheckoutService`.
- Criar `CheckoutCommand`.
- Isolar cupom e pagamento por interfaces.

## Slide 10 - Evidência 2: confirmação fiscal

Arquivo: `stoq/lib/gui/fiscalprinter.py`

Problema:

- `confirm()` mistura venda, cupom, pagamento, impressão, exceção e banco.

Proposta:

- Criar `SaleConfirmationWorkflow`.
- Separar `FiscalGateway`, `PaymentGateway`, `ReceiptPrinter` e `TransactionManager`.

## Slide 11 - Arquitetura proposta

Módulos:

- `retail-core`
- `sales-service`
- `inventory-service`
- `payment-service`
- `fiscal-gateway`
- `reporting-service`
- `legacy-adapter`
- `api`
- `web-pos`
- `sync-agent`

## Slide 12 - Estratégia de evolução

- Não reescrever tudo.
- Usar modernização incremental.
- Criar testes de caracterização.
- Extrair serviços críticos.
- Expor API.
- Migrar interface por piloto.
- Migrar banco com execução paralela.

## Slide 13 - Riscos e mitigação

Riscos:

- Quebra fiscal.
- Perda de dados.
- Hardware antigo.
- Baixa cobertura de testes.
- Resistência dos operadores.

Mitigação:

- Testes de caracterização.
- Backups.
- Homologação fiscal.
- Piloto controlado.
- Rollout gradual.

## Slide 14 - Cronograma

- Semanas 1-4: baseline e ambiente.
- Semanas 5-8: testes de caracterização.
- Semanas 9-14: refatoração interna.
- Semanas 15-22: API e adaptadores.
- Semanas 23-30: web/PWA piloto.
- Semanas 31-36: migração e rollout.

## Slide 15 - Conclusão

- O Stoq é um legado relevante, não descartável.
- A maior dívida está nos fluxos críticos de PDV, fiscal e domínio de venda.
- A modernização deve preservar conhecimento de negócio.
- A proposta incremental reduz risco e aumenta manutenibilidade.
