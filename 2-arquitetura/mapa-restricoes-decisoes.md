# Mapa de restricoes e decisoes

## Restricoes do envelope D

| Restricao | Decisao que atende | Referencias |
|---|---|---|
| Varios clientes no mesmo sistema. | Arquitetura celular por cidade, com `tenant_id` obrigatorio em chamadas, eventos, filas, bancos/projecoes e metricas. | ADR-0001, ADR-0002, ADR-0005; C4 Conteineres |
| Clientes variam de 200 mil a 3 milhoes de habitantes. | Plano de capacidade por cidade: cidades pequenas compartilham celula compacta; cidades grandes usam celula dedicada e consumidores escalados por fluxo. | ADR-0004, ADR-0005 |
| Pico sazonal brutal. | Filas, topicos e consumidores particionados por cidade; informacao ao passageiro e telemetria escalam por tenant sem aumentar toda a plataforma. | ADR-0001, ADR-0004, ADR-0005 |
| Falha em um cliente nao pode afetar os outros. | Quotas, circuit breakers, filas separadas e armazenamento particionado por cidade; falha de consumidor/projecao fica contida na celula. | ADR-0004, ADR-0005 |
| 25 desenvolvedores em 3 times distribuidos. | Produto dividido em plataforma multi-tenant, dominio financeiro/validacao e dados/observabilidade, com contratos padronizados entre celulas. | ADR-0001, ADR-0004 |
| Nuvem publica multirregiao. | Implantacao regional por celulas de cidades, com roteamento por cidade e replicacao apenas dos dados compartilhados de catalogo. | ADR-0004, ADR-0005 |

## Requisitos que apertam do caso Onibus

| Requisito | Decisao que atende | Referencias |
|---|---|---|
| Validador responde em ate 300 ms mesmo sem conexao. | Validador embarcado com armazenamento local, lista de bloqueio assinada, contador monotonicamente crescente por cartao e regras em microkernel local. | ADR-0001, ADR-0002; C4 Componentes |
| Nunca aceitar a mesma passagem duas vezes. | O validador impede repeticao local pelo contador do cartao; a conciliacao detecta uso duplicado entre onibus pelo par `cartao_pseudonimo + contador`. | ADR-0002, ADR-0005 |
| Saldo consistente; fraude de recarga zero. | Servico de Cartoes e Recargas e dono do saldo central; recargas confirmadas viram eventos assinados; validadores aplicam creditos pendentes apenas com recibo verificavel. | ADR-0002, ADR-0003 |
| Telemetria deve absorver media de 80 posicoes/s e pico 5x sem perder dados. | Ingestao de telemetria entra direto em broker por fluxo, isolada do banco transacional; consumidores escalam de forma independente. | ADR-0001, ADR-0004; C4 Conteineres |
| Informacao ao passageiro tolera atraso de segundos e tem pico no rush. | Projecoes de leitura e cache sao atualizados por eventos de telemetria; consultas nao batem no fluxo transacional. | ADR-0001, ADR-0004 |
| Fechamento mensal por operadora, auditado, com contestacao em ate 30 dias. | Fechamentos sao versoes de projecao derivadas do log de eventos; contestacoes geram eventos de ajuste, sem editar o passado. | ADR-0002, ADR-0005 |
| Recalcular o mes inteiro com regras vigentes na data de cada viagem. | Regras tarifarias sao eventos versionados com periodo de vigencia; replay escolhe a regra valida para cada evento de viagem. | ADR-0002 |
| Formatos impostos por terceiros e janelas de indisponibilidade. | Integracoes por ports and adapters, filas de saida e jobs de reentrega idempotente para banco/adquirente/operadoras. | ADR-0003 |
| Historico de viagens identificado e dado pessoal sob LGPD. | Dados pessoais ficam no cadastro da cidade; fatos financeiros usam pseudonimos e politica de minimizacao por tenant, sem misturar bases entre cidades. | ADR-0002, ADR-0005 |
| Atendimento precisa de trilha de quem alterou o que. | Alteracoes administrativas geram eventos de auditoria com usuario, papel, motivo e correlacao com solicitacao. | ADR-0004 |
