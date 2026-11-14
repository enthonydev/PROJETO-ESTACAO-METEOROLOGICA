# ADR-003 - Validação de temperatura da bancada DHT22

Estado: implementada para revisão no PR 42; sem alteração do formato JSON ou dos estados de qualidade.

O CT03 do roteiro do professor exige rejeitar T=150 °C. A fronteira da API aceitava esse valor porque o campo era apenas numérico. A bancada usa DHT22 e o firmware já considera -40 a 80 °C como faixa de leitura. A API aplica agora a mesma faixa inclusiva e rejeita NaN/infinito. Null continua permitido para ausência de leitura. O schema JSON documenta os limites para manter coerência com o modelo Python.

Essa validação de faixa não implementa remoção de outliers temporais, médias móveis ou calibração. Sensores futuros com outra faixa exigirão revisão explícita desta decisão e do contrato. Evidência de regressão: teste CT03 envia 150 °C e exige HTTP 422.
