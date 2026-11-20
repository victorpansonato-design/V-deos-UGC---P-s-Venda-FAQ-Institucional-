# Estúdio CX · UniAnchieta

Produção local de FAQs de até um minuto em português brasileiro para ingressantes e alunos do Grupo Anchieta. O fluxo começa com uma dúvida, uma resposta verificável e uma voz. Pode receber uma gravação do Marketing ou um apresentador já sincronizado no HeyGen ou no Higgsfield.

**Comece aqui** · Abra esta pasta no **Codex** do computador e envie **“Leia AGENTS.md e continue pelo próximo passo em docs/recuperacao/estado.md.”** Para a primeira sessão, há um [prompt pronto para copiar](prompts/codex-iniciar.md). A pasta mantém o contexto quando muda a pessoa ou o computador. Os ativos privados ficam na máquina da equipe.

| O que você quer fazer | Abra |
| --- | --- |
| Saber exatamente o que está pronto e o que fazer hoje | [Estado do projeto](docs/recuperacao/estado.md) e [plano até a diretoria](docs/recuperacao/plano.md) |
| Entender por que o primeiro vídeo foi recusado | [Diagnóstico com evidências](docs/recuperacao/diagnostico.md) |
| Escolher entre as três amostras | [Roteiros e planos de corte](docs/recuperacao/amostras.md) |
| Reunir direção, marketing e edição | [Mesa de direção com sete agentes](docs/recuperacao/mesa-de-direcao.md) |
| Escolher como a edição acompanha a explicação | [Direção ilustrada](docs/recuperacao/direcao-ilustrada.md) e [pesquisa de motion](docs/recuperacao/pesquisa-motion.md) |
| Produzir o bruto para edição | [Prompt mestre HeyGen](prompts/heygen.md) · [Prompt mestre Higgsfield](prompts/higgsfield.md) |
| Comparar a voz gravada e a voz sintética | [Teste de elenco e voz](docs/recuperacao/pesquisa-voz.md) e [pronúncia pt-BR](docs/04-voz-ptbr.md) · [voz local e inventário da conta](docs/recuperacao/voz-local.md) |
| Operar ou construir o piloto Windows | [Versão local e instruções](desktop/README.md) e [pesquisa de arquitetura](docs/recuperacao/studio-windows.md) |
| Escolher imagens, música e efeitos com licença | [Acervo e som](docs/06-acervo-e-som.md) |
| Entender o aluno e medir se a dúvida foi resolvida | [Público e indicadores](docs/02-publico-e-conteudo.md) |

### Primeira sessão na máquina da equipe

1. No GitHub Desktop, clone este projeto ou, se já estiver clonado, use **Fetch origin** e **Pull origin** quando houver mudanças. No Codex, abra a pasta que contém este README. O prompt inicial está acima.
2. Crie a pasta local `inbox/`. Coloque nela as duas vinhetas nos nomes `vinheta-vertical.mp4` e `vinheta-horizontal.mp4`. Adicione a gravação real do apresentador ou o bruto exportado do provedor. Guarde o áudio **exato** que animou a boca, quando houver. Veja a lista de insumos no plano. Para clonar voz, use só a de uma pessoa que tenha autorizado o uso definido.
3. Comece com uma frase e um take de 8–12 segundos em celular. Escute a fala sem imagem e depois assista à boca com o mesmo áudio. Só replique a edição completa quando esses dois testes passarem. A edição de um vídeo real funciona sem conexão com o HeyGen.
4. Se quiser usar o conector oficial via Codex CLI, no terminal rode `codex mcp add heygen --url https://mcp.heygen.com/mcp/v1/`, depois `codex mcp login heygen` quando a sessão pedir autorização e confira a lista com `codex mcp list`. Conectar a conta e mandar gerar são ações independentes. Confira o custo na conta antes de gerar. [MCP no Codex](https://developers.openai.com/codex/mcp/) · [MCP do HeyGen](https://www.heygen.com/model-context-protocol)

### Motor de edição e revisão

O motor CLI usa Python 3, FFmpeg e FFprobe. Para a composição opcional com HyperFrames, use Node e a versão fixada pelo lockfile. O corpo também pode ser montado em Kdenlive e voltar como clipe único. O master termina com o arquivo **integral** da vinheta correspondente à orientação.

```bash
python scripts/studio.py doctor
python scripts/studio.py roteiro examples/roteiro-pratica.txt
python scripts/studio.py inspecionar inbox/apresentador.mp4
python scripts/studio.py montar producoes/rematricula/plano.json producoes/rematricula/revisao-01 --progresso
python scripts/studio.py validar producoes/rematricula/revisao-01/entrega.mp4 --formato vertical
```

Use `py -3` no Windows se necessário. Os antigos [comandos para Claude Code](docs/01-operacao.md) seguem disponíveis. O Codex usa [AGENTS.md](AGENTS.md). Gerar um MP4 ou passar na verificação técnica ainda deixa a decisão de conteúdo, interpretação e marca com o CX.
