# Etapa 1: Escolha e Descrição do Sistema Legado

## 1. Identificação do sistema

**Nome:** Stoq Retail Management System  
**Repositório:** `https://github.com/stoq/stoq`  
**Tipo:** ERP/PDV desktop para gestão de varejo  
**Domínio de aplicação:** lojas físicas, pontos de venda, estoque, financeiro, compras, vendas, caixa, clientes, fornecedores e processos fiscais brasileiros  
**Licença:** GPL-2.0 e LGPL-2.1 em partes do projeto, conforme arquivos `COPYING` e `COPYING.stoqlib`  
**Origem:** projeto brasileiro associado à Async Open Source/Stoq, com histórico público no Launchpad e GitHub  
**Aplicação no projeto:** sistema de gestão de lojas aplicado ao contexto de supermercado/mercadinho brasileiro.

## 2. Contexto de negócio

O domínio supermercadista exige alta disponibilidade no caixa, cadastro confiável de produtos, atualização de preços, controle de estoque, integração fiscal, relatórios de vendas, controle financeiro e conciliação de pagamentos. Mesmo quando o sistema é usado em lojas de menor porte, falhas no PDV afetam diretamente filas, faturamento, reputação e conformidade fiscal.

O Stoq foi escolhido por representar um sistema real de varejo brasileiro com escopo próximo ao de supermercados. A página histórica do Launchpad descreve o Stoq como um ERP open source focado principalmente no mercado brasileiro. A página do GitHub identifica o projeto como "Stoq Retail Management System". Já a presença atual da marca Stoq no ecossistema Magalu reforça a relevância de negócio: a solução atual se apresenta como plataforma para varejo físico e digital, com controle de vendas, dashboards, estoque e PDV.

## 3. Tecnologias legadas identificadas

As tecnologias foram identificadas por inspeção do repositório, especialmente `pyproject.toml`, `Makefile`, estrutura de diretórios e arquivos de código.

| Camada | Tecnologia atual no legado | Observação técnica |
|---|---|---|
| Linguagem | Python 3.5 | Versão sem suporte oficial, segundo PEP 478. |
| Interface | GTK 3, GObject Introspection, Glade XML, Kiwi GTK | Forte dependência de desktop Linux/GTK e arquivos `.ui`. |
| Persistência | PostgreSQL, psycopg2, Storm ORM | ORM menos comum no mercado atual, com migrações próprias. |
| Relatórios | Mako, ReportLab, WeasyPrint, HTML/CSS | Relatórios fiscais/financeiros espalhados por módulos. |
| Internacionalização | gettext, arquivos `.po` | Boa base de localização, mas com manutenção dispersa. |
| Plugins | ECF, optical, books, bikeshop | Arquitetura extensível, porém acoplada ao plugin manager e ao banco. |
| Empacotamento | Poetry antigo, Debian packaging, scripts `bin/` | Forte herança de ambiente Linux/deb. |
| Testes | Nose, pytest, pycodestyle, pyflakes | Pipeline antigo e dependente de ambiente GUI/banco. |

## 4. Funcionalidades principais atuais

As funcionalidades abaixo foram mapeadas a partir dos módulos `stoq/gui`, `stoqlib/domain`, `stoq/lib/gui`, `stoqlib/reporting`, `stoqlib/importers`, `data/glade` e `data/sql`.

| Área funcional | Evidência no código | Descrição |
|---|---|---|
| PDV / Caixa | `stoq/gui/pos.py`, `stoq/lib/gui/fiscalprinter.py` | Registro de venda, itens, fechamento, cupom, integração fiscal e confirmação. |
| Vendas | `stoqlib/domain/sale.py`, `stoq/gui/sales.py` | Orçamentos, pedidos, confirmação, cancelamento, devolução e comissões. |
| Estoque | `stoq/gui/stock.py`, `stoqlib/domain/product.py`, `stoqlib/domain/inventory.py` | Cadastro de produtos, itens estocáveis, inventário, movimentações e ajustes. |
| Compras e recebimento | `stoq/gui/purchase.py`, `stoqlib/domain/purchase.py`, `stoqlib/domain/receiving.py` | Pedido de compra, cotação, recebimento e relação com fornecedores. |
| Financeiro | `stoq/gui/financial.py`, `stoq/gui/payable.py`, `stoq/gui/receivable.py`, `stoqlib/domain/payment` | Contas a pagar/receber, formas de pagamento, boletos, cartões e renegociação. |
| Clientes e fornecedores | `stoqlib/domain/person.py`, `stoq/lib/gui/wizards/personwizard.py` | Cadastro de pessoas físicas/jurídicas, clientes, fornecedores e funcionários. |
| Fiscal brasileiro | `plugins/ecf`, `stoqlib/domain/fiscal.py`, `stoqlib/domain/nfe.py` | ECF, NFC-e/NF-e, dados fiscais, CFOP e livros fiscais. |
| Relatórios | `stoqlib/reporting`, `data/template` | Relatórios de vendas, caixa, estoque, compras, boletos e etiquetas. |
| Importação/exportação | `stoqlib/importers`, `stoqlib/exporters` | CSV, OFX, planilhas e dados iniciais. |
| Plugins setoriais | `plugins/optical`, `plugins/books`, `plugins/bikeshop` | Extensões para nichos específicos. |

## 5. Justificativa da escolha

O Stoq foi selecionado por quatro motivos principais:

1. **Aderência ao domínio:** o sistema cobre processos típicos de loja e supermercado, como PDV, estoque, cadastro de produtos, caixa, compras, relatórios e integração fiscal.
2. **Disponibilidade de código:** o repositório público permite engenharia reversa, coleta de métricas e análise de módulos reais.
3. **Características de legado:** o projeto usa Python 3.5, GTK/Glade, Storm ORM, empacotamento antigo e possui último commit do clone em 19/04/2021.
4. **Relevância brasileira:** o projeto nasceu orientado ao mercado nacional e contém regras fiscais, localização em português do Brasil, dados de municípios brasileiros e plugins ligados ao varejo.

## 6. Problemas preliminares encontrados

| Problema preliminar | Evidência | Impacto |
|---|---|---|
| Runtime obsoleto | `python = "^3.5"` no `pyproject.toml`; Python 3.5 encerrado oficialmente | Risco de segurança, dificuldade de instalação e incompatibilidade com dependências modernas. |
| Classes muito grandes | `stoq/gui/pos.py` com classe `PosApp` de aproximadamente 1.617 linhas; `stoqlib/domain/sale.py` com classe `Sale` de aproximadamente 1.379 linhas | Baixa legibilidade, alto custo de manutenção e maior chance de regressões. |
| Alto acoplamento entre UI, domínio e fiscal | `PosApp.checkout()` chama criação de venda, cupom, plugin manager, rollback/commit e eventos | Dificulta testes unitários e evolução incremental. |
| Complexidade elevada | Função `FiscalPrinter.confirm()` com complexidade aproximada 33; `PosApp.checkout()` com complexidade aproximada 28 | Alto risco em alteração de regras de negócio. |
| Dívida explícita no código | 397 `FIXME`, 78 `TODO` e 117 `XXX` encontrados | Indica pendências conhecidas e manutenção acumulada. |
| Migração de banco fragmentada | 262 arquivos `patch-*` em `data/sql` | Dificulta rastreabilidade, rollback e evolução segura de schema. |
| Documentação incompleta | `docs/howto/structure.rst` termina com tópicos `XXX GTK`, `XXX Glade`, `XXX Kiwi` etc. | Onboarding mais difícil e perda de conhecimento arquitetural. |

## 7. Delimitação do escopo para o projeto

O projeto não propõe reescrever todo o Stoq. A proposta se concentra no fluxo crítico de supermercado:

- cadastro de produtos;
- consulta de estoque;
- venda no PDV;
- confirmação de pagamento;
- emissão fiscal/cupom;
- fechamento de caixa;
- relatório diário.

Essa delimitação reduz risco e permite aplicar modernização incremental, mantendo partes úteis do legado enquanto novos módulos são extraídos.
