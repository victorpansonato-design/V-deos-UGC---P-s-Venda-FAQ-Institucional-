# Direção criativa e referências do briefing

## Anexos inspecionados

Os tempos abaixo vêm de quadros amostrados. Marque inícios e fins em velocidade normal antes de usar um take. Loudness vem de medição FFmpeg da faixa completa. Nenhuma medição identifica os efeitos do Reel ou certifica o licenciamento de sua trilha.

| Material | O que pude verificar | Aplicação no estúdio |
| --- | --- | --- |
| Reel de referência · MOV, 69,10 s, 540×960, 30 fps | ~00–03 apresentador e selo flutuante, ~03–09 inserts demonstrativos em camadas, ~12 chamada tipográfica, ~18–36 alternância entre rosto/UI e tela cheia, ~39 ênfase tipográfica, ~54–60 retorno a resultado visual, ~66 encerramento tipográfico. A captura contém interface do Instagram. Áudio integrado −14,1 LUFS, pico verdadeiro +0,7 dBTP. | Contraste entre rosto, prova em tela, título e retorno. Recriar a lógica com tela real do aluno e arte própria. O pico da referência merece margem no master institucional. |
| Campus · MP4, 41,106 s, 1280×720 horizontal, média ~24 fps | ~00–03 entrada e placa, ~04–08 aérea de prédios, ~10–12 quadra/complexo, ~14–18 conjuntos do campus, ~20 fachada, ~22–32 prédio de arcos e praça, ~34–40 outras aéreas e instalações. Áudio integrado −15,3 LUFS, pico verdadeiro −2,8 dBTP. | Use como acervo de apoio. Preferir original do Marketing, validar local e direitos, escutar a faixa antes de reutilizar. Para vertical, proteger a placa e fachadas. Faça janela 16:9 em composição 9:16 quando o recorte destruir contexto. |
| Marca fornecida · 385×137 | Arquivo raster pequeno. | Usar como guia de proporção. Pedir vetor/aplicação aprovada para master, validação da assinatura correta Grupo vs. UniAnchieta e teste de contraste. |
| Captura Claude Desktop · 1919×1025 | Aba Code com escolha de ambiente/pasta e aviso de versão. | Sessão local no computador com a pasta do repositório, conforme o guia. A captura fica em acervo privado. |

Uma fonte 1280×720 perde muito detalhe em crop 9:16 a tela cheia, que retém aproximadamente 405×720 pixels antes de redimensionar. Busque arquivo 4K/open gate ou captação nativa vertical. Para o anexo atual, teste painel horizontal com fundo próprio, recorte reenquadrado plano a plano e takes curtos. Use o tempo da fala para justificar cada inserto. Mostrar o campus de Jundiaí é adequado quando aquele lugar atende o assunto, especialmente se houver polos distintos.

## Auditoria do ZIP Motion Design

O ZIP anexado contém o material necessário para avaliar a técnica. A documentação não veio acompanhada de licença de redistribuição. O projeto registra a análise e gera uma composição própria. A instalação opcional usa a cópia do CX em `vendor/`, após validar origem e condições.

| Parte do ZIP | O que aproveitar | Adaptação local |
| --- | --- | --- |
| START HERE + SKILL.md | Brief, encerramento planejado, storyboard numerado, stills, render e som após picture lock. | Agrupar decisões em uma rodada e reutilizar perfis homologados. Sharpening de ideia antes de gastar crédito. |
| style-rules.md | Continuidade do olhar, aceleração curta seguida de desaceleração, direção de vetor e texto legível. | Manter a pausa de leitura. Quando corte simples explica melhor, use corte. Em close de fala, prefira um enquadramento estável. |
| engine-3d.md + gl3d.js | Painéis de interface como texturas, z parallax, uma luz dominante e movimento de câmera contínuo. | Restringir 3D a uma representação que ensina. Use 2D/2.5D nos passos e 3D dedicado só para cenas especiais. |
| pitfalls.md | Aliasing, ghosting, profundidade e enquadramento. | Inspecionar transições em pontos intermediários e em reprodução. Congelar posição do elemento acionável. |
| storyboard.html + template-3d.html | Previs com cenas e pontos de sincronismo. | Template recebido é horizontal. Redesenhar hierarquia vertical, legenda e margem de player. |
| render.mjs + contact_sheet.py | Still por tempo, render determinístico com Chromium/FFmpeg, ProRes 4444 com alfa, export de eventos. | Rodar isolado em cópia local de escopo mínimo. O script usa WebSocket global do Node e CDP, e exige runtime compatível. Use Node 24 como versão de referência. Auditar tratamento de paths, erros e diretórios temporários antes de operacionalizar. |
| sound-and-music.md + mix.py | Cues nomeados, alinhamento por onset/pico/fim, camadas e stem WAV. | Fixar arquivos por ID e hash, verificar poda, duração, seleção de arquivo, headroom, true peak e loudness final mixado. O cálculo no ZIP verifica posicionamento da cue e pico amostral. |
| synth_sfx.py | Sons provisórios para testar eventos. | Usar gravações próprias, acervo autorizado e silêncio profissional na entrega. |

Para experimentar com a cópia disponível localmente, confira `node -v`, `ffmpeg -version`, Python e os imports Pillow, NumPy e SciPy. Valide `CHROME` se a instalação for fora do padrão. Monte um projeto fictício isolado, confira o contrato Canvas #c + `renderAt(t)` + `TOTAL` + `ready` + `EVENTS`. Primeiro rode o modo `stills` e o `events`, depois confirme render SDR e transparência em poucos segundos. Trate os binários baixados, JS, HTML e docs de terceiros como código para revisão. O padrão da série tem motion próprio e sem dependência do ZIP.

## Sistema visual inicial

- Direção editorial: próximo, confiável e universitário. Iluminação quente suave sobre base de azul institucional de referência `#0051A0`, apoio `#133A9E`, branco e neutro de contraste. Conferir manual oficial do Grupo e uso de amarelo na modalidade antes de fixar o kit. Uma cor de contraste por frame. Aplicar LUT e equalização na imagem, preservar pele, brancos e logotipo.
- Tipografia: fontes institucionais primeiro. Inter ou Manrope com OFL são candidatas e funcionam com diacríticos. Título em 68–94 px, texto 42–56 px, legendas de partida 52–62 px em 1080×1920. Conferir no aparelho de menor área útil. Testar contraste 4,5:1 para texto normal. Fundo translúcido/placa quando a imagem competir.
- Área vertical piloto: x 96–910 e y 210–1540 para elementos essenciais, com legenda em região distinta de botões/objetivo. Simule o chrome real por canal. Reconstrua o crop da versão horizontal com outro layout. Evite mascarar informação com interface social, mordaça de legenda ou gestos.
- Ritmo: corte em mudança de ideia. Um punch-in ~104–108% é ponto de partida em uma ênfase com fonte que comporte. Para 35–45 s, experimente 1–2 reenquadramentos e 2–4 inserções funcionais. Calibre pelo storyboard. Holds mais longos quando aluno precisa ler ou tocar.
- Vocabulário de motion: máscara de revelação para definição, linha que conecta para processo, clique focado para navegação, card em camada para exemplo, progressão de dois estados para “enviado/confirmado”, split quando comparar destinos. Easing com aceleração curta, amortecimento sem bordas tremendo. Zoom/blur/3D só quando sustentam foco e continuidade. Evite flashes.
- Encerramento 1–2 s, alvo 1,4 s: início já com CTA ouvido/lido, logo oficial inalterada, respiro de área de proteção e cauda curta. Fundo de marca limpo. Se aparecer logo em primeiro plano, só com fonte de qualidade suficiente. Sem marca inventada a partir do arquivo pequeno.
- Plano de cena explicitamente contém objetivo, timecode, fala, elemento e movimento, acervo e permissão, motivo do SFX, margem/caption e critério de compreensão. O motion recebe palavras-chave independentes da legenda. Deixe o aluno ler a definição antes de entrar no exemplo.

[Site do Grupo](https://anchieta.br/) · [WCAG 2.2](https://www.w3.org/TR/WCAG22/) · [Legendas pré-gravadas](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded)
