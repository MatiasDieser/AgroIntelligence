using AgroIntelligence.Api.Data;
using AgroIntelligence.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace AgroIntelligence.Api.Endpoints;

public static class LotesEndpoints
{
    public record LoteDto(Guid? CampoId, string Nombre, decimal? Hectareas,
                           string? CultivoActual, string? Descripcion, string? GeometriaWkt);

    public record LoteRespuestaDto(Guid Id, Guid? CampoId, string Nombre, decimal? Hectareas,
                                    string? CultivoActual, string? Descripcion, string? GeometriaWkt);

    private static LoteRespuestaDto AResp(Lote l) => new(
        l.Id, l.CampoId, l.Nombre, l.Hectareas, l.CultivoActual, l.Descripcion,
        l.Geometria?.AsText()
    );

    public static void MapLotesEndpoints(this WebApplication app)
    {
        var grupo = app.MapGroup("/lotes");

        grupo.MapGet("/", async (AppDbContext db) =>
            (await db.Lotes.OrderBy(l => l.Nombre).ToListAsync())
                .Select(AResp));

        grupo.MapGet("/{id:guid}", async (Guid id, AppDbContext db) =>
            await db.Lotes.FindAsync(id) is Lote lote
                ? Results.Ok(AResp(lote))
                : Results.NotFound());

        grupo.MapGet("/por-campo/{campoId:guid}", async (Guid campoId, AppDbContext db) =>
            (await db.Lotes.Where(l => l.CampoId == campoId).OrderBy(l => l.Nombre).ToListAsync())
                .Select(AResp));

        grupo.MapPost("/", async (LoteDto dto, AppDbContext db) =>
        {
            if (string.IsNullOrWhiteSpace(dto.Nombre))
                return Results.BadRequest("El nombre es obligatorio.");

            NetTopologySuite.Geometries.Polygon? geometria;
            try
            {
                geometria = GeometriaHelper.ParsearPoligono(dto.GeometriaWkt);
            }
            catch (ArgumentException ex)
            {
                return Results.BadRequest(ex.Message);
            }

            var lote = new Lote
            {
                Id = Guid.NewGuid(),
                CampoId = dto.CampoId,
                Nombre = dto.Nombre,
                Hectareas = dto.Hectareas,
                CultivoActual = dto.CultivoActual,
                Descripcion = dto.Descripcion,
                Geometria = geometria
            };

            db.Lotes.Add(lote);
            await db.SaveChangesAsync();
            return Results.Created($"/lotes/{lote.Id}", AResp(lote));
        });

        grupo.MapPut("/{id:guid}", async (Guid id, LoteDto dto, AppDbContext db) =>
        {
            var lote = await db.Lotes.FindAsync(id);
            if (lote is null) return Results.NotFound();

            NetTopologySuite.Geometries.Polygon? geometria;
            try
            {
                geometria = GeometriaHelper.ParsearPoligono(dto.GeometriaWkt);
            }
            catch (ArgumentException ex)
            {
                return Results.BadRequest(ex.Message);
            }

            lote.CampoId = dto.CampoId;
            lote.Nombre = dto.Nombre;
            lote.Hectareas = dto.Hectareas;
            lote.CultivoActual = dto.CultivoActual;
            lote.Descripcion = dto.Descripcion;
            if (!string.IsNullOrWhiteSpace(dto.GeometriaWkt))
                lote.Geometria = geometria;

            await db.SaveChangesAsync();
            return Results.Ok(AResp(lote));
        });

        grupo.MapDelete("/{id:guid}", async (Guid id, AppDbContext db) =>
        {
            var lote = await db.Lotes.FindAsync(id);
            if (lote is null) return Results.NotFound();

            db.Lotes.Remove(lote);
            try
            {
                await db.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                return Results.Conflict("No se puede eliminar: el lote tiene vuelos asociados.");
            }
            return Results.NoContent();
        });
    }
}
