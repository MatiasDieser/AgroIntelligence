using AgroIntelligence.Api.Data;
using AgroIntelligence.Api.Endpoints;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("DefaultConnection"),
        o => o.UseNetTopologySuite() // necesario para mapear columnas geometry(POLYGON,4326) 
    ));

var app = builder.Build();

app.MapClientesEndpoints();
app.MapCamposEndpoints();
app.MapLotesEndpoints();
app.MapVuelosEndpoints();
app.MapInformesEndpoints();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.Run();
