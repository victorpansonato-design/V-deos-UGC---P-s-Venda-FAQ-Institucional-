# Como operar pelo Claude Code

## Primeira configuração, feita pelo CX

1. Instale o Claude Desktop atualizado e abra a aba **Code**. Se aparecer o aviso de versão como na captura do briefing, atualize antes de começar. Escolha **Este computador** e **Escolha uma pasta para trabalhar**. Clone o repositório no GitHub Desktop ou pelo terminal e selecione a pasta que contém `CLAUDE.md`.
2. Instale Python e o FFmpeg local conforme [o guia técnico](07-pipeline-e-stack.md). Rode `python scripts/studio.py doctor`. A equipe técnica instala e fixa HyperFrames/Chromium se for produzir os componentes de motion em HTML.
3. A pasta já declara o conector oficial do HeyGen em `.mcp.json`. Habilite-o quando o Claude Code solicitar e faça login com a conta institucional autorizada. Na aba Code, verifique **+ → Conectores** junto ao campo de mensagem ou peça ao Claude para listar os conectores da sessão. Para diagnosticar no terminal, abra a mesma pasta e rode `/mcp` em uma sessão do Claude Code. Uma sessão de Claude Chat e uma sessão local de Claude Code têm configurações diferentes.
4. Crie `inbox/`, `acervo/` e `producoes/`. Coloque no acervo o kit de marca aprovado em vetor, takes originais do Marketing, capturas com dados de teste, fontes e sons com direitos verificados. O piloto funciona com um lote pequeno.
5. Rode **/calibrar-voz**, homologue uma dupla apresentadora/voz e uma alternativa. Registre perfil, limite de créditos por vídeo, pessoa responsável por conteúdo e pessoa responsável pela revisão. O perfil do projeto começa **a homologar**.

Compartilhar esta base pelo GitHub funciona para outra pessoa abrir o mesmo projeto. A sessão de chat, os arquivos locais e o login HeyGen independem do GitHub. Cada operadora usa sua sessão local e as permissões equivalentes na conta institucional. Para continuidade, compartilhe a pasta da produção pelos meios internos autorizados ou use um espelho interno do acervo. [Claude Code Desktop](https://code.claude.com/docs/pt/desktop)

## Uso diário

| O que você tem | O que escrever | O que recebe |
| --- | --- | --- |
| Dúvida e roteiro | “Quero um FAQ de 45 s sobre X para estudantes EAD. Use a apresentadora 1 e o roteiro abaixo.” | Resposta checada, proposta de cenas, estimativa de geração e prévia. |
| Vídeo original com pessoa falando | “Edite o arquivo X. Preserve a voz. Tire os erros de tomada e mostre Y na hora em que eu falo.” | Montagem, legenda e as verificações técnicas, sem consumo de HeyGen. |
| Vídeo de apoio sem locução | “Este é o apoio de campus. Prepare uma peça para X com a narração aprovada Y.” | Plano com imagens pertinentes e sincronização à locução disponibilizada. |
| Só uma ideia | “Planeje o vídeo, sem gerar.” | Brief, roteiro, duas opções só quando houver trade-off real, e storyboard. |
| Prévia pronta | “Valide a produção X.” | Duração, resolução, leitura de legenda, estado do marcador de publicação, pendências objetivas. |

Se houver um bloqueio, peça uma decisão em linguagem simples. “Qual tela o aluno deve abrir? 1. Aluno Online. 2. App Grupo Anchieta. 3. Ainda vou confirmar.” Não proponha rotas de portal, datas ou valores pela aparência da interface. Mantenha o roteiro e o motion preparados enquanto aguarda.

### Aprovação em uma rodada

Mostre primeiro ao CX a **resposta exata**, o **próximo passo do aluno**, **quem aparece**, **duração**, **cenas** e **custo estimado**. Na mesma rodada, solicite confirmação das pendências que realmente mudam o resultado. Com tema, fonte e perfil homologados e instrução explícita para gerar dentro do teto local, rode a produção. Ao final, apresente a prévia e pendências. Para roteiro sensível a calendário ou interface, registre validade e o dono da revisão. O envio ao estudante segue o canal oficial definido pelo CX.
