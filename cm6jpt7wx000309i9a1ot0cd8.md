---
title: "Building a .NET 8 Minimal API with EF Core, Identity, and SQL Server"
seoTitle: ".NET 8 Minimal API with EF Core & Identity - Complete Guide"
seoDescription: "Build a .NET 8 Minimal API using Entity Framework Core, ASP.NET Core Identity, and SQL Server. Learn to create a scalable User CRUD API"
datePublished: Thu Jan 30 2025 19:15:15 GMT+0000 (Coordinated Universal Time)
cuid: cm6jpt7wx000309i9a1ot0cd8
slug: dotnet-8-minimal-api-efcore-identity-sql-server
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1738262983706/c3aaa2c5-8abc-4006-a91f-ecea5da1e646.png
ogImage: https://cdn.hashnode.com/res/hashnode/image/upload/v1738264056867/d9470dd2-2cba-44ce-b274-6bfce034d750.png
tags: sql-server, entity-framework, webdev, net, rest-api, aspnet-core, dotnet

---

.NET 8 expands the simplicity and performance benefits of **Minimal APIs**, providing an alternative to the traditional Controller-based approach in ASP.NET Core. In this walkthrough, we will create a **User CRUD** application that uses:

* **Entity Framework Core (EF Core)** to interact with a **SQL Server** database
    
* **ASP.NET Core Identity** for user authentication and management
    
* **Minimal API** routing to keep the application lightweight
    

This guide demonstrates how to set up the folder structure, configure the database, and implement the endpoints required to manage user data.

> **Note**: All source code for this project is available in the following GitHub repository: [EFCoreMinimalAPI](https://github.com/arya2004/EFCoreMinimalAPI)

# Why Minimal APIs Over Controller-Based APIs?

### Advantages of Minimal APIs

1. **Reduced Boilerplate**: No separate controllers or startup files are needed.
    
2. **Improved Performance**: Fewer abstractions mean faster application startup and request handling.
    
3. **Straightforward Routing**: Define routes directly with `MapGet`, `MapPost`, etc., rather than using controller routes and attributes.
    

### When to Use Controller-Based APIs

* When you require **complex routing** scenarios or advanced filters.
    
* If your project follows a **strict MVC architecture**.
    
* When you need **robust organization** for very large APIs.
    

# **Getting Started with a Minimal API in .NET 8**

Before building a full-fledged API, let's start with a basic **Hello World** API in .NET 8:

```bash
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello, World!");

app.Run();
```

This example shows the fundamental **route definition** without using controllers. You can run this using `dotnet run` and access [`http://localhost:5000/`](http://localhost:5000/).

# Setting Up the Project in Visual Studio

### **Step 1: Create a New .NET 8 Minimal API Project**

1. Open **Visual Studio** and select **"**[**ASP.NET**](http://ASP.NET) **Core Web API"** as the project template.
    
2. Click **Next**.
    

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1738263478199/1d4460dd-7b0c-4d55-9957-793871fa78de.png align="center")

### **Step 2: Configure Project Name & Location**

1. Name your project **EFCoreMinimalAPI**.
    
2. Choose the desired location and click **Next**.
    

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1738263497115/f811c7b8-8ae2-45ff-9907-3890f73264c8.png align="center")

### **Step 3: Choose .NET 8 & Enable OpenAPI**

1. Select **.NET 8 (Long Term Support)**.
    
2. Enable **OpenAPI support**.
    
3. Click **Create**.
    

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1738263509486/ab384718-45f7-479b-84df-ef28c1002f20.png align="center")

You will now have a basic ASP.NET Core API project ready to extend with EF Core and Identity.

# **Project Structure**

Once the project is created, the structure should look like this:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1738264453486/e3a101f3-ac4b-4734-8a1e-b21a3936e377.png align="center")

## The `EFCoreMinimalAPI.csproj` File

Below is the project file referencing **.NET 8** and the necessary NuGet packages:

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

	<PropertyGroup>
		<TargetFramework>net8.0</TargetFramework>
		<Nullable>enable</Nullable>
		<ImplicitUsings>enable</ImplicitUsings>
	</PropertyGroup>

	<ItemGroup>
		<PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" Version="8.0.0" />
		<PackageReference Include="Microsoft.AspNetCore.Identity" Version="2.3.0" />
		<PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="8.0.12" />
		<PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
		<PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.12" />
		<PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="8.0.12" />

		<!-- JWT Authentication -->
		<PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.0.0" />
		<PackageReference Include="Microsoft.IdentityModel.Tokens" Version="8.0.0" />
		<PackageReference Include="System.IdentityModel.Tokens.Jwt" Version="8.0.0" />

		<!-- Swagger for API Documentation -->
		<PackageReference Include="Swashbuckle.AspNetCore" Version="7.2.0" />
	</ItemGroup>

</Project>
```

## `appsettings.Development.json`

Specify your SQL Server connection string in `appsettings.Development.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=G14\\SQLEXPRESS;Database=EFCoreMinimalAPI;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=true"
  },
  "Jwt": {
    "Key": "i_like_cats_and_dotnet",
    "Issuer": "UserAPI",
    "Audience": "UserAPI"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

## `Data/AppDbContext.cs`

This `AppDbContext` inherits from `IdentityDbContext<IdentityUser>`, enabling ASP.NET Core Identity tables and features:

```csharp
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace EFCoreMinimalAPI.Data
{
   
    public class AppDbContext : IdentityDbContext<IdentityUser>
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);
            builder.Entity<IdentityUser>().ToTable("Users");
            builder.Entity<IdentityRole>().ToTable("Roles");
        }
    }
}
```

## Models

We will use **Data Transfer Objects (DTOs)** to handle input/output payloads cleanly.

### `Models/UserDto.cs`

```csharp
namespace EFCoreMinimalAPI.Models
{
    public class UserDto
    {
        public string Id { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string? Role { get; set; }
    }
}
```

### `Models/RegisterUserDto.cs`

```csharp
namespace EFCoreMinimalAPI.Models
{
    public class RegisterUserDto
    {
        public string Email { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }
}
```

### `Models/LoginDto.cs`

```csharp
namespace EFCoreMinimalAPI.Models
{
    public class LoginDto
    {
        public string Email { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }
}
```

## `Services/UserService.cs`

This service encapsulates the user-related business logic using `UserManager<IdentityUser>` and `RoleManager<IdentityRole>`:

```csharp
using EFCoreMinimalAPI.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace EFCoreMinimalAPI.Services
{
    public class UserService
    {
        private readonly UserManager<IdentityUser> _userManager;
        private readonly RoleManager<IdentityRole> _roleManager;

        public UserService(UserManager<IdentityUser> userManager, RoleManager<IdentityRole> roleManager)
        {
            _userManager = userManager;
            _roleManager = roleManager;
        }

        public async Task<List<UserDto>> GetAllUsersAsync()
        {
            var users = await _userManager.Users.ToListAsync();
            return users.Select(u => new UserDto { Id = u.Id, Email = u.Email }).ToList();
            
        }

        public async Task<IdentityResult> RegisterUserAsync(RegisterUserDto model)
        {
            var user = new IdentityUser { UserName = model.Email, Email = model.Email };
            return await _userManager.CreateAsync(user, model.Password);
        }

        public async Task<IdentityUser?> GetUserByIdAsync(string userId)
        {
            return await _userManager.FindByIdAsync(userId);
        }

        public async Task<bool> DeleteUserAsync(string userId)
        {
            var user = await _userManager.FindByIdAsync(userId);
            if (user != null)
            {
                var result = await _userManager.DeleteAsync(user);
                return result.Succeeded;
            }
            return false;
        }
    }
}
```

## `Endpoints/UserEndpoints.cs`

Minimal APIs define routes directly in code. Below, we have **User CRUD endpoints**:

```csharp
using EFCoreMinimalAPI.Models;
using EFCoreMinimalAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace EFCoreMinimalAPI.Endpoints
{
    public static class UserEndpoints
    {
        public static void MapUserEndpoints(this IEndpointRouteBuilder routes)
        {
            var group = routes.MapGroup("/api/users");

            group.MapGet("/", async (UserService userService) =>
            {
                var users = await userService.GetAllUsersAsync();
                return Results.Ok(users);
            });

            group.MapGet("/{id}", async (string id, UserService userService) =>
            {
                var user = await userService.GetUserByIdAsync(id);
                return user is null ? Results.NotFound() : Results.Ok(user);
            });

            group.MapPost("/register", async ([FromBody] RegisterUserDto model, UserService userService) =>
            {
                var result = await userService.RegisterUserAsync(model);
                return result.Succeeded ? Results.Ok("User Created") : Results.BadRequest(result.Errors);
            });

            group.MapDelete("/{id}", async (string id, UserService userService) =>
            {
                var deleted = await userService.DeleteUserAsync(id);
                return deleted ? Results.Ok("User Deleted") : Results.NotFound("User Not Found");
            });
        }
    }
}
```

## `Program.cs`

Finally, wire everything up in `Program.cs`:

```csharp
using EFCoreMinimalAPI.Data;
using EFCoreMinimalAPI.Endpoints;
using EFCoreMinimalAPI.Services;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;


var builder = WebApplication.CreateBuilder(args);

// Add Database Context
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Add Identity
builder.Services.AddIdentity<IdentityUser, IdentityRole>()
    .AddEntityFrameworkStores<AppDbContext>()
    .AddDefaultTokenProviders();

// Add UserService
builder.Services.AddScoped<UserService>();

// Add Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Use Swagger
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Map Routes
app.MapUserEndpoints();

app.Run();
```

# Running the Application

1. **Restore NuGet packages** (if needed):
    
    ```sh
    dotnet restore
    ```
    
2. **Create and apply EF Core migrations** (in Package Manager Console):
    
    ```powershell
    Add-Migration InitialCreate
    Update-Database
    ```
    
3. **Run the project**:
    
    ```sh
    dotnet run
    ```
    
4. Access **Swagger UI** at `https://localhost:7186/swagger` (or the port shown in your console) to test your API.
    

# Conclusion

You now have a working **.NET 8 Minimal API** for **User CRUD** with **EF Core**, **Identity**, and **SQL Server**. This approach offers a lighter footprint compared to Controller-based projects, making it an excellent choice for modern microservices or simpler applications.

For a ready-to-use template, refer to the repository below:

**GitHub:** [EFCoreMinimalAPI](https://github.com/arya2004/EFCoreMinimalAPI)

This template provides a reliable foundation to expand your project further by adding additional entities, authentication flows, or advanced business logic.