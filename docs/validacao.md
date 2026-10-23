# Registro de validação

Data: **23/10/2026**, conforme a conversa do projeto no fuso America/Sao_Paulo.

| Etapa | Evidência | Limite |
|---|---|---|
| Compilação inicial da V1.2 | 1.156.124 bytes de programa e 43.928 bytes globais | Anterior à rotação 1 → 3; não equivale a teste físico |
| Compilação do autor | Log enviado: 1.156.300 bytes; posteriormente 36% com Huge APP | Ferramenta identificou um S2 numa tentativa; autor informou ter encontrado o erro. Causa exata não registrada |
| Orientação da tela | `setRotation(1)` alterado para `setRotation(3)` | Sem recompilação pelo assistente após pedido para não compilar |
| Teste físico da base Bluetooth | Autor: “otimo, esta funcionando com qualidade” | Confirmação geral; sem medições de SNR, THD, potência ou duração |
| SI4732-A10 | CI e cristal informados pelo autor; esquema preparado | Sem confirmação de recepção nem comunicação I²C |

SHA-256 do programa de referência publicado:

```text
4774dee7e8b5102b13a6cb9654b3ebbf3260586d2d30517edd9c08d121027c2d
```

Nome local anterior: RADIO_ESP32_PCM5102A.ino. Nome no repositório: RadioCiclista.ino, dentro de pasta homônima. Conteúdo idêntico à cópia preservada antes de iniciar o SI4732.

Nenhum resultado de compilação, bancada ou recepção deve ser inferido para funções planejadas.
