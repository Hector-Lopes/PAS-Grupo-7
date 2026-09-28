# Mapa de restricoes e decisoes

## Restricoes do envelope E

| Restricao | Decisao que atende | Referencias |
|---|---|---|
| Operacao sob fiscalizacao do tribunal de contas sobre repasse financeiro. | Eventos financeiros append-only para validacoes, recargas, ajustes e regras tarifarias; cada fechamento mensal e uma projecao reconstruivel a partir do log. | ADR-0001, ADR-0002, ADR-0005; C4 Conteineres |
| Nuvem publica com exigencia de trilha de auditoria completa. | Todos os servicos publicam eventos de dominio e eventos de auditoria em topicos imutaveis; observabilidade centralizada coleta logs, metricas e rastros. | ADR-0004; C4 Conteineres |
| Tudo que acontece precisa ser reconstruivel. | Event Sourcing no repasse/conciliação e registros assinados nos validadores; regras tarifarias sao versionadas por vigencia. | ADR-0002, ADR-0005 |
| LGPD com direito ao esquecimento. | Dados pessoais sao separados dos fatos contabeis; eventos guardam identificador cifrado e pseudonimo tecnico, com destruicao de chave individual quando houver pedido valido. | ADR-0002, ADR-0005 |
| Equipe de 15 desenvolvedores e 1 responsavel por conformidade. | Fronteiras por subdominio com poucos servicos centrais e contratos de evento padronizados; evitar malha excessiva de microsservicos. | ADR-0001, ADR-0004 |

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
| Historico de viagens identificado e dado pessoal sob LGPD. | Separar identidade do passageiro do fato de viagem; criptografia por titular e destruicao de chave para anonimizar eventos antigos. | ADR-0005 |
| Atendimento precisa de trilha de quem alterou o que. | Alteracoes administrativas geram eventos de auditoria com usuario, papel, motivo e correlacao com solicitacao. | ADR-0004 |
