using NetTopologySuite.Geometries;

namespace AgroIntelligence.Api.Models
{
    public class Lote
    {
        public Guid Id { get; set; }
        public Guid? CampoId { get; set; }
        public string Nombre { get; set; } = string.Empty;
        public decimal? Hectareas { get; set; }
        public string? CultivoActual { get; set; }
        public string? Descripcion { get; set; }
        public Polygon? Geometria { get; set; }
    }
}
