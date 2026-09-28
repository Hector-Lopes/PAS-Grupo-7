# ADR-0001 - Estrutura geral hibrida por subdominio

## Status

Aceita.

## Contexto

O sistema de bilhetagem precisa operar em tempo real dentro de 1.200 onibus, tolerar ate 4 horas sem rede, processar recargas financeiras, absorver telemetria em fluxo, recalcular repasses mensais e manter trilha auditavel por exigencia regulatoria. Um unico estilo arquitetural nao atende bem a todos esses perfis.

## Decisao

Adotar arquitetura hibrida com fronteiras explicitas:

| Fronteira | Estilo principal | Motivo |
|---|---|---|
| Validador embarcado | Hexagonal + microkernel | Dominio local precisa rodar offline, testavel e com regras tarifarias trocaveis. |
| Cartoes e recargas | Servico transacional com CQRS nas leituras | Saldo e dinheiro exigem dono claro e consistencia forte na escrita. |
| Telemetria | Eventos + pipes and filters | Alto volume e processamento em etapas independentes. |
| Informacao ao passageiro | Projecoes de leitura/cache | Consultas em pico nao podem pressionar o transacional. |
| Repasse e conciliacao | Event Sourcing + CQRS | Auditoria, replay e contestacao mensal. |
| Integracoes externas | Ports and adapters + filas de saida | Contratos de terceiros mudam e podem ficar indisponiveis. |

## Alternativas consideradas

- Monolito em camadas: descartado porque acopla implantacao e escalabilidade de subdominios com cargas muito diferentes.
- ESB central: descartado porque cria gargalo e ponto unico de falha para telemetria e validacao.
- Microsservicos para tudo: descartado porque elevaria custo operacional para uma equipe de 15 pessoas e dificultaria conformidade.

## Consequencias positivas

- Cada subdominio usa o estilo mais adequado ao seu requisito critico.
- Falhas de telemetria ou informacao ao passageiro nao derrubam validacao e recarga.
- A arquitetura torna explicito onde ha consistencia forte e onde ha consistencia eventual.

## Consequencias negativas

- Exige disciplina de contratos entre eventos, APIs e arquivos.
- Observabilidade e testes de integracao ficam mais importantes.
- A equipe precisa manter padroes de ADR, eventos e auditoria para evitar divergencia entre servicos.
