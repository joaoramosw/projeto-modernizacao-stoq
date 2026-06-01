# Etapa 2: Engenharia Reversa e Diagnóstico Técnico

## 1. Metodologia de engenharia reversa

A engenharia reversa foi conduzida por análise estática do repositório `stoq/stoq`, clonado localmente em `referencia/stoq`. Foram usadas as seguintes fontes:

- inspeção de `README.rst`, `pyproject.toml`, `Makefile`, `setup.cfg` e `docs/howto/structure.rst`;
- leitura de diretórios principais: `stoq/`, `stoqlib/`, `plugins/`, `data/`, `docs/` e `tests/`;
- contagem de arquivos, linhas de código, marcadores de dívida técnica e funções/classes extensas;
- inspeção manual de trechos críticos, especialmente `stoq/gui/pos.py`, `stoq/lib/gui/fiscalprinter.py`, `stoq/lib/gui/dialogs/tilldailymovement.py`, `stoqlib/domain/sale.py` e `stoqlib/database/tables.py`;
- comparação com fontes externas sobre o projeto, ciclo de vida do Python 3.5 e presença da Stoq no mercado brasileiro.

## 2. Visão arquitetural atual

O Stoq é um monólito desktop modularizado por pacotes internos. A arquitetura apresenta separação nominal entre interface, domínio, banco e plugins, mas a leitura do código mostra que essa separação é permeável: classes de interface coordenam transações, regras de negócio, plugins fiscais, eventos e persistência.

### 2.1 Componentes principais

| Componente | Papel arquitetural | Observação |
|---|---|---|
| `bin/` | Scripts de inicialização | Contém executáveis para iniciar aplicação e administração de banco. |
| `stoq/` | Aplicação desktop e janelas principais | Contém `gui`, `lib` e `main.py`. |
| `stoq/gui/` | Aplicações de alto nível | Módulos como `pos.py`, `sales.py`, `stock.py`, `purchase.py`, `financial.py`. |
| `stoq/lib/gui/` | Framework interno de interface | Dialogs, editors, search, slaves, widgets e wizards. |
| `stoqlib/` | Biblioteca de domínio e infraestrutura | Contém regras de negócio, banco, relatórios, importadores, exportadores e integração. |
| `stoqlib/domain/` | Modelo de domínio | Sale, Product, Person, Payment, Inventory, Purchase, Fiscal etc. |
| `stoqlib/database/` | Persistência | Configuração, ORM Storm, runtime, migrations e tabela central de classes. |
| `stoqlib/reporting/` | Relatórios | Geração de boletos, vendas, caixa, estoque e relatórios financeiros. |
| `plugins/` | Extensões | ECF, optical, books e bikeshop. |
| `data/glade/` | Layouts GTK/Glade | Interfaces XML desacopladas parcialmente do Python, mas dependentes de nomes de widgets. |
| `data/sql/` | Dados iniciais e migrações | SQL inicial, funções e centenas de patches incrementais. |
| `tests/` | Testes e fixtures | Testes unitários, GUI tests, dados esperados de relatórios e UI. |

### 2.2 Fluxo simplificado do PDV

1. O operador usa a tela de PDV em `stoq/gui/pos.py`.
2. A tela manipula itens de venda, cliente, token, troca e subtotal.
3. A venda é criada por métodos internos e objetos de domínio em `stoqlib/domain/sale.py`.
4. A confirmação chama cupom/fiscal printer em `stoq/lib/gui/fiscalprinter.py`.
5. O fluxo fiscal totaliza, configura pagamentos, fecha cupom, imprime recibos e confirma a venda.
6. As alterações são persistidas no PostgreSQL por Store/Storm.
7. Eventos internos notificam outras partes da aplicação.

## 3. Métricas coletadas

| Métrica | Resultado |
|---|---:|
| Arquivos Python | 954 |
| Linhas Python totais aproximadas | 165.509 |
| Linhas Python em `stoq`, `stoqlib` e `plugins` | 161.936 |
| Linhas Python em testes | 39.992 |
| Arquivos `.ui` GTK/Glade | 219 |
| Arquivos SQL | 249 |
| Arquivos `patch-*` em `data/sql` | 262 |
| Arquivos `.rst` em `docs` | 44 |
| Funções identificadas por varredura | 11.728 |
| Classes identificadas por varredura | 2.351 |
| Marcadores `FIXME` | 397 |
| Marcadores `TODO` | 78 |
| Marcadores `XXX` | 117 |
| Capturas genéricas `except Exception` / `except:` | 44 |
| Usos de `assert` | 668 |
| Blocos duplicados aproximados de 8 linhas fora de testes | 433 |

## 4. Arquivos e classes de maior risco

| Arquivo/classe/função | Tamanho/complexidade aproximada | Risco |
|---|---:|---|
| `stoq/gui/pos.py` - classe `PosApp` | 1.617 linhas, 289 decisões aproximadas | Concentra UI, estado de venda, cupom, plugins e persistência. |
| `stoqlib/domain/sale.py` - classe `Sale` | 1.379 linhas, 270 decisões aproximadas | Domínio de venda acumula estoque, pagamento, fiscal, comissão e entrega. |
| `stoq/lib/gui/fiscalprinter.py` - `confirm()` | 104 linhas, complexidade aproximada 33 | Fluxo crítico de confirmação com rollback, impressão e exceções genéricas. |
| `stoq/gui/pos.py` - `checkout()` | 92 linhas, complexidade aproximada 28 | Fluxo central de PDV com muitas responsabilidades. |
| `stoq/lib/gui/dialogs/tilldailymovement.py` - `_generate_dailymovement_data()` | 122 linhas, complexidade aproximada 27 | Mistura consulta, agregação, formatação e montagem de relatório. |
| `stoqlib/reporting/boleto.py` | Classe `BoletoPDF` com 761 linhas | Geração de boleto com desenho manual e alta dependência de layout. |

## 5. Diagnóstico de débito técnico

### 5.1 Acoplamento

O acoplamento é alto principalmente no fluxo de venda. A função `checkout()` em `stoq/gui/pos.py` combina validação de carrinho, regra de troca, criação de venda, controle de transação, cupom fiscal, plugin TEF, eventos e limpeza de estado da tela. Isso dificulta testar o fluxo de venda sem instanciar interface, banco e recursos fiscais.

Outro acoplamento relevante aparece em `stoqlib/domain/sale.py`. A própria documentação da classe `Sale` lista múltiplas responsabilidades: calcular preço, criar pagamentos, baixar estoque, criar entrega, verificar cliente, criar comissão, adicionar dinheiro ao caixa e calcular impostos/livros fiscais. Em termos de design, a classe atua como agregado de domínio, serviço de aplicação e coordenador de infraestrutura ao mesmo tempo.

### 5.2 Duplicação

A varredura encontrou 433 blocos duplicados aproximados de 8 linhas fora dos testes. Um exemplo aparece em `stoqlib/domain/payment/operation.py`, onde várias operações de pagamento repetem métodos como `can_pay`, `can_print`, `can_set_not_paid`, `payment_create`, `payment_delete` e `create_transaction`. Esse padrão sugere necessidade de uma política declarativa ou classe base parametrizada.

Outro exemplo está na repetição de referências fiscais (`icms_info`, `ipi_info`, `pis_info`, `cofins_info`) em módulos como `loan.py`, `returnedsale.py`, `sale.py`, `stockdecrease.py` e `transfer.py`. A duplicação aumenta o risco de inconsistência em mudanças fiscais.

### 5.3 Complexidade ciclomática alta

A medição aproximada por palavras-chave indicou funções críticas com complexidade elevada:

- `FiscalPrinter.confirm()` com complexidade aproximada 33;
- `PosApp.checkout()` com complexidade aproximada 28;
- `_generate_dailymovement_data()` com complexidade aproximada 27;
- `stoq/lib/startup.py::setup()` com complexidade aproximada 25.

Esses pontos são candidatos prioritários à extração de serviços, redução de condicionais e testes unitários.

### 5.4 Obsolescência tecnológica

O `pyproject.toml` define `python = "^3.5"`. O PEP 478 informa que Python 3.5 chegou ao fim de vida e foi retirado, sem novas releases. Isso representa risco de segurança, dificuldade de contratação, barreiras de instalação e incompatibilidade com bibliotecas modernas.

Além disso, o projeto usa bibliotecas antigas ou pouco comuns no mercado atual: Storm ORM, Kiwi GTK, Raven, Nose, Poetry antigo e dependências fixadas para compatibilidade com Ubuntu Xenial/Python 3.5. A modernização precisa tratar ambiente, testes e dependências antes de qualquer reescrita.

### 5.5 Documentação incompleta

Embora exista documentação em `docs/howto/structure.rst`, ela termina com tópicos marcados como `XXX GTK`, `XXX Glade`, `XXX Kiwi`, `XXX Proxy`, `XXX Delegate`, `XXX GUI concepts` etc. Isso indica lacunas de documentação arquitetural e dificulta onboarding de novos mantenedores.

### 5.6 Baixa manutenibilidade percebida

Os sinais combinados indicam baixa manutenibilidade em módulos críticos:

- classes grandes;
- responsabilidades misturadas;
- regras fiscais e de pagamento atravessando UI e domínio;
- migrações fragmentadas;
- dependências antigas;
- documentação incompleta;
- muitas marcações internas de dívida técnica.

## 6. Classificação do legado segundo a referência teórica

O artigo de Martins, Chervenski e Bordin (2017) destaca características recorrentes de sistemas legados: uso de tecnologia obsoleta, importância para a organização e ausência/insuficiência de documentação. O Stoq se enquadra nesse perfil:

- usa tecnologia obsoleta ou difícil de manter, como Python 3.5 e stack desktop GTK/Kiwi;
- implementa processos críticos de loja, como PDV, caixa, estoque, fiscal e financeiro;
- possui documentação, mas com lacunas e sinais de desatualização;
- contém alto volume de regras de negócio acumuladas.

## 7. Conclusão diagnóstica

O Stoq não deve ser tratado como um sistema "ruim", mas como um sistema que teve sucesso suficiente para acumular muitas regras de negócio e dependências históricas. A melhor estratégia é modernização incremental: estabilizar o ambiente, proteger fluxos críticos com testes, extrair serviços de domínio e substituir interfaces/integrações por camadas novas sem interromper a operação de caixa.
