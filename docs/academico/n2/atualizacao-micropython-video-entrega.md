# Ajustes da entrega e do vídeo — migração para MicroPython

## Estado técnico para slides e documento consolidado

Texto substituto para a seção de firmware:

> O firmware integrado foi implementado em MicroPython para ESP32, preservando a pinagem da bancada. O agendamento cooperativo usa ticks_ms e ticks_diff para ler DHT22 a cada dois segundos e consultar chuva e luz digitais sem aguardar a conexão de rede. A OLED apresenta os dados locais. O Wi-Fi suporta uma lista de redes e reconexão automática, enquanto o USB continua disponível para diagnóstico e para a ponte de temperatura e umidade ao dashboard. A pressão é demonstrativa, identificada como DEMO. A implementação passou em testes automatizados; o ensaio físico da versão MicroPython ainda deve ser registrado.

No slide de arquitetura, diferenciar os dois caminhos: **implementado para execução nesta etapa: ESP32 → USB → ponte Python → FastAPI → dashboard**; **arquitetura de telemetria prevista: ESP32 → Wi-Fi → MQTT → backend**. O broker/consumidor já existente não comprova publicação física pelo ESP32.

No slide de testes, conservar o print antigo do Arduino IDE como evidência histórica das leituras reais do DHT. Não apresentá-lo como captura do MicroPython. Substituir a captura do firmware atual por um registro do terminal USB após a migração. Scanner confirma somente dispositivos realmente presentes; pressão DEMO não é evidência de funcionamento do 280.

Resultados reais anteriores: DHT com temperatura de 21,3–21,4 °C e umidade de 82,0–82,2%, conforme logs fornecidos. Não extrapolar isso para vento, precipitação quantitativa ou pressão medida.

## Organização da equipe mantida

- James: contexto, objetivo e organização da apresentação.
- Enthony: hardware, montagem e sensores.
- Luan: software, MicroPython, Wi-Fi e fluxo de comunicação.
- Luiz: dashboard e visualização.

## Falas atualizadas do Luan

Duração estimada de 25–30 s por parágrafo, dependendo do ritmo; preservar a fala inteira. O texto explica o código preparado sem alegar ensaio físico ainda não realizado.

**Parágrafo 1:** Na parte do software, nós preparamos a migração do ESP32 para MicroPython, mantendo os mesmos pinos da montagem. O programa organiza as leituras por intervalos: temperatura e umidade são consultadas a cada dois segundos, enquanto chuva e luminosidade usam entradas digitais. Assim, conseguimos atualizar a tela e acompanhar os sensores sem depender da conexão com a internet.

**Parágrafo 2:** Para o Wi-Fi, o código aceita diferentes redes e tenta se reconectar automaticamente quando a conexão cai. Esse processo acontece junto com as leituras, sem deixar o protótipo esperando pela rede. A comunicação USB também foi preservada: ela permite acompanhar os registros, interromper o programa e levar as medições de temperatura e umidade até o nosso dashboard pela ponte Python.

**Parágrafo 3:** Nós também separamos os dados medidos dos demonstrativos. A temperatura e a umidade são obtidas pelo DHT22; já a pressão que aparece na OLED está identificada como DEMO. Foram preparados testes automatizados para as leituras, a tela e a reconexão. A próxima conferência é executar essa versão na placa e registrar o comportamento real durante a queda e o retorno do Wi-Fi.

Depois do ensaio real, a última frase pode ser substituída por uma descrição fiel do resultado observado. Não antecipar que passou.

## Plano de edição pronto para aplicação

Manter abertura e encerramento em grupo. Reutilizar as falas de hardware, contexto e dashboard que continuem corretas. Regravar somente trechos que atribuam ao firmware atual Arduino/C++, sketch, millis ou publicação MQTT já funcionando. A pinagem e a maior parte das tomadas do protótipo continuam utilizáveis.

Ordem: abertura do grupo → James/contexto → Enthony/hardware → Luan/software → Luiz/dashboard → conclusão James → encerramento do grupo.

Durante Luan 1, usar a pinagem e o código `run_station`/`Station.step`; durante Luan 2, destacar os perfis e a reconexão; durante Luan 3, mostrar a distinção entre DHT e pressão DEMO. As capturas reais da execução só entram após a gravação na placa. Imagens ilustrativas de componentes podem acompanhar os nomes, sem representar testes físicos.

Para edição Remotion: espelhar horizontalmente apenas os clipes de câmera, mantendo o formato paisagem; não espelhar textos, códigos ou capturas de tela. Preservar resolução/fps originais, manter aproximadamente 0,5–0,8 s antes/depois das falas e usar cortes por silêncio, sem cortar sílabas. Não acelerar voz para forçar 25 s: ajustar a duração da sequência ao áudio completo. Evitar novas compressões intermediárias. Revisar a fala inteira do Luan, que foi apontada como cortada na versão anterior.

## O que depende da equipe

Conectar e gravar a placa; confirmar sensores, OLED, USB e reconexão; registrar uma captura real do terminal/dashboard; regravar somente as falas incompatíveis. Os materiais anteriores de entrega não devem ser chamados de versão final atualizada até incorporar este ajuste e as evidências novas. As assinaturas da declaração continuam sendo dos integrantes.

## Revisão de aderência ao roteiro

CT01: variação de temperatura DHT22; CT02: queda e reconexão Wi-Fi sem travamento; CT03: rejeição de temperatura de 150 °C; CT04: marcador no mapa nas coordenadas. O CT03 foi adicionado explicitamente aos testes de API. CT04 continua pendente. O polling do painel foi reduzido de 10 s para 2 s para caber no orçamento de atualização de 5 s do roteiro; a latência real exige medição na bancada.
