# ADR-0004 - Operacao, implantacao e observabilidade

## Status

Aceita.

## Contexto

O envelope D usa nuvem publica multirregiao e atende cidades de 200 mil a 3 milhoes de habitantes. A equipe tem 25 desenvolvedores em 3 times distribuidos, portanto a operacao precisa permitir escala seletiva e isolamento sem exigir que cada cidade vire um produto diferente.

## Decisao

Implantar os servicos centrais em nuvem publica multirregiao com celulas por cidade ou grupo de cidades. A infraestrutura e declarativa e o CI/CD publica a mesma versao do produto nas celulas, com configuracoes por tenant. Servicos criticos possuem metricas, logs estruturados e rastreamento distribuido com `correlation_id` e `tenant_id`.

O validador embarcado e distribuido por pacote assinado. Regras tarifarias e listas de bloqueio tambem sao assinadas e versionadas por cidade. A telemetria escala por consumidores independentes do broker de cada celula. Projecoes de leitura podem ser reconstruidas a partir do log de eventos da cidade.

## Alternativas consideradas

- Operacao manual em servidores sem pipeline: descartada por risco de mudanca nao auditavel.
- Escalar tudo igualmente: descartado porque cidades pequenas pagariam pelo pico das grandes.
- Observabilidade apenas por logs de aplicacao: descartada porque incidentes precisam mostrar qual cidade, fila e consumidor foram afetados.

## Consequencias positivas

- Mudancas ficam rastreaveis.
- Picos de uma cidade podem ser tratados sem superdimensionar toda a plataforma.
- Incidentes sao investigaveis por cidade, fluxo de evento, usuario tecnico e versao de regra.

## Consequencias negativas

- Ha custo inicial de automacao e padronizacao.
- Pacotes embarcados exigem processo robusto de assinatura e rollback.
- A equipe precisa manter paineis e alertas por cidade/celula.
