# Estúdio UniAnchieta para Windows

Piloto local para montar um vídeo de FAQ a partir do bruto do Marketing ou de um avatar já gerado. A janela inclui prévia do material e do MP4 exportado, seleção dos dois perfis, ajuste de formato, locução externa, duas legendas animadas e vinheta oficial obrigatória. O indicador usa o tempo realmente processado pelo FFmpeg para calcular a estimativa restante.

## Abrir na sua máquina

1. Use Windows 10 ou 11 com Windows PowerShell 5.1, WPF, `ffmpeg.exe` e `ffprobe.exe`. Obtenha FFmpeg pelos [links recomendados pelo projeto](https://ffmpeg.org/download.html#build-windows). Escolha um build com `libx264` e `libass`. Coloque os dois binários em uma pasta `ffmpeg` ao lado de `Studio.ps1`, ou utilize uma versão aprovada pela TI no PATH.
2. No Explorador, mantenha `UniAnchieta-Studio.exe` e `Studio.ps1` juntos se estiver usando o pacote compilado. Abra o executável. A partir dos fontes, abra o PowerShell na pasta `desktop` e rode `powershell.exe -NoProfile -STA -File .\Studio.ps1`. Se o computador exigir assinatura para executar o arquivo, consulte a TI para a distribuição interna.
3. Se quiser carregar a logo do Grupo no cabeçalho, coloque o PNG autorizado nessa pasta com nome `marca.png`. A marca do vídeo vem da vinheta selecionada.

## Montar um FAQ

- Escolha **Filmagem do Marketing** ou **Avatar gerado**. No segundo caso, escolha **Apresentadora** ou **Apresentador** e carregue um bruto para aquele perfil. Para gerar o bruto, use o [guia do HeyGen](../prompts/heygen.md) ou [guia do Higgsfield](../prompts/higgsfield.md) na pasta do repositório.
- Use a voz do vídeo ou selecione um MP3/WAV de duração equivalente. A locução escolhida deve ser a que sincronizou a boca do avatar, ou deve ser usada em um vídeo em que ninguém está falando em quadro. A prévia permite conferir o arquivo. O aplicativo aplica a locução ao corpo do vídeo.
- Escolha formato e, se quiser, um SRT com os tempos revisados. **Editorial** dá uma placa azul escura com leve subida. **Cinema** usa texto claro com contorno e entrada suave. Os presets de legenda são o primeiro recorte do catálogo de identidades.
- Escolha a vinheta do formato. Ela entra inteira com seu próprio áudio. A duração total deve caber em 60 segundos. Corte o bruto ou monte a camada criativa primeiro no motor de edição ou em um editor como Kdenlive.
- Clique em **Exportar MP4**, salve com um nome novo e veja a estimativa de tempo. A saída é 1080×1920 ou 1920×1080, 30 fps, H.264/AAC. Confira a saída já aberta na prévia, inclusive a voz e a transição para a vinheta em um celular.

O primeiro piloto aplica acabamento sobre mídia que o operador já escolheu. Motion gráfico sincronizado à fala, cortes múltiplos e ajustes finos de som ficam no [motor de edição](../README.md) e nos [projetos de motion](../motion). Os perfis organizam o bruto escolhido durante a sessão. A síntese, o lip-sync e a edição de texto do roteiro são tarefas dos guias e das ferramentas correspondentes.

## Gerar o pacote

Com o [Go](https://go.dev/dl/) disponível no PATH, abra o PowerShell na pasta e execute `.\build.ps1`. O pacote fica em `dist/UniAnchieta-Studio-windows-x64.zip`. Ele contém o executável e o script que o executável abre como arquivo local, sob as regras vigentes do Windows PowerShell. FFmpeg/FFprobe são pré-requisitos instalados separadamente. A versão piloto precisa ser exercitada com os dois formatos no Windows e passar pela assinatura/distribuição da TI antes de compartilhamento amplo.
