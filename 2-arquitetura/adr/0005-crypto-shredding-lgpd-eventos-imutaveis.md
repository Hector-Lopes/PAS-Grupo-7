# ADR-0005 - Crypto-shredding para LGPD em eventos imutaveis

## Status

Aceita.

## Contexto

O repasse financeiro precisa manter fatos historicos reconstruiveis. Ao mesmo tempo, o historico de viagens identificado e dado pessoal e o envelope E exige compatibilizar auditoria completa com direito ao esquecimento.

## Decisao

Eventos financeiros permanecem imutaveis, mas nao guardam dados pessoais em claro. Quando um evento precisa referenciar uma pessoa, o identificador pessoal e cifrado com chave individual do titular. O evento tambem contem um pseudonimo tecnico sem reversao direta para permitir idempotencia, deteccao de duplicidade e agregacoes sem expor a identidade.

Quando ha pedido valido de exclusao, o sistema:

1. remove ou minimiza dados do cadastro operacional;
2. destroi a chave individual do titular no cofre de chaves;
3. registra evento de auditoria `ChaveDestruida`;
4. mantem os fatos contabeis anonimizados para repasse e fiscalizacao.

Esta e a decisao mais arriscada e sera provada no spike em `3-spike/`.

## Alternativas consideradas

- Apagar fisicamente todos os eventos da pessoa: descartado porque quebraria conciliacao, contestacao e replay.
- Manter dados pessoais em claro com controle de acesso: descartado porque nao atende direito ao esquecimento quando a retencao identificada deixa de ser necessaria.
- Substituir identificadores por hash simples: descartado porque pode permitir ataque por dicionario quando o universo de cartoes for conhecido.

## Consequencias positivas

- Auditoria financeira continua reconstruivel.
- O dado pessoal deixa de ser recuperavel apos destruicao da chave.
- O mecanismo e demonstravel com codigo pequeno e deterministico.

## Consequencias negativas

- Perder a chave antes da hora impede atendimento identificado e investigacao nominal.
- E preciso processo formal para validar pedidos de exclusao.
- O modelo exige cofre de chaves, trilha de acesso e rotacao planejada.
