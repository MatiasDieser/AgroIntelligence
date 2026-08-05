namespace AgroIntelligence.Api.Models
{
    public class Cliente
    {
        public Guid Id { get; set; }
        public string Nombre { get; set; } = string.Empty;
        public string? Telefono { get; set; }
        public string? Email { get; set; }
        public string? Notas { get; set; }
        public DateTime FechaAlta { get; set; }
    }
}
