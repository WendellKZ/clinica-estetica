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
- Segundos e microssegundos serão removidos.
- Exemplo: às 11:38, o início sugerido será 11:43.
- O fim será calculado a partir do início sugerido, usando a duração padrão do serviço.
- Antes de escolher um serviço, será mantida a duração inicial de 60 minutos. Assim, início 11:43 gera fim 12:43.
- Ao trocar o serviço, o comportamento existente de recalcular o fim pela duração do serviço será preservado.
- A regra vale somente para novos agendamentos; edições manterão os horários salvos.

## Validação e compatibilidade

- O backend fornecerá os valores iniciais, evitando dependência exclusiva de JavaScript.
- O formulário continuará bloqueando horários retroativos e conflitos do mesmo profissional.
- Sem JavaScript, todas as etapas permanecerão visíveis e o envio continuará funcional.
- Nenhuma alteração de banco de dados será necessária.

## Testes e publicação

- Um teste congelará o horário e confirmará início em `agora + 5 minutos` e fim em `início + 60 minutos`.
- Um teste verificará as quatro etapas e o cabeçalho “Novo agendamento”.
- A suíte Django completa será executada.
- Após validação, a alteração será enviada ao GitHub, publicada no Render e verificada na URL pública.
