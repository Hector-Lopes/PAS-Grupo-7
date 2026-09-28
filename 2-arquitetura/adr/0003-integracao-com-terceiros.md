# ADR-0003 - Integracao com banco, adquirente, operadoras e orgao gestor

## Status

Aceita.

## Contexto

O sistema se integra com banco, adquirente de cartao, pontos de recarga, operadoras de onibus, auditoria externa e orgao gestor. Esses atores podem impor formatos, indisponibilidades e janelas de envio.

## Decisao

Usar ports and adapters nas integracoes e filas de saida para comunicacoes externas. O dominio nao chama diretamente SDKs, arquivos ou APIs de terceiros. Cada integracao possui:

- adaptador de entrada ou saida;
- contrato versionado;
- idempotency key;
- fila de reentrega;
- registro de auditoria com correlacao entre evento interno e protocolo externo.

Arquivos diarios de operadoras e relatorios do orgao gestor sao tratados como conectores do tipo `arquivo`. Banco e adquirente usam conectores do tipo `chamada` com retry controlado e reconciliacao posterior.

## Alternativas consideradas

- Chamadas sincronas diretas a partir dos servicos de dominio: descartadas porque indisponibilidade externa travaria fluxos internos.
- ESB central corporativo: descartado porque adicionaria ponto unico de falha e latencia em fluxos criticos.
- Replicar todos os dados para terceiros em tempo real: descartado porque aumenta exposicao LGPD e custo sem necessidade.

## Consequencias positivas

- Terceiros podem cair sem paralisar validacao, recarga ja confirmada ou atendimento.
- E possivel trocar formato/API de um terceiro alterando apenas o adaptador.
- Auditoria consegue rastrear o que foi enviado, quando e com qual resposta.

## Consequencias negativas

- Ha atraso controlado em comunicacoes externas.
- Fila de reentrega exige monitoramento.
- Contratos precisam ser documentados e versionados com rigor.
