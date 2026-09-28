# Projeto de arquitetura - Caso Onibus / Envelope D

Este repositorio contem a proposta de arquitetura para o caso **Onibus: bilhetagem e mobilidade urbana**, considerando o envelope **D: empresa que vende o sistema para varias cidades**.

##Integrantes
- Priscila Amorim dos Santos - 24787350
- Bruna Rodrigues Cardoso
- Hector Lopes - 25013988

## Como navegar

- `1-matriz/matriz.md`: matriz de estilos aplicada ao caso.
- `2-arquitetura/`: diagramas C4, mapa de restricoes e decisoes, ADRs e respostas obrigatorias.
- `3-spike/`: codigo pequeno que prova a decisao mais arriscada.

## Resumo da proposta

A arquitetura e hibrida e multi-tenant. A validacao embarcada usa estilo hexagonal com microkernel de regras para operar offline. O backend central combina arquitetura celular por cidade, microsservicos por subdominio, arquitetura orientada a eventos, CQRS e Event Sourcing nos fluxos que exigem auditoria e reprocessamento. Cada cidade tem particoes, filas, limites e projecoes isoladas para que um pico sazonal ou falha local nao derrube outros clientes.
