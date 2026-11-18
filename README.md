# Estúdio CX · Vídeos FAQ do Grupo Anchieta

Base de produção para o **Claude Code no computador**. A equipe fornece a dúvida, a resposta validada e, quando houver, um vídeo original. O Claude Code prepara o roteiro, planeja a edição e usa as ferramentas locais para montar, revisar e exportar. O HeyGen entra quando o vídeo precisa de uma apresentadora virtual.

## Para criar um vídeo

1. Abra a aba **Code** do Claude Desktop e escolha a pasta deste repositório no computador.
2. Copie uma das mensagens abaixo. Pode escrever com suas próprias palavras.
3. O Claude devolve uma proposta com o que o aluno aprenderá, a duração estimada, as cenas e o que falta confirmar. Com a conta configurada e a produção autorizada, ele monta uma prévia local e prepara os arquivos de entrega.

**Com apresentadora**

> Crie um vídeo de até 45 segundos explicando o que é prática extensionista. É para quem acabou de entrar na graduação. Quero usar a apresentadora aprovada. Use a página institucional como fonte. Meu roteiro é: [cole aqui].

**Com gravação real**

> Edite o vídeo que deixei em inbox/. Preserve a voz e as informações da pessoa. É para alunos ingressantes. Quero legenda, cortes naturais e animações só onde ajudarem a entender. Aqui vai a fonte da orientação: [cole o link ou indique o arquivo interno].

**Somente planejamento**

> Planeje um vídeo de FAQ com o roteiro abaixo. Quero validar a resposta, o storyboard e a voz antes de gerar. [cole aqui]

Se a interface não sugerir o comando, envie a mensagem normalmente. Os comandos **/video-faq**, **/editar-video-real**, **/calibrar-voz** e **/validar-video** também estão disponíveis nas versões do Claude Code que carregam as configurações da pasta.

## Guias

| Para quem | Abra |
| --- | --- |
| Gestora e operação | [Primeira configuração e uso diário](docs/01-operacao.md) |
| Quem vai apresentar o projeto | [Proposta para a diretoria e piloto](docs/09-diretoria-e-plano.md) |
| Quem aprova conteúdo | [Público brasileiro, prioridades e medição](docs/02-publico-e-conteudo.md) |
| Quem configura a apresentadora | [Pesquisa HeyGen, modelos, catálogo e custos](docs/03-heygen.md) e [fonética e audição pt-BR](docs/04-voz-ptbr.md) |
| Quem dirige a edição | [Direção de arte e análise dos anexos](docs/05-direcao-e-referencias.md) e [design sonoro e acervo](docs/06-acervo-e-som.md) |
| Quem mantém a produção | [Arquitetura, stack e instalação](docs/07-pipeline-e-stack.md) e [qualidade e entrega](docs/08-qualidade.md) |
| Primeiro vídeo | [Storyboard de prática extensionista](examples/pratica-extensionista.md) |

O repositório público contém guias, perfis iniciais e código. Configure um acervo interno para originais do Marketing, consentimentos, roteiros internos, vozes da conta e arquivos entregues. O fluxo de produção gera arquivos para revisão local. Publicação aos alunos é uma etapa do CX.

## O que já roda localmente

```bash
python scripts/studio.py doctor
python scripts/studio.py roteiro examples/roteiro-pratica.txt
python scripts/studio.py inspecionar caminho/do/bruto.mp4
python scripts/studio.py montar caminho/do/plano.json pasta/da-producao
python scripts/studio.py validar pasta/da-producao/entrega.mp4
```

No Windows, use `py -3` se o comando `python` não estiver no PATH. O montador recebe cortes, enquadramentos, áudio final quando houver e legenda revisada. A direção, o storyboard, o plano de edição, a composição de motion e a escuta em português ficam no fluxo do Claude Code. A geração HeyGen depende da autenticação e dos recursos da conta do Grupo. O trabalho foi estruturado para permitir edição de vídeo real com custo HeyGen zero.
