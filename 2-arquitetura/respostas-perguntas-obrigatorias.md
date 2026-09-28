# Respostas as perguntas obrigatorias

## 1. Como o validador aceita a passagem sem rede e como o sistema descobre depois uso em dois onibus?

O validador embarcado e um componente local com arquitetura hexagonal e microkernel de regras. Ele mantem lista de bloqueio assinada da sua cidade, tabela local de transacoes pendentes, ultimo contador visto por cartao e pacote de regras tarifarias versionado. A validacao nao depende da rede: em ate 300 ms, o validador verifica assinatura do cartao, saldo/beneficio disponivel, bloqueios locais e contador de uso.

Quando a rede volta, o sincronizador publica os eventos `PassagemValidada` no topico da cidade. A conciliacao da celula compara `cartao_pseudonimo + contador_transacao`; se o mesmo par aparecer em dois onibus, gera `UsoDuplicadoDetectado`, bloqueia o cartao para a proxima lista e cria ajuste financeiro. Sustentacao: ADR-0001, ADR-0002, ADR-0005 e C4 Componentes.

## 2. Como o saldo fica consistente entre recarga no aplicativo e uso no onibus com atraso de sincronizacao?

O servico de Cartoes e Recargas da cidade e o dono do saldo central e so confirma recarga depois da confirmacao do adquirente/banco. A recarga confirmada gera um recibo assinado e um evento `RecargaConfirmada`. Validadores conectados recebem a atualizacao; validadores offline aceitam apenas o saldo e os creditos assinados ja presentes no cartao ou em carga local previamente sincronizada.

Se uma recarga ainda nao chegou ao onibus, ela nao e presumida. Ao sincronizar, o sistema aplica eventos idempotentes, reconcilia validacoes offline e ajusta a projecao de saldo. Sustentacao: ADR-0002, ADR-0003 e C4 Conteineres.

## 3. Como a telemetria escala no pico sem derrubar o restante do sistema?

A telemetria nao passa pelo banco transacional nem pelo caminho de validacao/recarga. Os validadores e modulos de GPS publicam posicoes em um topico de fluxo particionado por cidade. Consumidores independentes validam, enriquecem, agregam e atualizam cache de informacao ao passageiro da propria cidade.

Se uma cidade grande tiver pico de 400 posicoes/s, o broker acumula atraso apenas nessa particao/celula. A pior degradacao esperada e previsao de chegada alguns segundos mais velha naquela cidade; validacao, recarga e outras cidades continuam isoladas. Sustentacao: ADR-0001, ADR-0004, ADR-0005 e C4 Conteineres.

## 4. Como o repasse mensal e recalculado se uma regra de tarifa mudou no meio do mes?

O repasse e calculado por replay do log de eventos da cidade. Cada viagem tem data, linha, operadora, validador e regra aplicada; cada regra tarifaria tambem e versionada com vigencia. Para recalcular, o sistema cria uma nova projecao de fechamento para aquela cidade, percorre os eventos do periodo e escolhe a regra vigente no instante da viagem.

O fechamento anterior nao e apagado. Ele fica como versao auditavel, e a diferenca aparece como evento de ajuste. Sustentacao: ADR-0002, ADR-0005 e C4 Conteineres.

## 5. Como o historico de viagens de uma pessoa e apagado sem quebrar a conciliacao financeira?

O fato contabil da viagem nao e apagado, porque ele sustenta repasse e auditoria da cidade. O que e removido e a possibilidade de identificar a pessoa. Eventos imutaveis guardam apenas pseudonimo tecnico e dados pessoais ficam no cadastro da propria cidade, sujeitos a minimizacao, anonimização ou remocao conforme a base legal aplicavel.

Depois disso, a auditoria ainda consegue somar viagens por linha, horario e operadora, mas nao depende de dado pessoal identificavel. Sustentacao: ADR-0002 e ADR-0005.
