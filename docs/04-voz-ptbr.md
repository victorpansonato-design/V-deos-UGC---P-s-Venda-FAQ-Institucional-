# Voz e fonética em português brasileiro

A fala mais convincente começa com voz capaz de falar pt-BR, contexto escrito em pt-BR e direção de interpretação. A adaptação fonética é localizada por voz e engine. Variação brasileira de R, S, vogais átonas, palatalização e entonação é esperada. Avalie naturalidade e compreensão com ouvintes, considerando a diversidade do público. Barbosa & Albano descrevem uma variedade brasileira documentada, útil para estudar vogais tônicas e átonas, nasalidade e contrastes consonantais. [Artigo de referência](https://www.cambridge.org/core/journals/journal-of-the-international-phonetic-association/article/brazilian-portuguese/8EE69D52AE2D06C1EDA2841EA2E14FEC) · [Estudo fonético na Unicamp](https://econtents.sbu.unicamp.br/inpec/index.php/joss/article/download/14995/10054)

## Três versões de texto

| Arquivo | O que guardar |
| --- | --- |
| `roteiro-editorial.txt` | Texto aprovado e termos oficiais, valores, datas, CTA e fontes. |
| `roteiro-falado.txt` | Texto de fala da voz selecionada. Abreviações expandidas, pontuação respirável e substituições auditadas. |
| `legendas.srt` e `legendas.vtt` | Texto revisado que corresponde ao que se ouviu, com grafia oficial. Grafia especial do sintetizador fica fora. |

## Procedimento automático antes de gerar

1. Normalize Unicode NFC, quebras de linha, espaços e aspas. Confirme semântica. Trate datas por extenso com ano quando material, valores com reais e centavos, intervalo com “de… a…”, horários com contexto, siglas pelo significado ou por leitura aprovada. Confira todos os nomes próprios e números contra a fonte.
2. Execute `python scripts/studio.py roteiro producoes/tema/roteiro-editorial.txt` e examine alertas. A ferramenta propõe expansões locais cadastradas e aponta termos que pedem inspeção. Use `--perfil acervo/perfis/apresentadora.json` após homologação para gerar automaticamente a variante falada com os aliases exatos daquela voz. Confira siglas, citações e usos ambíguos. Endereço extenso vai no destino clicável e na tela, com referência curta na fala.
3. Em voz multilíngue, priorize pt-BR explícito quando o mecanismo expuser locale. Guarde a regra no glossário com idioma e versão. Tente primeiro grafia oficial em frase completa. Só aplique alias de som com evidência de que melhorou nessa combinação. IPA serve para diagnóstico, alinhamento e referência humana. Envie IPA, SSML ou marcação de pausas somente se a ferramenta específica documentar suporte e o teste passar.
4. Escute um teste de 8–15 s na mesma combinação quando houver termo novo ou voz/motor novo. Teste falas iniciais, em posição medial e final. Escute os números e nomes críticos na velocidade natural. Se falhar, ajuste por termo, passe pelo glossário escrevendo ou gravando a referência e gere só o trecho quando houver autorização. Se persistir, escolha áudio humano, guia nativa por mirroring ou outra voz homologada.
5. Grave lista de substituições, entrada, saída, observação da escuta e aprovador. Clone/guia humana ou áudio externo exigem autorização e respeito ao recurso disponível no HeyGen. Sincronize o rosto com o áudio que ficará na entrega. Trocar áudio depois se aplica a voz fora de quadro ou a novo lip-sync.

## Fenômenos que mudam o resultado

| Fenômeno | Onde escutar | Tratamento |
| --- | --- | --- |
| Sílaba tônica e abertura de vogal | “prática”, “acadêmico”, “protocolos” | Preserve os acentos e teste em frase. Um alias aprovado é particular da voz. |
| Nasalidade e ditongo | “extensão”, “matrícula”, “informações” | Um áudio de referência nativo é mais útil que um hífen arbitrário. |
| Consoante e encontro entre palavras | “sete dias”, “no aplicativo”, “fale com o polo” | Ouça ligações, ritmo, final de frase e variação regional. |
| Marca e topônimo | “UniAnchieta”, “Grupo Anchieta”, “Jundiaí”, “Lyceum” | Compare marca com o uso da equipe/Marketing. Jundiaí exige atenção à tônica final. Referência de “Lyceum” deve vir da instituição. |
| Sigla | AVA, RA, EAD, DP, ADAP | Primeira menção por extenso quando melhorar a clareza. Teste “a vê a”, “erre a” ou “ê a dê” apenas quando o CX confirmar sua leitura no vídeo. |
| Datas, períodos e valores | 04/08, 2026/74, R$ 25,50, 19h30 | Expandir por contexto. Período institucional pede significado confirmado. Legenda mantém forma oficial. |
| Homógrafo, empréstimo | “app”, “login”, “polo” | Escolha palavra usada pelo público. Teste “aplicativo” para reduzir ambiguidade quando couber. |

Dois arquivos orientam o trabalho: `config/pronuncia.json` para expansões semânticas aprováveis e termos de revisão, e `config/catalogo-vozes.csv` para registrar a audição. Os exemplos do glossário são candidatos editoriais. Homologue a forma falada para a equipe.

O perfil privado tem os campos `locale`, `status`, `voice_id`, `engine` e `aliases`. A referência inicial está em [perfil-voz.json](../examples/perfil-voz.json). Preencha o ID real e mude o status para `homologado` após a avaliação. aliases é um objeto de pares termo → leitura, sensível à grafia, aplicado uma vez por correspondência. O agente confere o roteiro falado com o original e resolve datas e valores por contexto.

## Teste cego de voz

Prepare três amostras com texto idêntico, volume igualado e nomes ocultos. Uma institucional, uma com marcas/siglas e outra com data, valor e frase longa. Mantenha posição e gestos quando comparar avatares. Três avaliadores brasileiros, incluindo alguém fora do CX, dão nota 1–5 para naturalidade, clareza, ritmo e adequação. Marquem cada termo crítico e descrevam os tropeços. Sugestão de aprovação inicial: cada termo crítico compreendido por todos, mediana de naturalidade e clareza ≥4, nenhum erro de data/valor/nome, nenhuma sincronia labial evidente. Registre quem ouviu e quando. ASR e alinhamento ajudam a apontar lacunas e a posicionar legendas. Uma boa transcrição não comprova sotaque, prosódia ou articulação.

**Amostras de laboratório, com datas e valores fictícios**

- “Oi! Quer entender o que é prática extensionista no UniAnchieta? Ela aproxima o que você aprende na graduação das necessidades da comunidade.”
- “Acesse o Aluno Online para consultar seu registro acadêmico. Se a orientação mencionar o AVA, procure pelo Ambiente Virtual de Aprendizagem.”
- “Neste exemplo, a orientação fica disponível em quatro de agosto, às dezenove horas e trinta minutos. O valor fictício é de vinte e cinco reais e cinquenta centavos. Confira as instruções para o seu curso.”

[Idiomas HeyGen](https://help.heygen.com/en/articles/11391932-voice-languages-we-support) · [Brand Glossary e amostra em frase](https://help.heygen.com/en/articles/8830251-how-to-use-brand-glossary) · [Speech to Speech](https://help.heygen.com/en/articles/17756130-how-to-use-speech-to-speech-voice-mirroring-in-heygen)
