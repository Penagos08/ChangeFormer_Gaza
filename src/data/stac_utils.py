"""Utilidades STAC para el Microsoft Planetary Computer.

Centraliza la busqueda de imagenes Sentinel y su carga como DataArray
georreferenciado, de modo que los scripts de descarga compartan la misma logica.
Las dependencias pesadas se importan dentro de las funciones para que el paquete
pueda importarse sin tener el stack completo instalado.
"""

from __future__ import annotations

from typing import Any, Iterable

STAC_ENDPOINT = "https://planetarycomputer.microsoft.com/api/stac/v1"


def get_catalog():
    """Abre el catalogo STAC del Planetary Computer con firma automatica de activos."""
    import planetary_computer
    import pystac_client

    return pystac_client.Client.open(
        STAC_ENDPOINT,
        modifier=planetary_computer.sign_inplace,
    )


def search_items(
    collection: str,
    bbox: list[float],
    datetime_range: str,
    query: dict[str, Any] | None = None,
) -> list:
    """Busca items en una coleccion y devuelve la lista de resultados.

    Parametros
    ----------
    collection: id de la coleccion STAC (p. ej. "sentinel-2-l2a").
    bbox: [min_lon, min_lat, max_lon, max_lat] en WGS84.
    datetime_range: intervalo ISO, p. ej. "2023-05-01/2023-06-15".
    query: filtros adicionales tipo {"eo:cloud_cover": {"lt": 15}}.
    """
    catalog = get_catalog()
    search = catalog.search(
        collections=[collection],
        bbox=bbox,
        datetime=datetime_range,
        query=query or {},
    )
    return list(search.items())


def sort_by_cloud(items: Iterable) -> list:
    """Ordena items Sentinel-2 por cobertura nubosa ascendente."""

    def cloud(item) -> float:
        return float(item.properties.get("eo:cloud_cover", 100.0))

    return sorted(items, key=cloud)


def load_stack(
    items: list,
    assets: list[str],
    bbox: list[float],
    epsg: int,
    resolution: float | None = None,
    aggregate: str = "median",
):
    """Carga los items como un DataArray (band, y, x) recortado al AOI.

    Usa stackstac para construir el cubo, lo agrega en el tiempo (median por
    defecto) y devuelve un arreglo con la proyeccion y la transformada listas
    para exportar con rioxarray.
    """
    import stackstac

    kwargs: dict[str, Any] = {
        "assets": assets,
        "epsg": epsg,
        "bounds_latlon": list(bbox),
        "dtype": "float32",
        "rescale": True,
    }
    if resolution is not None:
        kwargs["resolution"] = resolution

    cube = stackstac.stack(items, **kwargs)
    if aggregate == "median":
        mosaic = cube.median(dim="time", skipna=True)
    elif aggregate == "first":
        mosaic = cube.isel(time=0)
    else:
        raise ValueError(f"Agregacion no soportada: {aggregate}")

    # Renombramos la dimension de bandas a 'band' y aseguramos orden consistente.
    if "band" not in mosaic.dims:
        mosaic = mosaic.rename({"bands": "band"})
    return mosaic


def write_raster(array, out_path, dtype: str = "float32") -> str:
    """Escribe un DataArray georreferenciado como GeoTIFF."""
    from pathlib import Path

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    array.rio.to_raster(out_path, dtype=dtype)
    return str(out_path)
