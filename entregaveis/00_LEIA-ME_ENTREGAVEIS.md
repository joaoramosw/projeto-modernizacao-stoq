# Projeto: Evolução e Modernização de Sistema Legado

Discente: João Victor Silva Ramos  
E-mail: joaovictor.ramos@ucsal.edu.br  
Docente: Sheila Tirony de Almeida Silva  
E-mail docente: sheilatirony.silva@pro.ucsal.br  
Tema: Evolução e modernização de um sistema legado de gestão de lojas/PDV para varejo supermercadista brasileiro.

## Sistema escolhido

O sistema escolhido foi o **Stoq Retail Management System**, edição open source disponível no GitHub em `https://github.com/stoq/stoq`.

A escolha foi feita porque o Stoq possui aderência forte ao domínio de lojas, PDV, estoque, compras, caixa, financeiro e operações fiscais. Além disso, tem origem e uso no mercado brasileiro de varejo, com trajetória empresarial real: a Stoq foi adquirida pelo Magalu em 2020 e sua linha atual evoluiu para soluções SaaS/PDV para o varejo físico e digital. Para fins de engenharia reversa, foi analisado o repositório open source, que preserva uma base legada adequada ao objetivo acadêmico.

## Observação importante sobre "supermercado real"

Não foi escolhido um sistema proprietário fechado de uma rede específica de supermercados, pois a disciplina exige um software base analisável, preferencialmente de repositório público. O Stoq foi adotado como sistema real do varejo brasileiro aplicável a supermercados, mercadinhos e lojas físicas, preservando o requisito de código aberto para diagnóstico técnico.

## Estrutura dos entregáveis

1. `01_Etapa_1_Escolha_e_Descricao.md`  
   Ficha técnica, funcionalidades atuais, justificativa e problemas preliminares.

2. `02_Etapa_2_Engenharia_Reversa_Diagnostico.md`  
   Arquitetura atual, módulos/componentes, métricas coletadas e relatório de débito técnico.

3. `03_Etapa_3_Plano_Refatoracao_Evolucao.md`  
   Plano de modernização, modularização, evolução tecnológica, riscos, cronograma e trechos "Antes vs. Depois".

4. `04_Relatorio_Tecnico_ABNT.md`  
   Relatório formal com capa, introdução, fundamentação teórica, desenvolvimento, conclusão e referências. O texto foi dimensionado para exceder 8 páginas quando formatado em A4, fonte Times New Roman 12, espaçamento 1,5 e margens ABNT.

5. `05_Roteiro_Video_10_a_15_min.md`  
   Roteiro narrado para gravação do vídeo final, com marcação de tempo e o que mostrar na tela.

6. `06_Slides_Apresentacao.md`  
   Estrutura sugerida de slides para apoiar o vídeo.

7. `07_Matriz_Avaliacao_Checklist.md`  
   Checklist que relaciona cada critério de avaliação aos documentos produzidos.

8. `anexos/metricas_evidencias.md`  
   Métricas coletadas no repositório local, comandos usados, principais arquivos críticos e limitações.

9. `anexos/diagramas_mermaid.md`  
   Diagramas em Mermaid para arquitetura atual e arquitetura proposta.

10. `codigo_refatorado_proposto/`  
    Arquivos de exemplo que ilustram a proposta de refatoração sem alterar o repositório original.

## Fontes principais usadas

- Repositório oficial analisado: https://github.com/stoq/stoq
- Página histórica do projeto no Launchpad: https://launchpad.net/stoq
- Página do pacote Stoq no PyPI: https://pypi.org/project/stoq/
- Página atual da Stoq/Magalu Cloud: https://conteudo.magalu.cloud/stoq
- Notícia sobre aquisição da Stoq pelo Magalu: https://canaltech.com.br/negocios/magalu-compra-startup-que-desenvolve-sistemas-de-ponto-de-vendas/
- Artigo de referência da disciplina: https://sol.sbc.org.br/index.php/eres/article/view/10084
- PEP 478, ciclo de vida do Python 3.5: https://peps.python.org/pep-0478/

## Como usar na entrega

- Use o relatório `04_Relatorio_Tecnico_ABNT.md` como documento central.
- Use os arquivos das etapas 1, 2 e 3 como anexos ou como base para responder separadamente à rubrica da professora.
- Para o vídeo, siga `05_Roteiro_Video_10_a_15_min.md` e use `06_Slides_Apresentacao.md` como guia de tela.
- Na demonstração prática, mostre o repositório clonado em `referencia/stoq`, os trechos de código reais citados e os exemplos de refatoração em `codigo_refatorado_proposto`.
