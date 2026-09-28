# ADR-0002 - Dados, consistencia e replay auditavel

## Status

Aceita.

## Contexto

O caso mistura dados financeiros, dados pessoais, eventos offline e necessidade de recalculo mensal. O sistema deve impedir fraude de recarga, detectar uso duplicado depois da reconexao e recalcular repasses com regras historicas.

## Decisao

Definir donos de dados por subdominio:

| Dado | Dono | Consistencia |
|---|---|---|
| Saldo central, recargas e bloqueios | Cartoes e Recargas | Escrita transacional forte. |
| Validacoes offline | Validador local ate sincronizar; depois Event Store | Consistencia eventual com conciliacao. |
| Eventos financeiros | Event Store de Repasse | Append-only, imutavel, replay. |
| Regras tarifarias | Catalogo de Tarifas | Versionadas por vigencia. |
| Projecoes de consulta | Servicos de leitura | Recriaveis a partir dos eventos. |
| Dados pessoais do passageiro | Cadastro de Passageiros | Separados dos fatos contabeis e cifrados quando referenciados em eventos. |

Cada validacao usa um contador monotonicamente crescente por cartao. O par `cartao_pseudonimo + contador_transacao` e idempotency key para detectar duplicidade entre onibus. Recargas confirmadas geram recibos assinados e eventos idempotentes.

## Alternativas consideradas

- Banco relacional unico: descartado porque validadores offline nao conseguiriam depender dele e porque replay historico ficaria acoplado ao modelo atual.
- Sincronizacao por sobrescrita de saldo: descartada porque perderia conflitos offline e dificultaria auditoria.
- Apagar eventos antigos para atender LGPD: descartado porque quebraria fechamento financeiro e trilha regulatoria.

## Consequencias positivas

- O fechamento mensal e reconstruivel.
- Duplicidades e fraudes ficam detectaveis mesmo quando surgem apos reconexao.
- Leitura e relatorio podem escalar por projecoes sem afetar a escrita.

## Consequencias negativas

- Consistencia eventual precisa ser explicada para atendimento e auditoria.
- Evolucao de esquema de eventos exige versionamento.
- Reprocessamentos podem consumir tempo e precisam de janelas operacionais planejadas.
