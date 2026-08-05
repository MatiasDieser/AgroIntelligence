using AgroIntelligence.Api.Data;
using AgroIntelligence.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace AgroIntelligence.Api.Endpoints;

public static class CamposEndpoints
{
    // GeometriaWkt es opcional y viaja como texto plano (WKT), no como objeto
    // geométrico -- se pega ahí lo que exporta QGIS cuando dibuja el polígono.
    public record CampoDto(Guid? ClienteId, string Nombre, string? Descripcion,
                            decimal? Hectareas, string? Ubicacion, string? GeometriaWkt);

    // DTO de salida: la entidad Campo no se serializa directamente porque
    // System.Text.Json no sabe representar un tipo Polygon de NetTopologySuite.
    public record CampoRespuestaDto(Guid Id, Guid? ClienteId, string Nombre, string? Descripcion,
                                     decimal? Hectareas, string? Ubicacion, string? GeometriaWkt,
                                     DateTime FechaAlta);

    private static CampoRespuestaDto AResp(Campo c) => new(
        c.Id, c.ClienteId, c.Nombre, c.Descripcion, c.Hectareas, c.Ubicacion,
        c.Geometria?.AsText(), c.FechaAlta
    );

    public static void MapCamposEndpoints(this WebApplication app)
    {
        var grupo = app.MapGroup("/campos");

        grupo.MapGet("/", async (AppDbContext db) =>
            (await db.Campos.OrderBy(c => c.Nombre).ToListAsync())
                .Select(AResp));

        grupo.MapGet("/{id:guid}", async (Guid id, AppDbContext db) =>
            await db.Campos.FindAsync(id) is Campo campo
                ? Results.Ok(AResp(campo))
                : Results.NotFound());

        grupo.MapPost("/", async (CampoDto dto, AppDbContext db) =>
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

            var campo = new Campo
            {
                Id = Guid.NewGuid(),
                ClienteId = dto.ClienteId,
                Nombre = dto.Nombre,
                Descripcion = dto.Descripcion,
                Hectareas = dto.Hectareas,
                Ubicacion = dto.Ubicacion,
                Geometria = geometria,
                FechaAlta = DateTime.UtcNow
            };

            db.Campos.Add(campo);
            await db.SaveChangesAsync();
            return Results.Created($"/campos/{campo.Id}", AResp(campo));
        });

        grupo.MapPut("/{id:guid}", async (Guid id, CampoDto dto, AppDbContext db) =>
        {
            var campo = await db.Campos.FindAsync(id);
            if (campo is null) return Results.NotFound();

            NetTopologySuite.Geometries.Polygon? geometria;
            try
            {
                geometria = GeometriaHelper.ParsearPoligono(dto.GeometriaWkt);
            }
            catch (ArgumentException ex)
            {
                return Results.BadRequest(ex.Message);
            }

            campo.ClienteId = dto.ClienteId;
            campo.Nombre = dto.Nombre;
            campo.Descripcion = dto.Descripcion;
            campo.Hectareas = dto.Hectareas;
            campo.Ubicacion = dto.Ubicacion;
            // Si no mandan GeometriaWkt en el update, se conserva la que ya había
            // (no se pisa con null solo porque el campo vino vacío).
            if (!string.IsNullOrWhiteSpace(dto.GeometriaWkt))
                campo.Geometria = geometria;

            await db.SaveChangesAsync();
            return Results.Ok(AResp(campo));
        });

        grupo.MapDelete("/{id:guid}", async (Guid id, AppDbContext db) =>
        {
            var campo = await db.Campos.FindAsync(id);
            if (campo is null) return Results.NotFound();

            db.Campos.Remove(campo);
            try
            {
                await db.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                return Results.Conflict("No se puede eliminar: el campo tiene lotes o vuelos asociados.");
            }
            return Results.NoContent();
        });
    }
}
