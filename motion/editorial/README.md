# Estudo de rematrícula

Animação vertical de nove segundos para o CX avaliar leitura e hierarquia no celular. Uma pergunta abre o quadro, o pagamento de janeiro ativa a primeira etapa e a assinatura do contrato no App Grupo Anchieta ativa a segunda. O primeiro marcador fica aceso até o fim. Os contornos da base retomam as arcadas presentes no take de campus. O preenchimento dos cartões ilustra a explicação e não consulta o status de um aluno.

Com Node e FFmpeg instalados, execute na raiz do projeto. Use um take local em MP4 com ao menos nove segundos de imagem; o processo usa sua trilha visual. O take e o render ficam fora do Git.

```sh
npm ci
npm run motion:check -- editorial "acervo/campus/trecho-aprovado.mp4"
npm run motion:render -- editorial "acervo/campus/trecho-aprovado.mp4"
```

Abra `motion-editorial.mp4` no celular. Aos 0,8 s, confira a pergunta. Aos 4 s, leia a orientação de pagamento. Aos 8,4 s, confira o nome do aplicativo e as duas marcações. Cubra cada cartão com o polegar e confira se a orientação principal ainda faz sentido. A peça funciona como ensaio interno de composição. O FAQ de distribuição pede a fala aprovada, o apresentador em quadro e o encerramento institucional integral na proporção correspondente.

O movimento de preenchimento progressivo partiu da relação entre ação e estado na peça de Rory Flynn. No Reel fornecido, o apresentador volta a ocupar o centro depois de mostrar os exemplos. Para o FAQ, ele deve permanecer visível nos trechos falados, deixando o plano apenas no respiro breve do campus ou na vinheta. [Referência de movimento](https://prompt-motion.com/ror-fly-9950f1)
