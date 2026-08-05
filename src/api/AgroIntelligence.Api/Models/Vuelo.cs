namespace AgroIntelligence.Api.Models
{
    public class Vuelo
    {
        public Guid Id { get; set; }
        public Guid? CampoId { get; set; }
        public Guid? LoteId { get; set; }
        public string Tipo { get; set; } = string.Empty;
        public DateTime Fecha { get; set; }
        public string Estado { get; set; } = "pendiente";
        public string? CarpetaPath { get; set; }
        public decimal? AlturaVueloMetros { get; set; }
        public string? CondicionesClimaticas { get; set; }
        public string? Notas { get; set; }
        public DateTime FechaCreacion { get; set; }
    }
}
