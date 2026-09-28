# ADR-0002 - Dados, consistencia e replay auditavel

## Status

Aceita.

## Contexto

O caso mistura dados financeiros, dados pessoais, eventos offline e necessidade de recalculo mensal. O sistema deve impedir fraude de recarga, detectar uso duplicado depois da reconexao e recalcular repasses com regras historicas.
No envelope D, os mesmos mecanismos precisam funcionar por cidade sem misturar dados ou permitir que o volume de uma cidade atrase outra.

## Decisao

Definir donos de dados por subdominio:

| Dado | Dono | Consistencia |
|---|---|---|
| Saldo central, recargas e bloqueios | Cartoes e Recargas | Escrita transacional forte. |
| Validacoes offline | Validador local ate sincronizar; depois Event Store da cidade | Consistencia eventual com conciliacao. |
| Eventos financeiros | Event Store de Repasse por cidade | Append-only, imutavel, replay. |
| Regras tarifarias | Catalogo de Tarifas | Versionadas por vigencia. |
| Projecoes de consulta | Servicos de leitura por cidade | Recriaveis a partir dos eventos. |
| Dados pessoais do passageiro | Cadastro de Passageiros da cidade | Separados dos fatos contabeis e minimizados nos eventos. |

Cada validacao usa um contador monotonicamente crescente por cartao. O par `tenant_id + cartao_pseudonimo + contador_transacao` e idempotency key para detectar duplicidade entre onibus sem cruzar cidades. Recargas confirmadas geram recibos assinados e eventos idempotentes.

## Alternativas consideradas

- Banco relacional unico: descartado porque validadores offline nao conseguiriam depender dele e porque replay historico ficaria acoplado ao modelo atual.
- Sincronizacao por sobrescrita de saldo: descartada porque perderia conflitos offline e dificultaria auditoria.
- Event Store unico para todas as cidades: descartado porque aumenta risco de vazamento entre clientes e cria competicao por recursos.

## Consequencias positivas

- O fechamento mensal e reconstruivel.
- Duplicidades e fraudes ficam detectaveis mesmo quando surgem apos reconexao.
- Leitura e relatorio podem escalar por projecoes de cada cidade sem afetar a escrita das demais.

## Consequencias negativas

- Consistencia eventual precisa ser explicada para atendimento e auditoria.
- Evolucao de esquema de eventos exige versionamento.
- Reprocessamentos podem consumir tempo e precisam de janelas operacionais planejadas.
