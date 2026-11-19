# Acervo visual e desenho de som

## Ordem de escolha

| Acervo | O que buscar | Regra de produção |
| --- | --- | --- |
| Marketing Anchieta | Originais 4K, fachadas, corredores, mãos em ação, estudantes autorizados, interação com telefone e apoio de polo | Primeira fonte para mostrar o campus. Organize por unidade, modalidade, pessoa autorizada, resolução e data. |
| Capturas próprias de Aluno Online / AVA / App | Passo real que o aluno vai reproduzir | Use conta de demonstração. O nome do botão e o fluxo têm de corresponder à versão vigente e ao perfil do aluno. |
| [Pexels](https://www.pexels.com/license/) | Apoio neutro: mão usando telefone sem tela identificável, papel, objetos educacionais, chão/luz e textura | Verificar logos, direitos de imagem e restrições de endosso. Contexto ilustrativo sem representar um aluno ou instalação do Grupo. |
| [Mixkit](https://mixkit.co/license/) | Efeitos, música e imagem com licença adequada ao canal | Distinguir Stock Video Free e Restricted. Leia a licença específica de cada tipo de mídia. Use SFX gratuitos legítimos separados de anúncios Envato. |
| [Freesound](https://freesound.org/help/faq/) | Foley tátil curto em WAV, CC0 ou CC BY com crédito registrado | Verifique autor, licença do item e evidência de origem. CC BY-NC fica fora deste fluxo institucional. |
| [Sonniss GameAudioGDC](https://sonniss.com/gameaudiogdc/) | Arquivo de efeitos profissionais: papel, couro, foley mecânico, ar e transientes | Leia a versão da licença na data de obtenção. Curadoria humana e sincronização local de pós-produção. Arquivo bruto no acervo privado. Não envie arquivos para treinamento ou sistemas externos de IA. [Termos](https://sonniss.com/gdc-bundle-license/) |
| [Pixabay](https://pixabay.com/service/license-summary/) | Apoio visual e texturas sonoras quando documentados | Em música, confira documentação por faixa, possíveis claims e adequação ao canal. |
| Produção interna | Room tone, click de tecido/papel, maçaneta, caneta, passos e assinatura do Grupo | Melhor oportunidade de criar uma assinatura reconhecível, com som natural e origem controlada. |

No navegador remoto, a página [Transition Sound Effects](https://mixkit.co/free-sound-effects/transition/) exibiu candidatos gratuitos “Fast small sweep transition”, “Short transition sweep” e “Technology transition slide”, todos marcados como 1 s. São pontos de partida para audição. A seleção sonora final precisa do contexto e do licenciamento. Use a faixa de qualidade e a textura, sem reproduzir a trilha do Reel. Para referências visuais, priorize os próprios takes do Grupo e busque imagens genéricas só para lacunas.

Registre arquivo, hash, URL do item, autor, licença exata, data, crédito exigido, canais, restrições e prova de autorização. Use o cabeçalho de `config/acervo.csv`. Um banco gratuito pode ter restrição de redistribuição da mídia avulsa. Guarde evidências e arquivos fora do repositório público.

## Som guiado pela fala

Trilhas separadas: **diálogo**, **ambiente**, **música** opcional e **SFX**. Prefira uma locução próxima e natural. Retire ruído de fundo moderadamente, preserve respiração útil e elimine cliques de edição. Evite denoise que deixe voz aquosa. Use room tone real entre cortes. Faça audição em fone e no alto-falante do celular.

| Evento visual | Som de preferência | Como sincronizar |
| --- | --- | --- |
| Um conceito entra com leve deslocamento | Ar curto, quase imperceptível, ou silêncio | Entrada 1–3 frames antes só se ajudar a sensação de movimento. |
| Um item realmente é selecionado | Foley seco de toque em vidro ou papel, sem timbre de alerta | Ataque no frame do contato. |
| Associação curso → comunidade | Textura orgânica, breve, fora da sílaba crítica | Apoiar a junção, preservar o sentido sem som. |
| Confirmação visível documentada | Clique macio e cauda curta | Nada que pareça uma notificação do celular. |
| Encerramento | Vinheta institucional integral com áudio original | Preserve a passagem e confira o volume percebido no celular. |

Cue sheet por ID do evento, tempo em segundos ou frames, ID de ativo, ataque/pico/final, ganho inicial, offset e função. Prefira arquivos WAV e mescle a 48 kHz. Faça EQ/corte de graves das camadas que mascaram a voz quando necessário, duck manual nos trechos críticos e panorama compatível com mono. Comece com a cama sensivelmente abaixo do diálogo e compare A/B com a cena em silêncio antes de manter o efeito. Timing é verificado na mixagem final e no MP4 exportado.

Adote −16 LUFS integrado ±1 LU e teto −1,5 dBTP no arquivo distribuído como **perfil interno inicial**. Para acomodar overshoot do AAC, ajuste a normalização pré-codificação com teto inicial −2 dBTP e meça depois. O perfil não é uma especificação oficial da Meta. [EBU R128](https://tech.ebu.ch/publications/r128/) · [EBU streaming supplement](https://tech.ebu.ch/docs/r/r128s2.pdf)

### Candidatos para o piloto

| Uso | Acervo candidato | Antes de montar |
| --- | --- | --- |
| Contextualizar a instituição | Entrada do campus em ~00–03 s e prédio com arcos em ~24–32 s no anexo | Troque pelo original de maior resolução quando o Marketing disponibilizar. |
| Ilustrar a organização de uma oficina | [Mão fazendo anotações, Mixkit](https://mixkit.co/free-stock-video/close-up-a-hand-writing-notes-on-a-notebook-with-99890/) | A página indicava Stock Video Free. Verifique o item e use apenas como ilustração genérica. |
| Representar rotina de estudo no celular | [Anotações e celular com tela vazia, Pexels](https://www.pexels.com/video/person-writing-on-notebook-while-hold-mobile-phone-6278825/) | Preserve a função ilustrativa. Uma tela didática sobreposta usa a captura aprovada do CX. |
| Colar montagem na mudança de assunto | Sweeps curtos do Mixkit e gravação local de papel/mesa | Escute transiente em mono, corte caudas e combine com 1–2 eventos por módulo. |
