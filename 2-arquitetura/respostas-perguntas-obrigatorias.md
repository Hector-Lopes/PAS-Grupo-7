# Respostas as perguntas obrigatorias

## 1. Como o validador aceita a passagem sem rede e como o sistema descobre depois uso em dois onibus?

O validador embarcado e um componente local com arquitetura hexagonal e microkernel de regras. Ele mantem lista de bloqueio assinada, tabela local de transacoes pendentes, ultimo contador visto por cartao e pacote de regras tarifarias versionado. A validacao nao depende da rede: em ate 300 ms, o validador verifica assinatura do cartao, saldo/beneficio disponivel, bloqueios locais e contador de uso.

Quando a rede volta, o sincronizador publica os eventos `PassagemValidada` no broker. A conciliacao central compara `cartao_pseudonimo + contador_transacao`; se o mesmo par aparecer em dois onibus, gera `UsoDuplicadoDetectado`, bloqueia o cartao para a proxima lista e cria ajuste financeiro. Sustentacao: ADR-0001, ADR-0002, ADR-0005 e C4 Componentes.

## 2. Como o saldo fica consistente entre recarga no aplicativo e uso no onibus com atraso de sincronizacao?

O servico de Cartoes e Recargas e o dono do saldo central e so confirma recarga depois da confirmacao do adquirente/banco. A recarga confirmada gera um recibo assinado e um evento `RecargaConfirmada`. Validadores conectados recebem a atualizacao; validadores offline aceitam apenas o saldo e os creditos assinados ja presentes no cartao ou em carga local previamente sincronizada.

Se uma recarga ainda nao chegou ao onibus, ela nao e presumida. Ao sincronizar, o sistema aplica eventos idempotentes, reconcilia validacoes offline e ajusta a projecao de saldo. Sustentacao: ADR-0002, ADR-0003 e C4 Conteineres.

## 3. Como a telemetria escala no pico sem derrubar o restante do sistema?

A telemetria nao passa pelo banco transacional nem pelo caminho de validacao/recarga. Os validadores e modulos de GPS publicam posicoes em um topico de fluxo no broker. Consumidores independentes validam, enriquecem, agregam e atualizam cache de informacao ao passageiro.

Se houver pico de 400 posicoes/s, o broker acumula atraso apenas nesse fluxo. A pior degradacao esperada e previsao de chegada alguns segundos mais velha; validacao e recarga continuam isoladas. Sustentacao: ADR-0001, ADR-0004 e C4 Conteineres.

## 4. Como o repasse mensal e recalculado se uma regra de tarifa mudou no meio do mes?

O repasse e calculado por replay do log de eventos. Cada viagem tem data, linha, operadora, validador e regra aplicada; cada regra tarifaria tambem e versionada com vigencia. Para recalcular, o sistema cria uma nova projecao de fechamento, percorre os eventos do periodo e escolhe a regra vigente no instante da viagem.

O fechamento anterior nao e apagado. Ele fica como versao auditavel, e a diferenca aparece como evento de ajuste. Sustentacao: ADR-0002, ADR-0005 e C4 Conteineres.

## 5. Como o historico de viagens de uma pessoa e apagado sem quebrar a conciliacao financeira?

O fato contabil da viagem nao e apagado, porque ele sustenta repasse e auditoria. O que e removido e a possibilidade de identificar a pessoa. Eventos imutaveis guardam dados pessoais cifrados com chave individual do titular e um pseudonimo tecnico sem reversao direta. Quando ha pedido valido de exclusao, a chave individual e destruida e o cadastro identificavel e removido das bases operacionais.

Depois disso, a auditoria ainda consegue somar viagens por linha, horario e operadora, mas nao consegue recuperar quem era o passageiro. Sustentacao: ADR-0002, ADR-0005 e spike em `3-spike/`.
