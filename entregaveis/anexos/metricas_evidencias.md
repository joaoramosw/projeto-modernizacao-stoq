# Anexo: Métricas e Evidências Técnicas

## 1. Ambiente analisado

Diretório do repositório: `projeto-modernizacao-stoq/referencia/stoq`  
Fonte: `https://github.com/stoq/stoq`  
Clone realizado em: 01/06/2026  
Último commit do clone:

- hash: `c26991644d1affcf96bc2e0a0434796cabdf8448`
- autor: `luis <luisoishi@stoq.com.br>`
- data: `Mon Apr 19 15:12:18 2021 -0300`
- mensagem: `Bump version: 7.13.0 → 7.14.0`

## 2. Métricas de tamanho

| Métrica | Valor |
|---|---:|
| Arquivos Python | 954 |
| Linhas Python totais | 165.509 |
| Linhas Python em `stoq`, `stoqlib` e `plugins` | 161.936 |
| Linhas Python em testes | 39.992 |
| Arquivos `.ui` | 219 |
| Arquivos SQL | 249 |
| Arquivos `patch-*` em `data/sql` | 262 |
| Arquivos `.rst` em `docs` | 44 |
| Total aproximado de funções | 11.728 |
| Total aproximado de classes | 2.351 |

## 3. Arquivos Python mais extensos

| Arquivo | Linhas |
|---|---:|
| `stoqlib/domain/test/test_sale.py` | 2.495 |
| `stoqlib/domain/sale.py` | 2.414 |
| `stoqlib/domain/person.py` | 2.078 |
| `stoqlib/domain/test/test_product.py` | 1.524 |
| `stoqlib/domain/product.py` | 1.641 |
| `stoq/gui/pos.py` | 1.524 |
| `stoqlib/domain/workorder.py` | 1.361 |
| `stoq/lib/gui/slaves/paymentslave.py` | 1.354 |

## 4. Funções críticas por tamanho/complexidade aproximada

| Função | Arquivo | Linhas | Complexidade aproximada |
|---|---|---:|---:|
| `drawReciboCaixa` | `stoqlib/reporting/boleto.py:398` | 292 | 6 |
| `drawReciboSacado` | `stoqlib/reporting/boleto.py:163` | 215 | 3 |
| `_generate_dailymovement_data` | `stoq/lib/gui/dialogs/tilldailymovement.py:196` | 122 | 27 |
| `confirm` | `stoq/lib/gui/fiscalprinter.py:498` | 104 | 33 |
| `checkout` | `stoq/gui/pos.py:1282` | 92 | 28 |
| `_setup_widgets` | `stoq/lib/gui/dialogs/saledetails.py:155` | 91 | 23 |

Observação: a complexidade foi estimada por varredura de palavras-chave de decisão (`if`, `elif`, `for`, `while`, `except`, `and`, `or`). Portanto, deve ser usada como indicador aproximado, não como medição formal certificada.

## 5. Classes críticas

| Classe | Arquivo | Linhas | Decisões aproximadas |
|---|---|---:|---:|
| `PosApp` | `stoq/gui/pos.py:197` | 1.617 | 289 |
| `Sale` | `stoqlib/domain/sale.py:822` | 1.379 | 270 |
| `ExampleCreator` | `stoqlib/domain/exampledata.py:45` | 1.354 | 170 |
| `ShellWindow` | `stoq/gui/shell/shellwindow.py:117` | 1.078 | 136 |
| `SellableItemSlave` | `stoq/lib/gui/wizards/abstractwizard.py:80` | 773 | 174 |
| `WorkOrder` | `stoqlib/domain/workorder.py:524` | 746 | 163 |
| `Product` | `stoqlib/domain/product.py:208` | 735 | 153 |
| `Payment` | `stoqlib/domain/payment/payment.py:58` | 610 | 113 |

## 6. Marcadores de dívida técnica

| Marcador | Ocorrências |
|---|---:|
| `FIXME` | 397 |
| `TODO` | 78 |
| `XXX` | 117 |
| `except Exception` / `except:` | 44 |
| `assert` | 668 |
| `print(` | 89 |

## 7. Duplicação aproximada

Foi executada uma varredura por blocos normalizados de 8 linhas fora dos diretórios de teste. Resultado:

- 433 blocos duplicados aproximados.

Exemplos:

1. `stoqlib/domain/payment/operation.py` repete métodos como `can_pay`, `can_print`, `can_set_not_paid`, `payment_create`, `payment_delete` e `create_transaction` em múltiplas classes.
2. `stoqlib/domain/loan.py`, `returnedsale.py`, `sale.py`, `stockdecrease.py` e `transfer.py` repetem referências fiscais como `icms_info`, `ipi_info`, `pis_info` e `cofins_info`.
3. `stoqlib/domain/base.py` e módulos de migração `domainv1.py` a `domainv4.py` compartilham blocos muito semelhantes de controle de status.

## 8. Comandos usados

```powershell
git clone --depth 1 https://github.com/stoq/stoq.git "projeto-modernizacao-stoq\referencia\stoq"
rg --files -g "*.py" | Measure-Object
Get-ChildItem -Recurse -File -Filter *.py | Get-Content | Measure-Object -Line
rg -n "FIXME|TODO|XXX" stoq stoqlib plugins tests
rg -n "except Exception|except:" stoq stoqlib plugins
rg -n "def confirm|def order|def cancel|def return_" stoqlib\domain\sale.py
Get-Content pyproject.toml
Get-Content docs\howto\structure.rst
```

## 9. Limitações

- A suíte de testes não foi executada porque o ambiente local não possui Python instalado e o projeto depende de Python 3.5 e bibliotecas antigas.
- A complexidade foi estimada por análise textual, não por ferramenta especializada como Radon.
- A análise se concentrou na edição open source do repositório, não na solução comercial/SaaS atual da Stoq.
- A proposta de refatoração é arquitetural e exemplificativa; não foi aplicada ao repositório original.
