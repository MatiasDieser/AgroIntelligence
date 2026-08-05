using AgroIntelligence.Api.Data;
using Microsoft.EntityFrameworkCore;

namespace AgroIntelligence.Api.Endpoints;

public static class InformesEndpoints
{
    public record RevisionDto(string RevisadoPor, string? Estado);

    public static void MapInformesEndpoints(this WebApplication app)
    {
        app.MapGet("/informes/{link}", async (string link, AppDbContext db) =>
        {
            var informe = await db.Informes.FirstOrDefaultAsync(i => i.LinkUnico == link);

            if (informe is null || informe.PdfPath is null || !File.Exists(informe.PdfPath))
                return Results.NotFound("Informe no encontrado.");

            var bytes = await File.ReadAllBytesAsync(informe.PdfPath);
            return Results.File(bytes, "application/pdf", "informe.pdf");
        });

        // Endpoint para que el fran (o nosotros, por ahora) marque
        // un informe como revisado.
        app.MapPatch("/informes/{id:guid}/revision", async (Guid id, RevisionDto dto, AppDbContext db) =>
        {
            if (string.IsNullOrWhiteSpace(dto.RevisadoPor))
                return Results.BadRequest("RevisadoPor es obligatorio.");

            var informe = await db.Informes.FindAsync(id);
            if (informe is null) return Results.NotFound();

            informe.RevisadoPor = dto.RevisadoPor;
            informe.Estado = string.IsNullOrWhiteSpace(dto.Estado) ? "revisado" : dto.Estado;
            informe.FechaRevision = DateTime.UtcNow;

            await db.SaveChangesAsync();
            return Results.Ok(informe);
        });
    }
}
