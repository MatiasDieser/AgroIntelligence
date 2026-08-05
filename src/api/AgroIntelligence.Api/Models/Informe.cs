namespace AgroIntelligence.Api.Models
{
    public class Informe
    {
        public Guid Id { get; set; }
        public Guid VueloId { get; set; }
        public string? PdfPath { get; set; }
        public string? LinkUnico { get; set; }
        public string? Estado { get; set; }
        public string? RevisadoPor { get; set; }
        public DateTime? FechaRevision { get; set; }
        public DateTime FechaGeneracion { get; set; }
    }
}
