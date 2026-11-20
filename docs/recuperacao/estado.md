# Estado do Estúdio CX

Atualizado em **19/11/2026**, após a revisão de estilo pelo CX. Alvo: três amostras para a diretoria, com revisão técnica e de conteúdo antes do envio aos alunos.

| Frente | Estado verificado |
| --- | --- |
| Diagnóstico | Vídeo recebido inspecionado por quadros e métricas. A equipe relatou fala robótica e rosto pouco natural. A causa exata da configuração do provedor requer a sessão ou o bruto. A pasta da skill, os dois tutoriais enviados, o catálogo e o MP4 de Rory, o Reel e os takes institucionais estão mapeados. |
| Direção | Três roteiros com plano por tempo. O CX reprovou a estética do primeiro ZIP e considerou o plano de campus rápido. O novo estudo ensaia objetos ilustrados que mudam com a fala, com take real contínuo de 1,83 s. [Direção atual](direcao-ilustrada.md) |
| Mesa de marketing | Sete agentes no Codex. Sete pareceres independentes já definiram a comparação visual de rematrícula e corrigiram a interpretação do cartão. [Ata inicial](ata-rematricula.md) |
| Saída local | Motor FFmpeg exportou exemplos com as vinhetas corretas e completas nos dois formatos. Teste vertical de 6,50 s a −16,2 LUFS e horizontal de 7,10 s a −16,3 LUFS. Configuração de voz, enquadramento e legenda precisa de revisão no material final. |
| Voz | Script de preparação pt-BR, critério de escuta, catálogo HeyGen por conta e fluxo de clonagem local. Dois MP3 de referência, registro de autorização e escuta em pt-BR pendentes. Os roteiros e as versões destinadas ao TTS são arquivos separados. |
| Interface | Código do piloto Windows vive em `desktop/`. Pacote de teste Windows x64 compilado. Sintaxe, layout declarativo e render validados em Linux. Para distribuir, faça aceitação da janela e dos pré-requisitos em Windows real. Status e comandos em [desktop/README.md](../../desktop/README.md). |
| Provedores | Prompts mestres para [HeyGen](../../prompts/heygen.md) e [Higgsfield](../../prompts/higgsfield.md) incluem caminhos de tela, teste de 8–12 s, voz própria e revisão de custo. A descoberta de avatares e vozes depende da conta logada. |

## Retomar deste ponto

1. Identificar o bruto limpo e os arquivos da voz autorizada em `inbox/`. Se faltar material, usar uma captação natural de 8–12 s com a fala em [ata-rematricula.md](ata-rematricula.md), em pé e com luz frontal. Pode ser gravada como vídeo real.
2. Montar a comparação A/B. Escutar sem imagem, reproduzir com imagem na hora da fala e conferir com o teste de compreensão. Se a voz sintética estiver disponível, preservar os mesmos roteiro, duração e enquadramento em sua comparação.
3. Aplicar a identidade escolhida aos outros roteiros, confirmar as duas regras de extensão por modalidade e usar telas vigentes sem dados pessoais. Exportar, conferir em celular e registrar quem aprovou.

O fluxo detalhado, a lista de arquivos e o calendário estão no [plano](plano.md). Ao concluir uma etapa, atualize este estado. As evidências privadas de produção ficam em `producoes/`.
