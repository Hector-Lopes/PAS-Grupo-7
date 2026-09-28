# ADR-0004 - Operacao, implantacao e observabilidade

## Status

Aceita.

## Contexto

O envelope E permite nuvem publica, mas exige trilha de auditoria completa. A equipe tem 15 desenvolvedores e 1 responsavel por conformidade, portanto a operacao precisa ser padronizada e observavel sem depender de trabalho manual constante.

## Decisao

Implantar os servicos centrais em nuvem publica com ambientes separados, infraestrutura declarativa e pipeline de CI/CD com aprovacao para mudancas sensiveis. Servicos criticos possuem metricas, logs estruturados e rastreamento distribuido com `correlation_id`.

O validador embarcado e distribuido por pacote assinado. Regras tarifarias e listas de bloqueio tambem sao assinadas e versionadas. A telemetria escala por consumidores independentes do broker. Projecoes de leitura podem ser reconstruidas a partir do log de eventos.

## Alternativas consideradas

- Operacao manual em servidores sem pipeline: descartada por risco de mudanca nao auditavel.
- Escalar tudo igualmente: descartado porque telemetria e informacao ao passageiro variam mais do que recarga/repasse.
- Observabilidade apenas por logs de aplicacao: descartada porque investigacoes de auditoria exigem correlacao ponta a ponta.

## Consequencias positivas

- Mudancas ficam rastreaveis.
- Picos de telemetria e consulta podem ser tratados sem superdimensionar todo o sistema.
- Incidentes sao investigaveis por fluxo de evento, usuario tecnico e versao de regra.

## Consequencias negativas

- Ha custo inicial de automacao e padronizacao.
- Pacotes embarcados exigem processo robusto de assinatura e rollback.
- A equipe precisa manter paineis e alertas atualizados.
