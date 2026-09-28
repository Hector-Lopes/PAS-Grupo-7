# Spike - crypto-shredding em eventos financeiros imutaveis

Este spike prova o ADR-0005: o sistema consegue manter eventos financeiros imutaveis e auditaveis, mas tornar dados pessoais irrecuperaveis quando uma exclusao LGPD valida for executada.

O programa simula um `EventStore` append-only com hash encadeado, um cofre de chaves por passageiro e eventos de passagem validada. Os eventos guardam o fato contabil necessario para repasse: operadora, linha, valor, contador de transacao e pseudonimo tecnico do cartao. O identificador pessoal do passageiro fica cifrado com uma chave individual.

Para rodar:

```bash
python3 exemplo.py
```

No Windows, se `python3` nao estiver registrado, use:

```bash
python exemplo.py
```

O resultado esperado esta em `saida-esperada.txt`.

O que a prova demonstra:

- antes da exclusao, o sistema consegue decifrar os eventos do passageiro `P-100`;
- apos destruir a chave de `P-100`, os mesmos eventos continuam no log, mas a identidade nao pode ser recuperada;
- o fechamento por operadora continua igual antes e depois da exclusao;
- a cadeia de hashes continua valida, mostrando que os eventos financeiros nao foram alterados;
- uma duplicidade offline continua detectavel pelo par `cartao_pseudonimo + contador_transacao`.

Se a decisao estivesse errada, destruir a chave quebraria o calculo financeiro, ou entao os dados pessoais continuariam legiveis mesmo apos o pedido de esquecimento. Qualquer um dos dois resultados violaria o envelope E: ou a auditoria perderia reconstruibilidade, ou a LGPD nao seria atendida.
