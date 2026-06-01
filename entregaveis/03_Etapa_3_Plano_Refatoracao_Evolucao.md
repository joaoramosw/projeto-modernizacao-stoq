# Etapa 3: Refatoração e Evolução Proposta

## 1. Objetivo da evolução

Modernizar o Stoq como sistema de gestão de lojas aplicado a supermercados brasileiros, preservando regras críticas existentes e reduzindo o risco operacional. A proposta evita uma reescrita completa imediata. Em vez disso, usa modernização incremental, extração de módulos e criação de uma arquitetura evolutiva.

## 2. Estratégia geral

A estratégia recomendada é o padrão **Strangler Fig**: manter o legado funcionando enquanto novos serviços são criados ao redor dele. Os fluxos mais críticos são extraídos primeiro, com adaptadores para banco, fiscal, pagamentos e interface.

Prioridade inicial:

1. PDV e confirmação de venda;
2. estoque e produtos;
3. pagamentos e caixa;
4. relatórios diários;
5. fiscal e integrações externas.

## 3. Arquitetura-alvo proposta

| Módulo proposto | Responsabilidade | Substitui/encapsula |
|---|---|---|
| `retail-core` | Entidades e regras puras de domínio | Parte de `stoqlib/domain` |
| `sales-service` | Orquestração de venda, carrinho, troca, devolução e confirmação | `PosApp.checkout()`, parte de `Sale` |
| `inventory-service` | Saldo, movimentações, inventário e reserva | `product.py`, `inventory.py`, trechos de `sale.py` |
| `payment-service` | Formas de pagamento, autorização, conciliação e políticas | `stoqlib/domain/payment` |
| `fiscal-gateway` | NF-e/NFC-e/SAT/ECF via adaptadores | `plugins/ecf`, `fiscalprinter.py`, `domain/fiscal.py` |
| `reporting-service` | Relatórios de caixa, vendas e estoque | `stoqlib/reporting` e templates |
| `legacy-adapter` | Ponte com Storm ORM e banco atual | `stoqlib/database` |
| `api` | API REST para PDV, estoque, financeiro e relatórios | Nova camada |
| `web-pos` | Interface web/PWA para caixa | Evolução de `stoq/gui/pos.py` |
| `sync-agent` | Modo offline/local e sincronização com servidor | Nova camada |

## 4. Plano tecnológico

| Área | Estado atual | Proposta |
|---|---|---|
| Python | 3.5 | Python 3.12 ou 3.13 LTS operacional |
| ORM | Storm | SQLAlchemy 2.x ou Django ORM, com camada de repositórios |
| Migração | Patches SQL/Python próprios | Alembic ou migrações framework-first |
| Interface | GTK/Glade desktop | Web/PWA ou desktop híbrido com Tauri/Electron apenas se necessário |
| API | Ausente/limitada | FastAPI ou Django REST Framework |
| Relatórios | HTML/Mako/ReportLab dispersos | Serviço dedicado com templates versionados |
| Testes | Nose/pytest antigo | pytest moderno, testes de contrato, Playwright para UI |
| CI/CD | Makefile legado | GitHub Actions/GitLab CI com containers |
| Observabilidade | logs e Raven antigo | OpenTelemetry, logs estruturados, Sentry SDK atual |
| Deploy | ambiente local manual/debian | Docker/Compose para desenvolvimento e empacotamento automatizado |

## 5. Fases de execução

### Fase 0: Baseline e segurança operacional

Prazo estimado: 2 a 4 semanas.

- Congelar uma imagem Docker do legado.
- Documentar instalação mínima com PostgreSQL.
- Criar massa de teste de supermercado: produtos, operador, caixa, cliente, venda, pagamento, devolução.
- Executar testes possíveis e registrar os que falham por ambiente.
- Adicionar verificação de dependências e inventário de vulnerabilidades.

### Fase 1: Caracterização e testes dos fluxos críticos

Prazo estimado: 4 semanas.

- Criar testes de caracterização para `checkout`, confirmação fiscal e fechamento de caixa.
- Capturar entradas e saídas esperadas dos fluxos reais.
- Isolar dependências externas com fakes: impressora fiscal, TEF, banco, plugin manager.
- Medir cobertura dos módulos críticos.

### Fase 2: Refatoração interna sem mudança funcional

Prazo estimado: 6 semanas.

- Extrair `CheckoutService`.
- Extrair `SaleConfirmationWorkflow`.
- Extrair `DailyMovementReportBuilder`.
- Criar interfaces para `CouponGateway`, `PaymentGateway`, `FiscalGateway`, `SaleRepository` e `TillRepository`.
- Substituir condicionais grandes por políticas ou objetos de estratégia.

### Fase 3: API e camada de compatibilidade

Prazo estimado: 6 a 8 semanas.

- Criar API para produtos, estoque, carrinho, venda, pagamento e fechamento de caixa.
- Manter adaptador para banco atual via `legacy-adapter`.
- Publicar contratos OpenAPI.
- Implementar autenticação e autorização por perfil de operador/gerente.

### Fase 4: Interface moderna e piloto

Prazo estimado: 6 a 8 semanas.

- Desenvolver `web-pos` focado em fluxo de caixa rápido.
- Suportar leitor de código de barras, atalhos de teclado e modo offline.
- Pilotar em um caixa/loja antes de substituir a interface antiga.
- Medir tempo de atendimento, erros de operador e estabilidade.

### Fase 5: Migração de banco e desativação gradual

Prazo estimado: 8 a 12 semanas.

- Mapear tabelas legadas para novo modelo.
- Criar migrações reversíveis.
- Executar sincronização paralela por período controlado.
- Desativar módulos antigos apenas após equivalência funcional comprovada.

## 6. Antes vs. Depois: evidências de código

### 6.1 Refatoração do fluxo de checkout

**Antes:** em `stoq/gui/pos.py`, `checkout()` valida venda vazia, cria store, trata troca, cria venda, decide `save_only`, abre cupom, confirma cupom, cancela venda via plugin TEF, emite evento, fecha conexão e limpa tela.

Problema: a tela de PDV coordena regra de negócio, transação, plugin fiscal e estado visual.

**Depois proposto:** `PosApp` deve apenas coletar dados da interface e delegar para um serviço.

```python
class CheckoutService:
    def checkout(self, command: CheckoutCommand) -> CheckoutResult:
        self.validator.validate(command)
        sale = self.sale_factory.create(command)
        self.trade_service.apply_if_needed(command.trade, sale)

        if command.save_only:
            return self.order_service.save_order(sale)

        return self.confirmation_workflow.confirm(
            sale=sale,
            subtotal=command.subtotal,
            cancel_on_failure=command.cancel_clear,
        )
```

Melhoria: reduz acoplamento da UI, permite testes unitários do fluxo e centraliza regras de transação.

### 6.2 Refatoração da confirmação fiscal

**Antes:** `FiscalPrinter.confirm()` mistura confirmação da venda, diálogo de pagamento, totalização, pagamentos, fechamento de cupom, impressão, rollback, exceções e impressão de boletos/carnês.

**Depois proposto:** transformar em workflow explícito.

```python
class SaleConfirmationWorkflow:
    def confirm(self, sale, subtotal):
        with self.transaction.begin() as tx:
            self.payment_guard.ensure_not_overpaid(sale)
            model = self.confirm_sale_ui.request_confirmation(sale, subtotal)
            self.fiscal_gateway.totalize(sale)
            self.payment_gateway.setup_payments(sale)
            self.fiscal_gateway.close_coupon(sale)
            self.sale_service.confirm(sale)
            tx.commit(model)

        self.post_commit_printer.print_optional_documents(sale)
        return ConfirmationResult.confirmed(sale.id)
```

Melhoria: o fluxo passa a ter etapas nomeadas, rollback padronizado e integrações substituíveis por fakes em testes.

### 6.3 Refatoração do relatório diário de caixa

**Antes:** `_generate_dailymovement_data()` consulta pagamentos de entrada, pagamentos de saída, monta objetos de venda, formata dados de cartão/cheque, calcula resumo por método e busca suprimentos/sangrias.

**Depois proposto:** separar consulta, agregação e apresentação.

```python
class DailyMovementReportBuilder:
    def build(self, criteria):
        in_payments = self.repository.find_in_payments(criteria)
        out_payments = self.repository.find_out_payments(criteria)
        entries = self.repository.find_till_entries(criteria)

        return DailyMovementReport(
            sales=self.sales_aggregator.aggregate(in_payments),
            returns=self.returns_aggregator.aggregate(out_payments),
            method_summary=self.method_summary.aggregate(in_payments, out_payments),
            card_summary=self.card_summary.aggregate(in_payments),
            supplies=entries.supplies,
            removals=entries.removals,
        )
```

Melhoria: relatórios passam a ser testáveis sem GTK e sem widgets.

### 6.4 Redução de duplicação em operações de pagamento

**Antes:** `stoqlib/domain/payment/operation.py` repete métodos booleanos em várias classes.

**Depois proposto:** política declarativa de capacidades.

```python
@dataclass(frozen=True)
class PaymentOperationPolicy:
    can_cancel: bool = True
    can_change_due_date: bool = True
    can_pay: bool = True
    can_print: bool = False
    can_set_not_paid: bool = True
    create_transaction: bool = True

class PaymentOperation:
    policy = PaymentOperationPolicy()

    def can_pay(self, payment):
        return self.policy.can_pay
```

Melhoria: reduz repetição e torna diferenças entre meios de pagamento explícitas.

## 7. Plano de modularização

| Prioridade | Ação | Resultado esperado |
|---|---|---|
| Alta | Extrair `CheckoutService` | PDV testável sem GTK. |
| Alta | Criar portas `FiscalGateway` e `PaymentGateway` | TEF/ECF/NFC-e isolados. |
| Alta | Criar `SaleRepository` | Domínio separado do Storm. |
| Média | Extrair relatório diário | Relatórios testáveis e reutilizáveis pela API. |
| Média | Criar políticas de pagamento | Menos duplicação e regras mais claras. |
| Média | Criar camada `retail-core` | Domínio progressivamente independente. |
| Baixa | Substituir telas GTK por web | Deve ocorrer após estabilização das regras. |

## 8. Viabilidade, riscos e mitigação

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Quebra fiscal em venda real | Alta | Muito alto | Testes de caracterização, homologação fiscal e rollout por loja. |
| Perda de dados em migração | Média | Muito alto | Backup, migração reversível, execução paralela e validação por amostragem. |
| Resistência de operadores de caixa | Média | Alto | Interface com atalhos, treinamento e piloto controlado. |
| Dependência de hardware fiscal antigo | Alta | Alto | Adaptadores por dispositivo e inventário de equipamentos. |
| Escopo crescer demais | Alta | Alto | Modernizar por fluxo, não por reescrita completa. |
| Baixa cobertura de testes | Alta | Alto | Testes de caracterização antes de refatorar. |
| Equipe desconhecer regras antigas | Média | Alto | Documentar decisões e envolver usuários-chave. |

## 9. Cronograma macro recomendado

| Período | Entrega |
|---|---|
| Semanas 1-4 | Baseline, ambiente, métricas, documentação do legado e testes iniciais. |
| Semanas 5-8 | Testes de caracterização de PDV, venda, caixa e fiscal. |
| Semanas 9-14 | Refatoração interna: checkout, confirmação fiscal e relatórios. |
| Semanas 15-22 | API inicial e adaptadores para banco/fiscal/pagamento. |
| Semanas 23-30 | Interface web/PWA piloto para PDV. |
| Semanas 31-36 | Migração controlada, observabilidade e rollout gradual. |

## 10. Resultado esperado

Ao final da evolução, o sistema deixa de depender de uma tela monolítica para coordenar regras críticas. O PDV passa a ter serviços testáveis, adaptadores substituíveis, API documentada e caminho realista para modernização de interface e banco de dados. O legado continua útil durante a transição, mas deixa de ser o único ponto de manutenção.
