# Grupo 7 — Um problema, cinco realidades

**Disciplina:** Padrões e Arquitetura de Software · PUC-Campinas · 2026-2
**Caso:** Saúde — rede municipal de atenção à saúde
**Envelope:** B — consórcio de empresas de tecnologia (SLA de 99,9% sobre a regulação de leitos e a UPA)

## Integrantes

- Priscila Amorim dos Santos - 24787350
- Bruna Rodrigues Cardoso
- Hector Lopes - 25013988

## Como navegar

- `1-matriz/matriz.md`: matriz de estilos aplicada ao caso.
- `2-arquitetura/`: diagramas C4, mapa de restricoes e decisoes, ADRs e respostas obrigatorias.
- `3-spike/`: codigo pequeno que prova a decisao mais arriscada.

## Resumo da proposta

A arquitetura e hibrida. A validacao embarcada usa estilo hexagonal com microkernel de regras para operar offline. O backend central combina microsservicos por subdominio, arquitetura orientada a eventos, CQRS e Event Sourcing nos fluxos que exigem auditoria e reprocessamento. Dados pessoais em eventos imutaveis sao cifrados com chave por titular, permitindo auditoria financeira sem manter identificacao pessoal apos pedido valido de exclusao.
