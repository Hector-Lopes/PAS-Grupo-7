# ADR-0005 - Isolamento multi-tenant por cidade

## Status

Aceita.

## Contexto

O envelope D descreve uma empresa que vendera o sistema para varias cidades, de 200 mil a 3 milhoes de habitantes, em nuvem publica multirregiao. A exigencia dominante e que varios clientes coexistam no mesmo produto, que picos sazonais sejam absorvidos e que falha em uma cidade nao afete as outras.

Esta e a decisao mais arriscada do projeto, porque uma separacao fraca por `tenant_id` pode parecer suficiente no desenvolvimento, mas falhar em producao quando uma cidade grande acumular filas, consumir banco, derrubar projecoes ou atrasar consumidores compartilhados.

## Decisao

Adotar arquitetura celular por cidade, com dois modos de implantacao:

| Porte da cidade | Celula | Decisao |
|---|---|---|
| Pequena/media | Celula compartilhada com particoes isoladas | Reduz custo, mantendo filas, quotas, bancos logicos e metricas por `tenant_id`. |
| Grande/metropolitana | Celula dedicada | Isola broker, consumidores, banco operacional, projecoes e limites de escala. |

Todo evento, chamada e registro persistido carrega `tenant_id`. O roteador de cidade decide a celula de destino. Filas de validacao, recarga e telemetria sao particionadas por cidade. Consumidores escalam por cidade e possuem limite de processamento, circuit breaker e dead-letter queue tambem por cidade.

## Alternativas consideradas

- Banco e fila unicos para todos os clientes: descartado porque uma campanha ou falha de uma cidade poderia atrasar todas as demais.
- Instancia totalmente separada para cada cidade: descartada porque aumenta custo e operacao para cidades pequenas.
- Apenas coluna `tenant_id` no banco compartilhado: descartada porque isola autorizacao, mas nao isola consumo de CPU, fila, conexoes e atraso operacional.

## Consequencias positivas

- Uma cidade em pico acumula backlog apenas na propria fila.
- Cidades grandes podem escalar consumidores e armazenamento sem impactar cidades pequenas.
- Falha em projecao, integracao externa ou telemetria fica contida na celula.
- O produto continua unico para os 3 times, com variacao por configuracao de tenant.

## Consequencias negativas

- A plataforma precisa de roteamento por cidade e catalogo de tenants.
- Testes precisam cobrir vazamento entre tenants e competicao por recursos.
- Operacao multirregiao exige paineis por celula, tenant e fluxo.
