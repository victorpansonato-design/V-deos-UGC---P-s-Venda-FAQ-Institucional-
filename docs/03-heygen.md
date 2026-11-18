# HeyGen · seleção de recursos, integração e créditos

Verificação documental em 18/11/2026. O catálogo, a disponibilidade por conta, os modelos e as regras de cobrança são dinâmicos. Confira o seletor do workspace e a ferramenta MCP autenticada antes de consolidar preço ou promessa de qualidade.

## Como extrair qualidade com controle de edição

| Recurso | Uso no estúdio | Condição de adoção |
| --- | --- | --- |
| Avatar 6 Turbo / Pro | Primeiro bake-off em 1080p. Compare Turbo com Pro se a conta tiver os dois. | Qualidade de boca, olhos, postura e consistência em português. Pro depende do plano e superfície. |
| Avatar IV/V e Lipsync/III | Comparar um look equivalente quando o modelo primário falhar ou consumir mais do que o ganho percebido justifica. | A documentação usa nomenclaturas de gerações distintas. Grave o nome e o ID efetivamente usados. |
| Stock avatar / Photo Avatar | Começo rápido. Escolha enquadramento e expressão editorial. | Teste as falas críticas, contexto visual da marca e termos de uso. |
| Digital Twin | Construir apresentadora reconhecível e uma atuação mais coerente. | Imagem e voz autorizadas, consentimento próprio no HeyGen, captura controlada e plano de substituição. |
| Brand Glossary | Centralizar pronúncia por termo e idioma. Testar ouvindo em frase no Studio quando disponível. | Só aplique pelo MCP se a ferramenta expuser o parâmetro. Guarde cópia local e versão. |
| Voice Director | Ajustar tom, intenção e pausas na superfície que oferecer o controle. | Medir se melhora a fala em pt-BR. Confirmar compatibilidade de voz e engine. |
| Speech to Speech / Voice Mirroring | Puxar cadência, acento e intenção de uma guia gravada em pt-BR. | Confirmar acesso, idioma, créditos e consentimento. Usar o resultado no mesmo lip-sync. |
| Upload de narração | Escolha quando a pronúncia exige controle máximo ou quando o CX grava a voz. | Conferir se o modo escolhido usa esse áudio para animar a boca. |
| AI Studio / Quick Avatar Video | Alternativa à automação para exportar o take cru e reutilizar o mesmo pipeline local. | Tire música, legendas e elementos dispensáveis do bruto. |
| Video Agent, tradução, Creative Studio, LiveAvatar | Testes controlados quando o tema justificar. A série nasce em pt-BR e usa acervo próprio. | Fora do padrão do piloto. Video Agent completo adiciona escolhas automáticas de imagem e usa créditos diferentes. |

[Preços e limites do plano web](https://www.heygen.com/pt-br/pricing) · [Créditos por recurso](https://help.heygen.com/en/articles/15126059-how-to-use-credits-on-heygen) · [Digital Twin](https://help.heygen.com/en/articles/8389138-digital-twin-video-avatar-filming-tips) · [Brand Glossary](https://help.heygen.com/en/articles/8830251-how-to-use-brand-glossary) · [Voice Mirroring e Director](https://help.heygen.com/en/articles/11408956-how-to-use-mirror-voice-and-direct-voice)

## Escolha da integração

**Principal: MCP oficial OAuth**, vinculado ao plano web. A documentação do HeyGen indica debitarem-se créditos do workspace web, enquanto chave de API e CLI/skills dependentes de API podem consumir um saldo separado. Antes de escolher modo, leia as ferramentas da sessão e peça uma operação somente de leitura. Se MCP expuser apenas Video Agent para a combinação desejada e isso mudar custo ou tirar controle do take, use AI Studio para o bruto e continue a partir da importação local.

```bash
claude mcp add --transport http heygen https://mcp.heygen.com/mcp/v1/
```

Se a declaração de projeto em `.mcp.json` já estiver habilitada, pule o comando acima. Abra `/mcp` na sessão CLI da pasta e faça o fluxo OAuth oficial. No Desktop confira a seção Claude Code de servidores MCP. Evite a configuração da aba de chat. O catálogo oficial de skills pode servir de referência para descoberta de ferramentas, avatares e fluxo. Fixe uma revisão e confirme que o caminho usa OAuth antes de instalar skills que incluem CLI, dependências ou exigem token. [MCP oficial](https://www.heygen.com/model-context-protocol) · [Integrações e autenticação](https://www.heygen.com/integrations) · [HeyGen Skills](https://github.com/heygen-com/skills) · [Preço API](https://www.heygen.com/api-pricing)

### Estimativa para a diretoria

Na tabela de créditos web consultada, Avatar 6 Turbo 720p/1080p aparece a 20 créditos/min e Pro a 40, com 2K a 35/58 respectivamente. Avatar IV aparece a 16 créditos/min em Photo Look e 31 em Video Look. Avatar V aparece a 48. Video Agent Standard aparece a 80, com tarifas próprias por modo. O Creator web aparece a US$ 29/mês, 600 créditos e exportação até 1080p nas páginas consultadas. Use o preço e a franquia efetivos da conta. Estimativa de 12 vídeos × 40 s × 20 créditos/min = 160 créditos brutos. Quatro takes extras de 15 s elevam a estimativa a 180. A conta pode ter arredondamento, custo de geração, elegibilidade ou tarifa adicional. Registre a estimativa antes e o consumo real depois. [Plano web](https://www.heygen.com/pricing) · [Tabela de créditos](https://help.heygen.com/en/articles/15126059-how-to-use-credits-on-heygen)

## Inventário de todas as vozes acessíveis

O site público documenta **Português (Brasil e Portugal)**. A cobertura desta pesquisa é documental. Vozes privadas, clones, IDs e combinações com engine só ficam verificáveis na conta. Faça a extração inicial por operação de leitura, sem geração de vídeo:

1. Liste todas as vozes públicas e privadas. Percorra as páginas até o fim, preservando IDs e tags. O upstream recomenda ferramentas como `list_voices(type=private)` e `list_voices(type=public, language=<idioma>)` onde expostas. Leia o schema disponível e respeite o token de paginação real. Se o filtro de idioma só retornar o principal, faça inventário amplo e passe as multilíngues para triagem.
2. Classifique em **pt-BR explícito**, **Português sem variante**, **multilíngue a testar**, **pt-PT** e **uso restrito**. Use preview oficial quando disponível. Compatibilidade multilíngue é triagem e depende da audição por voz + engine + locale.
3. Exporte para CSV local com as colunas de `config/catalogo-vozes.csv`. Se a superfície paginar sem acesso a todas as páginas ou devolver campos incompletos, reporte as lacunas e faça conferência visual no Studio. Exporte o snapshot público/privado só no ambiente interno.
4. Use os mesmos três trechos comparáveis para 6–10 vozes pré-selecionadas e retenha duas homologadas. Mantenha ID estável e uma substituta. Refaça o teste quando mudar engine, avatar, voz ou glossário. [Idiomas oficiais de voz](https://help.heygen.com/en/articles/11391932-voice-languages-we-support) · [Busca oficial no guia de avatar](https://github.com/heygen-com/skills/blob/master/heygen-avatar/SKILL.md) · [HeyGen Developers](https://developers.heygen.com/)

## Direção da apresentadora

Casting de três perfis: acolhedora e próxima, objetiva e didática, e uma voz regional natural adequada ao piloto nacional. Idade aparente adulta, plano médio com espaço acima para respiro e separação de fundo. Roupa sem estampas finas, lente equivalente moderada, câmera à altura dos olhos, cenário de campus ou escritório institucional, luz suave em um lado, preenchimento discreto. Salve look, avatar, voz, motor, taxas, resolução e enquadramento. Oriente a intenção “explicar a uma pessoa com uma dúvida” com pausas entre ideias. Evite gestos com mãos encobrindo a boca, movimentos de cabeça extremos e brilho de fundo atrás do contorno do rosto.

Se adotar Digital Twin, filme a pessoa real autorizada seguindo o guia do tipo de avatar escolhido. Faça um take contínuo, dicção natural, luz estável, áudio limpo, fundo sem pessoas e olhar para a lente. Comece em 1080p/30 ou capture original 4K quando a câmera e o fluxo comportarem, confirme a resolução nativa no bruto entregue. Grave o consentimento exigido para o tipo de avatar. Documente internamente escopo de uso, canais, responsáveis por revogação e onde remover o ativo. Use stock enquanto a autorização ou a gravação dedicada estiver pendente. [Gravação Digital Twin](https://help.heygen.com/en/articles/8389138-digital-twin-video-avatar-filming-tips) · [Consentimento HeyGen](https://help.heygen.com/en/articles/12092609-recording-your-consent-video)

## Controle de jobs

Use o endpoint ou a ferramenta de vídeo simples disponível, com take de 12–20 s em tema fictício no primeiro ensaio autorizado. Valide um trecho com marca, sigla e frase contínua. Para produção, envie roteiro falado estável e master limpo, em take contínuo curto ou em blocos com poucos frames de respiro, cortando nas pausas. Registre título identificável, hash dos insumos, ID do job, perfil, status, custo estimado e observado. Baixe o arquivo prontamente por URL autenticada ou assinada, sem publicá-la. Se timeout acontecer depois do envio, procure job pelo ID ou título antes de qualquer retry. Reserve novo consumo ao erro confirmado dentro do teto acordado. 4K se destina ao acervo quando a fonte é nativa e o canal precisa. Exportação grande e detalhe real são especificações distintas.

### Onde fica a biblioteca no Studio

A academia oficial descreve a Biblioteca de Vozes como o local para navegar, ouvir e administrar vozes. Abra um projeto de teste, acesse a biblioteca na opção de voz, verifique os filtros e escute os resultados em Português do Brasil. Confira as vozes privadas autorizadas do workspace e anote o que é pesquisável pelo Studio e pelo MCP. Voice Design e clones são modos do HeyGen sujeitos a disponibilidade e perfil de uso. [Biblioteca de vozes em pt-BR](https://www.heygen.com/pt-br/academy/voices/accessing-voice-library)
