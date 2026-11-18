# Qualidade e formato de entrega

| Checagem | Automática | Revisão editorial |
| --- | --- | --- |
| Tempo e container | H.264/AAC, 1080×1920, 30 fps, SAR 1, BT.709 SDR, áudio estéreo 48 kHz, ≤60 s | A primeira frase resolve a dúvida. A peça faz sentido sem ver a vinheta. |
| Áudio final | −16 LUFS ±1 e true peak máximo −1,5 dBTP, com transcrição/alinhamento opcionais | Fala natural, sem cortes em sílabas, efeito íntegro em mono, termos críticos e lip-sync passados. |
| Legendas | SRT/VTT consistentes, UTF-8, ocupação compatível com a timeline | Grafia oficial e conteúdo correspondente ao áudio. Até duas linhas em ponto seguro. Teste com som mudo. |
| Dados e licenças | Arquivos e manifesto de direitos presentes no projeto | Fonte oficial vigente, uso válido de imagem, voz, marca, trilha e ausência de dados de alunos. |
| Arte e compreensão | Pontos-chave e testes de composição quando viáveis | Olhar para o elemento certo e tempo de leitura, demonstração alinhada à voz, marca correta e consistência de luz e cor. |
| Canal | Decode do arquivo inteiro e metadados de entrega | Teste no app/site e Instagram conforme destino. Verifique a interface do player e CTA tocável. |

### Política de export

- MP4 H.264, yuv420p, AAC estéreo, 48 kHz, BT.709, 30 CFR e `faststart`. Entrega principal no formato vertical 1080×1920. Para peça horizontal, faça composição dedicada com novo enquadramento e preset aprovado.
- CRF 18 é a partida da entrega padrão. Ajuste ao limite de upload e confira compressão em gradação, UI pequena e pele. Use versão de distribuição leve após teste no canal. Mantenha fontes e masters nativos em armazenamento interno. Não rotule upscale de material HD como fonte 4K.
- Legenda opcional no MP4 social e SRT/VTT separados para player. Máximo de duas linhas e alvo aproximado até 17 caracteres/s para revisão. Termos longos e velocidade precisam de avaliação humana. Evite esconder botões. Legendas públicas carregam grafia e nomes corretos. Forneça resposta textual de apoio a quem usa tecnologia assistiva.
- Arquivos sugeridos: `entrega.mp4`, `social.mp4` quando se fizer versão queimada, `legendas.srt`, `legendas.vtt`, `thumbnail.jpg` só quando o canal usar, e `qa.md` com teste, data, versão, aprovação e pendências.

### Gate editorial

Assistir do início ao fim em resolução de entrega e no aparelho. Escutar termos críticos com dois níveis de volume e comparar com a legenda. Conferir frames antes, durante e depois dos cortes, área segura com o player, cor, ausência de UI falsa, recorte de rosto, acento de pausa e ergonomia. Conferir link/destino com conta do público certo. Para vídeo virtual, revisar boca/dentes, piscadas, mãos, respiração, cadência e sincronismo. Se imagem falhar por alguns quadros, replaneje a cobertura com apoio pertinente antes de gerar tudo de novo. Erro de informação ou pronúncia de termo crítico bloqueia a publicação.

A versão final marca estado: `rascunho`, `tecnico_aprovado`, `pronto_para_revisao_cx` ou `aprovado_para_distribuicao` com responsável e data. Decisão editorial e distribuição são do CX. Validação automatizada relata conformidade medida. Reproduza o MP4 no leitor final porque metadado e taxa de quadros não demonstram qualidade percebida.

[WCAG 2.2](https://www.w3.org/TR/WCAG22/) · [Legendas](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded) · [Três flashes](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html)

## Interpretação dos testes automatizados

O normalizador converte fontes SDR rotuladas para BT.709 e assume BT.709 se faltarem metadados completos. Para esse segundo caso, compare visualmente com o original e prepare um intermediário revisado se houver desvio. O FFmpeg faz controle de loudness e de true peak após codificação. Caso um trecho tenha áudio muito baixo, clipping de origem ou efeitos comprimidos, trate a fonte e repita a medição. Checagens automáticas dão evidência técnica e a aprovação inclui percepção em reprodução.

## Verificação da base · 18/11/2026

| Exercício | Resultado observado |
| --- | --- |
| Composição de prática extensionista | HyperFrames 0.9.67 em Linux com Chromium headless, 1080×1920, 30 fps, 5,4 s. Checagem de runtime, área segura e contraste passou. Quadros amostrados mostraram a entrada dos elementos. |
| Vinheta | Render de 1,4 s testado com o PNG fornecido. Primeiro quadro conferido visualmente. Logo final de distribuição depende do arquivo aprovado pelo Marketing. |
| Montagem do campus | Duas formas de enquadrar o bruto real e legenda de teste. MP4 limpo e social aprovados tecnicamente com 4,0 s, −16,3 LUFS e −3,9 dBTP. |
| Montagem mista | Campus, insert e vinheta com áudio contínuo de teste e SRT/VTT. As duas versões passaram com 8,8 s, −15,9 LUFS e −3,5 dBTP. |
| Preparação de roteiro | Perfil fictício substituiu um termo da fala, preservou URL e texto editorial e sinalizou a data para revisão. |

Pendências do piloto institucional incluem validar o Claude Code no Windows da equipe, autenticar o workspace HeyGen, levantar o catálogo real, ouvir e homologar voz e validar o vídeo completo de FAQ com conteúdo e marca aprovados.
