# C4 - Conteineres

```mermaid
flowchart TB
    passageiro["Passageiro"]
    recargaExterna["App/loja/totem"]
    banco["Banco/adquirente"]
    operador["Operadoras"]
    auditoria["Auditoria externa"]

    subgraph onboard["Onibus"]
        validador["Validador embarcado\n(Python/firmware + storage local)"]
    end

    api["API Gateway"]
    tenantRouter["Roteador de Cidade\n(tenant_id)"]
    tenantCatalog["Catalogo de Tenants\n(cidade, regiao, plano)"]
    cartoes["Cartoes e Recargas\npor cidade"]
    tarifas["Catalogo de Tarifas\npor cidade"]
    broker["Broker/Filas da Celula\nparticionado por cidade"]
    eventstore["Event Store financeiro\npor cidade"]
    telemetria["Pipeline de Telemetria\npor cidade"]
    passageiroInfo["Informacao ao Passageiro\ncache/projecoes por cidade"]
    repasse["Repasse e Conciliacao\npor cidade"]
    integracoes["Adaptadores externos\n(ports and adapters)"]
    observabilidade["Observabilidade e Quotas\npor tenant"]

    passageiro -- "chamada" --> api
    recargaExterna -- "chamada" --> api
    api -- "chamada" --> tenantRouter
    tenantRouter -- "chamada" --> tenantCatalog
    tenantRouter -- "chamada" --> cartoes
    tenantRouter -- "chamada" --> passageiroInfo
    cartoes -- "chamada" --> banco
    cartoes -- "evento" --> broker
    tarifas -- "evento" --> broker
    validador -- "evento: sincronizacao de validacoes" --> broker
    validador -- "fluxo: GPS e estado" --> broker
    broker -- "evento" --> eventstore
    broker -- "fluxo" --> telemetria
    broker -- "evento" --> repasse
    telemetria -- "evento" --> passageiroInfo
    repasse -- "arquivo" --> auditoria
    repasse -- "arquivo" --> operador
    integracoes -- "chamada/arquivo" --> banco
    broker -- "evento" --> observabilidade
    observabilidade -- "evento" --> tenantCatalog
```
