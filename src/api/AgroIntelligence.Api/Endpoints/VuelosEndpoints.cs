using AgroIntelligence.Api.Data;
using AgroIntelligence.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace AgroIntelligence.Api.Endpoints;

public static class VuelosEndpoints
{
    public record VueloDto(Guid? CampoId, Guid? LoteId, string Tipo, DateOnly Fecha,
                            string? Estado, string? CarpetaPath, decimal? AlturaVueloMetros,
                            string? CondicionesClimaticas, string? Notas);

    public static void MapVuelosEndpoints(this WebApplication app)
    {
        var grupo = app.MapGroup("/vuelos");

        grupo.MapGet("/", async (AppDbContext db) =>
            await db.Vuelos.OrderByDescending(v => v.Fecha).ToListAsync());

        grupo.MapGet("/{id:guid}", async (Guid id, AppDbContext db) =>
            await db.Vuelos.FindAsync(id) is Vuelo vuelo
                ? Results.Ok(vuelo)
                : Results.NotFound());

        grupo.MapGet("/por-campo/{campoId:guid}", async (Guid campoId, AppDbContext db) =>
            await db.Vuelos.Where(v => v.CampoId == campoId)
                            .OrderByDescending(v => v.Fecha)
                            .ToListAsync());

        grupo.MapPost("/", async (VueloDto dto, AppDbContext db) =>
        {
            if (string.IsNullOrWhiteSpace(dto.Tipo))
                return Results.BadRequest("El tipo de vuelo es obligatorio.");

            var vuelo = new Vuelo
            {
                Id = Guid.NewGuid(),
                CampoId = dto.CampoId,
                LoteId = dto.LoteId,
                Tipo = dto.Tipo,
                Fecha = dto.Fecha.ToDateTime(TimeOnly.MinValue),
                Estado = string.IsNullOrWhiteSpace(dto.Estado) ? "pendiente" : dto.Estado,
                CarpetaPath = dto.CarpetaPath,
                AlturaVueloMetros = dto.AlturaVueloMetros,
                CondicionesClimaticas = dto.CondicionesClimaticas,
                Notas = dto.Notas,
                FechaCreacion = DateTime.UtcNow
            };

            db.Vuelos.Add(vuelo);
            await db.SaveChangesAsync();
            return Results.Created($"/vuelos/{vuelo.Id}", vuelo);
        });

        grupo.MapPut("/{id:guid}", async (Guid id, VueloDto dto, AppDbContext db) =>
        {
            var vuelo = await db.Vuelos.FindAsync(id);
            if (vuelo is null) return Results.NotFound();

            vuelo.CampoId = dto.CampoId;
            vuelo.LoteId = dto.LoteId;
            vuelo.Tipo = dto.Tipo;
            vuelo.Fecha = dto.Fecha.ToDateTime(TimeOnly.MinValue);
            if (!string.IsNullOrWhiteSpace(dto.Estado)) vuelo.Estado = dto.Estado;
            vuelo.CarpetaPath = dto.CarpetaPath;
            vuelo.AlturaVueloMetros = dto.AlturaVueloMetros;
            vuelo.CondicionesClimaticas = dto.CondicionesClimaticas;
            vuelo.Notas = dto.Notas;

            await db.SaveChangesAsync();
            return Results.Ok(vuelo);
        });

        grupo.MapDelete("/{id:guid}", async (Guid id, AppDbContext db) =>
        {
            var vuelo = await db.Vuelos.FindAsync(id);
            if (vuelo is null) return Results.NotFound();

            db.Vuelos.Remove(vuelo);
            try
            {
                await db.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                // El watcher/worker en Python referencia vuelo_id desde trabajos,
                // resultados e informes -- borrar un vuelo con datos procesados
                // rompe esas referencias.
                return Results.Conflict("No se puede eliminar: el vuelo tiene trabajos, resultados o informes asociados.");
            }
            return Results.NoContent();
        });
    }
}
