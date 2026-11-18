# Resposta do TRE-PE ao pedido por LAI (protocolo 82034721135306, 13/11/2026), com tarja

O que o TRE de Pernambuco mandou por e-mail em 13/11/2026, inteiro, com tarja preta em todo dado pessoal.

| Arquivo | O que é | Páginas |
|---|---|---|
| `resposta-do-tre-pe_2026-11-13_mascarada.pdf` | a impressão do e-mail com as respostas de cada zona | 13 |
| `Atas_ZE_11_mascarado.pdf` | atas da zona 11 (Jaboatão dos Guararapes), seções 55, 56, 103 e 283 | 11 |
| `Atas_ZE_78_mascarado.pdf` | ata da zona 78 (Parnamirim), seção 23 | 4 |
| `Atas_ZE_85_mascarado.pdf` | ata da zona 85 (Igarassu), seção 314 | 3 |
| `Atas_ZE_125_mascarado.pdf` | ata da zona 125 (Condado), seção 22 | 3 |
| `MANIFESTO.json` | páginas, número de tarjas e sha256 de cada PDF | |

## O que a tarja cobre

- **No e-mail:** o nome e o e-mail do requerente, o endereço do Gmail no rodapé e o nome de cada pessoa citada pelas zonas (fiscais, técnicos, juízes e promotores). O texto foi removido do PDF antes de a página virar imagem, então não há texto por baixo da tarja. O texto inteiro, com `[nome]` no lugar de cada pessoa, está em [`docs/lai/TRE_PE_RESPOSTA_2026-11-13.md`](../../../docs/lai/TRE_PE_RESPOSTA_2026-11-13.md).
- **Nas atas:** nome, assinatura e rubrica dos mesários, dos fiscais e do presidente, número de título, CPF, RG e as iniciais e nomes que a anonimização do cartório deixou. Cada página foi redesenhada como imagem com as caixas de [`../mascaras_atas.json`](../mascaras_atas.json).

Ficaram à vista: o cabeçalho (município, zona, seção, data), os horários, o texto das ocorrências sem nome, a sigla do partido dos fiscais e os quadros em branco. É isso que a [rodada 5](../../../docs/RODADA_5.md) usa.

## Como refazer

Os originais ficam fora do git (trazem os dados pessoais). Com eles numa pasta:

```
python ferramentas/mascarar_resposta_lai.py <pasta dos originais> --previa <pasta das prévias>
```

A prévia sai em PNG, página por página, para conferir a tarja antes de publicar. Qualquer pessoa pode pedir as mesmas atas ao TRE-PE pela Ouvidoria.
