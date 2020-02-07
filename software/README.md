# Funções Tivaware #

## 1.	Clock Geral do Sistema ##

### SyzCtlClockSet(uint32_t ui32Config) ###
- <b>Definição</b>: Configuração do clock geral do sistema. 
- <b>Parâmetros</b>: “ui32Config” é o parâmetro, ou os parâmetros de configuração (quando vários parâmetros, os mesmos são separados por “|”).
- <b>Exemplo</b>: 
```
SysCtlClockSet(SYSCTL_SYSDIV_5|SYSCTL_USE_PLL|SYSCTL_XTAL_16MHZ|SYSCTL_OSC_MAIN);
```
No exemplo acima, pode ser verificado a utilização de um cristal externo de 16MHz, representados pelos parâmetros SYSCTL_XTAL_16MHZ e SYSCTL_OSC_MAIN e configuração do clock do sistema através de uma PLL (que possui 200MHz de referencia para cálculos) e divisão da mesma por 5, representadas pelos parâmetros SYSCTL_SYSDIV5 e SYSCTL_USE_PLL. 
Assim, o clock geral do sistema estará configurado para trabalhar com o cristal de 16 MHz da placa de desenvolvimento e estará funcionando a 40 MHz conforme a divisão da PLL escolhida.

### SysCtlPeripheralEnable(ui32Peripheral) ###
- <b>Definição</b>: Função para habilitar periférico, como o GPIO.
- <b>Parâmetros</b>: “ui32Peripheral” é o periférico a ser habilitado.
- <b>Exemplo</b>: 
```
SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
```
Habilitação do periférico GPIO Port F.

## 2.	Configurando e usando o GPIO ##
### GPIOPinTypeGPIOOutput(uint32_t ui32Port, uint8_t ui8Pins) ###
- <b>Definição:</b> Função onde um pino da GPIO é configurado como saída.
- <b>Parâmetros:</b> “ui32Port” representa o PORT a ser configurado e o “ui8Pins” o pino.

### GPIOPinTypeGPIOInput(uint32_t ui32Port, uint8_t ui8Pins) ###
- <b>Definição:</b> Função onde um pino da GPIO é configurado como entrada.
- <b>Parâmetros:</b> “ui32Port” representa o PORT a ser configurado e o “ui8Pins” o pino.
- <b>Exemplo</b>:
```
  SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF); 
  GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3);
  GPIOPinTypeGPIOInput(GPIO_PORTF_BASE, GPIO_PIN_4|GPIO_PIN_0);
```
O exemplo acima configura na PORT F, os pinos PF1, PF2 e PF3 como saída (LED RGB da Launchpad) e os pinos PF0 e PF4 como entrada (dois botões da Launchpad). 

### GPIOPinRead(uint32_t ui32Port, uint8_t ui8Pins) ###
- <b>Definição:</b> Função que retorna se o pino está em nível lógico alto ou baixo.
- <b>Parâmetros: </b> “ui32Port” representa o PORT e o “ui8Pins” o pino a serem lidos.
- <b>Exemplo:</b> 
```
GPIOPinRead(GPIO_PORTF_BASE, GPIO_PIN_4);
```
Retorna o endereço, ou valor, do PIN_4 do PORTF caso 1.

### GPIOPinWrite(uint32_t ui32Port, uint8_t ui8Pins, uint8_t ui8Val) ###
- <b>Definição:</b> Função que manda o nível lógico alto ou baixo para o pino em questão.
- <b>Parâmetros:</b> “ui32Port” representa o PORT, o “ui8Pins” o pino de entrada e “ui8Val” o valor.
- <b>Exemplo:</b> 
```
GPIOPinWrite(GPIO_PORTF_BASE,GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3,GPIO_PIN _2); 
```
Aciona somente o PIN_2 do PORTF

## 3.	Utilizando uma UART ##

### UARTConfigSetExpClk(uint32_t ui32Base, uint32t ui32UARTClk, uint32_t ui32Baud, uint32_t ui32Config) ###
- <b>Definição:</b> Função que configura os parâmetros da serial utilizada.
- <b>Parâmetros:</b> “ui32Base” é a UART port ,  “ui32UARTClk” é o clock disponível para o modulo UART, “ui32Baud” é o baud rate, “ui32Config” indica o formato dos dados.

### UARTCharPut(uint32_t ui32Base, unsigned char ucData) ###
- <b>Definição: </b> Função que imprime na serial o parâmetro ucData.
- <b>Parâmetros: </b> “ui32Base” é a UART port, “ucData” é o caractere a ser transmitido.

### UARTPrintf(unsigned char *ucData) ###
- <b>Definição: </b> Função que imprime na serial o parâmetro ucData.
- <b>Parâmetros: </b> “ucData” é o caractere a ser transmitido.

### UARTCharGet(uint32_t ui32Base) ###
- <b>Definição:</b> Função que retorna o caractere lido na serial como int32_t.
- <b>Parâmetros:</b> “ui32Base” é a UART port.
- <b>Exemplo:</b> 
```
void ConfigureUART(void) { 
  SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
  SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
  GPIOPinConfigure(GPIO_PA0_U0RX); 
  GPIOPinConfigure(GPIO_PA1_U0TX); 
  GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);
  UARTClockSourceSet(UART0_BASE, UART_CLOCK_PIOSC); 
  UARTStdioConfig(0, 115200, 16000000); 
}
```

## 4.	Configurando interrupções. ##
### Configurando o ambiente ###
- <b>1º Passo:</b> Declare a função a ser chamada através da interrupção desejada como função externa ao código, aproximadamente na linha 58 do código do “tm4c123gh6pmi_sturtup_ccs.c”.
- <b>2º Passo:</b> Adicione essa função ao vetor de interrupções em sua devida posição substituindo a função padrão “IntDefaultHandler” pela sua função utilizada. Para uma interrupção no PORTF, sua posição será aproximadamente na linha 116 do código do “tm4c123gh6pmi_startup_ccs.c”. Após estas configurações, sempre que houver uma borda de descida no pino 4 do PortF (SW1 pressionado), sua função de interrupção será executada!

### IntMasterEnable() ###
- <b>Definição:</b> Função que permite ao processador responder a todas as chamadas de interrupção utilizadas.

### GPIOIntEnable(uint32_t ui32Port, uint32_t ui32IntFlags) ###
- <b>Definição:</b> Função onde um pino da GPIO do microcontrolador é configurado como interrupção e o parâmetro ui32IntFlags representa o pino a ser configurado da seguinte forma: GPIO_INT_PIN_0, GPIO_INT_PIN_1, ... ou GPIO_INT_PIN_7.
- <b>Parâmetros:</b> “ui32Port” é o GPIO port, “ui32IntFlags” é o pino do GPIO port.

### GPIOIntTypeSet(uint32_t ui32Port, uint8_t ui8Pins, uint32_t ui32IntType) ###
- <b>Definição:</b> Função onde um pino da GPIO do microcontrolador que é configurado como interrupção tem o seu modo de habilitação configurado, e o parâmetro ui32IntType que representa o modo de habilitação da interrupção pode ser configurado como: GPIO_FALLING_EDGE (para borda de descida), GPIO_RISING_EDGE (para borda de subida), GPIO_BOTH_EDGE (qualquer borda), GPIO_LOW_LEVEL (nível lógico baixo) e GPIO_HIGH_LEVEL (nível lógico alto).
- <b>Parâmetros:</b> “ui32Port” é o GPIO port, “ui8Pins” são os pinos, “ui32IntType” representa o modo de habilitação da interrupção.

## 5.	Configurando o Timer ##

### Configurando o ambiente ###
- <b>1º Passo:</b> Declare a função a ser chamada através da interrupção desejada como função externa ao código, aproximadamente na linha 59 do código do “tm4c123gh6pmi_sturtup_ccs.c”.
- <b>2º Passo:</b> Adicione essa função ao vetor de interrupções em sua devida posição substituindo a função padrão “IntDefaultHandler” pela sua função utilizada. Para uma interrupção no PORTF, sua posição será aproximadamente na linha 106 do código do “tm4c123gh6pmi_sturtup_ccs.c”.Após estas configurações, sempre que o timer atingir o período de contagem selecionado, ele vai gerar uma interrupção e a função declarada será executada!

### TimerConfigure(uint32_t ui32Base, uint32t ui32Config) ###
- <b>Definição:</b> Função que configura o tipo de timer utilizado onde o parâmetro ui32Config e escolhido conforme a configuração de Timer periódico, Disparo único, PWM, etc.  
- <b>Parâmetros:</b> "ui32Base" é o endereço base para o modulo do timer, "ui32Config" tipo de configuração do timer (Periódico, disparo único, PWM).

### TimerEnable(uint32_t ui32Base, uint32_t ui32Timer) ###
- <b>Definição:</b> Função que habilita o timer escolhido após a sua configuração onde o parâmetro ui32Timer é o Timer escolhido: TIMER_A, TIMER_B, ou TIMER_BOTH.
- <b>Parâmetros:</b> "ui32Base" é o endereço base para o modulo do timer, "ui32Timer" é o timer escolhido.

### TimerLoadSet(uint32_t ui32Base, uint32_t ui32Timer, uint32_t ui32Value) ###
- <b>Definição: </b> Função que seleciona o valor de estouro do Timer (Em caso de Timer periódico) onde o parâmetro ui32Value é um número inteiro representado por até 32 bits.
- <b>Parâmetros: </b> "ui32Base" é o endereço base para o modulo do timer, "ui32Timer" é o timer escolhido, "ui32Value" é o clock geral dividido pela frequencia gerada (ClockGeral / ClockDesejado).  

### TimerIntClear(uint32_t ui32Base, uint32_t ui32IntFlags) ###
- <b>Definição:</b> Função que deve ser chamada após a interrupção do timer periódico para manter o Trigger.
- <b>Parâmetros:</b> "ui32Base" é o endereço base para o modulo do timer, "ui32IntFlags" mascara de bits utilizada para limpar o vetor de interrupções do timer em questão.

# Link para requisitos de software #

https://www.dropbox.com/s/z635f89p6a7jl0g/myo_cap_gui_requisitos_2020.pdf?dl=0
