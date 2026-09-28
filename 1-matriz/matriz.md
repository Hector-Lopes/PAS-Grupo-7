# Matriz de estilos aplicada

Matriz resumida a partir da Entrega 1 para o Caso Onibus. As citacoes seguem a numeracao de secoes usada no material de apoio da disciplina.

| Estilo | Serve? | Subdominio | Justificativa | Melhora / Piora |
|---|---|---|---|---|
| Monolito em camadas | Nao | Nenhum | Inviavel para o sistema como um todo, pois acopla implantacao e nao isola validacao offline, telemetria e recarga. A Secao 5.6 alerta para evitar este estilo quando ha cargas heterogeneas e necessidade de autonomia. | Melhora custo operacional; piora escalabilidade e disponibilidade. |
| Monolito modular | Em parte | Atendimento; cartoes e recarga inicial | Serve onde ha transacao centralizada e baixa escala relativa. A Secao 6.5 recomenda quando a consistencia local e a simplicidade operacional importam. | Melhora testabilidade e modificabilidade; piora escala seletiva. |
| Hexagonal / Ports and Adapters | Sim | Validador embarcado; integracoes externas | Isola regra de negocio de leitores, rede, persistencia e APIs externas. A Secao 7.5 sustenta seu uso em ambientes com infraestrutura instavel e contratos externos. | Melhora testabilidade e modificabilidade; piora custo de desenvolvimento. |
| Microkernel | Sim | Validador embarcado | Regras de tarifa, desconto e gratuidade variam mais que o nucleo de validacao. A Secao 8.5 indica o estilo para nucleo estavel com extensoes trocaveis. | Melhora modificabilidade; piora testabilidade de contratos. |
| Microsservicos | Em parte | Cartoes, recarga e informacao ao passageiro | Ajuda a escalar e implantar subdominios com cargas distintas. A Secao 9.5 recomenda quando ha requisitos heterogeneos. | Melhora escalabilidade e implantabilidade; piora custo operacional e consistencia. |
| SOA / ESB | Nao | Nenhum | Um barramento central criaria gargalo e ponto unico de falha. A Secao 10.6 orienta evitar quando baixa latencia e desacoplamento temporal sao criticos. | Melhora governanca; piora desempenho e disponibilidade. |
| Orientada a eventos | Sim | Telemetria; sincronizacao de validacoes | Desacopla produtores e consumidores no tempo e absorve picos. A Secao 11.5 recomenda para alto volume continuo. | Melhora escalabilidade e disponibilidade; piora diagnostico. |
| Serverless | Em parte | Informacao ao passageiro | Pode absorver pico de consulta pagando por uso. A Secao 12.5 favorece cargas intermitentes ativadas por eventos. | Melhora custo em ociosidade e escala; piora latencia de cold start. |
| Arquitetura celular | Nao | Nenhum nesta combinacao | A divisao por celulas adiciona custo desproporcional e dificulta agregacao global de repasse. A Secao 13.6 recomenda evitar quando ha forte consolidacao global. | Melhora contencao de falha; piora custo e complexidade de dados. |
| CQRS | Sim | Cartoes, recarga, repasse e consultas | Separa escrita transacional de leituras/projecoes. A Secao 14.5 indica quando consultas e relatorios tem necessidades diferentes da escrita. | Melhora leitura e escala; piora consistencia percebida. |
| Event Sourcing | Sim | Repasse, conciliacao e historico financeiro | Eventos imutaveis permitem auditoria e replay. A Secao 15.5 indica quando o historico exato e requisito legal/financeiro. | Melhora rastreabilidade; piora armazenamento e evolucao de esquema. |
| Pipes and Filters | Sim | Telemetria e conciliacao em lote | Etapas independentes validam, enriquecem, agregam e projetam dados. A Secao 16.5 recomenda para processamento sequencial de fluxos e lotes. | Melhora reuso e modificabilidade; piora latencia por overhead. |
