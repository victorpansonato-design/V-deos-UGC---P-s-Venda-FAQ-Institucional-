# Preparar uma audição de voz no PC da equipe

Para o primeiro piloto, a pessoa pode ler o texto definitivo e entregar esse MP3 ao avatar. Para repetir a mesma voz em textos novos, o laboratório gera um WAV a partir de uma referência autorizada por perfil. Use-o na etapa de fala do provedor que fará o sincronismo. O computador realiza a síntese. Os comandos de inventário HeyGen e de instalação do modelo são operações separadas.

## 1. Inicie as pastas

No PowerShell aberto na pasta do projeto, com Python 3.11 e FFmpeg no PATH, execute:

```powershell
py -3.11 scripts/vozes.py iniciar
```

O arquivo `producoes/vozes/perfis.json` nasce com **apresentadora** e **apresentador**. Ambos começam desautorizados. Guarde junto dele `apresentadora.mp3` e `apresentador.mp3` ou indique o nome do WAV correspondente no manifesto. Registre fora do Git a autorização específica da pessoa para este uso e só então mude a chave `clonagem_local_autorizada` do perfil para `true`. A retirada da autorização requer desativar o perfil e tratar cópias/arquivos anteriores conforme o acordo estabelecido.

## 2. Instale o ambiente de audição

O código e o modelo regional da Resemble têm origens distintas. O card do checkpoint brasileiro declara MIT, o projeto Chatterbox também indica MIT. A receita pt-BR usa o carregador específico da demonstração oficial e o encoder do modelo-base. O programa fixa as três revisões pelo SHA completo. O executável do estúdio não distribui esse código externo nem os pesos. A instalação pelo operador precisa de internet, Python 3.11 de 64 bits, espaço para os pesos (~3,21 GB), PyTorch, cache e memória de inferência. Deixe espaço adicional para pacotes e temporários. Confira a licença das dependências antes de redistribuir. [Modelo brasileiro](https://huggingface.co/ResembleAI/Chatterbox-Multilingual-pt-br) · [Repositório Chatterbox](https://github.com/resemble-ai/chatterbox) · [Carregador da demonstração na revisão escolhida](https://huggingface.co/spaces/ResembleAI/Chatterbox-Multilingual-TTS-pt-br/blob/9e515821e826e207cd617a0fdd0223899ed108ea/chatterbox/src/chatterbox/tts.py)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install numpy==1.26.0 librosa==0.10.0 resampy==0.4.3 s3tokenizer transformers==4.46.3 diffusers==0.29.0 omegaconf==2.3.0 resemble-perth==1.0.1 silero-vad==5.1.2 conformer==0.3.2 safetensors huggingface_hub==0.25.2 soundfile
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts/vozes.py preparar-modelo
```

A primeira linha de instalação do PyTorch seleciona CPU. Em PC com NVIDIA compatível, a equipe pode escolher no seletor oficial um wheel CUDA suportado para a mesma dupla PyTorch/Torchaudio. O tempo de render depende da máquina. O comando de preparo busca somente o código do motor e os pesos oficiais em revisões fixadas e compara quatro hashes SHA-256. A inferência lê os arquivos locais e configura as bibliotecas Hugging Face para usar o modo offline. Para testar isso no PC da equipe, conclua os downloads antes e desconecte a rede durante a audição. [PyTorch 2.8](https://pytorch.org/get-started/previous-versions/#v280) · [Dependências da demo](https://huggingface.co/spaces/ResembleAI/Chatterbox-Multilingual-TTS-pt-br/blob/9e515821e826e207cd617a0fdd0223899ed108ea/requirements.txt)

## 3. Gere um trecho que diferencia as vozes

Crie `producoes/vozes/leitura.txt` em UTF-8. Para começar, use “Sua rematrícula tem duas etapas. Pague a mensalidade de janeiro e assine o contrato pelo aplicativo do Grupo Anchieta.” Grave a mesma frase com a voz humana. A seleção de referência mais limpa importa mais do que repetir várias gerações à procura de uma pronúncia aceitável. O piloto aceita até 300 caracteres por tomada e exige nome de saída novo para preservar os takes anteriores.

```powershell
.\.venv\Scripts\python.exe scripts/vozes.py sintetizar apresentadora leitura.txt take-a.wav
.\.venv\Scripts\python.exe scripts/vozes.py sintetizar apresentador leitura.txt take-b.wav
```

Compare cada pessoa com sua própria leitura. Duas pessoas da equipe devem ouvir em ordem alternada. Peça que transcrevam “rematrícula”, “janeiro” e “Grupo Anchieta” e avaliem a fala sem ver o rosto. Aprove somente a voz que funcionar no alto-falante do celular e nos fones. A ausência das referências pessoais impede homologar o timbre nesta rodada. O WAV escolhido segue para o teste de boca e depois para o estúdio. [Protocolo do projeto](pesquisa-voz.md)

## 4. Consulte o catálogo atual da sua conta HeyGen

Para isso basta Python, sem PyTorch. O inventário lê todas as páginas do endpoint de vozes baseadas em modelo. A chave da conta fica na sessão local. Os campos publicados podem trazer idioma sem variante regional. O relatório marca `brasil_declarado` quando há identificação explícita do Brasil e mantém `portugues_para_ouvir` para os registros genéricos. Filtre o campo `triagem` e ouça as prévias. Confira o que a conta efetivamente permite selecionar no editor. Um ID listado pelo endpoint sozinho não comprova compatibilidade entre todos os tipos de avatar e motor.

```powershell
$chaveHeyGen = Read-Host 'Chave da API HeyGen' -AsSecureString
$env:HEYGEN_API_KEY = [System.Net.NetworkCredential]::new('', $chaveHeyGen).Password
py -3.11 scripts/vozes.py catalogo-heygen --tipo public --saida catalogo-publico-01.json
py -3.11 scripts/vozes.py catalogo-heygen --tipo private --saida catalogo-privado-01.json
Remove-Item Env:HEYGEN_API_KEY
```

A opção privada inclui somente as vozes do workspace autorizado. Os arquivos JSON são privados, datados internamente e nunca enviados ao repositório. Falha de token, 401 ou paginação incompleta encerra a consulta sem gravar um inventário parcial. O script executa somente GET. A API documenta até 50 vozes públicas por página e o cursor `next_token`; a relação pode divergir da biblioteca apresentada pelo produto web. Sem acesso à conta, a lista nominal e o teste de escuta continuam pendentes. [HeyGen · List Audio Voices](https://developers.heygen.com/reference/list-voices)

## Verificação disponível nesta versão

Os testes locais verificam recusa sem autorização do titular, isolamento dos dois perfis, nomes de arquivos privados, preservação de dados, paginação e classificação de idioma com respostas simuladas. A estrutura e os nomes do carregador foram confrontados com a revisão oficial. A síntese com os pesos completos, o hardware Windows da equipe, os MP3 pessoais e a API autenticada exigem o ensaio na máquina de produção. Preserve a gravação humana original como alternativa para o prazo.

```powershell
py -3.11 -m unittest discover -s tests -p test_vozes.py
```
