using AgroIntelligence.Api.Data;
using AgroIntelligence.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace AgroIntelligence.Api.Endpoints;

public static class ClientesEndpoints
{
    public record ClienteDto(string Nombre, string? Telefono, string? Email, string? Notas);

    public static void MapClientesEndpoints(this WebApplication app)
    {
        var grupo = app.MapGroup("/clientes");

        grupo.MapGet("/", async (AppDbContext db) =>
            await db.Clientes.OrderBy(c => c.Nombre).ToListAsync());

        grupo.MapGet("/{id:guid}", async (Guid id, AppDbContext db) =>
            await db.Clientes.FindAsync(id) is Cliente cliente
                ? Results.Ok(cliente)
                : Results.NotFound());

        grupo.MapPost("/", async (ClienteDto dto, AppDbContext db) =>
        {
            if (string.IsNullOrWhiteSpace(dto.Nombre))
                return Results.BadRequest("El nombre es obligatorio.");

            var cliente = new Cliente
            {
                Id = Guid.NewGuid(),
                Nombre = dto.Nombre,
                Telefono = dto.Telefono,
                Email = dto.Email,
                Notas = dto.Notas,
                FechaAlta = DateTime.UtcNow
            };

            db.Clientes.Add(cliente);
            await db.SaveChangesAsync();
            return Results.Created($"/clientes/{cliente.Id}", cliente);
        });

        grupo.MapPut("/{id:guid}", async (Guid id, ClienteDto dto, AppDbContext db) =>
        {
            var cliente = await db.Clientes.FindAsync(id);
            if (cliente is null) return Results.NotFound();

            cliente.Nombre = dto.Nombre;
            cliente.Telefono = dto.Telefono;
            cliente.Email = dto.Email;
            cliente.Notas = dto.Notas;

            await db.SaveChangesAsync();
            return Results.Ok(cliente);
        });

        grupo.MapDelete("/{id:guid}", async (Guid id, AppDbContext db) =>
        {
            var cliente = await db.Clientes.FindAsync(id);
            if (cliente is null) return Results.NotFound();

            db.Clientes.Remove(cliente);
            try
            {
                await db.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                // Viola una FK: hay campos u otros registros que dependen de este cliente.
                return Results.Conflict("No se puede eliminar: el cliente tiene campos u otros registros asociados.");
            }
            return Results.NoContent();
        });
    }
}
