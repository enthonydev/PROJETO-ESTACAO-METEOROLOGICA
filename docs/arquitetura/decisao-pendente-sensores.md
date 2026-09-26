# Decisão pendente dos POs — BME280 versus DHT22 + BMP280

**Status:** GATE DE DECISÃO DOS POs  
**POs que precisam participar:** Luan, Enthony e James  
**Decisão tomada nesta branch:** nenhuma.

## O que a baseline atual diz

A arquitetura do projeto menciona, no escopo acadêmico, DHT22 para temperatura/umidade e BMP280 para pressão/temperatura auxiliar. A mesma arquitetura descreve BME280 no subsistema local de visualização, fornecendo temperatura, umidade e pressão para o display meteorológico. Ela registra que a coexistência ou a necessidade final de sensores sobrepostos deve ser validada e documentada antes de simplificação.

O Guia PO Luan e o plano N1 de Luan mantêm os dois conjuntos no backlog: BME280 para o subsistema local e testes de DHT22/BMP280 quando disponíveis. Portanto, os documentos oficiais não autorizam eliminar nenhum componente unilateralmente.

## O que o contrato exige

O contrato de telemetria v1.0 exige seis grandezas:

- `temperature_c`;
- `humidity_pct`;
- `pressure_hpa`;
- `air_quality_raw`;
- `luminosity_pct`;
- `rain_mm`.

O contrato não escolhe o componente físico que produz temperatura, umidade ou pressão. Ele define campos, unidades/semântica e estados de qualidade. A decisão deve ser refletida depois no mapeamento hardware→firmware, sem alterar o contrato silenciosamente.

## O que o firmware representa hoje

O firmware atual possui um serviço genérico que recebe drivers injetados por nome. Não há drivers concretos de BME280, DHT22 ou BMP280. Os testes usam drivers fake e demonstram somente isolamento estrutural de falhas. Portanto, o firmware ainda não resolve a origem física das três grandezas.

## O que o plano de Luan exige

O plano exige testar BME280 e DS3231 no subsistema local e testar DHT22/BMP280, MQ-135, LDR e pluviômetro se estiverem disponíveis, registrando ausências e limitações. Também exige não inventar modelos, disponibilidade, pinagem, tensão ou evidência.

## Sobreposição

| Grandeza | BME280 | DHT22 + BMP280 | Consequência |
|---|---|---|---|
| Temperatura | Sim | DHT22 e BMP280 | Há pelo menos duas fontes possíveis; é necessário definir fonte primária, comparação ou coexistência. |
| Umidade | Sim | DHT22 | Há sobreposição direta; unidade, prioridade e validação precisam ser definidas. |
| Pressão | Sim | BMP280 | Há sobreposição direta; unidade e origem precisam ser definidas. |
| Interface | I²C, conforme módulo | DHT22 em protocolo próprio; BMP280 I²C/SPI | Pinout, conflitos e drivers mudam conforme a escolha. |
| Subsistema OLED/RTC | Pode compartilhar domínio I²C | BMP280 pode compartilhar I²C, DHT22 não necessariamente | TCA9548A e endereços precisam ser analisados com módulos reais. |

## Consequências da escolha futura

### Se BME280 for a fonte única dessas grandezas

- Menos fontes redundantes para temperatura, umidade e pressão.
- Mapeamento mais simples para o subsistema I²C local.
- Ainda exige confirmar módulo, endereço, tensão, driver, limites e validação física.
- Pode haver impacto no cumprimento literal de requisitos acadêmicos que mencionem DHT22/BMP280; James deve confirmar o escopo e os critérios do professor.

### Se DHT22 + BMP280 forem mantidos

- Mantém explicitamente os componentes acadêmicos previstos.
- Exige drivers e testes separados, além de resolver a coexistência com BME280.
- Exige definir se BME280 será redundante, usado apenas no display local ou comparado como referência interna.
- Aumenta o número de leituras, possíveis divergências, conexões e critérios de qualidade.

### Se houver coexistência

- Deve haver uma regra aprovada para fonte primária, comparação, qualidade, divergência e publicação.
- O contrato provavelmente pode permanecer igual, mas o mapeamento interno e a documentação devem ser ampliados.
- Não se deve publicar múltiplas fontes como se fossem a mesma medição sem registrar a semântica.

## Gate de decisão

A decisão conjunta deve registrar:

1. componentes efetivamente exigidos pelo professor e pelo MVP;
2. modelos reais e disponibilidade;
3. origem de cada uma das três grandezas;
4. necessidade ou não de redundância/comparação;
5. impacto no pinout, alimentação, I²C, firmware, contrato e N1;
6. critérios de aceite e testes correspondentes.

Até essa decisão, a matriz de hardware mantém todos os componentes mencionados, marca a relação como TBD e não declara qualquer sensor como validado.
