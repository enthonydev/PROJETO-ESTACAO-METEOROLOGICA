# Wokwi — análise de simulação

**Estado:** NÃO EXECUTADO / SIMULAÇÃO NÃO CRIADA nesta versão.

A simulação foi preparada como possibilidade de desenvolvimento, mas não foi versionado um projeto Wokwi porque os modelos exatos dos componentes, a decisão entre BME280 e DHT22 + BMP280, a pinagem e as tensões ainda não estão confirmados. Criar um circuito completo agora exigiria substituir ou presumir componentes e poderia produzir uma representação enganosa.

## Escopo possível depois da decisão dos POs

- ESP32 e firmware estrutural compatível com a simulação;
- barramento I²C conceitual e, se suportados no modelo escolhido, TCA9548A, displays e sensores;
- exercícios de fluxo, estados e falhas simuladas;
- distinção explícita entre componentes simulados e componentes reais.

## Limitações

Wokwi seria classificado somente como **SIMULADO**. Não comprovaria alimentação real, níveis elétricos do módulo adquirido, endereço efetivo, desempenho do display, estabilidade do ESP32 em bancada, calibração, leitura ambiental real ou teste de campo. Um componente não suportado não deve ser substituído silenciosamente para fazer a simulação parecer completa.

Quando a decisão dos POs, os modelos e o pinout forem confirmados, este diretório poderá receber um projeto de simulação com README de versão, componentes, diferenças para o hardware real, procedimento e resultados simulados.
