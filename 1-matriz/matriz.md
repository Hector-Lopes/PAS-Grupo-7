# Entrega 1 — Matriz de Estilos Arquiteturais

## Grupo 07

**Caso:** Ônibus — bilhetagem e mobilidade urbana  
**Envelope:** D — empresa que vende o sistema para várias cidades  
**Contexto:** vários clientes, picos sazonais, nuvem multirregião e necessidade de isolar falhas entre cidades.

# Matriz de Estilos Arquiteturais Aplicada

| Estilo Arquitetural | Serve p/ o caso e envelope? | Subdomínio(s) de Aplicação | Justificativa (com citação do livro) | Atributo que MELHORA / Atributo que PIORA |
|---|---|---|---|---|
| **Monolito em camadas (Cap. 5)** | **Não** | Nenhum | Inviável para o sistema como um todo devido ao acoplamento de implantação e à incapacidade de isolar falhas de rede intermitente. Conforme a **Seção 5.6**, o estilo deve ser evitado quando partes do sistema têm perfis de carga heterogêneos e exigem autonomia de publicação. | **Melhora:** Custo (operacional baixo). **Piora:** Escalabilidade e Disponibilidade. |
