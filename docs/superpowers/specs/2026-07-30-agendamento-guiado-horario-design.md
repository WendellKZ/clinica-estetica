# Agendamento guiado e horário inicial adiantado

## Objetivo

Transformar o novo agendamento em um processo guiado, consistente com os cadastros do sistema, e evitar que o horário inicial sugerido coincida com o minuto atual.

## Etapas

O formulário terá quatro etapas:

1. Cliente: localizar um cliente existente ou cadastrar nome, telefone e e-mail na hora.
2. Serviço e profissional: escolher o procedimento e quem fará o atendimento.
3. Data e horário: conferir início, duração, fim, status e observações.
4. Conferir e agendar: revisar as informações e escolher entre agendar ou agendar já confirmado.

Em telas largas, as etapas aparecerão no painel verde-oliva à esquerda. Em celulares, aparecerão em uma faixa de progresso no topo. Os botões Voltar e Continuar seguirão o padrão dos demais assistentes.

## Regra de horário

- Ao abrir um novo agendamento, o início sugerido será o horário local atual acrescido de cinco minutos.
- A margem evita que o horário se torne retroativo enquanto o usuário preenche o formulário. Por exemplo, se o formulário abrir às 11:38 e levar dois minutos para ser preenchido, o início sugerido em 11:43 ainda será válido.
- Segundos e microssegundos serão removidos.
- Exemplo: às 11:38, o início sugerido será 11:43.
- O fim será calculado a partir do início sugerido, usando a duração padrão do serviço.
- Antes de escolher um serviço, será mantida a duração inicial de 60 minutos. Assim, início 11:43 gera fim 12:43.
- Ao trocar o serviço, o comportamento existente de recalcular o fim pela duração do serviço será preservado.
- A regra vale somente para novos agendamentos; edições manterão os horários salvos.

## Visibilidade do logo

- O arquivo atual possui grande área vazia ao redor da marca, o que reduz excessivamente a borboleta e o nome quando a imagem é encaixada na barra lateral.
- Será criada uma versão recortada próxima à borboleta, ao nome e à palavra “Estética”.
- O fundo rosa suave será preservado.
- A barra lateral usará a versão recortada com tamanho responsivo e sem distorção.
- A versão original será preservada no projeto para evitar perda do material fornecido.
- O mesmo recorte poderá ser usado no cabeçalho móvel para manter a marca legível em telas pequenas.

## Validação e compatibilidade

- O backend fornecerá os valores iniciais, evitando dependência exclusiva de JavaScript.
- O formulário continuará bloqueando horários retroativos e conflitos do mesmo profissional.
- Sem JavaScript, todas as etapas permanecerão visíveis e o envio continuará funcional.
- Nenhuma alteração de banco de dados será necessária.

## Testes e publicação

- Um teste congelará o horário e confirmará início em `agora + 5 minutos` e fim em `início + 60 minutos`.
- Um teste verificará as quatro etapas e o cabeçalho “Novo agendamento”.
- A apresentação do logo recortado será verificada em tela larga e em celular.
- A suíte Django completa será executada.
- Após validação, a alteração será enviada ao GitHub, publicada no Render e verificada na URL pública.
