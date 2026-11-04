# ADR-003 (PROPOSTA) — Firmware Arduino N2 para testes reais de Wi-Fi/MQTT

**Status:** Proposta — não substitui a ADR-001 nem a arquitetura aprovada sem decisão formal.

## Contexto

A baseline N1 prevê ESP32/MicroPython e Wi-Fi/MQTT. A montagem física e os testes disponíveis da equipe usam Arduino/C++ (DEV 1.1), com DHT22, OLED, LDR DO e chuva DO já validados. Para o ensaio presencial de redes e telemetria, refazer tudo imediatamente em MicroPython aumenta o risco de perder o firmware já funcional.

## Solução experimental

Preparar um firmware Arduino N2 isolado, preservando DEV 1.1 como rollback, com três perfis locais de rede, reconexão Wi-Fi/MQTT, NTP em UTC, publicação compatível com o contrato v1.0 e opcionais de BMP280/BME280 e MQ-135 desligados até verificação física.

O backend, worker, PostgreSQL, contrato de telemetria e dashboard permanecem os mesmos. O tópico diagnóstico separado de estados digitais **não substitui** a telemetria v1.0.

## Pontos de decisão antes do aceite

1. Professor/equipe autorizam Arduino/C++ como firmware de entrega ou exigem MicroPython?
2. A rede da UNIP usa WPA2-Personal, 802.1X/Enterprise, portal cativo ou isolamento de clientes?
3. Confirmar se o sensor de pressão é BMP280 ou BME280 e GPIO ADC1 disponível para MQ-135.
4. Fixar critério de teste de estresse e duração conforme rubrica.
5. Confirmar infraestrutura MQTT, credenciais, proteção e política temporal.

## Consequência

Até revisão desta ADR e testes físicos, a mudança permanece **experimental e não pode ser apresentada como hardware ou Wi-Fi validado**. Dados simulados do CI não equivalem a transmissão ESP32 real.
