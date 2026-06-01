# UNIVERSIDADE CATÓLICA DO SALVADOR

## CURSO DE TECNOLOGIA / ENGENHARIA DE SOFTWARE

<br><br><br>

# JOÃO VICTOR SILVA RAMOS

<br><br><br>

# EVOLUÇÃO E MODERNIZAÇÃO DE UM SISTEMA LEGADO DE GESTÃO DE LOJAS: ESTUDO TÉCNICO DO STOQ RETAIL MANAGEMENT SYSTEM APLICADO AO CONTEXTO SUPERMERCADISTA BRASILEIRO

<br><br><br><br>

Salvador  
2026

\pagebreak

# JOÃO VICTOR SILVA RAMOS

<br><br><br>

# EVOLUÇÃO E MODERNIZAÇÃO DE UM SISTEMA LEGADO DE GESTÃO DE LOJAS: ESTUDO TÉCNICO DO STOQ RETAIL MANAGEMENT SYSTEM APLICADO AO CONTEXTO SUPERMERCADISTA BRASILEIRO

<br><br>

Relatório técnico apresentado à disciplina de Evolução e Modernização de Sistemas Legados, como requisito avaliativo parcial.

Docente: Sheila Tirony de Almeida Silva

Discente: João Victor Silva Ramos  
E-mail: joaovictor.ramos@ucsal.edu.br

<br><br><br><br>

Salvador  
2026

\pagebreak

# RESUMO

Este relatório apresenta uma análise técnica, processo de engenharia reversa e proposta de modernização para o Stoq Retail Management System, sistema open source de gestão de varejo com funcionalidades de PDV, estoque, vendas, compras, financeiro, relatórios e integrações fiscais brasileiras. O estudo considera o sistema como base legada aplicada ao contexto de supermercados e mercadinhos no Brasil, uma vez que tais organizações dependem de sistemas de caixa e retaguarda para manter operação contínua, controle de estoque, emissão fiscal e acompanhamento financeiro. A metodologia adotada envolveu análise estática do repositório público, leitura de documentação interna, inspeção de arquivos críticos, coleta de métricas e comparação com conceitos de sistemas legados, evolução e refatoração. Os resultados indicam que o Stoq possui características clássicas de legado: tecnologia obsoleta, grande volume de regras de negócio acumuladas, acoplamento entre interface e domínio, classes extensas, complexidade elevada em fluxos críticos, documentação incompleta e dependência de infraestrutura antiga. Como proposta de evolução, recomenda-se uma modernização incremental baseada no padrão Strangler Fig, com extração progressiva de serviços de venda, estoque, pagamento, fiscal e relatórios, preservando o legado em funcionamento até que os novos módulos sejam validados. Conclui-se que o Stoq não deve ser tratado como um sistema descartável, mas como um ativo de software que exige estabilização, encapsulamento e evolução orientada a riscos.

Palavras-chave: sistema legado; engenharia reversa; refatoração; PDV; supermercado; modernização de software; Stoq.

\pagebreak

# 1 INTRODUÇÃO

Sistemas de gestão comercial são elementos centrais para a operação de lojas, supermercados e demais organizações varejistas. Em um supermercado, o sistema de informação não apenas registra vendas, mas também sustenta processos de estoque, formação de preço, compras, caixa, pagamentos, relatórios gerenciais e emissão de documentos fiscais. Assim, falhas no software podem produzir efeitos imediatos no negócio: filas no caixa, divergência de estoque, erro de cobrança, perda de faturamento, inconsistência contábil e risco de descumprimento fiscal.

O presente projeto tem como objetivo analisar um sistema legado de gestão de lojas, identificar seus problemas técnicos e propor um plano de reengenharia e modernização. O sistema selecionado foi o Stoq Retail Management System, disponível em repositório público no GitHub. O Stoq foi escolhido por possuir aderência ao domínio de varejo brasileiro, por apresentar funcionalidades típicas de sistemas de supermercado e por disponibilizar código suficiente para análise técnica. A página histórica do Launchpad descreve o Stoq como um ERP open source voltado principalmente ao mercado brasileiro, enquanto o repositório GitHub identifica o projeto como um sistema de gestão de varejo. A trajetória da marca também reforça a relevância do caso: a Stoq foi adquirida pelo Magalu em 2020 e sua linha atual é apresentada como solução de PDV, estoque, dashboards e gestão para varejo físico e digital.

A análise foi realizada sobre a edição open source do Stoq, e não sobre a solução SaaS atual da marca. Essa delimitação é importante porque a disciplina exige a escolha de um software base analisável, preferencialmente de repositório público. Sistemas proprietários de redes específicas de supermercados dificilmente disponibilizam seu código-fonte; portanto, o Stoq permite conciliar realismo de domínio, aderência ao mercado brasileiro e possibilidade concreta de engenharia reversa.

Segundo Martins, Chervenski e Bordin (2017), sistemas legados são frequentemente associados a três características recorrentes na literatura: uso de tecnologia obsoleta, importância para a organização e ausência ou insuficiência de documentação. O Stoq analisado apresenta esses sinais. O repositório contém dependência de Python 3.5, versão oficialmente retirada de suporte conforme o PEP 478; usa GTK/Glade e Kiwi para interface desktop; depende do ORM Storm e de migrações próprias; e possui classes extensas em fluxos críticos como PDV, venda, pagamento e fiscal.

Este relatório está organizado em quatro partes principais. A primeira apresenta a fundamentação teórica sobre sistemas legados, engenharia reversa, débito técnico e refatoração. A segunda descreve o sistema escolhido, suas funcionalidades e sua arquitetura atual. A terceira apresenta o diagnóstico técnico, com métricas e evidências de código. A quarta propõe uma estratégia de modernização incremental, incluindo modularização, atualização tecnológica, exemplos comparativos de código, análise de riscos e cronograma.

# 2 FUNDAMENTAÇÃO TEÓRICA

## 2.1 Sistemas legados

Um sistema legado pode ser entendido como um software que permanece relevante para a organização, mas que apresenta dificuldades crescentes de manutenção, evolução ou integração. Nem todo sistema antigo é necessariamente legado, e nem todo legado é tecnicamente inútil. Em muitos casos, o sistema se torna legado justamente porque foi bem-sucedido: acumulou regras de negócio, atendeu processos essenciais e passou a ser utilizado por longos períodos.

Bennett (1995) discute sistemas legados como resultado do próprio sucesso do software. Uma aplicação que permanece em uso por muitos anos tende a incorporar exceções, integrações, regras locais e decisões históricas. Com o tempo, mesmo que continue operacional, sua estrutura interna pode se tornar difícil de modificar com segurança. O problema central não é apenas idade, mas o custo de mudança.

Martins, Chervenski e Bordin (2017) reforçam essa interpretação ao identificar características recorrentes em definições de sistemas legados. Entre as características mais frequentes estão tecnologia obsoleta, criticidade para a organização e falta de documentação. Esses três elementos se combinam de forma perigosa: o sistema não pode ser simplesmente desligado, mas também não pode evoluir com facilidade.

No contexto supermercadista, a criticidade é ainda mais evidente. O PDV precisa funcionar durante o horário de loja; o estoque precisa refletir entrada, saída, perdas e devoluções; os documentos fiscais precisam ser emitidos corretamente; e os relatórios precisam apoiar decisões de reposição, preço e gestão financeira. Portanto, a modernização de um sistema desse tipo deve evitar abordagens disruptivas sem validação.

## 2.2 Engenharia reversa

Engenharia reversa de software consiste em analisar um sistema existente para compreender sua estrutura, comportamento, dependências e regras de negócio. Diferentemente da reengenharia, a engenharia reversa não altera necessariamente o sistema; seu objetivo é recuperar conhecimento. Em sistemas com documentação incompleta, a engenharia reversa é uma etapa essencial para reduzir incerteza antes de qualquer refatoração.

No projeto analisado, a engenharia reversa foi feita por inspeção estática do código, leitura de documentação interna, coleta de métricas e observação de fluxos críticos. Esse tipo de análise permite identificar componentes, responsabilidades, dependências externas, pontos de acoplamento e arquivos de maior risco. A análise estática não substitui testes dinâmicos, mas é adequada para uma primeira etapa acadêmica quando o ambiente de execução legado possui dependências difíceis de instalar.

## 2.3 Débito técnico

Débito técnico é a diferença entre a solução atualmente implementada e uma solução mais sustentável do ponto de vista de manutenção. O conceito não indica, necessariamente, erro de implementação. Muitas dívidas surgem de decisões pragmáticas tomadas para atender prazos, compatibilidades ou limitações de contexto. Entretanto, quando não são gerenciadas, tornam a evolução mais cara e arriscada.

No Stoq, a dívida técnica aparece em diferentes formas: dependência de runtime obsoleto, classes extensas, métodos com muitas decisões, duplicação, comentários `FIXME` e `TODO`, migrações fragmentadas e documentação incompleta. Esses elementos não têm o mesmo peso, mas juntos indicam aumento do custo de mudança.

## 2.4 Refatoração

Refatoração é a alteração da estrutura interna do código sem mudança intencional de comportamento externo. Fowler (2018) define refatoração como uma técnica disciplinada para melhorar o design de código existente. Em sistemas legados, a refatoração deve ser guiada por testes de caracterização, isto é, testes que registram o comportamento atual antes de alterar a estrutura.

Para o Stoq, a refatoração recomendada não deve começar por uma reescrita completa. O caminho mais seguro é extrair serviços de aplicação em torno de fluxos críticos, como fechamento de venda e confirmação fiscal. A interface de PDV deve deixar de coordenar diretamente regras de negócio, transação de banco e integrações fiscais. Em seu lugar, serviços testáveis devem concentrar a orquestração.

## 2.5 Modernização incremental

Modernização incremental é a estratégia de evoluir um sistema por partes, reduzindo risco e mantendo operação. Uma técnica comum é o padrão Strangler Fig, no qual novas funcionalidades ou módulos substituem gradualmente partes do legado. Em vez de desligar o sistema antigo de uma só vez, cria-se uma camada nova ao redor dele, com adaptadores e contratos definidos.

Essa abordagem é adequada ao varejo porque o sistema não pode parar. Um supermercado não pode aguardar uma reescrita completa de meses para voltar a vender. A evolução deve ser feita por módulos: primeiro proteger o legado, depois extrair serviços, depois expor APIs, depois substituir interfaces e, por fim, migrar banco ou infraestrutura.

# 3 METODOLOGIA

A metodologia adotada foi dividida em seis etapas. Primeiro, foram pesquisados sistemas open source ligados a PDV, varejo e supermercado. Entre alternativas possíveis, o Stoq foi escolhido por sua relação com o mercado brasileiro e pela disponibilidade de código. Segundo, o repositório foi clonado localmente para inspeção. Terceiro, foram lidos arquivos de configuração e documentação, incluindo `README.rst`, `pyproject.toml`, `Makefile`, `setup.cfg` e `docs/howto/structure.rst`. Quarto, foram coletadas métricas de tamanho, arquivos, linhas, classes, funções, marcadores de dívida técnica e duplicação aproximada. Quinto, foram analisados manualmente trechos críticos de código. Sexto, foi elaborada uma proposta de modernização alinhada ao diagnóstico.

As métricas foram coletadas por comandos de terminal e scripts de varredura em Node/PowerShell, já que o ambiente local não possuía Python instalado. A ausência de Python impediu a execução da suíte de testes original, que de todo modo exigiria dependências antigas e ambiente gráfico/banco compatível. Essa limitação foi registrada no anexo de métricas. Ainda assim, a análise estática foi suficiente para identificar riscos estruturais e propor evolução.

O clone analisado apresentou último commit em 19 de abril de 2021, com mensagem de atualização de versão de 7.13.0 para 7.14.0. O PyPI registra o pacote `stoq` com release pública 4.7.0.post1 em 25 de março de 2020. Essa diferença indica que o repositório e o pacote público não devem ser confundidos, mas ambos reforçam a característica de base legada para fins de análise em 2026.

# 4 DESCRIÇÃO DO SISTEMA

## 4.1 Ficha técnica

O sistema analisado é o Stoq Retail Management System, um ERP/PDV desktop voltado à gestão comercial. O repositório contém 954 arquivos Python, aproximadamente 165.509 linhas de código Python, 219 arquivos `.ui` de interface GTK/Glade, 249 arquivos SQL e 262 patches incrementais de banco em `data/sql`.

A stack principal é composta por Python 3.5, GTK 3, GObject Introspection, Kiwi GTK, PostgreSQL, psycopg2, Storm ORM, Mako, ReportLab, WeasyPrint, gettext, arquivos Glade XML e plugins. O projeto contém empacotamento Debian, scripts de inicialização e documentação em reStructuredText.

## 4.2 Funcionalidades

O Stoq cobre um conjunto amplo de funcionalidades de varejo. No PDV, permite registrar itens de venda, selecionar cliente, lidar com tokens de venda, trocas, cupom e confirmação. No módulo de vendas, trata orçamentos, pedidos, confirmação, devolução e comissões. Em estoque, gerencia produtos, itens estocáveis, inventário e movimentações. Em compras, cobre pedido, cotação e recebimento. Em financeiro, possui contas a pagar, contas a receber, métodos de pagamento, boletos, cartões e renegociações. Também contém cadastro de pessoas, clientes, fornecedores, funcionários, filiais e transportadores.

O sistema possui ainda funcionalidades fiscais brasileiras, incluindo módulos ligados a ECF, NF-e/NFC-e, CFOP, dados fiscais e livros fiscais. Para relatórios, há geração de documentos de venda, caixa, estoque, boleto, etiquetas e relatórios financeiros. Essa amplitude funcional explica parte da complexidade acumulada.

## 4.3 Arquitetura atual

A arquitetura atual pode ser resumida como um monólito desktop modular. A interface principal fica em `stoq/gui`, com aplicações como `pos.py`, `sales.py`, `stock.py`, `purchase.py`, `financial.py`, `payable.py` e `receivable.py`. A infraestrutura de interface fica em `stoq/lib/gui`, com dialogs, editors, searches, slaves, widgets e wizards. O domínio e infraestrutura reaproveitável ficam em `stoqlib`, especialmente `stoqlib/domain`, `stoqlib/database`, `stoqlib/reporting`, `stoqlib/importers`, `stoqlib/exporters` e `stoqlib/lib`.

A separação existe, mas não é rígida. A tela de PDV, por exemplo, não se limita a coletar dados do usuário. Ela também chama criação de venda, manipula stores de banco, aciona cupom fiscal, consulta plugin manager, decide rollback, emite eventos e limpa estado da venda. Esse padrão indica que o sistema cresceu com uma arquitetura pragmática, na qual a interface assumiu responsabilidades de aplicação.

O banco de dados é gerenciado por PostgreSQL e Storm ORM. A lista central de tabelas aparece em `stoqlib/database/tables.py`, que importa classes de domínio e também classes vindas de plugins. Isso facilita descoberta dinâmica, mas cria acoplamento entre domínio, infraestrutura e plugin manager. A presença de 262 patches de banco sugere evolução longa do schema.

# 5 DIAGNÓSTICO TÉCNICO

## 5.1 Acoplamento entre interface, domínio e infraestrutura

O acoplamento mais crítico está no fluxo de checkout do PDV. A função `checkout()` em `stoq/gui/pos.py` tem aproximadamente 92 linhas e complexidade aproximada 28. Ela valida se há itens, trata venda token, abre ou reutiliza store de banco, cria savepoint, valida troca, cria venda, salva pedido, imprime detalhes, abre cupom, adiciona itens, confirma cupom, cancela venda em caso de TEF ou cupom cancelado, executa rollback, emite evento de confirmação, fecha conexão e limpa o pedido.

Esse método deveria pertencer a uma camada de aplicação, mas está dentro da classe de interface `PosApp`. O resultado é um fluxo difícil de testar sem GTK, banco e plugin fiscal. Uma alteração simples, como mudar regra de troca ou comportamento de cupom, pode afetar várias responsabilidades ao mesmo tempo.

## 5.2 Classe de venda com excesso de responsabilidades

A classe `Sale`, em `stoqlib/domain/sale.py`, possui aproximadamente 1.379 linhas. A própria docstring lista responsabilidades como cálculo de preço, criação de pagamentos, baixa de estoque, criação de entrega, verificação de cliente, criação de comissões, adição de dinheiro ao caixa e cálculo de impostos/livros fiscais. Em arquitetura orientada a domínio, parte dessas responsabilidades poderia estar em serviços ou agregados separados. No estado atual, a venda concentra regras transacionais, fiscais, financeiras e logísticas.

Essa concentração dificulta isolamento de mudanças. Por exemplo, alterar a política de desconto pode ter impacto em pagamentos; alterar devolução pode afetar estoque; alterar confirmação pode afetar fiscal e caixa. A classe funciona como um ponto de convergência de regras de negócio, mas também se torna ponto de risco.

## 5.3 Complexidade em confirmação fiscal

A função `confirm()` em `stoq/lib/gui/fiscalprinter.py` possui aproximadamente 104 linhas e complexidade aproximada 33. O método verifica pagamento maior que total, abre wizard de confirmação, trata cancelamento, identifica cliente, totaliza cupom, configura pagamentos, fecha cupom, imprime recibos, confirma venda, faz commit, captura exceções genéricas, cancela cupom em caso de plugin ECF, imprime cheques, carnês e boletos.

Esse é um dos trechos mais sensíveis do sistema. Uma falha nesse fluxo pode gerar venda confirmada sem cupom, cupom sem venda confirmada, pagamento inconsistente ou impressão duplicada. O método precisa ser dividido em workflow com etapas explícitas e transações bem delimitadas.

## 5.4 Duplicação

A análise por blocos aproximados identificou 433 duplicações de 8 linhas fora dos testes. Um exemplo aparece em `stoqlib/domain/payment/operation.py`, com repetição de métodos booleanos para diferentes operações de pagamento. Outro exemplo é a repetição de campos fiscais em classes de itens de venda, devolução, empréstimo, transferência e baixa de estoque.

Duplicações desse tipo indicam que conceitos transversais não foram encapsulados. No caso de pagamento, uma política declarativa reduziria repetição. No caso fiscal, mixins ou componentes reutilizáveis poderiam concentrar campos e validações comuns.

## 5.5 Marcadores explícitos de dívida

Foram encontrados 397 `FIXME`, 78 `TODO` e 117 `XXX` em `stoq`, `stoqlib`, `plugins` e `tests`. Esses marcadores não provam, isoladamente, baixa qualidade. Porém, quando aparecem em grande quantidade e em áreas críticas, indicam pendências conhecidas pela equipe. Exemplos relevantes incluem comentários no próprio `checkout()` afirmando que a forma atual obriga a simplificações futuras, e observações em wizards de venda indicando que certas regras deveriam estar no domínio.

## 5.6 Obsolescência

O `pyproject.toml` declara Python `^3.5`. O PEP 478 afirma que Python 3.5 atingiu fim de vida e foi retirado, sem novas releases. Isso cria risco de segurança e compatibilidade. Bibliotecas como Raven, Nose, Kiwi GTK e versões antigas de psycopg2 aumentam a dificuldade de instalação em ambientes modernos.

Além disso, o sistema está preso a uma arquitetura desktop GTK/Glade. Embora desktop possa ser adequado para PDV local, a manutenção de GTK, Glade, Kiwi e empacotamento Debian exige conhecimento específico menos comum em equipes atuais de desenvolvimento web/cloud.

## 5.7 Documentação

A documentação interna é útil, especialmente `docs/howto/structure.rst`, mas apresenta sinais de incompletude. O arquivo descreve diretórios e conceitos, porém termina com tópicos marcados como `XXX GTK`, `XXX Glade`, `XXX Kiwi`, `XXX Proxy`, `XXX Delegate`, `XXX GUI concepts`, entre outros. Isso indica que parte da documentação planejada não foi concluída.

Em sistemas legados, documentação incompleta aumenta dependência de conhecimento tácito. Quando mantenedores saem do projeto, a equipe passa a depender do código como única fonte de verdade.

# 6 PROPOSTA DE MODERNIZAÇÃO

## 6.1 Princípios

A modernização proposta segue quatro princípios. Primeiro, preservar a operação: o PDV não pode parar. Segundo, proteger comportamento antes de alterar estrutura: testes de caracterização devem ser criados para fluxos críticos. Terceiro, extrair por domínio: vendas, estoque, pagamentos, fiscal e relatórios devem se tornar módulos separados. Quarto, substituir por adaptadores: banco, impressora fiscal, TEF e interface devem ser acessados por portas explícitas.

## 6.2 Arquitetura-alvo

A arquitetura-alvo propõe separar o monólito em módulos evolutivos. O `retail-core` concentraria entidades e regras puras. O `sales-service` cuidaria de carrinho, venda, troca, devolução e confirmação. O `inventory-service` trataria saldo, reserva, inventário e movimentação. O `payment-service` ficaria responsável por meios de pagamento, conciliação e políticas. O `fiscal-gateway` isolaria SAT, NFC-e, NF-e, ECF e integrações fiscais. O `reporting-service` geraria relatórios. Um `legacy-adapter` permitiria continuar usando o banco atual durante a transição. Uma API REST exporia contratos para interfaces modernas.

Essa arquitetura permite que a interface antiga continue funcionando enquanto uma nova interface web/PWA de PDV é criada. O supermercado poderia migrar caixa por caixa, reduzindo impacto operacional.

## 6.3 Atualização tecnológica

A atualização tecnológica deve começar pelo ambiente. Recomenda-se criar container do legado, com PostgreSQL e dependências antigas reproduzíveis. Em seguida, deve-se migrar gradualmente para Python 3.12 ou 3.13, substituindo bibliotecas incompatíveis. O ORM pode ser migrado para SQLAlchemy 2.x ou Django ORM, mas apenas após criação de repositórios e testes. As migrações devem sair de patches manuais para Alembic ou mecanismo equivalente.

A interface pode evoluir para web/PWA, mantendo suporte a leitor de código de barras, atalhos de teclado, impressão local e modo offline. Para integrações fiscais que dependem de hardware local, recomenda-se um agente local ou gateway fiscal instalado na loja.

## 6.4 Refatoração do checkout

O método `checkout()` deve ser substituído por uma chamada a `CheckoutService`. A tela de PDV enviaria um `CheckoutCommand` contendo itens, cliente, operador, filial, subtotal, modo de salvamento e contexto de troca. O serviço validaria o comando, criaria a venda, aplicaria troca se necessário e delegaria confirmação ao workflow fiscal/pagamento.

Essa mudança reduz acoplamento e permite testes unitários. A interface passa a ser substituível e o comportamento de checkout pode ser validado por entradas e saídas.

## 6.5 Refatoração da confirmação fiscal

A confirmação fiscal deve virar `SaleConfirmationWorkflow`. O workflow deve ter etapas nomeadas: validar pagamento, confirmar intenção do operador, totalizar cupom, configurar pagamentos, fechar cupom, confirmar venda, commitar transação e imprimir documentos pós-commit. Cada etapa deve retornar resultado explícito, evitando múltiplos `return False` espalhados.

Também é recomendada a criação de interfaces `FiscalGateway`, `PaymentGateway`, `ReceiptPrinter` e `TransactionManager`. Assim, testes podem simular impressora sem equipamento físico.

## 6.6 Refatoração de relatórios

O método `_generate_dailymovement_data()` deve ser dividido em repositório de consultas, agregadores e objeto de relatório. A consulta ao banco não deve montar diretamente estruturas de UI. A formatação de cheque, cartão e método de pagamento deve ser função separada. O resultado deve ser um DTO ou objeto imutável que possa ser usado por interface GTK, API ou relatório HTML.

## 6.7 Redução de duplicação

Operações de pagamento devem usar políticas declarativas. Em vez de repetir métodos como `can_pay`, `can_print` e `can_cancel` em várias classes, cada operação pode declarar capacidades em um objeto `PaymentOperationPolicy`. Regras excepcionais permanecem sobrescritas apenas quando necessário.

Campos fiscais comuns devem ser extraídos para mixins ou componentes reutilizáveis. A repetição de `icms_info`, `ipi_info`, `pis_info` e `cofins_info` em diferentes itens fiscais deve ser concentrada para reduzir inconsistência.

# 7 VIABILIDADE, RISCOS E CRONOGRAMA

## 7.1 Viabilidade

A proposta é viável se executada incrementalmente. A reescrita completa não é recomendada porque o sistema contém muitas regras fiscais e operacionais. A primeira entrega útil deve ser a estabilização do ambiente e a criação de testes de caracterização. Somente depois deve ocorrer extração de serviços.

Do ponto de vista de negócio, a modernização beneficia supermercados por reduzir risco de falha no caixa, permitir integração com canais digitais, melhorar relatórios e facilitar manutenção. Do ponto de vista técnico, reduz dependência de tecnologias antigas e cria base para novos módulos.

## 7.2 Riscos

O maior risco é quebrar o fluxo fiscal ou de pagamento. Outro risco é migrar dados de forma incorreta. Também existe risco de resistência operacional se a nova interface for menos rápida que a antiga no caixa. Para mitigar esses riscos, recomenda-se piloto controlado, execução paralela, backups, testes de contrato e homologação fiscal.

## 7.3 Cronograma

Um cronograma realista pode ser dividido em 36 semanas. Nas semanas 1 a 4, faz-se baseline, ambiente e testes iniciais. Nas semanas 5 a 8, criam-se testes de caracterização de PDV, fiscal e caixa. Nas semanas 9 a 14, refatora-se checkout, confirmação e relatórios. Nas semanas 15 a 22, cria-se API inicial. Nas semanas 23 a 30, desenvolve-se interface web/PWA piloto. Nas semanas 31 a 36, faz-se migração controlada, observabilidade e rollout gradual.

# 8 CONCLUSÃO

O Stoq Retail Management System apresenta forte aderência ao conceito de sistema legado. Ele é relevante para o domínio de varejo, possui regras de negócio acumuladas e usa tecnologias que já não representam o estado atual do ecossistema. A análise identificou acoplamento elevado, classes extensas, complexidade em fluxos críticos, duplicação, documentação incompleta, migrações fragmentadas e dependências antigas.

Apesar disso, o diagnóstico não conduz à conclusão de que o sistema deva ser descartado. Ao contrário, o Stoq deve ser visto como ativo de conhecimento. Sua base contém regras de venda, estoque, fiscal, caixa e pagamento que provavelmente resultaram de anos de uso e adaptação ao mercado brasileiro. Uma reescrita completa tenderia a ignorar esse conhecimento e aumentaria o risco de regressões.

A modernização recomendada é incremental. O caminho mais seguro é estabilizar o ambiente, criar testes de caracterização, extrair serviços de domínio, isolar integrações por adaptadores e criar uma API progressiva. Só então a interface e a persistência devem ser substituídas. Essa estratégia preserva a operação do supermercado, reduz risco técnico e cria uma base sustentável para evolução futura.

O projeto demonstra que a modernização de legado não é apenas atualização de tecnologia. É um processo de compreensão, preservação de conhecimento, redução de risco e melhoria gradual da capacidade de mudança. No contexto de supermercados brasileiros, essa abordagem é essencial porque o software sustenta diretamente a venda, o caixa, o estoque e a conformidade fiscal.

# REFERÊNCIAS

BENNETT, Keith. Legacy systems: coping with success. *IEEE Software*, v. 12, n. 1, p. 19-23, 1995.

CANALTECH. *Magalu compra startup de tecnologia para ponto de vendas*. 24 ago. 2020. Disponível em: https://canaltech.com.br/negocios/magalu-compra-startup-que-desenvolve-sistemas-de-ponto-de-vendas/. Acesso em: 1 jun. 2026.

FOWLER, Martin. *Refactoring: improving the design of existing code*. 2. ed. Boston: Addison-Wesley, 2018.

MARTINS, Daniele; CHERVENSKI, Alex; BORDIN, Andréa. Identificação de características de sistemas legados a partir da análise de conteúdo da literatura. In: ESCOLA REGIONAL DE ENGENHARIA DE SOFTWARE (ERES), 1., 2017, Alegrete. *Anais [...]*. Porto Alegre: Sociedade Brasileira de Computação, 2017. p. 81-88. Disponível em: https://sol.sbc.org.br/index.php/eres/article/view/10084. Acesso em: 1 jun. 2026.

PYTHON SOFTWARE FOUNDATION. *PEP 478: Python 3.5 Release Schedule*. Disponível em: https://peps.python.org/pep-0478/. Acesso em: 1 jun. 2026.

PYPI. *stoq 4.7.0.post1*. Disponível em: https://pypi.org/project/stoq/. Acesso em: 1 jun. 2026.

SOMMERVILLE, Ian. *Engenharia de software*. 9. ed. São Paulo: Pearson, 2011.

STOQ. *Stoq in Launchpad*. Disponível em: https://launchpad.net/stoq. Acesso em: 1 jun. 2026.

STOQ. *Stoq Retail Management System*. GitHub. Disponível em: https://github.com/stoq/stoq. Acesso em: 1 jun. 2026.

STOQ / MAGALU CLOUD. *Conheça a Stoq: a solução completa de ferramentas para o varejo digital e físico*. Disponível em: https://conteudo.magalu.cloud/stoq. Acesso em: 1 jun. 2026.
