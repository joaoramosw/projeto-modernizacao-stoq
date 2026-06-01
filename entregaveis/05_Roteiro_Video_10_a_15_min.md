# Roteiro para Vídeo Final - 10 a 15 minutos

Tempo-alvo: 12 minutos  
Formato: apresentação com narração + demonstração de repositório/código/documentos  
Tema: Evolução e modernização do Stoq, sistema legado de gestão de lojas aplicado a supermercados brasileiros.

## Antes de gravar

Abra estas janelas:

1. `04_Relatorio_Tecnico_ABNT.md`;
2. `referencia/stoq` no explorador ou editor;
3. `pyproject.toml`;
4. `stoq/gui/pos.py` na linha do método `checkout`;
5. `stoq/lib/gui/fiscalprinter.py` na linha do método `confirm`;
6. `stoqlib/domain/sale.py` na classe `Sale`;
7. `codigo_refatorado_proposto/checkout_service.py`;
8. `anexos/diagramas_mermaid.md`.

## 0:00 - 0:40 | Abertura

**Tela:** slide 1 ou capa do relatório.

**Fala sugerida:**

"Olá, professora Sheila. Meu nome é João Victor Silva Ramos. Neste vídeo eu apresento o projeto de evolução e modernização de um sistema legado. O sistema escolhido foi o Stoq Retail Management System, um ERP/PDV brasileiro de varejo, analisado como base para um cenário de supermercado ou mercadinho no Brasil. O objetivo foi fazer engenharia reversa, diagnosticar débito técnico e propor uma reengenharia incremental."

## 0:40 - 1:40 | Escolha do sistema

**Tela:** repositório GitHub do Stoq ou arquivo `01_Etapa_1_Escolha_e_Descricao.md`.

**Fala sugerida:**

"A escolha do Stoq foi feita por três motivos. Primeiro, ele tem aderência ao domínio de loja e supermercado, com PDV, estoque, vendas, compras, caixa, financeiro e fiscal. Segundo, o código é público no GitHub, o que permite uma análise real e não apenas hipotética. Terceiro, ele possui características claras de sistema legado: dependência de Python 3.5, interface desktop em GTK/Glade, ORM Storm, plugins fiscais e último commit do clone em abril de 2021."

## 1:40 - 2:40 | Contexto de negócio

**Tela:** slide sobre supermercado/fluxo de loja.

**Fala sugerida:**

"No contexto de um supermercado, o sistema de gestão é crítico. Se o PDV para, a fila cresce e a venda não acontece. Se o estoque fica errado, compras e reposição são prejudicadas. Se a parte fiscal falha, a loja pode ter problema legal. Por isso, o sistema legado não pode ser simplesmente descartado. Ele precisa ser compreendido, protegido e modernizado por etapas."

## 2:40 - 4:00 | Arquitetura atual

**Tela:** `anexos/diagramas_mermaid.md`, diagrama da arquitetura atual.

**Fala sugerida:**

"A engenharia reversa mostrou uma arquitetura desktop monolítica, organizada por pacotes. O pacote `stoq` concentra a aplicação e as telas principais. O pacote `stoqlib` concentra domínio, banco, relatórios e infraestrutura. O diretório `plugins` adiciona integrações, como ECF. O diretório `data` tem arquivos Glade de interface, templates, SQL e dados fiscais. Existe separação por pastas, mas na prática a tela de PDV coordena regra de negócio, banco, cupom fiscal e eventos."

## 4:00 - 5:30 | Métricas e evidências

**Tela:** `anexos/metricas_evidencias.md`.

**Fala sugerida:**

"Foram encontrados 954 arquivos Python, cerca de 165 mil linhas Python, 219 arquivos de interface `.ui`, 249 arquivos SQL e 262 patches de banco. Também foram encontrados 397 `FIXME`, 78 `TODO`, 117 `XXX`, 44 capturas genéricas de exceção e 433 blocos duplicados aproximados fora dos testes. Esses números não significam que o sistema não funciona; eles indicam que a manutenção acumulou risco."

## 5:30 - 7:00 | Trecho crítico 1: checkout do PDV

**Tela:** `stoq/gui/pos.py`, método `checkout`.

**Fala sugerida:**

"O primeiro trecho crítico é o método `checkout`, dentro da classe `PosApp`. Ele deveria ser apenas uma ação da interface, mas concentra validação de venda vazia, token, store de banco, savepoint, troca, criação de venda, confirmação de cupom, TEF, rollback, evento e limpeza do pedido. Isso mostra alto acoplamento entre interface, domínio e infraestrutura. A proposta é extrair esse fluxo para um `CheckoutService`, deixando a tela apenas coletar dados e exibir resultado."

## 7:00 - 8:15 | Trecho crítico 2: confirmação fiscal

**Tela:** `stoq/lib/gui/fiscalprinter.py`, método `confirm`.

**Fala sugerida:**

"O segundo trecho crítico é a confirmação fiscal. O método `confirm` verifica pagamento, executa wizard, totaliza cupom, configura pagamentos, fecha cupom, imprime recibos, confirma a venda e trata rollback. É um fluxo sensível porque envolve venda, banco, impressão e fiscal. A proposta é transformar esse método em um workflow explícito, com etapas nomeadas e adaptadores para fiscal, pagamento e impressão."

## 8:15 - 9:20 | Trecho crítico 3: domínio de venda

**Tela:** `stoqlib/domain/sale.py`, início da classe `Sale`.

**Fala sugerida:**

"A classe `Sale` também evidencia excesso de responsabilidades. A própria documentação da classe informa que ela calcula preço, cria pagamentos, baixa estoque, cria entrega, verifica cliente, cria comissões, movimenta caixa e calcula impostos. A proposta é separar regras em serviços de domínio e aplicação, como `sales-service`, `inventory-service`, `payment-service` e `fiscal-gateway`."

## 9:20 - 10:40 | Arquitetura proposta

**Tela:** diagrama da arquitetura proposta em `anexos/diagramas_mermaid.md`.

**Fala sugerida:**

"A arquitetura proposta usa modernização incremental. O legado continua funcionando, mas novos módulos são criados ao redor dele. Primeiro, criamos uma camada `legacy-adapter` para conversar com o banco e o código antigo. Depois extraímos serviços de venda, estoque, pagamento, fiscal e relatórios. Em seguida, uma API expõe esses serviços para uma interface web/PWA de PDV. Assim, a migração pode acontecer caixa por caixa ou módulo por módulo."

## 10:40 - 11:40 | Plano e riscos

**Tela:** `03_Etapa_3_Plano_Refatoracao_Evolucao.md`, cronograma e matriz de riscos.

**Fala sugerida:**

"O cronograma proposto é de aproximadamente 36 semanas, começando por baseline e testes de caracterização, depois refatoração interna, API, interface moderna e migração controlada. Os principais riscos são quebra fiscal, perda de dados, dependência de hardware antigo, baixa cobertura de testes e resistência de operadores. A mitigação é piloto controlado, execução paralela, backups, testes de contrato e homologação fiscal."

## 11:40 - 12:30 | Conclusão

**Tela:** conclusão do relatório.

**Fala sugerida:**

"Concluindo, o Stoq é um bom exemplo de sistema legado porque é útil, possui regras relevantes e, ao mesmo tempo, apresenta dificuldades de evolução. A proposta não é jogar o sistema fora, mas preservar o conhecimento de negócio e reduzir risco por modernização incremental. O resultado esperado é um PDV mais testável, uma arquitetura mais modular e uma base mais segura para evolução tecnológica."

## 12:30 - 13:00 | Encerramento

**Tela:** checklist da matriz de avaliação.

**Fala sugerida:**

"Neste projeto foram entregues a ficha técnica, engenharia reversa, diagnóstico de débito técnico, plano de refatoração, relatório formal ABNT, evidências de código e roteiro de apresentação. Obrigado."

## Dicas de gravação

- Fale em ritmo calmo, sem ler cada tabela inteira.
- Mostre pelo menos dois trechos reais do código para a demonstração prática.
- Ao falar de métricas, explique o impacto, não apenas o número.
- Não diga que "o sistema é ruim"; diga que "o sistema acumulou dívida técnica por sucesso e tempo de vida".
- Termine reforçando viabilidade: modernizar por etapas, sem parar a loja.
