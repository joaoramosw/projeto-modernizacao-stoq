# Anexo: Diagramas Mermaid

Os diagramas abaixo podem ser colados em editores compatíveis com Mermaid, como GitHub, Obsidian, Mermaid Live Editor ou extensões do VS Code.

## 1. Arquitetura atual

```mermaid
flowchart TD
    User[Operador de caixa / gestor] --> GTK[Interface desktop GTK/Glade]
    GTK --> StoqGUI[stoq/gui<br/>POS, vendas, estoque, financeiro]
    StoqGUI --> GuiLib[stoq/lib/gui<br/>dialogs, editors, widgets, wizards]
    StoqGUI --> Domain[stoqlib/domain<br/>Sale, Product, Payment, Person]
    GuiLib --> Domain
    Domain --> Database[stoqlib/database<br/>Storm ORM, Store, migrations]
    Database --> Postgres[(PostgreSQL)]
    StoqGUI --> FiscalPrinter[stoq/lib/gui/fiscalprinter.py]
    FiscalPrinter --> Plugins[plugins<br/>ECF, optical, books, bikeshop]
    Plugins --> Devices[Impressora fiscal / TEF / integrações]
    Domain --> Reporting[stoqlib/reporting]
    Reporting --> Templates[data/template]
    GTK --> UIXML[data/glade e data/uixml]
```

## 2. Fluxo atual de checkout

```mermaid
sequenceDiagram
    actor Operador
    participant PosApp as stoq/gui/pos.py::PosApp
    participant Store as Storm Store
    participant Sale as stoqlib/domain/sale.py::Sale
    participant Coupon as FiscalPrinter/Coupon
    participant Plugins as Plugin Manager

    Operador->>PosApp: Finalizar venda
    PosApp->>PosApp: Validar itens/token/troca
    PosApp->>Store: Criar store ou savepoint
    PosApp->>Sale: Criar venda
    PosApp->>Coupon: Abrir cupom/adicionar itens
    PosApp->>Coupon: Confirmar venda
    Coupon->>Sale: Confirmar domínio
    Coupon->>Store: Commit/Rollback
    PosApp->>Plugins: Verificar TEF/ECF em falha
    PosApp->>PosApp: Emitir evento e limpar pedido
```

## 3. Arquitetura proposta

```mermaid
flowchart TD
    Cashier[Operador de caixa] --> WebPOS[web-pos / PWA PDV]
    Manager[Gestor] --> Backoffice[Backoffice web]

    WebPOS --> API[API REST/OpenAPI]
    Backoffice --> API

    API --> Sales[Sales Service]
    API --> Inventory[Inventory Service]
    API --> Payments[Payment Service]
    API --> Reports[Reporting Service]

    Sales --> Core[Retail Core<br/>entidades e regras puras]
    Inventory --> Core
    Payments --> Core

    Sales --> Fiscal[Fiscal Gateway]
    Payments --> PaymentGateway[Payment Gateway/TEF]
    Fiscal --> FiscalAgent[Agente fiscal local]
    FiscalAgent --> Devices[Impressora/NFC-e/SAT/ECF]

    Sales --> LegacyAdapter[Legacy Adapter]
    Inventory --> LegacyAdapter
    Reports --> LegacyAdapter
    LegacyAdapter --> LegacyDB[(PostgreSQL legado)]

    NewMigrations[Alembic / Migrações modernas] --> LegacyDB
```

## 4. Estratégia Strangler Fig

```mermaid
timeline
    title Modernização incremental
    1-4 semanas : Baseline do legado
                : Ambiente reproduzível
                : Inventário de riscos
    5-8 semanas : Testes de caracterização
                : Fluxos PDV, fiscal e caixa
    9-14 semanas : CheckoutService
                 : SaleConfirmationWorkflow
                 : DailyMovementReportBuilder
    15-22 semanas : API REST
                  : Legacy Adapter
                  : Contratos OpenAPI
    23-30 semanas : Web/PWA PDV piloto
                  : Treinamento e operação paralela
    31-36 semanas : Migração controlada
                  : Observabilidade
                  : Rollout gradual
```
