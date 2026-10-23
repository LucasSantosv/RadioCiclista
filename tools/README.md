# Fontes dos esquemas

Os scripts usam Python e Pillow para gerar PNG e SVG a partir das mesmas primitivas. Não usam geração de imagem por IA.

Instale Pillow e execute `python desenhar_esquema_expandido.py` nesta pasta. Os dois scripts devem permanecer juntos. A fonte padrão é Arial no Windows; em outro sistema, ajuste `font_path` no script base.

Os arquivos resultantes são gravados na pasta dos scripts; após revisão elétrica e visual, copie SVG/PNG para `hardware/esquemas/`. O script base também contém o desenho anterior em blocos. O esquema expandido é o principal publicado.
