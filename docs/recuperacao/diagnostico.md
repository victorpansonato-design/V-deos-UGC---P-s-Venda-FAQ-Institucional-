# O que o piloto mostrou e o que muda no próximo corte

Revisão de 19/11/2026. O CX e a gestão rejeitaram três aspectos do primeiro FAQ de prática extensionista: naturalidade da voz, realismo da apresentadora e acabamento. A voz e o rosto precisam de uma decisão de elenco antes de investir no episódio. Há também problemas de hierarquia visual que conseguimos localizar diretamente na cópia entregue.

## Evidência disponível

Inspeção dos fluxos de vídeo e áudio com ffprobe, medição de faixa completa com o filtro ebur128 do FFmpeg e leitura de quadros amostrados a cada 2 s no piloto, 3 s no Reel e 2 s no campus e no diagrama. Os tempos de cenas abaixo são aproximações observadas nesses quadros. Não houve avaliação auditiva humana adicional nesta auditoria, entrevista com os alunos, acesso ao projeto de edição original ou à sessão que gerou o piloto. O “robótico” registra a percepção da equipe. A medição de volume não diagnostica sotaque, timbre, pausa ou sincronismo labial.

| Material e identificação local | Arquivo analisado | Loudness integrado / pico verdadeiro | Uso no projeto |
| --- | --- | --- | --- |
| Piloto recusado • vídeo de WhatsApp | 39,300 s, 576×1024, 30 fps, H.264, AAC estéreo 44,1 kHz | −15,8 LUFS / −1,9 dBTP | Comparação privada. Buscar original da geração para distinguir limitação de origem e recompressão. |
| Reel de referência • MOV ImportedSegment | 69,100 s, 540×960, 30 fps | −14,1 LUFS / +0,7 dBTP | Estudo do apresentador e da alternância de provas visuais. |
| Acervo do Marketing • MP4 InShot | 41,106 s, 1280×720, taxa média de cerca de 24 fps | −15,3 LUFS / −2,8 dBTP | Usar breves transições de campus adequadas ao tema. |
| Vinheta horizontal • SaveClip que começa com AQN0PA | 4,083 s, 1276×718, 24 fps, AAC estéreo | −16,6 LUFS / −6,2 dBTP | Encerrar 16:9 com o arquivo inteiro. |
| Vinheta vertical • SaveClip que começa com AQNYal | 3,500 s, 720×1280, 24 fps, AAC estéreo | −27,4 LUFS / −15,5 dBTP | Encerrar 9:16 com o arquivo inteiro. |
| Diagrama “Negroni recipe animation” • MP4 do Prompt Motion | 30,000 s, 1080×1080, 30 fps, H.264 | O contêiner possui apenas fluxo de vídeo | Estudar a transformação do objeto e construir os movimentos e o som do FAQ. |

As vinhetas mostram os arcos de tijolos, a marca e a assinatura. Na vertical, há diferença de 10,8 LU em relação à horizontal. Conferir a emenda na saída de celular e nos fones. Resolver o encontro da fala com a vinheta na montagem do corpo, preservando o conteúdo e a duração da assinatura. Com teto de 60 s, reservar 3,5 s no vertical e 4,084 s no horizontal antes de fixar a duração da fala. Quando o vídeo pai estiver a 30 fps, pode haver arredondamento de um quadro na conversão.

## Onde o primeiro vídeo perde a atenção

| Tempo no piloto | O que se vê | Decisão de remontagem e teste |
| --- | --- | --- |
| 0–3 s | Apresentadora de blazer verde contra fundo claro. Cartão da pergunta à frente do tronco e marca do fornecedor no material. | Abrir já com a dúvida em linguagem do aluno, comparar duas leituras da mesma frase. Testar enquadramento e figurino com rosto em escala de conversa. Usar a origem e a modalidade de exportação permitidas para entrega institucional. |
| 4–12 s | A apresentadora encolhe numa área no topo. Abaixo, título e barras de alturas diferentes sugerem uma distribuição de horas por período. Etiquetas finas e espaço livre competem pelo olhar. | Reservar espaço estável para a pessoa. Usar um único calendário que atravessa os semestres e termina em “até o fim do curso”. Só representar valores se houver dados aprovados. Teste mudo: o aluno identifica o prazo sem ampliar? |
| 14–22 s | Repete-se o mesmo close com cartão da pergunta. Duas pequenas colunas fazem o estudante procurar a diferença entre modelos. | Em “dois projetos”, mostrar dois cartões grandes com nomes curtos de modelos validados. Destacar “modelos diferentes” quando a frase chega. No semestre seguinte, deslocar o mesmo calendário e demonstrar a regra com um exemplo. |
| 24–32 s | O close se repete. Aparecem oito ícones sob o título de grupo e o texto sugere um limite de participantes. | A quantidade precisa de fonte vigente e escopo. Enquanto aguarda, concluir a dúvida principal em dois exemplos. A equipe pode tratar composição do grupo em um FAQ separado. |
| 34–39 s | Apresentadora e mockup de telefone ficam pequenos sob “Escolha o Modelo do Projeto”. A cópia termina nessa composição. | Mostrar a ação em captura real do portal com dados removidos e texto legível. Concluir a fala antes da entrada da vinheta institucional do formato. |

Não há evidência para atribuir o resultado à operadora ou a uma configuração específica do fornecedor. O repositório anterior oferecia montagem por segmentos, normalização, legendas e um exemplo de card. Essa via conseguia produzir um MP4 válido sem demonstrar que o aluno entendeu a regra, que o rosto convenceu ou que o motion acompanhou cada verbo. O histórico da sessão local seria necessário para saber se a skill foi invocada e quais componentes chegaram a esse arquivo. Confirmar isso pela existência de um ZIP levaria a uma conclusão errada.

## O que vimos nas referências

**Reel do apresentador.** Aos 0–3 s, o rosto estabelece a relação com a câmera enquanto um elemento gráfico ocupa a parte de cima. Perto de 6 s entra uma imagem demonstrativa grande. Aos 12 s uma expressão aparece como título. Entre 18 e 36 s, exemplos da interface ocupam a área superior enquanto o rosto reaparece embaixo. Perto de 39 s uma palavra volta a ocupar o primeiro plano. Por volta de 42–54 s alternam evidência de interface e resultado, e aos 60–66 s o apresentador reassume a imagem. Para a versão CX, manter a pessoa visível durante a explicação, reservando tela cheia para a breve transição de campus e para a vinheta. O material original inclui a interface do Instagram e uma trilha de terceiros: serve à leitura de ritmo.

**MP4 de Rory Flynn.** Além da página do catálogo, o arquivo original foi baixado e lido quadro a quadro em amostras. Perto de 0–2 s, o título vermelho-rosado se estabelece sobre fundo marfim. Aos 4 s, copo e gelo ocupam o eixo esquerdo, com uma ficha à direita e uma faixa de seis estados embaixo. Entre 6 e 10 s a garrafa chega, inclina e o líquido aparece. Entre 12 e 20 s a quantidade e a cor mudam enquanto copo, ficha e régua permanecem reconhecíveis. Por volta de 22 s surge a colher. Aos 24–28 s aparecem a casca alaranjada e a proporção final. A graça está em o olho prever onde o efeito da próxima ação vai aparecer. Em rematrícula, conservar o mesmo par de estados na tela: pagamento da mensalidade de janeiro → assinatura do contrato. A frequência de cortes deve dar tempo para ler cada ação. Fazer a ficha em azul institucional e escolher tipografia própria. O MP4 é mudo, portanto a referência não permite inferir estilo de trilha ou de efeitos sonoros. A entrada do catálogo é de 23/09/2026 e consta aqui por escolha explícita do CX. [Entrada original e autoria](https://prompt-motion.com/ror-fly-9950f1) · [MP4 original](https://media.prompt-motion.com/ror-fly-opus-5-5-rendered-this/video.d79b7c51.mp4)

**Campus de Jundiaí.** Em ~0–3 s há entrada e placa, ~4–12 s aéreas e edificações, ~14–20 s fachadas e vegetação, ~22–32 s prédio de arcos e praça e ~34–40 s novas aéreas. Usar uma passagem curta entre duas ideias, com ponto de entrada e saída descritos no plano. Um crop vertical integral da fonte 1280×720 retém cerca de 405×720 pixels. Uma janela horizontal preserva a arquitetura. Conferir com o Marketing se existe o original de câmera ou uma versão vertical. O campus da sede deve ser identificado quando a explicação vale também para alunos de polos.

## O que realmente existe no ZIP

O arquivo contém **13 arquivos em quatro grupos técnicos e uma introdução**, distribuídos por cinco entradas de diretório. São uma introdução, o guia principal, quatro referências, dois modelos HTML e cinco scripts. Sem licença de redistribuição identificada no arquivo consultado. Não há elenco, modelo de síntese de voz, base de áudio premium ou integração pronta ao HeyGen. A proposta principal do autor é produzir peças curtas de produto e marca, de aproximadamente 8 a 20 segundos.

| Arquivo ou grupo | O que foi examinado | Como aplicar à série |
| --- | --- | --- |
| START HERE e SKILL | Briefing, inventário de assets, definição do final, storyboard, render de quadros, render final e desenho de som. Define aprovações por etapa. | Para uma identidade nova, guardar a ficha numerada e o trecho de prova. Episódios subsequentes reutilizam o que já passou em teste. |
| style-rules, pitfalls | Continuidade do movimento, enquadramento, pausas após entrada rápida, qualidade das texturas e inspeção do meio da transição. | Olhos livres de legenda, leitura estável sobre fundo claro e trajetória que termina no passo a ser entendido. Congelar quatro instantes por transição e conferir em movimento. |
| engine-3d e gl3d.js | Painéis WebGL para interface, profundidade, câmera e luz. | Aplicar perspectiva durante a entrada e devolver a tela a uma posição legível antes da instrução. Fontes reais de interface para botões, textos e caminhos. |
| storyboard.html e template-3d.html | Modelo de storyboard e composição pronta para parametrizar por tempo. O exemplo parte de cenário horizontal. | Refazer a composição para 9:16 usando o mesmo objetivo de cena. Testar metade da tela para o rosto e depois ajustar pela legibilidade da ação. |
| render.mjs e contact_sheet.py | Render por tempo em Chrome, grade de quadros, extração de eventos e possibilidade de transparência com ProRes 4444. | Renderizar elemento em camada ou composição com a pessoa, conferir as entradas e o ponto de ação em escala de celular antes do master. |
| sound-and-music, mix.py e synth_sfx.py | Relacionam eventos temporais a arquivos de som, montam faixa e oferecem um pequeno gerador de sons. | Usar a lista temporal para decidir onde um som esclarece a ação. Gravar ou escolher timbres licenciados e deixar silêncio em volta da palavra importante. Sons provisórios não viram assinatura automaticamente. |

Para experimentar a cópia privada no computador do CX, seguir a [auditoria e o contrato de execução](../05-direcao-e-referencias.md). Entregar ao motion designer um único insert com objetivo, duração exata, arquivo de imagem válido, estado inicial e final, tempo da sílaba acentuada, trajetória e critério de leitura. Exemplo: “pague a mensalidade de **janeiro**” faz a indicação “Janeiro” chegar ao centro durante a sílaba forte e permanecer legível até a fala passar ao contrato. O rascunho de quatro quadros e o trecho com áudio mostram se a ideia funciona antes do render longo.

## O que aproveitamos do MD de curadoria

O material anexado tem nove blocos, de configuração a continuidade. Para este estúdio interessam o método de registro (autor, fonte original, data, observação concreta), o catálogo de ferramentas e o experimento com uma variável por vez. O calendário recorrente e as entregas comerciais da Azuria ficam fora da operação. Aplicações imediatas:

- Em cada referência, registrar um gesto observável e a função que ele cumpre. Exemplo: o mesmo copo recebe três ingredientes; a rematrícula recebe duas ações na mesma composição.
- Gravar a mesma fala com voz real e com a candidata sintética. Nivelar volume, alternar a ordem e pedir a quem escuta que marque a palavra problemática e o instante. Para o próximo teste, alterar só a pausa ou a pronúncia que falhou.
- Escolher ferramentas por etapa. FFmpeg mede, monta e exporta. O motor de motion desenha a ação. ASR ajuda a marcar texto, mas nomes próprios e siglas continuam sujeitos à escuta e correção. Ver [pesquisa de ferramentas](pesquisa-motion.md).
- Medir com um aluno de cada público disponível: depois de assistir sem replay, “o que você faz agora e onde?”. Registrar resposta literal, dúvida restante e eventual erro crítico. Medir compreensão e execução do CTA além de retenção em tela.

## Antes de apresentar à diretoria

1. Ouvir 8–12 s de uma voz real autorizada e da candidata sintética às cegas, incluindo “Grupo Anchieta”, uma pergunta e um verbo de ação. Regravar a palavra que soar estrangeira ou metálica. Guardar os resultados localmente.
2. Usar a tomada curta aprovada na geração do rosto e compará-la a uma gravação real. Conferir o fechamento da boca em “pague”, a pausa antes da resposta e o retorno ao olhar de câmera. Repetir a leitura em celular, em velocidade normal e a 0,5× para localizar o desvio.
3. Exibir o trecho composto sem som em largura de celular e pedir que a pessoa reproduza o próximo passo. A redução do rosto, troca de atenção ou texto pequeno devem aparecer aqui, enquanto a cena continua barata de alterar.
4. Repetir com som. O ataque do efeito pode acompanhar o check, e a fala deve terminar antes da assinatura. Se o som cobrir consoante ou parecer chamar para outro botão, reduzir ou eliminar a cue.
5. Somente após as aprovações editorial e de elenco, montar as três amostras com seus encerramentos, conferir cada uma em telefone e guardar master técnico, cópia para envio e resultado da compreensão. Ver [roteiros e decupagens](amostras.md).
