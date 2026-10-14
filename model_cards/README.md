# Fichas de modelos (model cards)

Este directorio reune las fichas de descripcion de los modelos del proyecto
**ChangeFormer_Gaza**. Cada ficha sigue la estructura recomendada en Mitchell et al.
(2019) y la plantilla de model card de Hugging Face.

Referencia metodologica: Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L.,
Hutchinson, B., Spitzer, E., Raji, I. D. y Gebru, T. (2019). *Model cards for model
reporting*. En Proceedings of the Conference on Fairness, Accountability, and
Transparency (pp. 220-229). https://arxiv.org/abs/1810.03993

---

## ChangeFormerV6

ChangeFormerV6 es una red siamesa basada en transformers para deteccion de cambios
binaria en pares de imagenes bitemporales. Combina un codificador jerarquico tipo
transformer (encoder MiT) con un decodificador tambien transformer, y es el modelo base
que usa el proyecto, con pesos preentrenados en LEVIR-CD.

- **Ficha completa:** [changeformer_v6.md](./changeformer_v6.md)
- **Autor de la ficha:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas
  (GitHub: [Penagos08](https://github.com/Penagos08)).

---

## ChangeFormer_Gaza

ChangeFormer_Gaza es la version ajustada de ChangeFormerV6 para detectar cambio asociado
a edificios destruidos en la Franja de Gaza. Parte de los pesos de LEVIR-CD y se
especializa con el dataset xBD (xView2) de dano a edificios, agrupando las clases de dano
menor, mayor y destruido en una sola clase de cambio.

- **Ficha completa:** [changeformer_gaza.md](./changeformer_gaza.md)
- **Autor de la ficha:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas
  (GitHub: [Penagos08](https://github.com/Penagos08)).

---

Las fichas de los conjuntos de datos estan en [`../dataset_cards/README.md`](../dataset_cards/README.md).
