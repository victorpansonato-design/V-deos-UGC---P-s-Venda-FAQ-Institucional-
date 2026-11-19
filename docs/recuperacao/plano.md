# Plano até a apresentação · 19 a 23 de novembro de 2026

**Entrega desejada para segunda, 23/11:** três FAQs de até 60 s, com uma resposta acionável, um apresentador convincente, legibilidade no celular, conteúdo vigente e a assinatura final do Grupo. O primeiro investimento vai para 10 s de fala e rosto. Uma composição cara sobre um rosto que o público rejeita continua sendo um vídeo que a equipe não quer usar.

## Sequência da produção

| Quando e quem | Fazer | Como sabemos que dá para seguir |
| --- | --- | --- |
| Qui 19 · Codex + Victor | Recuperar referências e fontes. Escolher uma fala comum para o teste. Colocar as duas vinhetas e o material de captação na pasta de trabalho. Comparar voz humana, voz nativa e clone autorizado se já disponível. | Dois ouvintes de pt-BR conseguem repetir o próximo passo. Ninguém trava no nome da marca nem descreve a fala como robótica. Registrar defeito e segundo exato se travar. |
| Qui 19 · apresentador + CX | Com **o mesmo áudio final**, testar enquadramento, olhar e boca em 8–12 s. Referência para escuta: “Pra fazer sua rematrícula, você precisa pagar a mensalidade de janeiro e assinar o contrato no aplicativo do Grupo Anchieta.” | Pele e olhos consistentes, consoantes de “pagar” e “aplicativo” sincronizadas em playback normal, nome inteligível e natural. Ouvir também em alto-falante de celular. |
| Sex 20 · direção + Marketing | Aplicar uma identidade ao mesmo take após a [mesa de direção](mesa-de-direcao.md). Fazer uma mudança visual no instante em que a primeira ação aparece e uma segunda quando entra o contrato. Comparar com o vídeo recusado no mesmo aparelho. | A gestora consegue ler os dois passos e vê o rosto durante a explicação. Pausando qualquer frame, nenhum texto sobre a boca ou a legenda. Guardar o trecho aprovado e as escolhas usadas. |
| Sáb 21 · Codex + área de conteúdo | Montar os três roteiros da pasta, voz e capturas reais da versão do app usada pelos alunos. Reservar o tempo integral do encerramento. Acelerar por reaproveitamento dos estados de animação, nunca por acelerar a voz do estudante. | Roteiro conferido linha a linha, ordem e telas correspondem à modalidade, sem dados pessoais. Quem edita identifica a fonte de cada afirmação. |
| Dom 22 · revisão independente | Fazer última mixagem, conferir legendas palavra por palavra, orientação, cor, duração, decodificação e vinheta. Reproduzir em celular com som, sem som e em fone. Mostrar a alguém que desconhece o processo. | Essa pessoa explica a ação sem ajuda. Assinalar qualquer diferença que possa induzir erro no portal. Guardar versão e exportações com letra legível no canal de destino. |
| Seg 23 · CX | Apresentar o antes/depois do mesmo problema, três amostras aprovadas e o tempo/custo medidos. Recolher decisão sobre o padrão de voz/identidade para repetir. | Distinguir amostra aprovada, estudo visual e pendência. Em uma pauta pendente, mostrar o trecho aprovado e descrever a lacuna. |

Esse calendário organiza o trabalho. Aprovações de terceiros e acesso às contas dependem da disponibilidade real no feriado. Se o avatar sintético reprovar, usar vídeo real do Marketing com voz original. Se a trilha distrair, ouvir primeiro a mixagem seca. Os dois caminhos preservam o prazo e evitam refazer os três vídeos.

## Onde colocar os arquivos no computador

| Caminho local sugerido | O que vai ali | Para qual decisão |
| --- | --- | --- |
| `inbox/vinheta-vertical.mp4` e `inbox/vinheta-horizontal.mp4` | Encerramentos oficiais com a faixa original | 3,50 s no vertical e aproximadamente 4,08 s no horizontal. Reservar duração desde o roteiro. |
| `inbox/campus.mp4` | Original do Marketing de melhor resolução disponível | Plano de passagem de 0,7–1,2 s, entre duas frases. |
| `inbox/apresentador.mp4` | Bruto sem gráficos, legendas ou música, com boca visível | Edição real direta ou take do HeyGen/Higgsfield. Para a primeira comparação, basta a frase comum. |
| `inbox/interpretacao.mp3` | A frase aprovada gravada limpa; idealmente guardar também o WAV original | Áudio definitivo para animar o rosto; para câmera real, priorizar a voz captada em sincronia. |
| `acervo/vozes/` | Referências autorizadas dos dois perfis e registro privado de escopo | Triagem local da naturalidade. O consentimento de um titular não cobre o outro. |
| `inbox/capturas/` | Fluxo atual do app/portal com conta de demonstração ou dados mascarados antes de gravar | Prova do CTA. Se a captura faltar, usar diagrama autoral identificado e manter pendente a demonstração de tela. |
| `producoes/<tema>/` | Roteiro aprovado, plano, fontes, decisões, SRT, master e registros | Repetir a edição a partir da versão registrada. |

## Operar depois do piloto

A gestora abre o projeto e diz **“Edite o vídeo que deixei em inbox”** ou **“Quero um FAQ de [assunto] com a apresentadora”**. O Codex lê a pendência atual, o roteiro e o material. Trabalha em gravação existente quando disponível. Para avatar, usa o prompt do provedor, orçamento da conta e áudio aprovado. Ela só precisa decidir conteúdo institucional que mudou, elenco ou interpretação que ainda não foram homologados.

Use `producoes/<tema>/decisoes.md` para anotar versão do roteiro, objetivo, responsável, resultado de voz/rosto, instantes de corte, autorização do material, versão final, compreensão e defeitos. Ao encerrar cada rodada, diga **o que foi executado, o que falta e a próxima ação concreta**. Atualize o estado compartilhável apenas com resultados que possam ser públicos.

## Instalação e distribuição

O piloto Windows e seus pré-requisitos estão em [desktop](../../desktop/README.md). Fazer o primeiro teste em Windows com os dois formatos: instalar ou localizar FFmpeg/FFprobe, abrir o aplicativo, selecionar arquivos, editar, cancelar uma exportação, retomar em outro nome, abrir o MP4 e repetir sem rede. Validar também em uma máquina limpa sem ferramentas de desenvolvimento. Medir tempo de processamento em relação à duração e anotar CPU/GPU usada. Tratar assinatura, distribuição e análise do pacote pela TI antes de divulgar para toda a instituição. O GitHub atual é público. Um novo repositório para binários não altera a visibilidade do histórico deste.

A versão de distribuição deve incluir versão, tamanho, SHA-256, pré-requisitos e canal de atualização. Disponibilizar apenas código e componentes redistribuíveis de licença conferida. Vozes, arquivos das contas, vídeos do Marketing e vinhetas ficam no acervo do Grupo.
