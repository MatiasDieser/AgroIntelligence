using NetTopologySuite.Geometries;

namespace AgroIntelligence.Api.Models
{
    public class Campo
    {
        public Guid Id { get; set; }
        public Guid? ClienteId { get; set; }
        public string Nombre { get; set; } = string.Empty;
        public string? Descripcion { get; set; }
        public decimal? Hectareas { get; set; }
        public string? Ubicacion { get; set; }
        public Polygon? Geometria { get; set; }
        public DateTime FechaAlta { get; set; }
    }
}
