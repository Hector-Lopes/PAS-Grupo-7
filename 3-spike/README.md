# Spike - isolamento multi-tenant por cidade

Este spike prova o ADR-0005: uma cidade em pico ou com falha nao deve derrubar as outras cidades no mesmo produto.

O programa simula tres cidades atendidas pela mesma plataforma. Cada cidade possui uma celula logica com fila, limite de processamento por rodada, dead-letter queue, deteccao de duplicidade e projecao de repasse por operadora. O roteador publica cada evento pela chave `tenant_id`, impedindo que eventos de uma cidade entrem na fila de outra.

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

- Campinas recebe mais eventos do que consegue processar em tres rodadas, simulando pico sazonal em cidade grande;
- Valinhos recebe uma falha de integracao externa, que vai para dead-letter queue da propria cidade;
- Sumare continua processando suas passagens mesmo com backlog em Campinas e falha em Valinhos;
- a duplicidade offline de Campinas continua detectavel dentro da propria celula;
- totais por operadora sao projetados separadamente por cidade.

Se a decisao estivesse errada, haveria uma fila compartilhada ou consumidor global: o pico de Campinas atrasaria Valinhos e Sumare, ou a falha de Valinhos pararia o processamento das demais cidades. Isso violaria diretamente o envelope D, cuja exigencia dominante e isolamento entre clientes e escala apenas onde precisa.
