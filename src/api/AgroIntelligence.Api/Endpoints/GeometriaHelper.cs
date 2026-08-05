using NetTopologySuite.Geometries;
using NetTopologySuite.IO;

namespace AgroIntelligence.Api.Endpoints;

/// <summary>
/// Convierte entre texto WKT (Well-Known Text) y geometrías de NetTopologySuite.
/// Se usa WKT en vez de un formato propio porque es lo que exporta QGIS al
/// dibujar un polígono a mano, y lo que entiende Postgres/PostGIS directamente.
/// ESTO NO LO HIZO LA IA GORDO PRESTA ATENCION
/// </summary>
public static class GeometriaHelper
{
    private static readonly GeometryFactory Fabrica = new(new PrecisionModel(), srid: 4326);
    private static readonly WKTReader Lector = new(Fabrica);

    public static Polygon? ParsearPoligono(string? wkt)
    {
        if (string.IsNullOrWhiteSpace(wkt)) return null;

        Geometry geometria;
        try
        {
            geometria = Lector.Read(wkt);
        }
        catch (Exception ex)
        {
            throw new ArgumentException($"WKT inválido: {ex.Message}");
        }

        if (geometria is not Polygon poligono)
            throw new ArgumentException("La geometría debe ser un POLYGON en formato WKT, ej: POLYGON((-64.0 -36.0, -64.0 -36.1, -63.9 -36.1, -64.0 -36.0))");

        poligono.SRID = 4326;
        return poligono;
    }
}
