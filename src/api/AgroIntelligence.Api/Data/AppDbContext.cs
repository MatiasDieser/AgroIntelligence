using Microsoft.EntityFrameworkCore;
using AgroIntelligence.Api.Models;

namespace AgroIntelligence.Api.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Cliente> Clientes { get; set; }
    public DbSet<Campo> Campos { get; set; }
    public DbSet<Lote> Lotes { get; set; }
    public DbSet<Vuelo> Vuelos { get; set; }
    public DbSet<Informe> Informes { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Cliente>(entity =>
        {
            entity.ToTable("clientes");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.Nombre).HasColumnName("nombre");
            entity.Property(e => e.Telefono).HasColumnName("telefono");
            entity.Property(e => e.Email).HasColumnName("email");
            entity.Property(e => e.Notas).HasColumnName("notas");
            entity.Property(e => e.FechaAlta).HasColumnName("fecha_alta");
        });

        modelBuilder.Entity<Campo>(entity =>
        {
            entity.ToTable("campos");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.ClienteId).HasColumnName("cliente_id");
            entity.Property(e => e.Nombre).HasColumnName("nombre");
            entity.Property(e => e.Descripcion).HasColumnName("descripcion");
            entity.Property(e => e.Hectareas).HasColumnName("hectareas");
            entity.Property(e => e.Ubicacion).HasColumnName("ubicacion");
            entity.Property(e => e.Geometria).HasColumnName("geometria").HasColumnType("geometry (polygon, 4326)");
            entity.Property(e => e.FechaAlta).HasColumnName("fecha_alta");
        });

        modelBuilder.Entity<Lote>(entity =>
        {
            entity.ToTable("lotes");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.CampoId).HasColumnName("campo_id");
            entity.Property(e => e.Nombre).HasColumnName("nombre");
            entity.Property(e => e.Hectareas).HasColumnName("hectareas");
            entity.Property(e => e.CultivoActual).HasColumnName("cultivo_actual");
            entity.Property(e => e.Descripcion).HasColumnName("descripcion");
            entity.Property(e => e.Geometria).HasColumnName("geometria").HasColumnType("geometry (polygon, 4326)");
        });

        modelBuilder.Entity<Vuelo>(entity =>
        {
            entity.ToTable("vuelos");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.CampoId).HasColumnName("campo_id");
            entity.Property(e => e.LoteId).HasColumnName("lote_id");
            entity.Property(e => e.Tipo).HasColumnName("tipo");
            entity.Property(e => e.Fecha).HasColumnName("fecha").HasColumnType("date");
            entity.Property(e => e.Estado).HasColumnName("estado");
            entity.Property(e => e.CarpetaPath).HasColumnName("carpeta_path");
            entity.Property(e => e.AlturaVueloMetros).HasColumnName("altura_vuelo_metros");
            entity.Property(e => e.CondicionesClimaticas).HasColumnName("condiciones_climaticas");
            entity.Property(e => e.Notas).HasColumnName("notas");
            entity.Property(e => e.FechaCreacion).HasColumnName("fecha_creacion");
        });

        modelBuilder.Entity<Informe>(entity =>
        {
            entity.ToTable("informes");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.VueloId).HasColumnName("vuelo_id");
            entity.Property(e => e.PdfPath).HasColumnName("pdf_path");
            entity.Property(e => e.LinkUnico).HasColumnName("link_unico");
            entity.Property(e => e.Estado).HasColumnName("estado");
            entity.Property(e => e.RevisadoPor).HasColumnName("revisado_por");
            entity.Property(e => e.FechaRevision).HasColumnName("fecha_revision");
            entity.Property(e => e.FechaGeneracion).HasColumnName("fecha_generacion");
        });
    }
}
