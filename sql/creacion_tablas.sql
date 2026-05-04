CREATE DATABASE SMV_FONDOS
USE SMV_FONDOS

CREATE TABLE dim_administradoras (
    idAdministradora INT IDENTITY(1,1) PRIMARY KEY,
    RazonSocial NVARCHAR(250) NOT NULL UNIQUE
)

CREATE TABLE fact_fondos (
    id_fondo INT IDENTITY(1,1) PRIMARY KEY,
    idAdministradora INT NOT NULL,
    DenominacionFondo NVARCHAR(250) NOT NULL,
    TipoFondo NVARCHAR(100),
    FechaInscripcion DATE,
    ResolucionInscripcion NVARCHAR(200),
    Moneda NVARCHAR(50),
    FechaInformacion DATE,
    PatrimonioInscrito DECIMAL(15,2),
    ValorCuota DECIMAL(15,6),
    NumeroParticipes INT,
    NumeroCuotas DECIMAL(10,6),
    AnioInscripcion SMALLINT,
    TieneDatos BIT,
	FechaCarga DATETIME2 NOT NULL

    CONSTRAINT fk_administradora
        FOREIGN KEY (idAdministradora)
        REFERENCES dim_administradoras(idAdministradora)
)
